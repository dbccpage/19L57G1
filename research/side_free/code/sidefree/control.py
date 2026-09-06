"""The decisive computation: six gates, two carriers, one decided record.

Classification: METATHEORY APPARATUS throughout.  Nothing here is admitted,
and no function of this module changes a regime except by ``replay`` of an
explicit history in the carrier it belongs to.

``decide()`` returns one deterministic record.  If any gate fails the record
carries ``VOID`` and NO difference is reported.

The sign of the answer is fixed in advance by gate ``G5``: the forgetful
lemma's corollary says side-free separation implies side-typed separation at
every matched cell, and every side-free candidate has a side-typed
counterpart at the same capability count, so the pinned minimum is at most
the side-free minimum.  A negative difference is unreachable, and a tie is
the strongest statement available against the admitted primitive.  That is
what NOTHING_IN_COST means, and it is not the same sentence as "it bought
nothing".
"""

from __future__ import annotations

import ast
import hashlib
import json
import pathlib
import re
import subprocess
from dataclasses import dataclass
from typing import Callable, Sequence

from sidefree import candidates as ctl
from sidefree import mirror as mir
from sidefree.enumerate import (
    Json,
    eligible,
    enumerate_rows,
    everywhere_satisfying,
    minima,
    named,
)
from sidefree.model import (
    DECLARED_KEY_CHOICE,
    KEY_CHOICES,
    Admitted,
    AdmitMark,
    AdmitOccurrence,
    Regime,
    genesis,
    mark_observations,
    marks_separable_under,
    observation_holds,
    replay,
    step,
)
from sidefree.requirement import (
    DELETED_FROM_DECLARED,
    DELETED_FROM_SECOND_READING,
    DELETED_WORDS,
    REQUIREMENT,
    REQUIREMENT_SECOND_READING,
    RETAINED_MARKS,
    separates,
)

TREE = pathlib.Path(__file__).resolve().parents[2]
REPO = TREE.parent.parent
PIN_PATH = TREE / "pinned" / "boundary_challenge3.json"
PIN_META_PATH = TREE / "pinned" / "BOUNDARY_PIN.json"
MANIFEST_PATH = TREE / "SOURCE_MANIFEST.json"

# The four values that fix the vendored bytes, each recomputable with no git
# at all.  A fifth, conditional, check compares them against the pinned
# commit and reports SKIPPED-with-reason rather than passing quietly.
PIN_SHA256 = "e4904075aaa07dd05a2f9d0cba313e77b6eb965a44efecb5cff51864f70a64ab"
PIN_BLOB = "dbb4cce3cdd49d15d0784c2a73bf7afeab9de7a0"
PIN_BYTES = 220518

# The pinned rows the decisive gate replays: the base row and the six
# one-step rows of each reading, which is exactly what the minimum ranges
# over.  Stated as a scope, not as a completeness claim: a defect in a bundle
# row's recorded verdict is invisible to this gate.
G4_SCOPE = (
    "the base row and the six one-step rows of each reading -- fourteen rows, "
    "which is what the minimum is computed FROM.  It is not total over all 48 "
    "points per reading, so a defect in a bundle row's recorded verdict is "
    "invisible to it"
)

COLLAPSE_MAP: dict[str, str] = {
    "extra_mark_0": "extra_mark",
    "extra_mark_1": "extra_mark",
}

# The modules the deletion register's totality test scans.  ``mirror.py`` and
# ``control.py`` are excluded BY DECLARATION and for a stated reason: the
# first is the side-typed countermodel-domain object and the second is the
# comparison driver, and both must be able to name the deleted structure in
# order to compare against it.  The exclusion is named here rather than left
# implicit in a glob.
SIDE_FREE_MODULES: tuple[str, ...] = (
    "model.py",
    "presentation.py",
    "requirement.py",
    "candidates.py",
    "enumerate.py",
)

# Identifiers of the side-free modules that carry a deleted word component and
# are nevertheless allowed.  Declared one by one, with a reason each, so the
# stem scan can be strict everywhere else.  Two kinds appear here and no
# third:
#
#   * metatheory ABOUT the deletion, which must be able to spell what it
#     deletes -- the criterion's own pattern, the list of pinned facts that
#     have no side-free subject, and the name of the control carrier itself;
#   * the word "reading" in its OTHER pinned sense.  The pinned world uses it
#     twice: for the index over the two sides, which is deleted, and for a
#     SECOND READING of the requirement, which is a second way of reading the
#     imposed challenge and has nothing to do with sides.  The three names
#     below carry the second sense.
DELETION_WORD_ALLOWLIST: tuple[str, ...] = (
    "_SIDE_WORD",
    "PINNED_COLLATERAL_FACTS_WITHOUT_A_SIDE_FREE_SUBJECT",
    "SideFreeCarrier",
    "DELETED_FROM_SECOND_READING",
    "REQUIREMENT_SECOND_READING",
    "satisfies_second_reading",
)
DELETION_WORD_ALLOWLIST_REASONS: dict[str, str] = {
    "_SIDE_WORD": "the deletion criterion's own pattern; it must spell what it deletes",
    "PINNED_COLLATERAL_FACTS_WITHOUT_A_SIDE_FREE_SUBJECT": (
        "the declared list of pinned facts that have no side-free subject"
    ),
    "SideFreeCarrier": "the name of the control carrier itself",
    "DELETED_FROM_SECOND_READING": (
        "'reading' in its other pinned sense: a second way of reading the "
        "imposed challenge, not the index over the two sides"
    ),
    "REQUIREMENT_SECOND_READING": (
        "'reading' in its other pinned sense: a second way of reading the "
        "imposed challenge, not the index over the two sides"
    ),
    "satisfies_second_reading": (
        "'reading' in its other pinned sense: a second way of reading the "
        "imposed challenge, not the index over the two sides"
    ),
}

DELETED_STEMS: frozenset[str] = frozenset(
    {
        "side",
        "sides",
        "placement",
        "reflect",
        "reflection",
        "reading",
        "readings",
        "convention",
        "conventions",
        "near",
        "far",
    }
)

REMOVED_REFUSAL = {
    "pinned_refusal": (
        "an admission naming the other side would move an already admitted "
        "mark, and is refused by name"
    ),
    "status": "REMOVED, not absorbed",
    "why": (
        "it has no side-free statement at all: with no sides there is nowhere "
        "to move a mark to.  It is recorded here rather than quietly folded "
        "into the no-op, and its computed consequence is reported beside the "
        "two identity policies"
    ),
}


def _components(name: str) -> list[str]:
    parts: list[str] = []
    for chunk in name.split("_"):
        parts.extend(
            re.findall(r"[A-Z]+(?![a-z])|[A-Z][a-z]*|[a-z]+|\d+", chunk)
        )
    return [p.lower() for p in parts]


def carries_a_deleted_stem(name: str) -> bool:
    """Whether an identifier carries one of the deleted word components."""
    return bool(set(_components(name)) & DELETED_STEMS)


