"""The reconstructions are checked against their sources, not just pinned.

A pin proves that a source did not move.  It does not prove that the
reconstruction says the same thing, and the rung's own leftover list named
that gap.  This file closes it mechanically: every declaration the
reconstruction shares with its source is compared, and any difference is
named.

What is compared, exactly.  Doc comments and block comments are stripped,
because the reconstruction's comments are its own by declaration; the
outer namespace lines are stripped, because the reconstruction is
deliberately in a different namespace; and whitespace is normalized,
because Lean does not care and a re-wrap is not a drift.  Everything
else -- every binder, every hypothesis, every tactic of every proof -- must
match character for character.

What is NOT compared, and is still read by hand: whether the declarations
the reconstruction OMITS are safe to omit.  The reconstruction carries the
slice the theorems need and no more, and this file records which names are
absent rather than judging the omission.  That residual is real and stays
named in STATUS.md.

The sources are read from the SNAPSHOT recorded in `SOURCE_MANIFEST.json`,
by git blob, not from the working tree: a comparison against a file that
may have moved would prove nothing about the pinned revision.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import unittest

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
LEAN = HERE / "lean" / "SecondNoFirst"

# source under the snapshot -> the module reconstructing it here
PAIRS = (
    ("lean4/Derivation/Basic.lean", "Kernel.lean"),
    ("lean4/Derivation/Inertia.lean", "Kernel.lean"),
    (
        "research/standing_commitment/lean/StandingCommitment/Base.lean",
        "Inherited.lean",
    ),
    (
        "research/standing_commitment/lean/StandingCommitment/Commitment.lean",
        "Inherited.lean",
    ),
)

DECL_START = (
    r"(?m)^(?=theorem |def |abbrev |structure |inductive |instance |@\[simp\])"
)
DECL_NAME = r"(?:theorem|def|abbrev|structure|inductive) ([A-Za-z_][\w'.]*)"


def normalize(text: str) -> dict[str, str]:
    """Declaration name -> normalized body: comments gone, namespace and
    `end` lines gone, whitespace collapsed."""
    text = re.sub(r"/-[!-]?.*?-/", "", text, flags=re.S)
    out: dict[str, str] = {}
    for part in re.split(DECL_START, text):
        match = re.match(DECL_NAME, part.strip())
        if match is None:
            continue
        body = re.sub(r"(?m)^end [\w.]+\s*$", "", part)
        body = re.sub(r"(?m)^namespace [\w.]+\s*$", "", body)
        out[match.group(1)] = re.sub(r"\s+", " ", body).strip()
    return out


def snapshot() -> str:
    manifest = json.loads(
        (HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
    )
    commit = manifest["snapshot_commit"]
    assert isinstance(commit, str)
    return commit


def blob(revision: str, path: str) -> str:
    return subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        capture_output=True,
        cwd=REPO,
        check=True,
    ).stdout.decode("utf-8")


class ReconstructionTests(unittest.TestCase):
    def test_every_shared_declaration_is_identical(self) -> None:
        commit = snapshot()
        differing: list[str] = []
        shared_total = 0
        for source, module in PAIRS:
            want = normalize(blob(commit, source))
            got = normalize((LEAN / module).read_text(encoding="utf-8"))
            shared = sorted(set(want) & set(got))
            shared_total += len(shared)
            for name in shared:
                if want[name] != got[name]:
                    differing.append(f"{source} -> {module}: {name}")
        self.assertEqual(differing, [])
        # Not a vacuous pass: the comparison must actually have compared
        # something, and a slice this small would be suspicious.
        self.assertGreaterEqual(shared_total, 40)

    def test_a_changed_binder_would_be_caught(self) -> None:
        """NEGATIVE: the comparison bites.  Renaming one binder in a
        reconstructed statement makes the normalized bodies differ."""
        commit = snapshot()
        want = normalize(blob(commit, "lean4/Derivation/Basic.lean"))
        got = normalize((LEAN / "Kernel.lean").read_text(encoding="utf-8"))
        name = "collapsed"
        self.assertEqual(want[name], got[name])
        tampered = got[name].replace("(d d' : Nat)", "(d dd : Nat)")
        self.assertNotEqual(want[name], tampered)

    def test_comment_and_namespace_differences_are_permitted(self) -> None:
        """The normalizer must not fail on the two differences that ARE
        declared: the reconstruction's own doc comments and its namespace."""
        sample = (
            "namespace Other\n"
            "/-- a doc comment of the reconstruction -/\n"
            "def f (n : Nat) : Nat := n + 1\n"
            "end Other\n"
        )
        original = "def f (n : Nat) : Nat := n + 1\n"
        self.assertEqual(normalize(sample)["f"], normalize(original)["f"])

    def test_the_omitted_declarations_are_recorded_not_judged(self) -> None:
        """The reconstruction carries the slice the theorems need.  This
        records which names it leaves behind; whether leaving them is safe
        is read by hand and stays a named leftover."""
        commit = snapshot()
        omitted: dict[str, list[str]] = {}
        for source, module in PAIRS:
            want = normalize(blob(commit, source))
            got = normalize((LEAN / module).read_text(encoding="utf-8"))
            missing = sorted(set(want) - set(got))
            if missing:
                omitted[source] = missing
        # Every omission is from the sealed kernel's augmentation and
        # example machinery, or from the sibling's counting theorems --
        # none is a definition the reconstructed theorems mention.
        for source, names in omitted.items():
            for name in names:
                for module in {m for s, m in PAIRS if s == source}:
                    body = (LEAN / module).read_text(encoding="utf-8")
                    body = re.sub(r"/-[!-]?.*?-/", "", body, flags=re.S)
                    self.assertNotRegex(
                        body, r"(?<![\w'.])" + re.escape(name) + r"(?![\w'])",
                        f"{name} is omitted from {module} but named in it",
                    )


if __name__ == "__main__":
    unittest.main()
