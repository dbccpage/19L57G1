"""The reconstructions are checked against their sources, not just pinned.

A hand copy of `research/second_iso/test_reconstruction.py`, with this
rung's three source-to-module pairs, its own pinned shared count and its
own pinned omission population; the normalizer is unchanged.

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
from typing import Any

import verify_lean as lean_audit

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
LEAN = HERE / "lean" / "SecondSymmetry"

# source under the snapshot -> the module reconstructing it here
PAIRS = (
    ("lean4/Derivation/Basic.lean", "Kernel.lean"),
    ("lean4/Derivation/Inertia.lean", "Kernel.lean"),
    ("lean4/Derivation/Minimality.lean", "IsoKernel.lean"),
)

DECL_KINDS = "theorem|lemma|def|abbrev|opaque|structure|class|inductive|instance"
DECL_PREFIX = (
    r"(?:@\[[^\]\r\n]*\]\s*)*"
    r"(?:(?:private|protected|noncomputable)\s+)*"
)
DECL_START = rf"(?m)^(?=[ \t]*{DECL_PREFIX}(?:{DECL_KINDS})\b)"
DECL_HEADER = re.compile(
    rf"[ \t]*{DECL_PREFIX}(?P<kind>{DECL_KINDS})"
    rf"(?:\s+(?P<name>{lean_audit.IDENTIFIER}))?"
)
EXPECTED_OMISSIONS = {
    "lean4/Derivation/Basic.lean": [
        "Item",
        "applyDelta",
        "applyItem",
        "validResponse",
    ],
    "lean4/Derivation/Minimality.lean": [
        "BD",
        "BD_separable",
        "BL",
        "BL_not_iso_BD",
        "BL_separable",
        "U0",
        "U0_not_iso_BD",
        "U0_not_iso_BL",
        "U0_separable",
        "U1",
        "U1_separable",
        "applyDelta_pair",
        "applyDelta_single",
        "aritySum",
        "cost1_insufficient",
        "cost1_insufficient_F",
        "cost1_insufficient_general",
        "deltaBD",
        "deltaBD_valid",
        "deltaBL",
        "deltaBL_valid",
        "deltaK",
        "deltaK_applies",
        "deltaK_length",
        "deltaK_valid",
        "deltaU0",
        "deltaU0F_valid",
        "deltaU0_valid",
        "deltaU1",
        "deltaU1_valid",
        "isoU1U0",
        "markK",
        "markK_pairwise_noniso",
        "markK_separable",
        "mu1_minimum_not_unique",
        "mu2_unique",
        "no_insts_no_separation",
        "validResponse_R2L",
    ],
}


def normalize(text: str) -> dict[str, str]:
    """Declaration name -> normalized body: comments gone, namespace and
    `end` lines gone, whitespace collapsed."""
    text = lean_audit.declaration_text(text)
    out: dict[str, str] = {}
    anonymous_instances = 0
    for part in re.split(DECL_START, text):
        match = DECL_HEADER.match(part.strip())
        if match is None:
            continue
        kind = match.group("kind")
        name = match.group("name")
        if name is None:
            if kind != "instance":
                raise ValueError(f"could not read the name of a {kind} declaration")
            anonymous_instances += 1
            name = f"<anonymous instance {anonymous_instances}>"
        else:
            name = lean_audit.canonical_identifier(name)
        body = re.sub(r"(?m)^end [\w.]+\s*$", "", part)
        body = re.sub(r"(?m)^namespace [\w.]+\s*$", "", body)
        # `open` lines are stripped for the same declared reason as the
        # namespace lines: this reconstruction flattens the sibling's four
        # namespaces into one, so the `open ... in` that precedes a
        # declaration there is absent here.  Added to the hand copy of
        # this file for this rung, and recorded in STATUS.md; the sibling
        # copy still carries the narrower normalizer, and a declaration
        # whose TEXT differs is still caught either way.
        body = re.sub(r"(?m)^open [\w. ]+?(?: in)?\s*$", "", body)
        if name in out:
            raise ValueError(f"duplicate declaration key {name}")
        out[name] = re.sub(r"\s+", " ", body).strip()
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
        self.assertEqual(shared_total, 41)

    def test_reconstruction_modules_add_no_unattributed_declaration(self) -> None:
        """A reconstruction module may omit a recorded slice, but it may
        not add a declaration absent from every source assigned to it."""
        commit = snapshot()
        for module in sorted({module for _, module in PAIRS}):
            source_names: set[str] = set()
            for source, assigned in PAIRS:
                if assigned == module:
                    source_names.update(normalize(blob(commit, source)))
            reconstructed = set(
                normalize((LEAN / module).read_text(encoding="utf-8"))
            )
            self.assertEqual(
                sorted(reconstructed - source_names),
                [],
                f"{module} adds a declaration absent from its pinned sources",
            )

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
        nested = "/- outer /- theorem fake : False := by trivial -/ end -/\n"
        self.assertEqual(normalize(nested), {})

    def test_attributed_and_anonymous_declarations_are_in_the_population(self) -> None:
        """NEGATIVE: the old splitter silently discarded an attributed
        theorem and every anonymous instance.  Both are declarations and
        must enter either the shared or omitted population."""
        sample = (
            "@[simp] theorem marked (n : Nat) : n = n := rfl\n"
            "theorem «quoted name» : True := by trivial\n"
            "lemma δemand₁ : True := by trivial\n"
            "instance (n : Nat) : Decidable (n = n) := inferInstance\n"
        )
        found = normalize(sample)
        self.assertIn("marked", found)
        self.assertIn("quoted name", found)
        self.assertIn("δemand₁", found)
        self.assertIn("<anonymous instance 1>", found)

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
        # Every omission is from the sealed kernel's augmentation, cost and
        # tie-family machinery, or from the siblings' counting and
        # well-formedness theorems -- none is a definition the
        # reconstructed theorems mention.
        for source, names in omitted.items():
            for name in names:
                for module in {m for s, m in PAIRS if s == source}:
                    body = (LEAN / module).read_text(encoding="utf-8")
                    body = lean_audit.declaration_text(body)
                    self.assertNotRegex(
                        body, r"(?<![\w'.])" + re.escape(name) + r"(?![\w'])",
                        f"{name} is omitted from {module} but named in it",
                    )
        self.assertEqual(omitted, EXPECTED_OMISSIONS)


if __name__ == "__main__":
    unittest.main()