def side_free_identifiers() -> set[str]:
    """Every identifier appearing in the side-free modules' syntax trees.

    Read from the SYNTAX, not from the text, so a deleted word inside a
    comment or a doc string -- which is how a deletion gets explained -- is
    never mistaken for a use of it.
    """
    found: set[str] = set()
    for name in SIDE_FREE_MODULES:
        tree = ast.parse((pathlib.Path(__file__).parent / name).read_text("utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                found.add(node.id)
            elif isinstance(node, ast.Attribute):
                found.add(node.attr)
            elif isinstance(node, ast.arg):
                found.add(node.arg)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                found.add(node.name)
            elif isinstance(node, ast.keyword) and node.arg:
                found.add(node.arg)
            elif isinstance(node, ast.alias):
                found.add((node.asname or node.name).split(".")[0])
    return found


# ---------------------------------------------------------------------------
# Reading the pin
# ---------------------------------------------------------------------------


def pin_bytes() -> bytes:
    return PIN_PATH.read_bytes()


def pin_data() -> Json:
    payload = json.loads(pin_bytes().decode("utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("the vendored pin must be a JSON object")
    return payload


def pin_meta() -> Json:
    payload = json.loads(PIN_META_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("the pin metadata must be a JSON object")
    return payload


def as_list(value: object) -> list[object]:
    """Read a JSON-shaped list, refusing anything else by name."""
    if not isinstance(value, list):
        raise TypeError(f"expected a list, got {type(value).__name__}")
    return value


def as_dict(value: object) -> dict[str, object]:
    """Read a JSON-shaped object, refusing anything else by name."""
    if not isinstance(value, dict):
        raise TypeError(f"expected an object, got {type(value).__name__}")
    return value


def dig(root: object, path: str) -> object:
    """Read one dotted path out of a JSON-shaped object."""
    cur = root
    for part in path.split("."):
        if isinstance(cur, list):
            cur = cur[int(part)]
        elif isinstance(cur, dict):
            cur = cur[part]
        else:
            raise KeyError(f"{path}: cannot descend into {type(cur).__name__}")
    return cur


def pin_reading(reading: str) -> Json:
    block = dig(pin_data(), f"readings.{reading}")
    if not isinstance(block, dict):
        raise TypeError(f"pinned reading {reading} is not an object")
    return block


def pin_rows(reading: str, key: str) -> list[Json]:
    rows = pin_reading(reading)[key]
    if not isinstance(rows, list):
        raise TypeError(f"pinned {reading}.{key} is not a list")
    return [r for r in rows if isinstance(r, dict)]


def pin_verdict_rows(reading: str) -> list[Json]:
    """The base row and the six one-step rows: what the minimum ranges over."""
    base = pin_reading(reading)["base"]
    if not isinstance(base, dict):
        raise TypeError("the pinned base row is not an object")
    return [base, *pin_rows(reading, "one_step_detail")]


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------


def gate_pin_bytes() -> Json:
    raw = pin_bytes()
    meta = pin_meta()
    vendored = meta["vendored"]
    if not isinstance(vendored, dict):
        raise TypeError("BOUNDARY_PIN.json carries no vendored block")
    got_sha = hashlib.sha256(raw).hexdigest()
    got_blob = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
    problems: list[str] = []
    if got_sha != PIN_SHA256:
        problems.append(f"sha256 {got_sha} wanted {PIN_SHA256}")
    if got_blob != PIN_BLOB:
        problems.append(f"git blob {got_blob} wanted {PIN_BLOB}")
    if len(raw) != PIN_BYTES:
        problems.append(f"byte count {len(raw)} wanted {PIN_BYTES}")
    if b"\r" in raw:
        problems.append("the vendored pin contains CR bytes")
    for field, value in (
        ("sha256", got_sha),
        ("git_blob_sha1", got_blob),
        ("byte_count", len(raw)),
    ):
        if vendored.get(field) != value:
            problems.append(
                f"BOUNDARY_PIN.json {field} is {vendored.get(field)!r}, bytes say {value!r}"
            )
    checked_commit = commit_check()
    declared_commit = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["pinned_commit"]
    if meta.get("source_commit") != declared_commit:
        problems.append("BOUNDARY_PIN.json source_commit differs from SOURCE_MANIFEST.json pinned_commit")
    if checked_commit["status"] == "FAIL":
        problems.append(f"pinned commit: {checked_commit['reason']}")
    return {
        "gate": "G1",
        "name": "pin_bytes_ok",
        "sha256": got_sha,
        "git_blob_sha1": got_blob,
        "byte_count": len(raw),
        "carries_cr": b"\r" in raw,
        "commit_check": checked_commit,
        "problems": problems,
        "passed": not problems,
    }


def commit_check() -> Json:
    """The conditional third check.  PASS or SKIPPED-with-reason, never silent."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    source_path = dig(manifest, "vendored_blob.source_path")
    # The commit is read from the manifest, which is the one place it is
    # declared; decide() reports that same manifest value.
    commit = str(dig(manifest, "pinned_commit"))
    proc = subprocess.run(
        ["git", "show", f"{commit}:{source_path}"],
        cwd=REPO,
        capture_output=True,
    )
    if proc.returncode != 0:
        return {
            "status": "SKIPPED",
            "reason": (
                f"the pinned commit {commit} is unreachable in this "
                f"clone: {proc.stderr.decode('utf-8', 'replace').strip()}"
            ),
            "residual": (
                "the link from the vendored bytes to that commit is only as "
                "strong as source availability here; the required pin verifier fails without it"
            ),
        }
    same = proc.stdout == pin_bytes()
    return {
        "status": "PASS" if same else "FAIL",
        "reason": (
            "the vendored bytes equal the blob at the pinned commit"
            if same
            else "the vendored bytes DIFFER from the blob at the pinned commit"
        ),
        "residual": (
            "the link from the vendored bytes to that commit is only as "
            "strong as source availability here; the required pin verifier fails without it"
        ),
    }


def gate_requirement_texts() -> Json:
    pinned_declared = str(dig(pin_data(), "requirement.declared"))
    pinned_second = str(dig(pin_data(), "requirement.second_reading"))
    problems: list[str] = []
    for label, pinned, phrase, control in (
        ("declared", pinned_declared, DELETED_FROM_DECLARED, REQUIREMENT),
        (
            "second_reading",
            pinned_second,
            DELETED_FROM_SECOND_READING,
            REQUIREMENT_SECOND_READING,
        ),
    ):
        if pinned.count(phrase) != 1:
            problems.append(
                f"the deleted phrase {phrase!r} occurs {pinned.count(phrase)} "
                f"times in the pinned {label}, so the deletion is not unambiguous"
            )
        elif pinned.replace(phrase, "", 1) != control:
            problems.append(
                f"the pinned {label} with {phrase!r} deleted is not the "
                f"control text byte for byte"
            )
    if str(dig(pin_data(), "requirement.retained_marks")) != str(list(RETAINED_MARKS)):
        problems.append("the retained marks differ from the pinned pair")
    leaked = [
        word
        for word in DELETED_WORDS
        if re.search(rf"\b{re.escape(word)}\b", REQUIREMENT + " " + REQUIREMENT_SECOND_READING)
    ]
    if leaked:
        problems.append(f"the control requirement strings still name {leaked}")
    return {
        "gate": "G2",
        "name": "requirement_texts_match",
        "control_requirement": REQUIREMENT,
        "control_second_reading": REQUIREMENT_SECOND_READING,
        "deleted_phrases": [DELETED_FROM_DECLARED, DELETED_FROM_SECOND_READING],
        "words_scanned_for": list(DELETED_WORDS),
        "words_found": leaked,
        "retained_marks": list(RETAINED_MARKS),
        "problems": problems,
        "passed": not problems,
    }


def gate_capability_texts() -> Json:
    problems: list[str] = []
    pinned_names = dig(pin_data(), "candidate_space.coordinates")
    if not isinstance(pinned_names, list):
        raise TypeError("the pinned coordinate list is not a list")
    missing = [name for name in ctl.COORDINATES if name not in pinned_names]
    if missing:
        # The cross-world join is by string equality, so a rename fails it BY
        # NAME here instead of silently dropping a route.
        problems.append(f"coordinate names absent from the pinned list: {missing}")
    for name in ctl.COORDINATES:
        if name in missing:
            continue
        pinned = str(dig(pin_data(), f"candidate_space.capability_of.{name}"))
        if ctl.CAPABILITY_OF[name] != pinned:
            problems.append(f"capability text for {name} is not byte-identical")
    mechanical = sorted(
        name
        for name in pinned_names
        if ctl.transfers(str(dig(pin_data(), f"candidate_space.capability_of.{name}")))
    )
    if mechanical != sorted(ctl.COORDINATES):
        problems.append(
            f"the mechanical partition {mechanical} is not the implemented one "
            f"{sorted(ctl.COORDINATES)}"
        )
    return {
        "gate": "G3",
        "name": "capability_texts_match",
        "criterion": ctl.DELETION_CRITERION,
        "transferring": list(ctl.COORDINATES),
        "deleted": [str(n) for n in pinned_names if str(n) not in ctl.COORDINATES],
        "mechanical_partition": mechanical,
        "problems": problems,
        "passed": not problems,
    }


def gate_verdict_replay() -> Json:
    """The decisive gate: this tree's verdict against the pinned world's answers."""
    i, j = RETAINED_MARKS
    checked: list[Json] = []
    problems: list[str] = []
    for reading in (mir.READING_U, mir.READING_O):
        for row in pin_verdict_rows(reading):
            entries = row["automorphism_entries"]
            if not isinstance(entries, list):
                raise TypeError("a pinned row carries no automorphism entries")
            perms = [
                tuple(int(x) for x in e["permutation"])
                for e in entries
                if isinstance(e, dict)
            ]
            got = separates(perms, i, j)
            want = bool(row["satisfies"])
            checked.append(
                {
                    "reading": reading,
                    "name": str(row["name"]),
                    "recorded_satisfies": want,
                    "replayed_satisfies": got,
                    "agrees": got == want,
                }
            )
            if got != want:
                problems.append(
                    f"reading {reading} row {row['name']}: this tree's verdict "
                    f"{got} against the pinned recorded {want}"
                )
    return {
        "gate": "G4",
        "name": "verdict_replay_agrees",
        "scope": G4_SCOPE,
        "rows": checked,
        "row_count": len(checked),
        "agreements": sum(1 for r in checked if r["agrees"]),
        "problems": problems,
        "passed": not problems,
    }


def gate_forgetful_lemma() -> Json:
    report = mir.forgetful_lemma(False)
    problems: list[str] = []
    if not report["holds"]:
        problems.append(f"the forgetful lemma fails: {report['first_violation']}")
    if not report["corollary_holds"]:
        problems.append(
            f"the corollary fails: {report['first_corollary_violation']}"
        )
    # Two checks, two messages, because a single line here would misname what
    # it caught.  The first is the corollary's own non-vacuity: no cell
    # satisfies its antecedent, so the implication is empty.  The second is
    # the check the frozen design declares -- forgetting loses a separation
    # somewhere -- which is what the smuggle injection drives to zero.
    if not report["corollary_non_vacuous"]:
        problems.append(
            "the corollary is vacuous over the declared census: no cell "
            "satisfies its antecedent"
        )
    if not report["forgetting_loses_separation"]:
        problems.append(
            "forgetting loses no separation at any cell of the declared "
            "census: the converse fails nowhere"
        )
    return {
        "gate": "G5",
        "name": "forgetful_lemma",
        "report": report,
        "what_it_catches": (
            "any structure the side-free carrier keeps beyond forgetting "
            "shrinks its automorphism set below the image of the side-typed "
            "one, so the lemma fails by name at a named cell"
        ),
        "sign_consequence": (
            "the pinned minimum is at most the side-free minimum, so a "
            "negative difference is unreachable and a tie is the strongest "
            "statement available against the admitted primitive"
        ),
        "problems": problems,
        "passed": not problems,
    }


MIRROR_FIELDS: tuple[str, ...] = (
    "mu1",
    "mu2",
    "satisfies",
    "satisfies_second_reading",
    "class_key",
    "effective_structure",
    "collateral_facts",
    "one_step",
    "bundles",
    "coordinates",
    "capability_coordinates",
)
MIRROR_DETAIL_FIELDS: tuple[str, ...] = (
    "automorphism_count",
    "automorphism_entries",
    "no_permitted_renaming_moves_an_index",
    "orbit_size",
    "marks",
    "labels",
    "permitted_renamings",
    "invariant_mark_properties",
    "separating_mark_properties",
    "invariant_separating_mark_properties",
    "history",
)


def gate_mirror_matches_the_pin(rows_by_reading: dict[str, list[Json]]) -> Json:
    problems: list[str] = []
    compared = 0
    for reading, rows in rows_by_reading.items():
        pinned_points = {str(r["name"]): r for r in pin_rows(reading, "points")}
        pinned_detail = {str(r["name"]): r for r in pin_verdict_rows(reading)}
        block = pin_reading(reading)
        if len(rows) != int(str(block["space_size"])):
            problems.append(f"reading {reading}: space size {len(rows)}")
        refused = sum(1 for r in rows if r["bundles"])
        if refused != int(str(block["bundles_refused_count"])):
            problems.append(f"reading {reading}: refused bundles {refused}")
        for row in rows:
            name = str(row["name"])
            pinned = pinned_points.get(name)
            if pinned is None:
                problems.append(f"reading {reading}: {name} is absent from the pin")
                continue
            for field in MIRROR_FIELDS:
                if row[field] != pinned[field]:
                    problems.append(
                        f"reading {reading} {name}.{field}: {row[field]!r} "
                        f"against pinned {pinned[field]!r}"
                    )
            compared += 1
            detail = pinned_detail.get(name)
            if detail is not None:
                for field in MIRROR_DETAIL_FIELDS:
                    if row[field] != detail[field]:
                        problems.append(
                            f"reading {reading} {name}.{field}: {row[field]!r} "
                            f"against pinned {detail[field]!r}"
                        )
        got = minima(rows, "mu1")
        want = block["minima_by_mu1"]
        if not isinstance(want, dict):
            raise TypeError("the pinned minima block is not an object")
        for field in ("minimum", "points", "class_count", "unique"):
            if got[field] != want[field]:
                problems.append(
                    f"reading {reading} minima.{field}: {got[field]!r} "
                    f"against pinned {want[field]!r}"
                )
        got_members = [as_dict(c)["members"] for c in as_list(got["classes"])]
        want_members = [
            c["members"] for c in want["classes"] if isinstance(c, dict)
        ]
        if got_members != want_members:
            problems.append(
                f"reading {reading} minima classes: {got_members!r} against "
                f"pinned {want_members!r}"
            )
    return {
        "gate": "G6",
        "name": "mirror_matches_the_pin",
        "rows_compared": compared,
        "status_of_the_mirror": (
            "a countermodel-domain object of this tree, never claimed to be "
            "the pinned carrier; a divergence VOIDS the run"
        ),
        "problems": problems,
        "passed": not problems,
    }


# ---------------------------------------------------------------------------
# The deletion register: a closure over the pinned source's own names
# ---------------------------------------------------------------------------
#
# The POPULATION is enumerated independently of the classifier: it is the set
# of pinned defined names carrying a deleted word component (the direct seed),
# together with every pinned top-level definition whose body reaches one of
# those names (the closure).  A required test recomputes that population
# from the pinned source at the pinned commit and requires it to equal the
# names below, so the register cannot quietly lose an entry.
#
# The CLASSIFICATION is declared here, by reading this tree's own modules, and
# is held in BOTH directions by tests: every DELETED name must be absent from
# the side-free modules' identifier census, and every NARROWED name must be
# present in it.  Neither test is computed with the classifier's own pattern.
DELETION_REGISTER: tuple[tuple[str, str, str], ...] = (
    ("CONVENTIONS", "DELETED", "direct: the name carries the deleted component conventions"),
    ("DECLARED_CONVENTION", "DELETED", "direct: the name carries the deleted component convention"),
    ("OTHER_CONVENTION", "DELETED", "direct: the name carries the deleted component convention"),
    ("OnSide", "DELETED", "direct: the name carries the deleted component side"),
    ("PRESENTED_SIDES", "DELETED", "direct: the name carries the deleted component sides"),
    ("READINGS", "DELETED", "direct: the name carries the deleted component readings"),
    ("READING_O", "DELETED", "direct: the name carries the deleted component reading"),
    ("READING_O_BUNDLE", "DELETED", "direct: the name carries the deleted component reading"),
    ("READING_U", "DELETED", "direct: the name carries the deleted component reading"),
    ("REQUIREMENT_READINGS_AGREE_BECAUSE", "DELETED", "direct: the name carries the deleted component readings"),
    ("REQUIREMENT_SECOND_READING", "NARROWED", "direct: the name carries the deleted component reading"),
    ("SIDE_NAMES", "DELETED", "direct: the name carries the deleted component side"),
    ("SideNamed", "DELETED", "direct: the name carries the deleted component side"),
    ("admitted_side", "DELETED", "direct: the name carries the deleted component side"),
    ("convention", "DELETED", "direct: the name carries the deleted component convention"),
    ("convention_facts", "DELETED", "direct: the name carries the deleted component convention"),
    ("different_sides_census", "DELETED", "direct: the name carries the deleted component sides"),
    ("expected_placement", "DELETED", "direct: the name carries the deleted component placement"),
    ("is_automorphism_reflection", "DELETED", "direct: the name carries the deleted component reflection"),
    ("mark_side", "DELETED", "direct: the name carries the deleted component side"),
    ("marks_on_different_sides", "DELETED", "direct: the name carries the deleted component sides"),
    ("on_side_0", "DELETED", "direct: the name carries the deleted component side"),
    ("on_side_1", "DELETED", "direct: the name carries the deleted component side"),
    ("other_convention", "DELETED", "direct: the name carries the deleted component convention"),
    ("placement", "DELETED", "direct: the name carries the deleted component placement"),
    ("presented_side", "DELETED", "direct: the name carries the deleted component side"),
    ("reading", "DELETED", "direct: the name carries the deleted component reading"),
    ("reading_facts", "DELETED", "direct: the name carries the deleted component reading"),
    ("reflect", "DELETED", "direct: the name carries the deleted component reflect"),
    ("reflection", "DELETED", "direct: the name carries the deleted component reflection"),
    ("reflection_permitted", "DELETED", "direct: the name carries the deleted component reflection"),
    ("refused_under_every_convention", "DELETED", "direct: the name carries the deleted component convention"),
    ("side", "DELETED", "direct: the name carries the deleted component side"),
    ("side_exchange", "DELETED", "direct: the name carries the deleted component side"),
    ("side_exchanging_automorphism", "DELETED", "direct: the name carries the deleted component side"),
    ("side_exchanging_automorphism_under", "DELETED", "direct: the name carries the deleted component side"),
    ("side_profile", "DELETED", "direct: the name carries the deleted component side"),
    ("sides_collapsed", "DELETED", "direct: the name carries the deleted component sides"),
    ("sides_fact_agrees_with_the_requirement", "DELETED", "direct: the name carries the deleted component sides"),
    ("withdraw_reflection", "DELETED", "direct: the name carries the deleted component reflection"),
    ("AdmitMark", "NARROWED", "via: its pinned definition reaches side"),
    ("AdmitOccurrence", "NARROWED", "via: its pinned definition reaches side"),
    ("Augmentation", "NARROWED", "via: its pinned definition reaches withdraw_reflection"),
    ("DECLARED_MARK_PROPERTIES", "NARROWED", "via: its pinned definition reaches on_side_0, on_side_1"),
    ("OBSERVATION_TYPES", "NARROWED", "via: its pinned definition reaches OnSide, SideNamed"),
    ("Observation", "NARROWED", "via: its pinned definition reaches OnSide, SideNamed"),
    ("Regime", "NARROWED", "via: its pinned definition reaches READINGS, placement, reading"),
    ("Whole", "NARROWED", "via: its pinned definition reaches PRESENTED_SIDES, presented_side"),
    ("admission_event", "NARROWED", "via: its pinned definition reaches admitted_side, convention, presented_side"),
    ("automorphism_facts", "DELETED", "via: its pinned definition reaches reflect, side_exchange, side_exchanging_automorphism"),
    ("automorphisms_under", "NARROWED", "via: its pinned definition reaches reflection"),
    ("build", "DELETED", "via: its pinned definition reaches READING_O, READING_U, REQUIREMENT_READINGS_AGREE_BECAUSE"),
    ("caller_history", "NARROWED", "via: its pinned definition reaches admitted_side, convention, presented_side"),
    ("candidate_history", "NARROWED", "via: its pinned definition reaches convention"),
    ("canonical", "DELETED", "via: its pinned definition reaches READING_U, reading, reflect"),
    ("canonical_under", "NARROWED", "via: its pinned definition reaches reflection"),
    ("changed_coordinates", "NARROWED", "via: its pinned definition reaches withdraw_reflection"),
    ("class_key", "DELETED", "via: its pinned definition reaches reading"),
    ("collateral_facts", "NARROWED", "via: its pinned definition reaches other_convention, reading, side_exchanging_automorphism_under"),
    ("comparison_regimes", "NARROWED", "via: its pinned definition reaches DECLARED_CONVENTION, OTHER_CONVENTION, other_convention"),
    ("contents", "DELETED", "via: its pinned definition reaches placement, side"),
    ("counterfactual_square", "DELETED", "via: its pinned definition reaches _convention, reading, reflection_permitted"),
    ("domain_images", "NARROWED", "via: its pinned definition reaches reflection"),
    ("effective_structure", "NARROWED", "via: its pinned definition reaches reading, reflection_permitted"),
    ("event_json", "NARROWED", "via: its pinned definition reaches side"),
    ("fixed_up_to_mark_renaming", "DELETED", "via: its pinned definition reaches reflect"),
    ("flags", "NARROWED", "via: its pinned definition reaches reading, reflection_permitted"),
    ("genesis", "NARROWED", "via: its pinned definition reaches reading"),
    ("identity_policy_facts", "DELETED", "via: its pinned definition reaches CONVENTIONS, convention, refused_under_every_convention"),
    ("is_isomorphic_under", "NARROWED", "via: its pinned definition reaches reading, reflection"),
    ("isomorphism_witness", "DELETED", "via: its pinned definition reaches reading"),
    ("label_facts", "DELETED", "via: its pinned definition reaches placement, reading"),
    ("later_event_facts", "DELETED", "via: its pinned definition reaches OnSide, mark_side"),
    ("mark_automorphism_to_under", "NARROWED", "via: its pinned definition reaches reflection"),
    ("mark_form_invariant", "DELETED", "via: its pinned definition reaches OnSide, side"),
    ("mark_observations", "NARROWED", "via: its pinned definition reaches OnSide, placement"),
    ("mark_orbit_under", "NARROWED", "via: its pinned definition reaches reflection"),
    ("mark_profile", "NARROWED", "via: its pinned definition reaches OnSide"),
    ("marks_separable_under", "NARROWED", "via: its pinned definition reaches reflection"),
    ("name_observations", "DELETED", "via: its pinned definition reaches READING_U, SIDE_NAMES, SideNamed"),
    ("names_admitted", "DELETED", "via: its pinned definition reaches READING_O, reading"),
    ("observation_holds", "NARROWED", "via: its pinned definition reaches OnSide, READING_O, SIDE_NAMES"),
    ("one_step_detail", "DELETED", "via: its pinned definition reaches DECLARED_CONVENTION, SIDE_NAMES, _convention"),
    ("orbit_property_separates", "DELETED", "via: its pinned definition reaches _reflection, reading"),
    ("order_facts", "DELETED", "via: its pinned definition reaches DECLARED_CONVENTION, placement"),
    ("permitted_images", "DELETED", "via: its pinned definition reaches READING_U, reading, reflect"),
    ("permitted_images_under", "NARROWED", "via: its pinned definition reaches reflect, reflection"),
    ("point_row", "DELETED", "via: its pinned definition reaches _convention, reading"),
    ("policy_event", "DELETED", "via: its pinned definition reaches side"),
    ("policy_facts", "DELETED", "via: its pinned definition reaches convention, placement"),
    ("price_facts", "DELETED", "via: its pinned definition reaches READING_O, reading"),
    ("process_admission_facts", "DELETED", "via: its pinned definition reaches DECLARED_CONVENTION, reading"),
    ("property_domain", "NARROWED", "via: its pinned definition reaches placement, reading"),
    ("regime_domain", "DELETED", "via: its pinned definition reaches placement, reading"),
    ("relabelled", "NARROWED", "via: its pinned definition reaches placement, reading"),
    ("rename_marks", "NARROWED", "via: its pinned definition reaches placement, reading"),
    ("requirement_met", "DELETED", "via: its pinned definition reaches reading"),
    ("retained_facts", "DELETED", "via: its pinned definition reaches DECLARED_CONVENTION, marks_on_different_sides, placement"),
    ("score", "DELETED", "via: its pinned definition reaches SIDE_NAMES, withdraw_reflection"),
    ("score_c1x", "DELETED", "via: its pinned definition reaches SIDE_NAMES"),
    ("separating_mark_forms", "DELETED", "via: its pinned definition reaches OnSide, side"),
    ("separation_facts", "DELETED", "via: its pinned definition reaches READING_O, SIDE_NAMES, mark_side"),
    ("serialize", "NARROWED", "via: its pinned definition reaches placement, reading"),
    ("serialize_keeping_labels", "NARROWED", "via: its pinned definition reaches placement, reading"),
    ("step", "NARROWED", "via: its pinned definition reaches placement, reading, side"),
    ("DeepRegime", "DELETED", "via: its pinned definition reaches READINGS, reading, side"),
    ("Renamings", "DELETED", "via: its pinned definition reaches reflection"),
    ("_read_nested", "DELETED", "via: its pinned definition reaches _split_sides"),
    ("_split_sides", "DELETED", "direct: the name carries the deleted component sides"),
    ("configurations_isomorphic", "DELETED", "via: its pinned definition reaches reading"),
    ("deep_genesis", "DELETED", "via: its pinned definition reaches reading"),
    ("deep_is_isomorphic", "DELETED", "via: its pinned definition reaches reading"),
    ("deep_rename_marks", "DELETED", "via: its pinned definition reaches reading"),
    ("deep_serialize", "DELETED", "via: its pinned definition reaches reading"),
    ("deep_step", "DELETED", "via: its pinned definition reaches reading, side"),
    ("exchange_level", "DELETED", "via: its pinned definition reaches reading, side"),
    ("flatten_deep", "DELETED", "via: its pinned definition reaches reading"),
    ("pair_marks", "DELETED", "via: its pinned definition reaches admitted_side, convention"),
    ("permitted_configuration_images", "DELETED", "via: its pinned definition reaches reflection"),
)


# ---------------------------------------------------------------------------
# The two carriers, enumerated by the one generic enumerator
# ---------------------------------------------------------------------------


def control_rows() -> list[Json]:
    return enumerate_rows(ctl.SideFreeCarrier())


def mirror_rows() -> dict[str, list[Json]]:
    return {
        reading: enumerate_rows(mir.MirrorCarrier(reading))
        for reading in (mir.READING_U, mir.READING_O)
    }


def joined_routes() -> list[tuple[str, list[str]]]:
    """The cross-world join, by string equality on the coordinate names.

    A rename fails this join BY NAME rather than silently dropping a route: an
    unjoined control name appears with an empty pinned member list, and the
    route table reports the failure instead of omitting the row.
    """
    out: list[tuple[str, list[str]]] = [("base", ["base"])]
    for name in ctl.COORDINATES:
        collapsed = sorted(k for k, v in COLLAPSE_MAP.items() if v == name)
        out.append((name, collapsed or [name]))
    return out


def route_table(rows: Sequence[Json], pinned_reading: str) -> list[Json]:
    """The two price lists side by side, cell by cell.  Reported, not deciding."""
    pinned = {str(r["name"]): r for r in pin_verdict_rows(pinned_reading)}
    table: list[Json] = []
    for control_name, pinned_names in joined_routes():
        row = named(rows, control_name)
        members = [pinned[n] for n in pinned_names if n in pinned]
        verdicts = sorted({bool(m["satisfies"]) for m in members})
        table.append(
            {
                "coordinate": control_name,
                "pinned_members": pinned_names,
                "joined": len(members) == len(pinned_names) and bool(members),
                "control_satisfies": bool(row["satisfies"]),
                "control_automorphisms": int(str(row["automorphism_count"])),
                "control_mu1": int(str(row["mu1"])),
                "pinned_satisfies": verdicts[0] if len(verdicts) == 1 else None,
                "pinned_verdicts_uniform": len(verdicts) == 1,
                "pinned_automorphisms": [
                    int(str(m["automorphism_count"])) for m in members
                ],
                "pinned_mu1": [int(str(m["mu1"])) for m in members],
                "agrees": len(verdicts) == 1 and verdicts[0] == bool(row["satisfies"]),
            }
        )
    return table


UNMATCHED_PINNED_ROUTES: tuple[Json, ...] = (
    {
        "coordinate": "withdraw_reflection",
        "removed_because": (
            "its pinned capability sentence names the sides, so the mechanical "
            "criterion drops it"
        ),
        "side_free_counterpart": None,
        "counterpart_note": (
            "there is none: withdrawing an exchange of two sides has no "
            "statement in a world with no sides"
        ),
    },
    {
        "coordinate": "admit_names",
        "removed_because": (
            "its pinned capability sentence names the sides, so the mechanical "
            "criterion drops it"
        ),
        "side_free_counterpart": "keep_labels",
        "counterpart_note": (
            "the nearest surviving route of the same shape -- a name made "
            "internally available -- is keep_labels, and it FAILS in both "
            "worlds, so a naming route is worth nothing in either"
        ),
    },
)


# ---------------------------------------------------------------------------
# The endowment ledger: a report, not a fairness proof, and computed except
# at the cells each row flags as declared
# ---------------------------------------------------------------------------

CONTROL_GENERATOR_KEYS: tuple[str, ...] = ("mark_permutations",)
MIRROR_GENERATOR_KEYS: tuple[str, ...] = ("side_exchange", "mark_permutations")

# The three columns of the ledger, declared once so that a cell census counts
# cells and never rows.  A row times these is the cell population.
LEDGER_COLUMNS: tuple[str, ...] = ("control", "unnamed", "named")

# The endowment cells this module DECLARES rather than computes, kept apart
# from the computed ones exactly as ``comparison.py`` keeps ``Declared`` apart
# from ``Computed``: a typed-in value must not be read as a measurement.  The
# map is total over the ledger -- a row absent from it has no declared column
# -- and every row carries the answer in its own ``declared_columns`` field.
DECLARED_ENDOWMENT_CELLS: dict[str, tuple[str, ...]] = {
    "declarations_at_genesis": ("control", "unnamed", "named"),
    "coordinates_the_genesis_declaration_fixes": ("control",),
}

WHY_ENDOWMENT_CELLS_ARE_DECLARED: dict[str, str] = {
    "declarations_at_genesis": (
        "what a carrier declares at genesis is prose in all three columns: "
        "nothing in either carrier enumerates its own genesis declaration, so "
        "the three cells are statements ABOUT the carriers and not readings "
        "taken off them"
    ),
    "coordinates_the_genesis_declaration_fixes": (
        "the two reading columns are computed against the carrier's inherited "
        "defaults; this control has no reading level to declare at, so its "
        "zero is the statement that there is nothing here to compute and is "
        "not the outcome of a comparison"
    ),
}


def generators(base_row: Json, keys: Sequence[str]) -> int:
    """How many declared renaming generators the carrier permits at base."""
    permitted = base_row["permitted_renamings"]
    if not isinstance(permitted, dict):
        raise TypeError("a base row carries no permitted renamings")
    return sum(1 for key in keys if bool(permitted[key]))


def forms_with_a_holding_instance(pairs: Sequence[tuple[str, bool]]) -> list[str]:
    """The named forms that hold somewhere.  One collector, both worlds."""
    return [name for name, holds in pairs if holds]


def control_judgment_forms() -> list[str]:
    """The judgment forms with a non-empty extension somewhere in the domain."""
    domain = ctl.property_domain(2)
    return forms_with_a_holding_instance(
        [
            (
                "Admitted",
                any(
                    observation_holds(r, Admitted(i))
                    for r in domain
                    for i in range(r.n_marks())
                ),
            )
        ]
    )


def mirror_judgment_forms(reading: str) -> list[str]:
    domain = mir.property_domain(reading, 2)
    return forms_with_a_holding_instance(
        [
            (
                "OnSide",
                any(
                    mir.observation_holds(r, mir.OnSide(i, s))
                    for r in domain
                    for i in range(r.n_marks())
                    for s in (0, 1)
                ),
            ),
            (
                "SideNamed",
                any(
                    mir.observation_holds(r, mir.SideNamed(s, n))
                    for r in domain
                    for s in (0, 1)
                    for n in mir.SIDE_NAMES
                ),
            ),
        ]
    )


def control_judgments_at_genesis() -> int:
    return len(mark_observations(genesis()))


def mirror_judgments_at_genesis(reading: str) -> int:
    holding = len(mir.mark_observations(mir.genesis(reading)))
    return holding + (2 if mir.names_admitted(reading, mir.NULL_AUGMENTATION) else 0)


def mirror_coordinates_fixed_at_genesis(reading: str) -> int:
    """Coordinates the reading's genesis declaration fixes away from the
    carrier's inherited defaults.

    The reference is the structure a carrier declares with no reading-level
    declaration beyond the one primitive itself, which in that world is
    reading U at the null augmentation.
    """
    inherited = mir.effective_structure(mir.READING_U, mir.NULL_AUGMENTATION)
    here = mir.effective_structure(reading, mir.NULL_AUGMENTATION)
    return sum(1 for a, b in zip(inherited, here) if a != b)


def endowment_ledger(rows: Sequence[Json], mrows: dict[str, list[Json]]) -> Json:
    control_base = named(rows, "base")
    u_base = named(mrows[mir.READING_U], "base")
    o_base = named(mrows[mir.READING_O], "base")
    shared = list(ctl.COLLATERAL_FACTS)

    def facts_at_base(base_row: Json) -> Json:
        block = base_row["collateral_facts"]
        if not isinstance(block, dict):
            raise TypeError("a base row carries no collateral facts")
        return {name: bool(block[name]) for name in shared}

    ledger: list[Json] = [
        {
            "row": "declarations_at_genesis",
            "control": [],
            "unnamed": ["one whole with two sides, the two left unnamed"],
            "named": [
                "one whole with two sides",
                "the two sides carry admitted names",
            ],
        },
        {
            "row": "coordinates_the_genesis_declaration_fixes",
            "control": 0,
            "unnamed": mirror_coordinates_fixed_at_genesis(mir.READING_U),
            "named": mirror_coordinates_fixed_at_genesis(mir.READING_O),
            "price_if_bought": len(mir.changed_coordinates(mir.READING_O_BUNDLE)),
        },
        {
            "row": "judgment_forms",
            "control": control_judgment_forms(),
            "unnamed": mirror_judgment_forms(mir.READING_U),
            "named": mirror_judgment_forms(mir.READING_O),
        },
        {
            "row": "judgments_holding_at_genesis",
            "control": control_judgments_at_genesis(),
            "unnamed": mirror_judgments_at_genesis(mir.READING_U),
            "named": mirror_judgments_at_genesis(mir.READING_O),
        },
        {
            "row": "renamings_at_the_retained_regime",
            "control": {
                "automorphism_order": control_base["automorphism_count"],
                "generators": generators(control_base, CONTROL_GENERATOR_KEYS),
            },
            "unnamed": {
                "automorphism_order": u_base["automorphism_count"],
                "generators": generators(u_base, MIRROR_GENERATOR_KEYS),
            },
            "named": {
                "automorphism_order": o_base["automorphism_count"],
                "generators": generators(o_base, MIRROR_GENERATOR_KEYS),
            },
        },
        {
            "row": "invariant_and_separating_mark_properties_at_base",
            "control": control_base["invariant_separating_mark_properties"],
            "unnamed": u_base["invariant_separating_mark_properties"],
            "named": o_base["invariant_separating_mark_properties"],
        },
        {
            "row": "collateral_facts_both_worlds_can_state",
            "control": facts_at_base(control_base),
            "unnamed": facts_at_base(u_base),
            "named": facts_at_base(o_base),
        },
    ]
    for entry in ledger:
        declared = list(DECLARED_ENDOWMENT_CELLS.get(str(entry["row"]), ()))
        entry["declared_columns"] = declared
        # DEFINITION-level here means what it means in ``comparison.py``:
        # declared on BOTH sides, so the row's agreement unfolds declarations
        # rather than measurements.  A row declared in the control column
        # alone is NOT that, and this flag is what says so.
        entry["definition_level"] = len(declared) == len(LEDGER_COLUMNS)
    mismatching = [
        str(entry["row"])
        for entry in ledger
        if not (entry["control"] == entry["unnamed"] == entry["named"])
    ]
    priced = [
        str(entry["row"])
        for entry in ledger
        if str(entry["row"]) in mismatching and "price_if_bought" in entry
    ]
    return {
        "rows": ledger,
        "mismatching_rows": mismatching,
        "mismatching_rows_with_a_stated_price": priced,
        "mismatching_rows_with_no_stated_price": [
            row for row in mismatching if row not in priced
        ],
        "columns": list(LEDGER_COLUMNS),
        "rows_with_a_declared_column": [
            str(entry["row"]) for entry in ledger if entry["declared_columns"]
        ],
        "declared_cells": [
            f"{entry['row']}:{column}"
            for entry in ledger
            for column in LEDGER_COLUMNS
            if column in as_list(entry["declared_columns"])
        ],
        "computed_cells": [
            f"{entry['row']}:{column}"
            for entry in ledger
            for column in LEDGER_COLUMNS
            if column not in as_list(entry["declared_columns"])
        ],
        "definition_level_rows": [
            str(entry["row"]) for entry in ledger if entry["definition_level"]
        ],
        "why_the_declared_cells_are_declared": dict(
            WHY_ENDOWMENT_CELLS_ARE_DECLARED
        ),
        "named_mismatches": [
            "the control has one renaming generator fewer than the unnamed "
            "reading: the side exchange has no side-free statement",
            "the named reading holds two judgments at genesis that the control "
            "cannot hold, and that mismatch is UNMATCHABLE: a container exists "
            "before its contents, an order does not",
        ],
        "status": (
            "a report, not a fairness proof, computed by the same code in each "
            "column at every cell no row flags as declared.  Mismatching rows "
            "are NAMED and never smoothed; a price is stated for the rows this "
            "tree computes one for and for no others, and both lists are here"
        ),
    }


# ---------------------------------------------------------------------------
# Censuses, identity policies, caller histories
# ---------------------------------------------------------------------------


def census_block() -> Json:
    control_kept = ctl.withdrawal_census(True)
    control_withdrawn = ctl.withdrawal_census(False)
    mirror_kept = mir.withdrawal_census(True)
    mirror_withdrawn = mir.withdrawal_census(False)
    return {
        "withdrawal": {
            "declared_domain": {
                "control": (
                    "the two declared labels in each of the two retained "
                    "positions, and each keep_labels value"
                ),
                "mirror": (
                    "the two declared labels in each of the two retained "
                    "positions, each reading, each keep_labels value, and each "
                    "placement"
                ),
            },
            "control": {
                "cells": len(control_kept),
                "separating_with_permutations_kept": sum(control_kept),
                "separating_with_permutations_withdrawn": sum(control_withdrawn),
            },
            "mirror": {
                "cells": len(mirror_kept),
                "separating_with_permutations_kept": sum(mirror_kept),
                "separating_with_permutations_withdrawn": sum(mirror_withdrawn),
            },
        },
        "route": (
            "per candidate, in each row's route_census field, over that world's "
            "own two-mark configuration domain at that candidate's own flags"
        ),
    }


def refusal_message(thunk: Callable[[], object]) -> str | None:
    """The message a refusal carries, or ``None`` when nothing was refused.

    One capture point, so a refusal is always reported by name and never
    silently converted into a value.
    """
    try:
        thunk()
    except ValueError as exc:
        return str(exc)
    return None


def identity_policies() -> Json:
    wholes = ctl.caller_wholes()
    declared = replay(ctl.caller_history(wholes), genesis())
    shared = replay(ctl.shared_policy_history(wholes), genesis())
    i, j = RETAINED_MARKS
    refusal = refusal_message(lambda: marks_separable_under(shared, i, j, True, False))
    fresh = refusal_message(lambda: replay([AdmitOccurrence("q")], genesis()))
    one_mark = Regime((ctl.SUPPLIED_TOKEN,))
    return {
        "declared_policy": {
            "name": "occurrence identity: an admission admits a fresh mark",
            "marks": declared.n_marks(),
            "requirement_has_a_subject": declared.n_marks() > 1,
            "inherited": (
                "already paid, exactly as the pinned world pays it one rung "
                "earlier; the inheritance is visible here rather than assumed"
            ),
        },
        "shared_policy": {
            "name": "shared identity: an admission names the mark its token names",
            "marks": shared.n_marks(),
            "requirement_has_a_subject": shared.n_marks() > 1,
            "refusal_of_the_subject": refusal,
            "reading": (
                "a REFUSAL OF THE SUBJECT, never a false and never a satisfied "
                "requirement: side-free the second admission is admit-then-no-op"
            ),
        },
        "removed_refusal": REMOVED_REFUSAL,
        "removed_refusal_computed_consequence": {
            "second_admission_of_an_admitted_label_is_a_no_op": (
                step(one_mark, AdmitMark(ctl.SUPPLIED_TOKEN)) == one_mark
            ),
            "note": (
                "the pinned refusal fired when the second admission named the "
                "OTHER side.  There is no other side here, so the no-op is the "
                "whole of what is left, and nothing was absorbed into it"
            ),
        },
        "never_supplied_token_refusal": fresh,
    }


def caller_histories() -> Json:
    wholes = ctl.caller_wholes()
    forward = replay(ctl.caller_history(wholes), genesis())
    backward = replay(ctl.caller_history(list(reversed(wholes))), genesis())
    return {
        "inscriptions": list(ctl.INSCRIPTIONS),
        "wholes": [
            {"token": w.token, "presented_position": w.presented_position}
            for w in wholes
        ],
        "presentation_is_metatheory": (
            "the presented position reaches nothing in the carrier: it is not "
            "an argument of any event, and the convention that would have made "
            "it one is deleted"
        ),
        "forward_marks": list(forward.marks),
        "reversed_marks": list(backward.marks),
        "the_two_orders_give_the_same_regime": forward == backward,
        "order_fact_reason": ctl.ORDER_FACT_REASON,
    }


# ---------------------------------------------------------------------------
# The two second measures, and why only one of them crosses
# ---------------------------------------------------------------------------

MU2_IS_NEVER_DIFFERENCED = (
    "mu2 counts each carrier's OWN collateral facts and the two lists are not "
    "the same length, so a raw cross-world difference would charge the pinned "
    "world one unit for re-reporting the answer: the pinned receipt itself "
    "computes that its first collateral fact takes the requirement's value at "
    "every point of its space.  This receipt therefore carries NO cross-world "
    "mu2 difference field anywhere, and a test asserts it.  Only "
    "mu2_restricted, over the two facts both worlds can state, ever appears in "
    "a cross-carrier comparison"
)


def mu2_restricted_from_pin(reading: str) -> dict[str, int]:
    """The restricted second measure, by DATA JOIN from the pinned receipt.

    Read from the pin's own per-point collateral facts, never by importing
    pinned code.  It is compared with the mirror's independently computed
    value, so a divergence between the re-declaration and the pin is visible
    here as well as at G6.
    """
    base = pin_reading(reading)["base"]
    if not isinstance(base, dict):
        raise TypeError("the pinned base row is not an object")
    base_facts = base["collateral_facts"]
    if not isinstance(base_facts, dict):
        raise TypeError("the pinned base row carries no collateral facts")
    out: dict[str, int] = {}
    for row in pin_rows(reading, "points"):
        facts = row["collateral_facts"]
        if not isinstance(facts, dict):
            raise TypeError("a pinned point carries no collateral facts")
        out[str(row["name"])] = sum(
            1
            for name in mir.RESTRICTED_FACTS
            if bool(facts[name]) and not bool(base_facts[name])
        )
    return out


def mu2_block(rows: Sequence[Json], mrows: dict[str, list[Json]]) -> Json:
    joins: Json = {}
    problems: list[str] = []
    for reading, table in mrows.items():
        from_pin = mu2_restricted_from_pin(reading)
        mismatched = [
            str(r["name"])
            for r in table
            if int(str(r["mu2_restricted"])) != from_pin[str(r["name"])]
        ]
        joins[reading] = {
            "rows_joined": len(from_pin),
            "mismatched_rows": mismatched,
        }
        problems.extend(
            f"reading {reading}: mu2_restricted differs from the pin at {name}"
            for name in mismatched
        )
    return {
        "declaration": MU2_IS_NEVER_DIFFERENCED,
        "control_fact_list": list(ctl.COLLATERAL_FACTS),
        "mirror_fact_list": list(mir.COLLATERAL_FACTS),
        "restricted_fact_list": list(mir.RESTRICTED_FACTS),
        "pinned_facts_without_a_side_free_subject": list(
            ctl.PINNED_COLLATERAL_FACTS_WITHOUT_A_SIDE_FREE_SUBJECT
        ),
        "control_minima_by_mu2": minima(rows, "mu2"),
        "mirror_minima_by_mu2": {
            reading: minima(table, "mu2") for reading, table in mrows.items()
        },
        "control_minima_by_mu2_restricted": minima(rows, "mu2_restricted"),
        "mirror_minima_by_mu2_restricted": {
            reading: minima(table, "mu2_restricted")
            for reading, table in mrows.items()
        },
        "data_join_against_the_pin": joins,
        "problems": problems,
    }


# ---------------------------------------------------------------------------
# The deletion register
# ---------------------------------------------------------------------------


def deletion_register_block() -> Json:
    census = side_free_identifiers()
    deleted = [name for name, kind, _why in DELETION_REGISTER if kind == "DELETED"]
    narrowed = [name for name, kind, _why in DELETION_REGISTER if kind == "NARROWED"]
    survivors = sorted(name for name in deleted if name in census)
    absent = sorted(name for name in narrowed if name not in census)
    stem_leaks = sorted(
        name
        for name in census
        if carries_a_deleted_stem(name) and name not in DELETION_WORD_ALLOWLIST
    )
    return {
        "entries": [
            {"name": name, "kind": kind, "reason": why}
            for name, kind, why in DELETION_REGISTER
        ],
        "deleted_count": len(deleted),
        "narrowed_count": len(narrowed),
        "modules_scanned": list(SIDE_FREE_MODULES),
        "modules_excluded_by_declaration": {
            "mirror.py": "the side-typed countermodel-domain object",
            "control.py": "the comparison driver",
            "why": (
                "both must be able to NAME the deleted structure in order to "
                "compare against it; the exclusion is declared here rather "
                "than left implicit in a glob"
            ),
        },
        "identifier_census_size": len(census),
        "deleted_names_surviving": survivors,
        "narrowed_names_absent": absent,
        "deleted_stem_leaks": stem_leaks,
        "stem_allowlist": dict(DELETION_WORD_ALLOWLIST_REASONS),
        "removed_refusal": REMOVED_REFUSAL,
        "scan_reads_the_syntax": (
            "identifiers are read from the syntax tree, not from the text, so "
            "a deleted word inside a comment or a doc string -- which is how a "
            "deletion gets explained -- is never mistaken for a use of it"
        ),
        "totality": not survivors and not absent and not stem_leaks,
    }


# ---------------------------------------------------------------------------
# The decided object
# ---------------------------------------------------------------------------


def verdict_value(gates_passed: bool, side_free_minimum: object, delta: object) -> str:
    if not gates_passed:
        return "VOID"
    if side_free_minimum is None:
        return "NO_SATISFYING_CANDIDATE"
    if delta == 0:
        return "NOTHING_IN_COST"
    return f"COST_DIFFERENCE_{delta}"


def decided_object(
    rows: Sequence[Json],
    mrows: dict[str, list[Json]],
    gates_passed: bool,
    exclude: Sequence[str] = (),
) -> Json:
    control_min = minima(rows, "mu1", exclude)
    unnamed_min = minima(
        mrows[mir.READING_U], "mu1", [n for n in exclude_for_mirror(exclude, mrows, mir.READING_U)]
    )
    named_min = minima(
        mrows[mir.READING_O], "mu1", [n for n in exclude_for_mirror(exclude, mrows, mir.READING_O)]
    )
    side_free_minimum = control_min["minimum"]
    unnamed_minimum = unnamed_min["minimum"]
    named_minimum = named_min["minimum"]
    delta_unnamed: object = None
    delta_named: object = None
    if isinstance(side_free_minimum, int):
        if isinstance(unnamed_minimum, int):
            delta_unnamed = side_free_minimum - unnamed_minimum
        if isinstance(named_minimum, int):
            delta_named = side_free_minimum - named_minimum
    control_members = [
        str(name)
        for entry in as_list(control_min["classes"])
        for name in as_list(as_dict(entry)["members"])
    ]
    unnamed_members = sorted(
        {
            COLLAPSE_MAP.get(str(name), str(name))
            for entry in as_list(unnamed_min["classes"])
            for name in as_list(as_dict(entry)["members"])
        }
    )
    bought = sorted(set(unnamed_members) - set(control_members))
    definition_level: object = None
    if len(control_members) == 1:
        definition_level = named(rows, control_members[0])[
            "no_permitted_renaming_moves_an_index"
        ]
    return {
        "side_free_minimum": side_free_minimum,
        "side_free_classes": control_min["class_count"],
        "side_free_unique": control_min["unique"],
        "side_free_minimum_members": control_members,
        "unnamed_minimum": unnamed_minimum,
        "unnamed_classes": unnamed_min["class_count"],
        "unnamed_minimum_members_collapsed": unnamed_members,
        "named_minimum": named_minimum,
        "named_classes": named_min["class_count"],
        "delta_vs_unnamed": delta_unnamed,
        "delta_vs_named": delta_named,
        "plurality_vs_unnamed": (
            int(str(control_min["class_count"])) - int(str(unnamed_min["class_count"]))
        ),
        "plurality_is_not_price": (
            "routes and price are separate columns and are NEVER summed.  A "
            "test walks THIS receipt and requires that the only fields whose "
            "names carry both words are the two copies of this declaration "
            "itself, in the primary block and in the secondary one; a second "
            "test walks the price list's record and requires no such field "
            "there at all"
        ),
        "routes_the_admitted_primitive_bought": bought,
        "routes_bought_count": len(bought),
        "routes_bought_are_side_mediated": (
            "both of them: the withdrawal of the side exchange names the "
            "sides, and the further mark separates the two retained marks "
            "there because the two sides then carry different numbers of marks"
        ),
        "side_free_minimum_is_definition_level": definition_level,
        "what_the_admitted_primitive_bought": verdict_value(
            gates_passed, side_free_minimum, delta_unnamed
        ),
        "excluded": list(exclude),
    }


def exclude_for_mirror(
    exclude: Sequence[str], mrows: dict[str, list[Json]], reading: str
) -> list[str]:
    """Translate an exclusion set into the pinned world's own point names.

    The secondary computation excludes candidates that satisfy at every cell
    of a world's OWN route census, so the exclusion is computed in each world
    separately by the same function rather than carried across by name.
    """
    if not exclude:
        return []
    return everywhere_satisfying(eligible(mrows[reading]))


def secondary_block(
    rows: Sequence[Json], mrows: dict[str, list[Json]], gates_passed: bool
) -> Json:
    control_everywhere = everywhere_satisfying(eligible(rows))
    mirror_everywhere = {
        reading: everywhere_satisfying(eligible(table))
        for reading, table in mrows.items()
    }
    return {
        "declared_in_advance": (
            "frozen in PREDICTIONS.md before the enumeration ran, reported "
            "here, and NEVER deciding.  Both numbers are frozen precisely "
            "because the answer flips between them"
        ),
        "rule": (
            "exclude every candidate that separates at every cell of its own "
            "world's route census, computed in both worlds by the same "
            "function over each world's own census"
        ),
        "control_everywhere_satisfying": control_everywhere,
        "mirror_everywhere_satisfying": mirror_everywhere,
        "decided": decided_object(rows, mrows, gates_passed, control_everywhere),
        "why_the_primary_counts_the_vacuous_route": (
            "excluding it in the control while it stands in the pinned world "
            "would itself be the rigging.  The pinned tree retains it and "
            "records whether the requirement should have been declared so as "
            "to exclude it as OPEN; this control inherits that as OPEN too"
        ),
    }


def key_choice_block(rows: Sequence[Json]) -> Json:
    per_row: list[Json] = []
    problems: list[str] = []
    for r in rows:
        block = r["satisfies_under_key_choice"]
        if not isinstance(block, dict):
            raise TypeError("a row carries no key-choice block")
        values = sorted({bool(v) for v in block.values()})
        per_row.append(
            {
                "name": r["name"],
                "verdicts": {k: bool(v) for k, v in block.items()},
                "agree": len(values) == 1,
            }
        )
        if len(values) != 1:
            problems.append(f"{r['name']}: the two key choices disagree")
    return {
        "choices": list(KEY_CHOICES),
        "declared": DECLARED_KEY_CHOICE,
        "why_the_arity_is_declared": (
            "the pinned key keeps a tuple whose length is the arity, so both "
            "worlds get the arity free.  Of the TWO choices declared here, "
            "arity is the richer and empty the poorer, and a poorer key gives "
            "fewer distinctions and so more automorphisms: within this pair "
            "the declared choice is the more generous to this control, not "
            "the less.  What errs against the control is the scope the frozen "
            "design states -- the arity alone is the poorest DEFENSIBLE key, "
            "against richer keys that lie outside this pair and are not "
            "declared here.  Neither declared choice is load-bearing, and "
            "that is DEFINITION-level rather than a computed finding: a "
            "permitted renaming permutes indices and never changes the mark "
            "count, so the key is constant across the images under either "
            "choice and both admit the same automorphisms.  The rows below "
            "recompute every verdict under both"
        ),
        "rows": per_row,
        "agree_everywhere": not problems,
        "problems": problems,
    }


# ---------------------------------------------------------------------------
# The observation grammar, proved inert rather than merely absent
# ---------------------------------------------------------------------------


def admitted_separates(r: Regime) -> bool:
    """Whether the one judgment form separates the two retained marks here."""
    i, j = RETAINED_MARKS
    return ctl.admitted(r, i) != ctl.admitted(r, j)


def observation_grammar_block(rows: Sequence[Json]) -> Json:
    verdicts = [
        admitted_separates(r)
        for aug in ctl.candidate_space()
        for r in ctl.route_census_regimes(aug)
    ]
    cells = len(verdicts)
    separating = verdicts.count(True)
    return {
        "form": "Admitted",
        "holds_when": "0 <= mark < n_marks()",
        "why_this_and_not_an_empty_grammar": (
            "the pinned side judgment is literally the conjunction of 'the "
            "mark is admitted' and 'its placement is that side', so this is "
            "the side-free conjunct of a pinned judgment: the honest residue, "
            "neither emptied nor enriched.  Unlike an absence it can be PROVED "
            "inert"
        ),
        "extension_at_genesis": control_judgments_at_genesis(),
        "census_cells_checked": cells,
        "census_cells_where_it_separates": separating,
        "inert": separating == 0,
        "rows_reporting_it": [
            {
                "name": r["name"],
                "invariant": "admitted" in as_list(r["invariant_mark_properties"]),
                "separating": "admitted" in as_list(r["separating_mark_properties"]),
            }
            for r in rows
        ],
    }


def summarize(rows: Sequence[Json]) -> Json:
    """The compact per-row view the frozen predictions are scored against."""
    return {
        str(r["name"]): {
            "mu1": r["mu1"],
            "mu2": r["mu2"],
            "mu2_restricted": r["mu2_restricted"],
            "satisfies": r["satisfies"],
            "satisfies_second_reading": r["satisfies_second_reading"],
            "automorphism_count": r["automorphism_count"],
            "no_permitted_renaming_moves_an_index": r[
                "no_permitted_renaming_moves_an_index"
            ],
            "route_census": r["route_census"],
            "collateral_facts": r["collateral_facts"],
            "one_step": r["one_step"],
            "bundles": r["bundles"],
        }
        for r in rows
    }


def withdrawal_port(rows: Sequence[Json]) -> Json:
    """Whether the withdrawal of the mark permutations ports at the same cost."""
    name = "withdraw_mark_permutations"
    here = named(rows, name)
    there = named(pin_verdict_rows(mir.READING_U), name)
    identical = ctl.CAPABILITY_OF[name] == str(
        dig(pin_data(), f"candidate_space.capability_of.{name}")
    )
    same = (
        int(str(here["mu1"])) == int(str(there["mu1"]))
        and bool(here["satisfies"])
        and bool(there["satisfies"])
        and identical
    )
    return {
        "coordinate": name,
        "control_mu1": here["mu1"],
        "pinned_mu1": there["mu1"],
        "control_satisfies": here["satisfies"],
        "pinned_satisfies": there["satisfies"],
        "control_automorphisms": here["automorphism_count"],
        "pinned_automorphisms": there["automorphism_count"],
        "capability_text_identical": identical,
        "same_cost": same,
        "definition_level_here": here["no_permitted_renaming_moves_an_index"],
    }


# ---------------------------------------------------------------------------
# Scoring the frozen predictions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Clause:
    path: str
    expected: object


@dataclass(frozen=True)
class Prediction:
    ident: str
    forced: bool
    quote: str
    clauses: tuple[Clause, ...]


PREDICTIONS: tuple[Prediction, ...] = (
    Prediction(
        "P1",
        False,
        "`side_free_minimum = 1` under `mu1`",
        (Clause("decided.side_free_minimum", 1),),
    ),
    Prediction(
        "P2",
        False,
        "`side_free_classes = 1`, and `unique` is `true`",
        (
            Clause("decided.side_free_classes", 1),
            Clause("decided.side_free_unique", True),
            Clause("decided.side_free_minimum_members", ["withdraw_mark_permutations"]),
        ),
    ),
    Prediction(
        "P3",
        False,
        "It costs `mu1 = 1` in both worlds",
        (
            Clause("withdrawal_port.same_cost", True),
            Clause("withdrawal_port.control_mu1", 1),
            Clause("withdrawal_port.pinned_mu1", 1),
            Clause("withdrawal_port.capability_text_identical", True),
            Clause("withdrawal_port.control_automorphisms", 1),
        ),
    ),
    Prediction(
        "P4",
        False,
        "what_the_admitted_primitive_bought = NOTHING_IN_COST",
        (
            Clause("decided.delta_vs_unnamed", 0),
            Clause("decided.delta_vs_named", 1),
            Clause("decided.what_the_admitted_primitive_bought", "NOTHING_IN_COST"),
            Clause("route_disagreements", ["extra_mark"]),
        ),
    ),
    Prediction(
        "P5",
        False,
        "`mu1 = 0`, **2** automorphisms, FAILS",
        (
            Clause("control.summary.base.mu1", 0),
            Clause("control.summary.base.automorphism_count", 2),
            Clause("control.summary.base.satisfies", False),
        ),
    ),
    Prediction(
        "P6",
        False,
        "**P6 — `keep_labels`.**",
        (
            Clause("control.summary.keep_labels.mu1", 1),
            Clause("control.summary.keep_labels.automorphism_count", 2),
            Clause("control.summary.keep_labels.satisfies", False),
        ),
    ),
    Prediction(
        "P7",
        False,
        "**P7 — `extra_mark`.**",
        (
            Clause("control.summary.extra_mark.mu1", 1),
            Clause("control.summary.extra_mark.automorphism_count", 6),
            Clause("control.summary.extra_mark.satisfies", False),
        ),
    ),
    Prediction(
        "P8",
        True,
        "**P8 — `withdraw_mark_permutations`.**",
        (
            Clause("control.summary.withdraw_mark_permutations.mu1", 1),
            Clause("control.summary.withdraw_mark_permutations.automorphism_count", 1),
            Clause("control.summary.withdraw_mark_permutations.satisfies", True),
            Clause(
                "control.summary.withdraw_mark_permutations."
                "no_permitted_renaming_moves_an_index",
                True,
            ),
        ),
    ),
    Prediction(
        "P9",
        True,
        "Four of the eight points carry",
        (
            Clause("candidate_space.space_size", 8),
            Clause("candidate_space.one_step_count", 3),
            Clause("candidate_space.bundles_refused_count", 4),
        ),
    ),
    Prediction(
        "P10",
        False,
        "`plurality_vs_unnamed = -2`",
        (
            Clause("decided.side_free_classes", 1),
            Clause("decided.unnamed_classes", 3),
            Clause("decided.plurality_vs_unnamed", -2),
        ),
    ),
    Prediction(
        "P11",
        False,
        "`withdraw_reflection` and `extra_mark`, obtained by mapping",
        (
            Clause("decided.routes_bought_count", 2),
            Clause(
                "decided.routes_the_admitted_primitive_bought",
                ["extra_mark", "withdraw_reflection"],
            ),
        ),
    ),
    Prediction(
        "P12",
        False,
        "`base` 0, `keep_labels` 1,",
        (
            Clause("control.summary.base.mu2", 0),
            Clause("control.summary.keep_labels.mu2", 1),
            Clause("control.summary.withdraw_mark_permutations.mu2", 0),
            Clause("control.summary.extra_mark.mu2", 0),
        ),
    ),
    Prediction(
        "P13",
        False,
        "The minimum is **0** in all three",
        (
            Clause("second_measures.control_minima_by_mu2_restricted.minimum", 0),
            Clause("second_measures.mirror_minima_by_mu2_restricted.U.minimum", 0),
            Clause("second_measures.mirror_minima_by_mu2_restricted.O.minimum", 0),
        ),
    ),
    Prediction(
        "P14",
        False,
        "is `false` at every one of the eight points",
        # Both facts at ALL EIGHT points, because that is the population
        # the frozen sentence quantifies over.  Four sampled clauses stood
        # here and would have scored HIT with a violation at any of the
        # twelve unchecked places; P9 pins the point count at eight, so
        # these sixteen are total over it.
        (
            Clause(
                "control.summary.base.collateral_facts."
                "order_internally_available",
                False,
            ),
            Clause(
                "control.summary.extra_mark.collateral_facts."
                "order_internally_available",
                False,
            ),
            Clause(
                "control.summary.keep_labels.collateral_facts."
                "order_internally_available",
                False,
            ),
            Clause(
                "control.summary.keep_labels+extra_mark.collateral_facts."
                "order_internally_available",
                False,
            ),
            Clause(
                "control.summary.withdraw_mark_permutations.collateral_facts."
                "order_internally_available",
                False,
            ),
            Clause(
                "control.summary.withdraw_mark_permutations+extra_mark.collateral_facts."
                "order_internally_available",
                False,
            ),
            Clause(
                "control.summary.withdraw_mark_permutations+keep_labels.collateral_facts."
                "order_internally_available",
                False,
            ),
            Clause(
                "control.summary.withdraw_mark_permutations+keep_labels+extra_mark.collateral_facts."
                "order_internally_available",
                False,
            ),
            Clause(
                "control.summary.base.collateral_facts."
                "label_internally_available",
                False,
            ),
            Clause(
                "control.summary.extra_mark.collateral_facts."
                "label_internally_available",
                False,
            ),
            Clause(
                "control.summary.keep_labels.collateral_facts."
                "label_internally_available",
                True,
            ),
            Clause(
                "control.summary.keep_labels+extra_mark.collateral_facts."
                "label_internally_available",
                True,
            ),
            Clause(
                "control.summary.withdraw_mark_permutations.collateral_facts."
                "label_internally_available",
                False,
            ),
            Clause(
                "control.summary.withdraw_mark_permutations+extra_mark.collateral_facts."
                "label_internally_available",
                False,
            ),
            Clause(
                "control.summary.withdraw_mark_permutations+keep_labels.collateral_facts."
                "label_internally_available",
                True,
            ),
            Clause(
                "control.summary.withdraw_mark_permutations+keep_labels+extra_mark.collateral_facts."
                "label_internally_available",
                True,
            ),
        ),
    ),
    Prediction(
        "P15",
        False,
        "**64 of 64** with the mark permutations withdrawn",
        (
            Clause("censuses.withdrawal.mirror.cells", 64),
            Clause(
                "censuses.withdrawal.mirror.separating_with_permutations_withdrawn", 64
            ),
            Clause("censuses.withdrawal.mirror.separating_with_permutations_kept", 28),
            Clause("censuses.withdrawal.control.cells", 8),
            Clause(
                "censuses.withdrawal.control.separating_with_permutations_withdrawn", 8
            ),
            Clause("censuses.withdrawal.control.separating_with_permutations_kept", 2),
        ),
    ),
    Prediction(
        "P16",
        True,
        "**0** lemma violations and **0** corollary violations",
        (
            Clause("gates.G5.report.violations", 0),
            Clause("gates.G5.report.corollary_violations", 0),
        ),
    ),
    Prediction(
        "P17",
        False,
        "**2140** side-typed automorphisms checked",
        (
            Clause("gates.G5.report.automorphisms_checked", 2140),
            # The frozen sentence describes this count exactly -- cells where
            # the side-typed world separates and the side-free does not -- and
            # then mislabels it as the corollary's non-vacuity.  The clause
            # follows the description to the field that now carries it; the
            # mislabel is recorded in STATUS.md and beside the ledger entry.
            Clause("gates.G5.report.converse_failure_cells", 228),
        ),
    ),
    Prediction(
        "P18",
        False,
        "produces **12** lemma violations",
        (
            Clause("smuggle_tripwire.violations", 12),
            Clause("smuggle_tripwire.first_violation.reading", "U"),
            Clause("smuggle_tripwire.first_violation.labels", ["a", "a"]),
            Clause("smuggle_tripwire.first_violation.placement", [0, 1]),
            Clause("smuggle_tripwire.first_violation.automorphism.reflected", True),
            Clause("smuggle_tripwire.first_violation.automorphism.permutation", [1, 0]),
        ),
    ),
    Prediction(
        "P19",
        False,
        "separates the two retained marks at **no** cell",
        (
            Clause("observation_grammar.inert", True),
            Clause("observation_grammar.census_cells_where_it_separates", 0),
        ),
    ),
    Prediction(
        "P20",
        False,
        "**P20 — G4 agrees on all fourteen rows.**",
        (
            Clause("gates.G4.row_count", 14),
            Clause("gates.G4.agreements", 14),
            Clause("gates.G4.passed", True),
        ),
    ),
    Prediction(
        "P21",
        False,
        "refused-bundle count **41**",
        (
            Clause("gates.G6.passed", True),
            Clause("mirror.U.space_size", 48),
            Clause("mirror.U.bundles_refused_count", 41),
            Clause("mirror.U.minima_by_mu1.minimum", 1),
            Clause("mirror.U.minima_by_mu1.class_count", 3),
            Clause("mirror.O.minima_by_mu1.minimum", 0),
            Clause("mirror.O.minima_by_mu1.class_count", 1),
        ),
    ),
    Prediction(
        "P22",
        False,
        "**P22 — the four numeric rows.**",
        (
            Clause(
                "endowment_ledger.by_row.coordinates_the_genesis_declaration_fixes."
                "control",
                0,
            ),
            Clause(
                "endowment_ledger.by_row.coordinates_the_genesis_declaration_fixes."
                "unnamed",
                0,
            ),
            Clause(
                "endowment_ledger.by_row.coordinates_the_genesis_declaration_fixes."
                "named",
                2,
            ),
            Clause("endowment_ledger.by_row.judgments_holding_at_genesis.control", 0),
            Clause("endowment_ledger.by_row.judgments_holding_at_genesis.unnamed", 0),
            Clause("endowment_ledger.by_row.judgments_holding_at_genesis.named", 2),
            Clause(
                "endowment_ledger.by_row.renamings_at_the_retained_regime.control."
                "automorphism_order",
                2,
            ),
            Clause(
                "endowment_ledger.by_row.renamings_at_the_retained_regime.unnamed."
                "automorphism_order",
                2,
            ),
            Clause(
                "endowment_ledger.by_row.renamings_at_the_retained_regime.named."
                "automorphism_order",
                1,
            ),
            Clause(
                "endowment_ledger.by_row.renamings_at_the_retained_regime.control."
                "generators",
                1,
            ),
            Clause(
                "endowment_ledger.by_row.renamings_at_the_retained_regime.unnamed."
                "generators",
                2,
            ),
            Clause(
                "endowment_ledger.by_row.renamings_at_the_retained_regime.named."
                "generators",
                1,
            ),
        ),
    ),
    Prediction(
        "P23",
        False,
        "yielding\n**one** mark",
        (
            Clause("identity_policies.shared_policy.marks", 1),
            Clause("identity_policies.shared_policy.requirement_has_a_subject", False),
            Clause("identity_policies.declared_policy.marks", 2),
            Clause(
                "identity_policies.removed_refusal_computed_consequence."
                "second_admission_of_an_admitted_label_is_a_no_op",
                True,
            ),
        ),
    ),
    Prediction(
        "P24",
        False,
        "**P24 — key-choice invariance.**",
        (Clause("key_choice_invariance.agree_everywhere", True),),
    ),
    Prediction(
        "P25",
        False,
        "the secondary\n  answer is `NO_SATISFYING_CANDIDATE`",
        (
            Clause(
                "secondary.decided.what_the_admitted_primitive_bought",
                "NO_SATISFYING_CANDIDATE",
            ),
            Clause("secondary.decided.unnamed_minimum", 1),
            Clause("secondary.decided.unnamed_classes", 2),
            Clause("secondary.control_everywhere_satisfying", [
                "withdraw_mark_permutations",
            ]),
        ),
    ),
    Prediction(
        "P26",
        False,
        "**P26 — the decided value.**",
        (Clause("decided.what_the_admitted_primitive_bought", "NOTHING_IN_COST"),),
    ),
    Prediction(
        "P27",
        True,
        "no price that the admission\norder could not buy at the same price",
        (Clause("terminal.sentence_is_the_scoped_one", True),),
    ),
)


def frozen_text(name: str) -> str:
    return (TREE / name).read_text(encoding="utf-8")


LEDGER_CELL_PREFIX = "endowment_ledger.by_row."


def ledger_declared_cells(record: Json) -> list[str] | None:
    """The ledger's declared-cell census, or ``None`` when there is none.

    ``None`` is not the empty list.  A record carrying no census cannot say
    that no cell is declared, and converting that absence into a
    classification is the move this tree bars everywhere else.
    """
    try:
        cells = dig(record, "endowment_ledger.declared_cells")
    except (KeyError, IndexError, TypeError):
        return None
    return [str(name) for name in as_list(cells)]


def ledger_cells_read(clauses: Sequence[Clause], declared: list[str] | None) -> Json:
    """The distinct endowment-ledger CELLS a prediction's clauses read.

    A clause names a path, and several clauses can read one cell: the
    renaming row's cells are objects, so two clauses read one cell there.
    Clauses are therefore not cells, and this counts cells.  Each is then put
    through the ledger's own declared-cell census, so which of a prediction's
    cells are declarations of this tree rather than measurements is computed
    here and never typed into prose.
    """
    cells: list[str] = []
    for clause in clauses:
        if not clause.path.startswith(LEDGER_CELL_PREFIX):
            continue
        parts = clause.path[len(LEDGER_CELL_PREFIX) :].split(".")
        cell = f"{parts[0]}:{parts[1]}"
        if cell not in cells:
            cells.append(cell)
    if declared is None:
        return {
            "cells": sorted(cells),
            "declared": None,
            "computed": None,
            "why_unclassified": (
                "the record carries no endowment_ledger.declared_cells, so the "
                "absence is reported and is NOT read as no cell being declared"
            ),
        }
    return {
        "cells": sorted(cells),
        "declared": sorted(cell for cell in cells if cell in declared),
        "computed": sorted(cell for cell in cells if cell not in declared),
    }


def score_predictions(record: Json) -> Json:
    frozen = frozen_text("PREDICTIONS.md")
    declared_cells = ledger_declared_cells(record)
    scored: list[Json] = []
    for prediction in PREDICTIONS:
        failures: list[Json] = []
        for clause in prediction.clauses:
            try:
                computed = dig(record, clause.path)
            except (KeyError, IndexError, TypeError) as exc:
                failures.append({"path": clause.path, "error": str(exc)})
                continue
            if computed != clause.expected:
                failures.append(
                    {
                        "path": clause.path,
                        "expected": clause.expected,
                        "computed": computed,
                    }
                )
        scored.append(
            {
                "id": prediction.ident,
                "forced": prediction.forced,
                "status": "HIT" if not failures else "MISS",
                "clauses": len(prediction.clauses),
                "failures": failures,
                "quote": prediction.quote,
                "quote_found_in_the_frozen_file": prediction.quote in frozen,
                "ledger_cells": ledger_cells_read(
                    prediction.clauses, declared_cells
                ),
            }
        )
    hits = [s for s in scored if s["status"] == "HIT"]
    return {
        "frozen_file_sha256": hashlib.sha256(
            (TREE / "PREDICTIONS.md").read_bytes()
        ).hexdigest(),
        "design_file_sha256": hashlib.sha256(
            (TREE / "DESIGN.md").read_bytes()
        ).hexdigest(),
        "scored": scored,
        "hits": len(hits),
        "misses": len(scored) - len(hits),
        "forced_hits": sum(1 for s in hits if s["forced"]),
        "quotes_all_found": all(
            bool(s["quote_found_in_the_frozen_file"]) for s in scored
        ),
        "tally_criterion": (
            "a HIT on a FORCED prediction is a hit by construction and is not "
            "counted as content; a miss on one is an implementation defect.  A "
            "miss is recorded next to its computed value and never edited away"
        ),
    }


# ---------------------------------------------------------------------------
# The terminal sentence, and its scope
# ---------------------------------------------------------------------------

TERMINAL_SENTENCE = (
    "Within the three declared coordinates, at the pinned requirement and "
    "prices, at the retained two-mark configuration, under mu1: the admitted "
    "primitive reduced the price of the required internal separation by ZERO "
    "under the unnamed reading and by ONE under the named reading.  What it "
    "bought under the unnamed reading is two additional routes at the same "
    "price, both mediated by the sides.  It bought no price that the "
    "admission order could not buy at the same price."
)

OPEN_OBSTRUCTIONS: tuple[Json, ...] = (
    {
        "id": "(a)",
        "statement": "whether the admission order is itself a container",
        "why_open": (
            "what pays for separation in a world with no container is the "
            "ADMISSION ORDER.  This control prices that route; it does not "
            "decide what kind of thing an order is"
        ),
    },
    {
        "id": "(b)",
        "statement": (
            "the price of re-purchasing a per-mark two-valued datum, which "
            "lies outside the pinned candidate space and is therefore priced "
            "in neither world"
        ),
        "why_open": (
            "allowing it would price a route the pinned world was never "
            "charged for either, and it answers a different question: the "
            "PRICE of rebuilding the admitted primitive, not the WORTH of "
            "having it free"
        ),
    },
    {
        "id": "(c)",
        "statement": (
            "the pinned premise that a candidate's permitted renamings are "
            "closed under composition and inverse"
        ),
        "why_open": (
            "inherited as OPEN, and not treated as discharged by the renaming "
            "set having shrunk"
        ),
    },
    {
        "id": "(d)",
        "statement": (
            "whether the requirement should have been declared so as to "
            "exclude a route that satisfies it by unfolding"
        ),
        "why_open": (
            "the pinned tree retains such a route and records this as OPEN; "
            "this control inherits it, counts the route in the primary answer, "
            "and freezes the secondary answer that excludes it"
        ),
    },
)

SCOPE_LIMITS: tuple[str, ...] = (
    "G4 covers the fourteen rows the minimum ranges over and is total over "
    "what the minimum is computed FROM, but not over all 48 points per "
    "reading, so a defect in a bundle row's recorded verdict is invisible to "
    "it.",
    "The control is one rung wide and says nothing about what the admitted "
    "primitive bought at earlier rungs, nor about whether the requirement was "
    "the right one to impose.",
    "The Lean package of this tree is a MANUAL RECEIPT: no CI job builds it, "
    "so its axiom report is unchecked by any gate.  Recorded as a live "
    "residual, not closed.",
    "The conditional commit field remains in this record as frozen; required "
    "source verification and unconditional CI replay comparison now fail "
    "when its landed source is unavailable or differs.",
)


def terminal_block(decided: Json) -> Json:
    return {
        "sentence": TERMINAL_SENTENCE,
        "sentence_is_the_scoped_one": (
            "no price that the admission order could not buy at the same price"
            in TERMINAL_SENTENCE
            and "bought nothing" not in TERMINAL_SENTENCE
        ),
        "the_sentence_this_tree_may_not_write": (
            "the unscoped one, which drops the clause about the admission "
            "order.  What pays for separation in a world with no container is "
            "that order, and whether an order is itself a container is open "
            "obstruction (a)"
        ),
        "why_the_tie_holds": (
            "only because a route that satisfies the requirement without "
            "reading anything is counted -- a route the pinned tree itself "
            "retains and itself records as OPEN"
        ),
        "decided_value": decided["what_the_admitted_primitive_bought"],
    }


# ---------------------------------------------------------------------------
# decide()
# ---------------------------------------------------------------------------


def decide() -> Json:
    rows = control_rows()
    mrows = mirror_rows()
    gate_list = [
        gate_pin_bytes(),
        gate_requirement_texts(),
        gate_capability_texts(),
        gate_verdict_replay(),
        gate_forgetful_lemma(),
        gate_mirror_matches_the_pin(mrows),
    ]
    gates: Json = {str(g["gate"]): g for g in gate_list}
    passed = all(bool(g["passed"]) for g in gate_list)
    gates["all_passed"] = passed
    table = route_table(rows, mir.READING_U)
    ledger = endowment_ledger(rows, mrows)
    decided = decided_object(rows, mrows, passed)
    record: Json = {
        "authority_effect": "None",
        "tree": "side_free",
        "what_this_is": (
            "the control the pinned derivation could not run from inside "
            "itself: the same requirement, at the same prices, in a carrier "
            "with no placement, no sides, and no admitted whole with two of "
            "them"
        ),
        "admits": "nothing; this tree admits no primitive at all",
        "pinned_commit": str(json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["pinned_commit"]),
        "void": not passed,
        "gates": gates,
        "requirement": {
            "declared": REQUIREMENT,
            "second_reading": REQUIREMENT_SECOND_READING,
            "retained_marks": list(RETAINED_MARKS),
            "inherited_by": (
                "one declared textual deletion each, asserted byte for byte "
                "against the vendored bytes by G2"
            ),
            "readings_agree_premise": (
                "the pinned premise that a candidate's permitted renamings are "
                "closed under composition and inverse is INHERITED AS OPEN and "
                "is not treated as discharged"
            ),
        },
        "candidate_space": {
            "coordinates": list(ctl.COORDINATES),
            "capability_of": dict(ctl.CAPABILITY_OF),
            "inherited_values": dict(ctl.INHERITED),
            "extra_mark_values": [str(v) for v in ctl.EXTRA_MARK_VALUES],
            "pinned_extra_mark_values": list(ctl.PINNED_EXTRA_MARK_VALUES),
            "value_set_change": {
                "coordinate": "extra_mark",
                "note": (
                    "the SINGLE value-set change of the whole deletion, "
                    "flagged because it is the one place a second deletion "
                    "could hide.  Read from the pin, not asserted, and SCOPED "
                    "to the unnamed reading: there the two pinned further-mark "
                    "points carry one class key and stand as the two members "
                    "of one retained class.  Under the named reading they "
                    "carry two different class keys and are two classes, so "
                    "the one-class sentence is not a fact of both readings"
                ),
            },
            "deletion_criterion": ctl.DELETION_CRITERION,
            "exhaustive_over": ctl.SPACE_IS_EXHAUSTIVE_OVER,
            "rejected_coordinate": ctl.REJECTED_COORDINATE,
            "space_size": len(rows),
            "one_step_count": sum(1 for r in rows if r["one_step"]),
            "bundles_refused_count": sum(1 for r in rows if r["bundles"]),
        },
        "control": {
            "world": "control",
            "row_order": [str(r["name"]) for r in rows],
            "rows": list(rows),
            "summary": summarize(rows),
            "minima_by_mu1": minima(rows, "mu1"),
        },
        "mirror": {
            "status": (
                "a COUNTERMODEL-DOMAIN object of this tree: its own "
                "re-declaration of a side-typed carrier, never claimed to be "
                "the pinned carrier, pinned against the pinned vector by G6, "
                "and a divergence VOIDS the run"
            ),
            **{
                reading: {
                    "row_order": [str(r["name"]) for r in table_rows],
                    "rows": list(table_rows),
                    "summary": summarize(table_rows),
                    "space_size": len(table_rows),
                    "bundles_refused_count": sum(
                        1 for r in table_rows if r["bundles"]
                    ),
                    "minima_by_mu1": minima(table_rows, "mu1"),
                }
                for reading, table_rows in mrows.items()
            },
        },
        "decided": decided,
        "withdrawal_port": withdrawal_port(rows),
        "route_table": table,
        "route_disagreements": [
            str(r["coordinate"]) for r in table if not r["agrees"]
        ],
        "unmatched_pinned_routes": list(UNMATCHED_PINNED_ROUTES),
        "endowment_ledger": {
            **ledger,
            # Keyed by row name and carrying every OTHER field the row
            # carries.  Written this way rather than as a list of picked
            # columns because the picked version silently dropped
            # ``declared_columns``, so a consumer reading a cell through this
            # projection could not see that the cell was a declaration.  A
            # projection that enumerates what it keeps loses the next field
            # too; this one cannot.
            "by_row": {
                str(entry["row"]): {
                    key: value for key, value in entry.items() if key != "row"
                }
                for entry in as_list(ledger["rows"])
                if isinstance(entry, dict)
            },
        },
        "censuses": census_block(),
        "smuggle_tripwire": {
            **mir.forgetful_lemma(True),
            "what_was_injected": (
                "the side re-admitted into the side-free key as a per-mark "
                "two-valued attribute -- exactly the substitute the lemma "
                "exists to catch.  This is a declared PARAMETER of the lemma "
                "function exercised deliberately, not an edit to any source "
                "file, so no receipt is written under a live source injection"
            ),
        },
        "observation_grammar": observation_grammar_block(rows),
        "identity_policies": identity_policies(),
        "caller_histories": caller_histories(),
        "deletion_register": deletion_register_block(),
        "second_measures": mu2_block(rows, mrows),
        "key_choice_invariance": key_choice_block(rows),
        "secondary": secondary_block(rows, mrows, passed),
        "open_obstructions": list(OPEN_OBSTRUCTIONS),
        "scope_limits": list(SCOPE_LIMITS),
        "terminal": terminal_block(decided),
    }
    record["predictions"] = score_predictions(record)
    return record


def render(record: Json) -> bytes:
    """Deterministic bytes: sorted keys, LF only, no timestamp, no environment."""
    text = json.dumps(record, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    return text.encode("utf-8")
