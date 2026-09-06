"""The price list: the pinned world beside the side-free control.

Classification: METATHEORY APPARATUS throughout.  Nothing here is admitted,
no regime changes except by ``replay`` of an explicit history, and every row
value is READ from a pinned receipt or COMPUTED from a carrier.  No boundary
number is typed into this file.

What this module is for.  The pinned derivation's own claims about which of
its results need the admitted primitive live in a hand-written dictionary in
its four challenge modules, which its own ledger files as a limitation that
nothing computes.  A test there pins each dictionary against its own module
constant, so its BYTES are held while nothing adjudicates its claims.  An
earlier version of this sentence said the dictionary lived in the runner
modules and was read by no test; both halves were wrong and are withdrawn.
This module reads that dictionary, and it
prices, row by row, what the two worlds can say at each of the pinned rungs
and what each says it costs.

Three disciplines hold here and are enforced by the gates below.

* **Every value cites its source.**  A pinned value carries the challenge
  index and the JSON path it was read from; a control value carries either
  the receipt path or the name of the computation that produced it.
* **Every pinned value is declared twice.**  ``pinned/BOUNDARY_PIN.json``
  declares the value at its path, and gate ``C1`` requires the vendored bytes
  to agree.  A hand edit of either side fails BY NAME.  The declaration is
  also required to be TOTAL in both directions: an undeclared value that a
  row uses fails, and a declared value that no row uses fails.
* **Absence is never equality.**  Where a notion has no statement in one
  world the row says ABSENT and says why.  An absent row is in neither
  bucket: it is not evidence that the primitive bought something, and it is
  not evidence that it bought nothing.

The record is deterministic and carries no environment value.  In particular
it does NOT record whether the pinned commit was reachable in the clone that
produced it: the vendored bytes and the bytes at that commit are held to one
sha256, so the rows are the same either way, and the reachability report is
printed by the runner instead of being written into the receipt.  That is a
deliberate difference from the sibling record, which does carry it; see the
open item this module reports.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from dataclasses import dataclass
from typing import Callable, Mapping, Sequence, Union

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE / "code"))

from sidefree import candidates as ctl  # noqa: E402
from sidefree import mirror as mir  # noqa: E402
from sidefree.model import (  # noqa: E402
    JUDGMENT_FORMS,
    STATE_CHANGING_EVENT_KINDS,
    AdmitMark,
    Regime,
    Supply,
    canonical_under,
    event_follows,
    genesis,
    marks_separable_under,
    observations,
    replay,
    serialize,
    step,
)
from sidefree.requirement import RETAINED_MARKS  # noqa: E402

Json = dict[str, object]

MANIFEST_PATH = HERE / "SOURCE_MANIFEST.json"
PIN_META_PATH = HERE / "pinned" / "BOUNDARY_PIN.json"
SIDE_FREE_RECEIPT = HERE / "receipts" / "side_free.json"
COMPARISON_RECEIPT = HERE / "receipts" / "comparison.json"
COMPARISON_DOC = HERE / "COMPARISON.md"

CHALLENGES: tuple[int, ...] = (0, 1, 2, 3)
UNNAMED = "U"
NAMED = "O"

BOUGHT_NOTHING = "BOUGHT_NOTHING"
BOUGHT_SOMETHING = "BOUGHT_SOMETHING"
ABSENT = "ABSENT"

# A pinned dependence sentence is classified by its own opening words.  The
# three classes are exhaustive over the pinned population or the gate fails.
DEPENDENCE_INDEPENDENT = "INDEPENDENT"
DEPENDENCE_DEPENDENT = "DEPENDENT"
DEPENDENCE_MIXED = "MIXED"
DEPENDENCE_UNCLASSIFIED = "UNCLASSIFIED"


# ---------------------------------------------------------------------------
# Reading the pinned bytes
# ---------------------------------------------------------------------------


def manifest() -> Json:
    data: object = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError("SOURCE_MANIFEST.json must be an object")
    return data


def pin_meta() -> Json:
    data: object = json.loads(PIN_META_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError("BOUNDARY_PIN.json must be an object")
    return data


def as_dict(value: object) -> Json:
    if not isinstance(value, dict):
        raise TypeError(f"not an object: {value!r}")
    return value


def as_list(value: object) -> list[object]:
    if not isinstance(value, list):
        raise TypeError(f"not a list: {value!r}")
    return value


def dig(root: object, path: str) -> object:
    """Walk a dotted JSON path.  A list step takes an integer index."""
    current = root
    for part in path.split("."):
        if isinstance(current, list):
            current = current[int(part)]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise KeyError(f"{path}: cannot descend into {type(current).__name__}")
    return current


def vendored_receipts() -> list[Json]:
    """The four declared vendored copies, by challenge index."""
    block = as_list(dig(manifest(), "vendored_receipts"))
    rows = [as_dict(entry) for entry in block]
    return sorted(rows, key=lambda row: int(str(row["challenge"])))


def git_bytes(spec: str) -> bytes | None:
    proc = subprocess.run(["git", "show", spec], cwd=REPO, capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


@dataclass(frozen=True)
class Load:
    """One challenge's pinned bytes, and how they were obtained."""

    challenge: int
    source: str
    reason: str
    problems: tuple[str, ...]
    data: Json


def load_pinned(row: Json, commit: str) -> Load:
    """Read one pinned receipt at the pinned commit, held by its declared hash.

    The blob at the commit and the vendored copy are held to ONE sha256 that
    the manifest declares, so whichever is parsed the values are the same.
    The vendored copy is checked unconditionally, so this gate's problem list
    does not depend on whether the commit is reachable; a blob at the commit
    whose digest differs is a problem and never a silent fallback.
    """
    challenge = int(str(row["challenge"]))
    want = str(row["sha256"])
    source_path = str(row["source_path"])
    vendored = (HERE / str(row["local_path"])).read_bytes()
    problems: list[str] = []
    got = hashlib.sha256(vendored).hexdigest()
    if got != want:
        problems.append(
            f"challenge {challenge}: {row['local_path']} has sha256 {got}, "
            f"the manifest declares {want}"
        )
    if b"\r" in vendored:
        problems.append(f"challenge {challenge}: {row['local_path']} contains CR bytes")
    if len(vendored) != int(str(row["byte_count"])):
        problems.append(
            f"challenge {challenge}: {row['local_path']} is {len(vendored)} bytes, "
            f"the manifest declares {row['byte_count']}"
        )
    raw = git_bytes(f"{commit}:{source_path}")
    if raw is None:
        source = "the vendored copy"
        reason = (
            f"the pinned commit {commit} is unreachable in this clone; the "
            f"vendored bytes are held by their declared sha256, which needs no git"
        )
        chosen = vendored
    elif hashlib.sha256(raw).hexdigest() == want:
        source = "the pinned commit"
        reason = f"read at {commit} and equal to the declared sha256"
        chosen = raw
    else:
        source = "the vendored copy"
        reason = "the blob at the pinned commit does not match the declared digest"
        problems.append(
            f"challenge {challenge}: the blob at {commit} for the path the "
            f"manifest declares has sha256 {hashlib.sha256(raw).hexdigest()}, "
            f"the manifest declares {want}"
        )
        chosen = vendored
    return Load(
        challenge,
        source,
        reason,
        tuple(problems),
        as_dict(json.loads(chosen.decode("utf-8"))),
    )


def side_free_record() -> Json:
    return as_dict(json.loads(SIDE_FREE_RECEIPT.read_text(encoding="utf-8")))


# ---------------------------------------------------------------------------
# Where a value comes from
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Pin:
    """A value of the pinned world, at a challenge and a JSON path."""

    challenge: int
    path: str


@dataclass(frozen=True)
class Receipt:
    """A value of this tree's own committed record, at a JSON path."""

    path: str


@dataclass(frozen=True)
class Computed:
    """A value computed here from a carrier, named by its computation."""

    key: str


@dataclass(frozen=True)
class Declared:
    """A control value this module DECLARES, because nothing computes it.

    Kept apart from ``Computed`` so that a typed-in string cannot be read as
    a measurement.  A row with a declared column on both sides is true by
    unfolding two declarations, is flagged DEFINITION-level, and the verdict
    reports its tallies with and without such rows.
    """

    key: str


# The declared control values, and why each is declared rather than computed.
# ``paid_by`` has no genesis declaration in this carrier and is not a value the
# enumeration produces: what pays here is the run, and saying so is a statement
# about this tree's own procedure rather than a reading off a carrier.  The
# pinned world flags its own side of the same field as declared and not
# computed, so the row compares two declarations and is content in neither.
DECLARED_CONTROL_VALUES: dict[str, object] = {"control_paid_by": "the run"}
WHY_DECLARED: dict[str, str] = {
    "control_paid_by": (
        "there is no genesis declaration of a payer in this carrier and the "
        "enumeration produces none, so the payer is stated here rather than "
        "measured; the pinned world flags its own side of this field as "
        "declared and not computed too"
    )
}


@dataclass(frozen=True)
class Count:
    """The length of a pinned list, so a list and a count are never compared."""

    inner: Pin


@dataclass(frozen=True)
class Collapsed:
    """A pinned list of point names under the declared collapse map.

    The map takes both pinned further-mark point NAMES to the one control
    point, so the cross-world join is by equality of names.  Its one-class
    justification is a fact of the UNNAMED reading alone: there the two
    points carry one class key and stand as the two members of one retained
    class.  Under the NAMED reading they carry two different class keys and
    are two classes, so a named column resolved under this map shows one name
    fewer than that reading has points, and the rows that use it say so.  The
    map is declared in ``pinned/BOUNDARY_PIN.json`` and applied here, never
    by eye.
    """

    inner: Pin


@dataclass(frozen=True)
class NoStatement:
    """The notion has no statement in this world.  Never an equality."""

    reason: str


Source = Union[Pin, Receipt, Computed, Declared, Count, Collapsed, NoStatement]


@dataclass(frozen=True)
class Cell:
    value: object
    source: str
    absent: bool
    absent_reason: str | None


class Resolver:
    """Turns a source into a cell, and records every pinned path it touched."""

    def __init__(
        self,
        pinned: Mapping[int, Json],
        record: Json,
        computed: Mapping[str, object],
        collapse: Mapping[str, object],
    ) -> None:
        self.pinned = pinned
        self.record = record
        self.computed = computed
        self.collapse = collapse
        self.used: list[tuple[int, str]] = []

    def resolve(self, source: Source) -> Cell:
        if isinstance(source, Pin):
            self.used.append((source.challenge, source.path))
            value = dig(self.pinned[source.challenge], source.path)
            return Cell(value, f"pinned challenge {source.challenge}: {source.path}", False, None)
        if isinstance(source, Receipt):
            value = dig(self.record, source.path)
            return Cell(value, f"receipts/side_free.json: {source.path}", False, None)
        if isinstance(source, Computed):
            return Cell(
                self.computed[source.key],
                f"computed here: {source.key}",
                False,
                None,
            )
        if isinstance(source, Declared):
            return Cell(
                DECLARED_CONTROL_VALUES[source.key],
                f"declared here, not computed: {source.key}",
                False,
                None,
            )
        if isinstance(source, Count):
            inner = self.resolve(source.inner)
            return Cell(
                len(as_list(inner.value)), f"{inner.source} (length)", False, None
            )
        if isinstance(source, Collapsed):
            inner = self.resolve(source.inner)
            names = [str(name) for name in as_list(inner.value)]
            collapsed = sorted({str(self.collapse.get(name, name)) for name in names})
            return Cell(
                collapsed, f"{inner.source} (under the declared collapse map)", False, None
            )
        return Cell(None, "no statement in this world", True, source.reason)


# ---------------------------------------------------------------------------
# Differences
# ---------------------------------------------------------------------------


def comparable(value: object) -> str:
    """A JSON-comparable rendering, so nested keys can be set-differenced."""
    return json.dumps(value, sort_keys=True)


def difference(boundary: Cell, control: Cell) -> Json:
    """What separates one boundary cell from the control cell.  Computed."""
    if boundary.absent or control.absent:
        which = "the control" if control.absent else "the pinned world"
        reason = control.absent_reason if control.absent else boundary.absent_reason
        return {
            "kind": "absent",
            "same": False,
            "absent_in": which,
            "reason": reason,
        }
    left, right = boundary.value, control.value
    if isinstance(left, bool) and isinstance(right, bool):
        return {"kind": "bool", "same": left == right}
    if (
        isinstance(left, int)
        and isinstance(right, int)
        and not isinstance(left, bool)
        and not isinstance(right, bool)
    ):
        return {
            "kind": "count",
            "same": left == right,
            "control_minus_boundary": right - left,
        }
    if isinstance(left, list) and isinstance(right, list):
        seen_left = [comparable(item) for item in left]
        seen_right = [comparable(item) for item in right]
        return {
            "kind": "set",
            "same": left == right,
            "only_in_the_pinned_world": [
                json.loads(item) for item in seen_left if item not in seen_right
            ],
            "only_in_the_control": [
                json.loads(item) for item in seen_right if item not in seen_left
            ],
        }
    return {"kind": "value", "same": left == right}


# ---------------------------------------------------------------------------
# The control's own values, computed from its carrier
# ---------------------------------------------------------------------------


def retained_regime() -> Regime:
    """The two-mark configuration, replayed from genesis."""
    return replay(ctl.caller_history(ctl.caller_wholes()), genesis())


def one_mark_regime() -> Regime:
    """One admitted mark, replayed from genesis by the label-keyed admission."""
    return replay([Supply(ctl.SUPPLIED_TOKEN), AdmitMark(ctl.SUPPLIED_TOKEN)], genesis())


def available_admissions(r: Regime, supplied: Sequence[str]) -> list[str]:
    """The label-keyed admissions the grammar can form that admit a mark.

    The pinned space is each supplied, not yet admitted token ON EACH SIDE.
    The side argument is gone here, so the same enumeration over the same
    tokens yields one event per token and no more.
    """
    return sorted(token for token in supplied if token not in r.marks)


def control_computed() -> Json:
    """Every control value the rows need that its receipt does not carry."""
    start = genesis()
    one = one_mark_regime()
    two = retained_regime()
    supplied = [ctl.SUPPLIED_TOKEN]
    admissions = available_admissions(start, supplied)
    admitted_regimes = [
        replay([Supply(token), AdmitMark(token)], start) for token in admissions
    ]
    classes = {
        comparable(list(canonical_under(r, True, False))) for r in admitted_regimes
    }
    return {
        "genesis_marks": start.n_marks(),
        "genesis_judgments": len(observations(start)),
        "genesis_key": list(serialize(start)),
        "genesis_supply_is_inert": step(start, Supply(ctl.SUPPLIED_TOKEN)) == start,
        "event_follows_relation_empty": not any(
            event_follows(r, e)
            for r in (start, one, two)
            for e in (Supply(ctl.SUPPLIED_TOKEN), AdmitMark(ctl.SUPPLIED_TOKEN))
        ),
        "declared_judgment_forms": list(JUDGMENT_FORMS),
        "state_changing_event_kinds": sorted(STATE_CHANGING_EVENT_KINDS),
        "one_mark_admissions_available": len(admissions),
        "one_mark_admission_classes": len(classes),
        "one_mark_marks": one.n_marks(),
        "one_mark_judgments": len(observations(one)),
        "one_mark_key": list(serialize(one)),
        "supply_alone_equals_genesis": replay([Supply(ctl.SUPPLIED_TOKEN)], start)
        == start,
        "two_marks_marks": two.n_marks(),
        "two_marks_judgments": len(observations(two)),
        "two_marks_key": list(serialize(two)),
        "two_marks_labels": list(two.marks),
        "policies_admitting_both_wholes": policy_probe()["admitting_both"],
        "the_two_caller_orders_give_equal_regimes": order_probe()["equal"],
        "the_two_caller_orders_are_isomorphic": order_probe()["isomorphic"],
        "caller_order_classes": order_probe()["classes"],
    }


def order_probe() -> Json:
    """The two caller orders, replayed, and what separates them.  Computed."""
    wholes = ctl.caller_wholes()
    forward = replay(ctl.caller_history(wholes), genesis())
    reversed_regime = replay(ctl.caller_history(list(reversed(wholes))), genesis())
    keys = {
        comparable(list(canonical_under(r, True, False)))
        for r in (forward, reversed_regime)
    }
    return {
        "equal": forward == reversed_regime,
        "isomorphic": canonical_under(forward, True, False)
        == canonical_under(reversed_regime, True, False),
        "classes": len(keys),
    }


def policy_probe() -> Json:
    """The two declared identity policies, replayed.  Which admits both?"""
    wholes = ctl.caller_wholes()
    regimes = {
        "occurrence": replay(ctl.caller_history(wholes), genesis()),
        "shared": replay(ctl.shared_policy_history(wholes), genesis()),
    }
    return {
        "marks_by_policy": {name: r.n_marks() for name, r in regimes.items()},
        "admitting_both": sum(1 for r in regimes.values() if r.n_marks() == 2),
    }


# ---------------------------------------------------------------------------
# Which minima read a side: two criteria, both computed
# ---------------------------------------------------------------------------


def names_a_side(sentence: str) -> bool:
    """The mechanical criterion the deletion itself used, run the other way."""
    return not ctl.transfers(sentence)


def mirror_reads_the_placement(reading: str, aug: mir.Augmentation) -> Json:
    """Does the candidate's verdict move when only the placement moves?

    Over the candidate's own route-census domain, group the cells by their
    labels and vary the placement inside each group.  A verdict that is not
    constant inside some group reads the placement; one that is constant in
    every group does not.  Nothing here is judged.
    """
    refl, perms, keep = mir.flags(reading, aug)
    i, j = RETAINED_MARKS
    groups: dict[str, list[bool]] = {}
    for regime in mir.route_census_regimes(reading, aug):
        key = comparable(list(regime.marks))
        verdict = mir.marks_separable_under(regime, i, j, refl, perms, keep)
        groups.setdefault(key, []).append(verdict)
    varying = sorted(key for key, verdicts in groups.items() if len(set(verdicts)) > 1)
    return {
        "cells": sum(len(v) for v in groups.values()),
        "label_groups": len(groups),
        "groups_whose_verdict_moves_with_the_placement": len(varying),
        "reads_the_placement": bool(varying),
    }


def control_reads_the_placement(aug: ctl.Augmentation) -> Json:
    """The same question in a world with no placement: it cannot be asked."""
    perms, keep = ctl.flags(aug)
    i, j = RETAINED_MARKS
    verdicts = [
        marks_separable_under(r, i, j, perms, keep)
        for r in ctl.route_census_regimes(aug)
    ]
    return {
        "cells": len(verdicts),
        "label_groups": len(verdicts),
        "groups_whose_verdict_moves_with_the_placement": 0,
        "reads_the_placement": False,
        "why": "there is no placement here, so no group can vary with one",
    }


def minima_reading_a_side(pinned: Mapping[int, Json], record: Json) -> Json:
    """Every minimum of both worlds, under both criteria."""
    capability_of = as_dict(dig(pinned[3], "candidate_space.capability_of"))
    mirror_augs = {mir.point_name(aug): aug for aug in mir.candidate_space()}
    control_augs = {ctl.point_name(aug): aug for aug in ctl.candidate_space()}
    rows: list[Json] = []
    for reading in (UNNAMED, NAMED):
        for entry in as_list(dig(pinned[3], f"readings.{reading}.minima_by_mu1.points")):
            point = str(entry)
            aug = mirror_augs[point]
            coordinates = mir.changed_coordinates(aug)
            rows.append(
                {
                    "whose_minimum": "the pinned world",
                    "reading": reading,
                    "point": point,
                    "coordinates_moved": coordinates,
                    "names_a_side_in_its_capability_sentence": any(
                        names_a_side(str(capability_of[coord])) for coord in coordinates
                    ),
                    "placement": mirror_reads_the_placement(reading, aug),
                }
            )
    for entry in as_list(dig(record, "decided.side_free_minimum_members")):
        point = str(entry)
        control_aug = control_augs[point]
        coordinates = ctl.changed_coordinates(control_aug)
        rows.append(
            {
                "whose_minimum": "the control",
                "reading": None,
                "point": point,
                "coordinates_moved": coordinates,
                "names_a_side_in_its_capability_sentence": any(
                    names_a_side(ctl.CAPABILITY_OF[coord]) for coord in coordinates
                ),
                "placement": control_reads_the_placement(control_aug),
            }
        )
    return {
        "criterion_by_name": ctl.DELETION_CRITERION,
        "criterion_by_behaviour": (
            "a candidate READS the placement when its separation verdict is not "
            "constant across the placements of one label configuration in its own "
            "route-census domain, and does not read it when the verdict is "
            "constant in every such group"
        ),
        "where_each_criterion_is_evaluated": (
            "the first column says whose minimum a row is and NOT where its "
            "verdicts were taken.  The pinned rows' point names and capability "
            "sentences are read from the pinned receipts, so the by-name "
            "verdict is computed over pinned text.  The by-behaviour verdict "
            "is computed for every row on a carrier of THIS TREE -- the mirror "
            "for the pinned rows, the control for its own -- over that "
            "carrier's own route-census domain.  No pinned path carries a "
            "placement verdict and the pinned world's kernel is not run here, "
            "so no cell of the last column is a reading off the pinned world"
        ),
        "rows": rows,
        "the_two_criteria_disagree_on": sorted(
            {
                str(row["point"])
                for row in rows
                if bool(row["names_a_side_in_its_capability_sentence"])
                != bool(as_dict(row["placement"])["reads_the_placement"])
            }
        ),
    }


# ---------------------------------------------------------------------------
# The pinned world's own dependence dictionary, now read
# ---------------------------------------------------------------------------


def classify_dependence(sentence: str) -> str:
    lowered = sentence.strip().lower()
    if lowered.startswith("does not depend"):
        return DEPENDENCE_MIXED if "requir" in lowered else DEPENDENCE_INDEPENDENT
    if lowered.startswith("requir"):
        return DEPENDENCE_DEPENDENT
    return DEPENDENCE_UNCLASSIFIED


def dependence_block(pinned: Mapping[int, Json], record: Json) -> Json:
    """Enumerate the pinned dependence claims and classify them mechanically.

    The pinned tree's own ledger files this dictionary as a limitation
    computed by nothing; a test there holds its bytes against its own module
    constant, and nothing adjudicates it.  It is read here.  What is
    adjudicated is not each sentence -- these are prose -- but the one entry
    the mechanical selector below picks out, against computed evidence.
    """
    entries: list[Json] = []
    for challenge in CHALLENGES:
        claims = as_dict(dig(pinned[challenge], "boundary_dependence"))
        for subject, sentence in sorted(claims.items()):
            entries.append(
                {
                    "challenge": challenge,
                    "subject": subject,
                    "claim": str(sentence),
                    "class": classify_dependence(str(sentence)),
                    "subject_claims_every_result_of_its_rung": "every"
                    in subject.lower().split(),
                }
            )
    universal = [
        entry
        for entry in entries
        if entry["class"] == DEPENDENCE_DEPENDENT
        and bool(entry["subject_claims_every_result_of_its_rung"])
    ]
    port = as_dict(dig(record, "withdrawal_port"))
    counts = {
        name: sum(1 for entry in entries if entry["class"] == name)
        for name in (
            DEPENDENCE_DEPENDENT,
            DEPENDENCE_INDEPENDENT,
            DEPENDENCE_MIXED,
            DEPENDENCE_UNCLASSIFIED,
        )
    }
    return {
        "what_it_is": (
            "the pinned world's own claims about which of its results need the "
            "admitted primitive, hand written in its four challenge modules and "
            "filed by its own ledger as computed by nothing.  A test there pins "
            "each dictionary against its own module constant, so its bytes are "
            "held while nothing adjudicates its claims"
        ),
        "entries": entries,
        "entry_count": len(entries),
        "counts_by_class": counts,
        "classification_is_mechanical": (
            "by the sentence's own opening words: 'does not depend' is "
            "INDEPENDENT, or MIXED when the same sentence also says something "
            "requires the primitive; 'require' is DEPENDENT"
        ),
        "classification_is_total": counts[DEPENDENCE_UNCLASSIFIED] == 0,
        "selector": (
            "the entries that are DEPENDENT and whose subject carries the whole "
            "word 'every', so the claim is universal over its rung"
        ),
        "universal_entries": universal,
        "adjudication": {
            "selected": [str(entry["subject"]) for entry in universal],
            "evidence": {
                "coordinate": port["coordinate"],
                "it_is_one_of_the_pinned_minima": str(port["coordinate"])
                in [
                    str(name)
                    for name in as_list(
                        dig(pinned[3], f"readings.{UNNAMED}.minima_by_mu1.points")
                    )
                ],
                "pinned_cost": port["pinned_mu1"],
                "control_cost": port["control_mu1"],
                "pinned_satisfies": port["pinned_satisfies"],
                "control_satisfies": port["control_satisfies"],
                "capability_sentence_is_byte_identical": port[
                    "capability_text_identical"
                ],
                "same_cost": port["same_cost"],
            },
            "verdict": (
                "CONTRADICTED within the declared scope"
                if bool(port["same_cost"]) and bool(port["control_satisfies"])
                else "NOT CONTRADICTED"
            ),
            "what_is_declared_and_what_is_computed": (
                "the selector is declared; the evidence under it is computed, and "
                "the contradiction is of one universal clause at one rung and of "
                "nothing else in the dictionary"
            ),
        },
    }


# ---------------------------------------------------------------------------
# The rows
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Price:
    """What each world states this row costs, if either states anything."""

    unnamed: Source
    named: Source
    control: Source


@dataclass(frozen=True)
class Spec:
    id: str
    stage: str
    item: str
    unnamed: Source
    named: Source
    control: Source
    price: Price | None = None
    note: str | None = None


GENESIS = "genesis"
ONE_MARK = "one admitted mark"
TWO_MARKS = "two retained marks"
REQUIREMENT = "the imposed requirement"
PRICES = "the prices each world states"

# The rung order, declared rather than sorted: the alphabet would put the
# prices between the first mark and the second, which is not the order the
# pinned world runs them in.
STAGES: tuple[str, ...] = (GENESIS, ONE_MARK, TWO_MARKS, REQUIREMENT, PRICES)

# The declared taxonomy of items.  It is about the KIND of thing an item is,
# not about how the row came out, and it is fixed here so that a difference in
# a world's own bookkeeping is not read as a capability the primitive bought.
# A row's bucket is decided by the computation regardless; the kind only says
# what sort of thing is being compared.
OBSERVABLE = "what holds"
STRUCTURE = "declared structure"
DISCIPLINE = "event discipline"
VERDICT = "verdict"
PRICE = "price"
KINDS: tuple[str, ...] = (OBSERVABLE, STRUCTURE, DISCIPLINE, VERDICT, PRICE)

KIND_OF: dict[str, str] = {
    "R01": OBSERVABLE,
    "R02": STRUCTURE,
    "R03": OBSERVABLE,
    "R04": STRUCTURE,
    "R05": STRUCTURE,
    "R06": DISCIPLINE,
    "R07": DISCIPLINE,
    "R08": STRUCTURE,
    "R09": STRUCTURE,
    "R10": OBSERVABLE,
    "R11": OBSERVABLE,
    "R12": STRUCTURE,
    "R13": DISCIPLINE,
    "R14": DISCIPLINE,
    "R15": OBSERVABLE,
    "R16": OBSERVABLE,
    "R17": OBSERVABLE,
    "R18": STRUCTURE,
    "R19": VERDICT,
    "R20": VERDICT,
    "R21": VERDICT,
    "R22": OBSERVABLE,
    "R23": OBSERVABLE,
    "R24": STRUCTURE,
    "R25": STRUCTURE,
    "R26": STRUCTURE,
    "R27": STRUCTURE,
    "R28": STRUCTURE,
    "R29": DISCIPLINE,
    "R30": VERDICT,
    "R31": PRICE,
    "R32": VERDICT,
    "R33": VERDICT,
    "R34": VERDICT,
    "R35": STRUCTURE,
    "R36": STRUCTURE,
    "R37": STRUCTURE,
    "R38": VERDICT,
    "R39": STRUCTURE,
    "R40": PRICE,
    "R41": PRICE,
    "R42": PRICE,
    "R43": PRICE,
    "R44": PRICE,
    "R45": PRICE,
    "R46": PRICE,
    "R47": STRUCTURE,
}

NO_SIDE = "the notion names a side, and a world with no sides cannot state it"


def specs() -> list[Spec]:
    """The comparable items, declared once, resolved by the resolver."""
    return [
        Spec(
            "R01",
            GENESIS,
            "marks admitted at genesis",
            Pin(0, "readings.U.marks"),
            Pin(0, "readings.O.marks"),
            Computed("genesis_marks"),
        ),
        Spec(
            "R02",
            GENESIS,
            "the declared observation vocabulary",
            Pin(0, "observation_vocabulary"),
            Pin(0, "observation_vocabulary"),
            Computed("declared_judgment_forms"),
        ),
        Spec(
            "R03",
            GENESIS,
            "judgments holding at genesis",
            Pin(1, "readings.U.genesis_holding_judgments"),
            Pin(1, "readings.O.genesis_holding_judgments"),
            Computed("genesis_judgments"),
            price=Price(
                Receipt("endowment_ledger.by_row.coordinates_the_genesis_declaration_fixes.unnamed"),
                Receipt("endowment_ledger.by_row.coordinates_the_genesis_declaration_fixes.named"),
                Receipt("endowment_ledger.by_row.coordinates_the_genesis_declaration_fixes.control"),
            ),
            note=(
                "the named reading's two judgments hold before any mark is "
                "admitted, and the control cannot hold them at any price: a "
                "container exists before its contents, an admission order does not"
            ),
        ),
        Spec(
            "R04",
            GENESIS,
            "the serialization key at genesis",
            Pin(0, "readings.U.canonical_key"),
            Pin(0, "readings.O.canonical_key"),
            Computed("genesis_key"),
        ),
        Spec(
            "R05",
            GENESIS,
            "the two sides are collapsed at genesis",
            Pin(0, "readings.U.sides_collapsed"),
            Pin(0, "readings.O.sides_collapsed"),
            NoStatement(NO_SIDE),
        ),
        Spec(
            "R06",
            GENESIS,
            "an external presentation leaves admitted state unchanged",
            Pin(0, "readings.U.supply_leaves_state_unchanged"),
            Pin(0, "readings.O.supply_leaves_state_unchanged"),
            Computed("genesis_supply_is_inert"),
        ),
        Spec(
            "R07",
            GENESIS,
            "no event is entailed by admitted state",
            Pin(0, "readings.U.event_follows_relation_empty"),
            Pin(0, "readings.O.event_follows_relation_empty"),
            Computed("event_follows_relation_empty"),
        ),
        Spec(
            "R08",
            ONE_MARK,
            "admissions available from the one supplied token",
            Pin(1, "readings.U.candidate_space.count"),
            Pin(1, "readings.O.candidate_space.count"),
            Computed("one_mark_admissions_available"),
        ),
        Spec(
            "R09",
            ONE_MARK,
            "isomorphism classes of those admissions",
            Pin(1, "readings.U.candidate_space.classes_under_isomorphism"),
            Pin(1, "readings.O.candidate_space.classes_under_isomorphism"),
            Computed("one_mark_admission_classes"),
        ),
        Spec(
            "R10",
            ONE_MARK,
            "marks after one admission",
            Pin(1, "readings.U.candidates.0.marks"),
            Pin(1, "readings.O.candidates.0.marks"),
            Computed("one_mark_marks"),
        ),
        Spec(
            "R11",
            ONE_MARK,
            "judgments holding after one admission",
            Pin(1, "readings.U.candidates.0.holding_judgments"),
            Pin(1, "readings.O.candidates.0.holding_judgments"),
            Computed("one_mark_judgments"),
        ),
        Spec(
            "R12",
            ONE_MARK,
            "the serialization key after one admission",
            Pin(1, "readings.U.candidates.0.canonical_key"),
            Pin(1, "readings.O.candidates.0.canonical_key"),
            Computed("one_mark_key"),
        ),
        Spec(
            "R13",
            ONE_MARK,
            "the state after the supply alone equals genesis",
            Pin(1, "readings.U.current_state.regime_equals_genesis"),
            Pin(1, "readings.O.current_state.regime_equals_genesis"),
            Computed("supply_alone_equals_genesis"),
        ),
        Spec(
            "R14",
            ONE_MARK,
            "an admission that would move an admitted mark is refused",
            Pin(1, "readings.U.candidates.0.retention.moving_admission_refused"),
            Pin(1, "readings.O.candidates.0.retention.moving_admission_refused"),
            NoStatement(
                "the refusal is REMOVED, not absorbed: with no sides there is "
                "nowhere to move a mark to, so the refusal has no side-free "
                "statement at all"
            ),
        ),
        Spec(
            "R15",
            TWO_MARKS,
            "marks retained",
            Pin(2, "readings.U.retained.marks"),
            Pin(2, "readings.O.retained.marks"),
            Computed("two_marks_marks"),
        ),
        Spec(
            "R16",
            TWO_MARKS,
            "judgments holding at the retained regime",
            Pin(2, "readings.U.retained.holding_judgments_after"),
            Pin(2, "readings.O.retained.holding_judgments_after"),
            Computed("two_marks_judgments"),
        ),
        Spec(
            "R17",
            TWO_MARKS,
            "presentation labels at the retained regime",
            Pin(2, "readings.U.retained.labels"),
            Pin(2, "readings.O.retained.labels"),
            Computed("two_marks_labels"),
        ),
        Spec(
            "R18",
            TWO_MARKS,
            "state-changing event kinds",
            Pin(2, "state_changing_event_kinds"),
            Pin(2, "state_changing_event_kinds"),
            Computed("state_changing_event_kinds"),
        ),
        Spec(
            "R19",
            TWO_MARKS,
            "automorphisms of the retained regime",
            Pin(2, "readings.U.automorphisms.count"),
            Pin(2, "readings.O.automorphisms.count"),
            Receipt("control.summary.base.automorphism_count"),
        ),
        Spec(
            "R20",
            TWO_MARKS,
            "the two retained marks are internally separable at base",
            Pin(2, "readings.U.automorphisms.marks_internally_separable"),
            Pin(2, "readings.O.automorphisms.marks_internally_separable"),
            Receipt("control.summary.base.satisfies"),
        ),
        Spec(
            "R21",
            TWO_MARKS,
            "invariant separating mark properties at base",
            Pin(3, "readings.U.base.invariant_separating_mark_properties"),
            Pin(3, "readings.O.base.invariant_separating_mark_properties"),
            Receipt("control.rows.0.invariant_separating_mark_properties"),
        ),
        Spec(
            "R22",
            TWO_MARKS,
            "the admission order is internally available",
            Pin(2, "readings.U.order.order_internally_available"),
            Pin(2, "readings.O.order.order_internally_available"),
            Receipt(
                "control.summary.base.collateral_facts.order_internally_available"
            ),
            note=(
                "false everywhere, and for the same reason in each world: the two "
                "supplies carry one token, so reversing them is not a change to "
                "notice.  The order still EXISTS side-free -- it is the mark's "
                "internal identity, and it is what the result turns on"
            ),
        ),
        Spec(
            "R23",
            TWO_MARKS,
            "the presentation label is internally available",
            Pin(2, "readings.U.label.label_internally_available"),
            Pin(2, "readings.O.label.label_internally_available"),
            Receipt(
                "control.summary.base.collateral_facts.label_internally_available"
            ),
        ),
        Spec(
            "R24",
            TWO_MARKS,
            "the serialization key at the retained regime",
            Pin(2, "readings.U.retained.canonical_key"),
            Pin(2, "readings.O.retained.canonical_key"),
            Computed("two_marks_key"),
        ),
        Spec(
            "R25",
            TWO_MARKS,
            "the caller's two orders give equal regimes",
            Pin(2, "readings.U.convention.regimes_equal"),
            Pin(2, "readings.O.convention.regimes_equal"),
            Computed("the_two_caller_orders_give_equal_regimes"),
        ),
        Spec(
            "R26",
            TWO_MARKS,
            "the caller's two orders are isomorphic",
            Pin(2, "readings.U.convention.isomorphic_under_reading"),
            Pin(2, "readings.O.convention.isomorphic_under_reading"),
            Computed("the_two_caller_orders_are_isomorphic"),
        ),
        Spec(
            "R27",
            TWO_MARKS,
            "isomorphism classes of the caller's two orders",
            Pin(2, "readings.U.convention.classes_under_isomorphism"),
            Pin(2, "readings.O.convention.classes_under_isomorphism"),
            Computed("caller_order_classes"),
        ),
        Spec(
            "R28",
            TWO_MARKS,
            "identity policies that admit both retained wholes",
            Count(Pin(2, "readings.U.identity_policies.policies_admitting_both_wholes")),
            Count(Pin(2, "readings.O.identity_policies.policies_admitting_both_wholes")),
            Computed("policies_admitting_both_wholes"),
        ),
        Spec(
            "R29",
            TWO_MARKS,
            "marks the shared identity policy retains",
            Pin(2, "readings.U.identity_policies.rows.0.marks"),
            Pin(2, "readings.O.identity_policies.rows.0.marks"),
            Receipt("identity_policies.shared_policy.marks"),
            note=(
                "the pinned world REFUSES the second admission and retains none; "
                "the control accepts it as a no-op and retains ONE, so the "
                "requirement has no subject and the retained-mark check raises by "
                "name.  Neither is a false, and neither is a satisfied requirement"
            ),
        ),
        Spec(
            "R30",
            REQUIREMENT,
            "the requirement holds at base",
            Pin(3, "readings.U.base.satisfies"),
            Pin(3, "readings.O.base.satisfies"),
            Receipt("control.summary.base.satisfies"),
        ),
        Spec(
            "R31",
            REQUIREMENT,
            "the minimum cost to meet the requirement, under mu1",
            Pin(3, "readings.U.minima_by_mu1.minimum"),
            Pin(3, "readings.O.minima_by_mu1.minimum"),
            Receipt("decided.side_free_minimum"),
            price=Price(
                Pin(3, "readings.U.price.minimum_capability_count"),
                Pin(3, "readings.O.price.minimum_capability_count"),
                Receipt("decided.side_free_minimum"),
            ),
        ),
        Spec(
            "R32",
            REQUIREMENT,
            "tied non-isomorphic minima",
            Pin(3, "readings.U.minima_by_mu1.class_count"),
            Pin(3, "readings.O.minima_by_mu1.class_count"),
            Receipt("decided.side_free_classes"),
            note=(
                "plurality is its own column and is NEVER summed with price: two "
                "worlds can pay the same and reach a different number of routes"
            ),
        ),
        Spec(
            "R33",
            REQUIREMENT,
            "the minimum is unique",
            Pin(3, "readings.U.minima_by_mu1.unique"),
            Pin(3, "readings.O.minima_by_mu1.unique"),
            Receipt("decided.side_free_unique"),
        ),
        Spec(
            "R34",
            REQUIREMENT,
            "the members attaining the minimum, under the declared collapse map",
            Collapsed(Pin(3, "readings.U.minima_by_mu1.points")),
            Collapsed(Pin(3, "readings.O.minima_by_mu1.points")),
            Receipt("decided.side_free_minimum_members"),
            note=(
                "the unnamed column is the pinned point list with the declared "
                "collapse map applied, so one control point stands against one "
                "pinned class and the join is like for like"
            ),
        ),
        Spec(
            "R35",
            REQUIREMENT,
            "the declared candidate space",
            Pin(3, "readings.U.space_size"),
            Pin(3, "readings.O.space_size"),
            Receipt("candidate_space.space_size"),
        ),
        Spec(
            "R36",
            REQUIREMENT,
            "one-step points in that space, under the declared collapse map",
            Collapsed(Pin(3, "readings.U.one_step_points")),
            Collapsed(Pin(3, "readings.O.one_step_points")),
            Computed("control_one_step_points"),
            note=(
                "the map joins by NAME in both reading columns, but its "
                "one-class justification is a fact of the unnamed reading "
                "only: there the two pinned further-mark points carry one "
                "class key, while under the named reading they carry two "
                "different class keys and are two classes.  So the named "
                "column shows five names where that reading has six points, "
                "and the decision this table reports is taken against the "
                "unnamed reading"
            ),
        ),
        Spec(
            "R37",
            REQUIREMENT,
            "bundles refused at two capabilities or more",
            Pin(3, "readings.U.bundles_refused_count"),
            Pin(3, "readings.O.bundles_refused_count"),
            Receipt("candidate_space.bundles_refused_count"),
        ),
        Spec(
            "R38",
            REQUIREMENT,
            "one-step points that satisfy, under the declared collapse map",
            Collapsed(Pin(3, "readings.U.satisfying_one_step_points")),
            Collapsed(Pin(3, "readings.O.satisfying_one_step_points")),
            Computed("control_satisfying_one_step_points"),
            note=(
                "as R36: the map joins by name in both columns, its one-class "
                "justification holds under the unnamed reading only, and the "
                "named column therefore shows five names where that reading "
                "has six satisfying points"
            ),
        ),
        Spec(
            "R39",
            REQUIREMENT,
            "collateral facts the world declares",
            Pin(3, "collateral_facts"),
            Pin(3, "collateral_facts"),
            Receipt("second_measures.control_fact_list"),
            note=(
                "the two lists are not the same length, so the second measure "
                "counted over them is NOT comparable across the worlds and is "
                "never differenced.  The restricted measure below is"
            ),
        ),
        Spec(
            "R40",
            REQUIREMENT,
            "the minimum of the restricted second measure",
            Receipt("second_measures.mirror_minima_by_mu2_restricted.U.minimum"),
            Receipt("second_measures.mirror_minima_by_mu2_restricted.O.minimum"),
            Receipt("second_measures.control_minima_by_mu2_restricted.minimum"),
            note=(
                "a row whose boundary value cells are not read from a pinned "
                "path.  Which rows those are is not asserted here but computed "
                "over every row's value and stated-price sources, with each "
                "cell's role and path recorded, at "
                "`boundary_source_census.rows_whose_boundary_cells_are_not_"
                "read_from_a_pinned_path`.  No pinned receipt carries a "
                "minimum of the restricted measure, so both are minima "
                "computed on THIS TREE'S OWN mirror carrier and read out of "
                "this tree's record.  "
                "The totality gate over the declared pinned values therefore "
                "does not reach them, and never counted them: what holds them "
                "instead is the weaker per-point data join, "
                "`second_measures.data_join_against_the_pin`, which joins 48 "
                "rows per reading against the pin and reports its mismatches"
            ),
        ),
        Spec(
            "R41",
            PRICES,
            "the requirement is met with no augmentation",
            Pin(3, "readings.U.price.requirement_met_without_augmentation"),
            Pin(3, "readings.O.price.requirement_met_without_augmentation"),
            Receipt("control.summary.base.satisfies"),
        ),
        Spec(
            "R42",
            PRICES,
            "nothing new is paid at this rung",
            Pin(3, "readings.U.price.nothing_new_paid_at_challenge_3"),
            Pin(3, "readings.O.price.nothing_new_paid_at_challenge_3"),
            Computed("control_nothing_new_paid"),
        ),
        Spec(
            "R43",
            PRICES,
            "capabilities newly paid for at this rung",
            Collapsed(Pin(3, "readings.U.price.new_at_challenge_3")),
            Collapsed(Pin(3, "readings.O.price.new_at_challenge_3")),
            Computed("control_satisfying_one_step_points"),
        ),
        Spec(
            "R44",
            PRICES,
            "capabilities the satisfaction uses",
            Pin(3, "readings.U.price.capabilities_the_satisfaction_uses"),
            Pin(3, "readings.O.price.capabilities_the_satisfaction_uses"),
            Receipt("decided.side_free_minimum_members"),
            note=(
                "the pinned world flags this field as declared and not computed, "
                "in its own receipt; the control column is the computed member "
                "list of its minimum, and the two are not the same kind of thing"
            ),
        ),
        Spec(
            "R45",
            PRICES,
            "who pays for the satisfaction",
            Pin(3, "readings.U.price.paid_by"),
            Pin(3, "readings.O.price.paid_by"),
            Declared("control_paid_by"),
            note=(
                "declared and not computed on the pinned side, by its own flag, "
                "and declared and not computed on the control side too: nothing "
                "in this carrier computes a payer.  Both columns are "
                "declarations, so the agreement is true by unfolding them and "
                "is DEFINITION-level, not a measurement"
            ),
        ),
        Spec(
            "R46",
            PRICES,
            "coordinates the world prices at this rung",
            Pin(3, "candidate_space.coordinates"),
            Pin(3, "candidate_space.coordinates"),
            Receipt("candidate_space.coordinates"),
            note=(
                "the control's three are the pinned five minus the two whose "
                "pinned capability sentence names a side; the three that transfer "
                "carry their pinned sentences byte for byte"
            ),
        ),
        Spec(
            "R47",
            PRICES,
            "declared values of the further-mark coordinate",
            Pin(3, "candidate_space.extra_mark_values"),
            Pin(3, "candidate_space.extra_mark_values"),
            Receipt("candidate_space.extra_mark_values"),
            note=(
                "the single value-set change of the whole deletion, read from the "
                "pin.  Under the UNNAMED reading the two pinned further-mark "
                "points carry one class key and stand as the two members of one "
                "retained class; under the NAMED reading they carry two different "
                "class keys and are two classes, so the one-class sentence is "
                "scoped to the unnamed reading and is not a fact of both"
            ),
        ),
    ]


def extra_computed(record: Json) -> Json:
    """The control values the rows need that come from its enumerated rows."""
    summary = as_dict(dig(record, "control.summary"))
    one_step = sorted(
        name for name, row in summary.items() if bool(as_dict(row)["one_step"])
    )
    satisfying = sorted(
        name
        for name, row in summary.items()
        if bool(as_dict(row)["one_step"]) and bool(as_dict(row)["satisfies"])
    )
    return {
        "control_one_step_points": one_step,
        "control_satisfying_one_step_points": satisfying,
        "control_nothing_new_paid": bool(dig(record, "control.summary.base.satisfies")),
    }


# ---------------------------------------------------------------------------
# Building the table
# ---------------------------------------------------------------------------


def price_cells(resolver: Resolver, price: Price | None, kind: str) -> Json:
    if price is None:
        return {
            "stated": False,
            "why": (
                "the item IS a price statement; what each world states is the "
                "row's own three columns"
                if kind == PRICE
                else "neither world states a price for this item"
            ),
            "unnamed": None,
            "named": None,
            "control": None,
            "control_equals_unnamed": True,
            "control_equals_named": True,
            "columns_reading_a_declared_ledger_cell": [],
        }
    unnamed = resolver.resolve(price.unnamed)
    named = resolver.resolve(price.named)
    control = resolver.resolve(price.control)
    return {
        "stated": True,
        "unnamed": unnamed.value,
        "named": named.value,
        "control": control.value,
        "unnamed_source": unnamed.source,
        "named_source": named.source,
        "control_source": control.source,
        "control_equals_unnamed": control.value == unnamed.value,
        "control_equals_named": control.value == named.value,
        "columns_reading_a_declared_ledger_cell": [
            column
            for column, source in (
                ("unnamed", price.unnamed),
                ("named", price.named),
                ("control", price.control),
            )
            if record_field_is_declared_not_computed(resolver, source)
        ],
    }


def status_of(against: Json, price: Json, price_key: str) -> str:
    """The bucket, decided by the computation: same value AND same price."""
    if str(against["kind"]) == "absent":
        return ABSENT
    if bool(against["same"]) and bool(price[price_key]):
        return BOUGHT_NOTHING
    return BOUGHT_SOMETHING


def pinned_field_is_declared_not_computed(resolver: Resolver, source: Source) -> bool:
    """Does the pinned world itself flag this price field as declared?

    Its own receipt carries ``fields_declared_not_computed`` beside each
    reading's price block.  A row that reads one of those is comparing a
    DECLARED pinned field against a computed control value, and says so
    rather than letting the difference read as a measurement.
    """
    if not isinstance(source, Pin):
        return False
    parts = source.path.split(".")
    if len(parts) != 4 or parts[0] != "readings" or parts[2] != "price":
        return False
    flagged = resolver.resolve(
        Pin(source.challenge, f"readings.{parts[1]}.price.fields_declared_not_computed")
    )
    return parts[3] in [str(name) for name in as_list(flagged.value)]


def record_field_is_declared_not_computed(resolver: Resolver, source: Source) -> bool:
    """Does THIS TREE'S own record flag the endowment cell this reads?

    The mirror of the check above, on the control side.  Every endowment
    ledger row carries ``declared_columns``, and the ``by_row`` projection
    carries it too, so a column that reads a flagged cell can say it is
    reading a DECLARATION of this tree rather than a measurement taken off a
    carrier.  The projection used to drop the field, which meant a consumer
    reading a cell through it could not ask this question at all.
    """
    if not isinstance(source, Receipt):
        return False
    parts = source.path.split(".")
    if len(parts) != 4 or parts[0] != "endowment_ledger" or parts[1] != "by_row":
        return False
    flagged = resolver.resolve(
        Receipt(f"endowment_ledger.by_row.{parts[2]}.declared_columns")
    )
    return parts[3] in [str(name) for name in as_list(flagged.value)]


def reads_a_pinned_path(source: Source) -> bool:
    """Does this column resolve, in the end, to a path of a pinned receipt?

    A length or a collapse of a pinned path still reads the pin; a receipt
    path, a computed key or a declared value does not.
    """
    if isinstance(source, Pin):
        return True
    if isinstance(source, (Count, Collapsed)):
        return reads_a_pinned_path(source.inner)
    return False


def boundary_source_census() -> Json:
    """Classify boundary value and stated-price cells by declared source.

    The former value-only population missed R03's price cells.  Cell paths
    identify the actual output slots; roles keep a price from being mistaken
    for the value beside it.  Tests independently gather the rendered rows'
    source metadata and require this census to cover that whole population.
    """
    row_specs = specs()
    cells: list[Json] = []
    for spec in row_specs:
        sources = [
            ("value", "unnamed", "unnamed_reading", spec.unnamed),
            ("value", "named", "named_reading", spec.named),
        ]
        if spec.price is not None:
            sources.extend(
                [
                    ("price", "unnamed", "price.unnamed", spec.price.unnamed),
                    ("price", "named", "price.named", spec.price.named),
                ]
            )
        cells.extend(
            {
                "row": spec.id,
                "column": column,
                "role": role,
                "path": path,
                "reads_a_pinned_path": reads_a_pinned_path(source),
            }
            for role, column, path, source in sources
        )
    return {
        "rule": (
            "every boundary value and stated-price cell is checked.  A cell "
            "reads a pinned path when its source is a pinned "
            "path, or the length or the collapse of one.  Anything else is "
            "produced on a carrier of this tree or read out of this tree's own "
            "record, and the totality gate over the declared pinned values does "
            "not reach it"
        ),
        "rows_checked": [spec.id for spec in row_specs],
        "cells_checked": cells,
        "rows_whose_boundary_cells_are_not_read_from_a_pinned_path": [
            {
                "row": spec.id,
                "cells": [
                    cell
                    for cell in cells
                    if cell["row"] == spec.id and not cell["reads_a_pinned_path"]
                ],
            }
            for spec in row_specs
            if any(
                cell["row"] == spec.id and not cell["reads_a_pinned_path"]
                for cell in cells
            )
        ],
    }


def build_row(resolver: Resolver, spec: Spec) -> Json:
    unnamed = resolver.resolve(spec.unnamed)
    named = resolver.resolve(spec.named)
    control = resolver.resolve(spec.control)
    kind = KIND_OF[spec.id]
    declared_only = pinned_field_is_declared_not_computed(
        resolver, spec.unnamed
    ) or pinned_field_is_declared_not_computed(resolver, spec.named)
    control_declared = isinstance(spec.control, Declared)
    why_declared = (
        WHY_DECLARED[spec.control.key] if isinstance(spec.control, Declared) else None
    )
    price = price_cells(resolver, spec.price, kind)
    against_unnamed = difference(unnamed, control)
    against_named = difference(named, control)
    row: Json = {
        "id": spec.id,
        "stage": spec.stage,
        "kind": kind,
        "item": spec.item,
        "unnamed_reading": unnamed.value,
        "named_reading": named.value,
        "control": control.value,
        "control_is_absent": control.absent,
        "absent_reason": control.absent_reason,
        "difference_against_the_unnamed_reading": against_unnamed,
        "difference_against_the_named_reading": against_named,
        "the_pinned_field_is_declared_not_computed": declared_only,
        "the_control_field_is_declared_not_computed": control_declared,
        "why_the_control_field_is_declared": why_declared,
        "columns_reading_a_declared_ledger_cell": [
            column
            for column, source in (
                ("unnamed", spec.unnamed),
                ("named", spec.named),
                ("control", spec.control),
            )
            if record_field_is_declared_not_computed(resolver, source)
        ],
        "is_definition_level": declared_only and control_declared,
        "price": price,
        "status": status_of(against_unnamed, price, "control_equals_unnamed"),
        "status_against_the_named_reading": status_of(
            against_named, price, "control_equals_named"
        ),
        "sources": {
            "unnamed": unnamed.source,
            "named": named.source,
            "control": control.source,
        },
    }
    if spec.note is not None:
        row["note"] = spec.note
    return row


def bought_table(rows: Sequence[Json]) -> Json:
    """The three columns, built from the row statuses and nothing else."""
    bought: list[Json] = []
    for row in rows:
        if str(row["status"]) != BOUGHT_SOMETHING:
            continue
        stage = str(row["stage"])
        bought.append(
            {
                "what_the_admitted_boundary_bought": {
                    "row": row["id"],
                    "kind": row["kind"],
                    "item": row["item"],
                    "in_the_unnamed_reading": row["unnamed_reading"],
                    "in_the_control": row["control"],
                    "difference": row["difference_against_the_unnamed_reading"],
                },
                "what_it_cost": row["price"],
                "which_results_depend_on_its_presence": {
                    "this_row": row["id"],
                    "stage": stage,
                    "other_rows_at_this_stage_that_also_move": [
                        other["id"]
                        for other in rows
                        if other["stage"] == stage
                        and other["id"] != row["id"]
                        and str(other["status"]) == BOUGHT_SOMETHING
                    ],
                },
            }
        )
    named_only = [
        {
            "row": row["id"],
            "item": row["item"],
            "in_the_named_reading": row["named_reading"],
            "in_the_control": row["control"],
            "difference": row["difference_against_the_named_reading"],
            "what_it_cost": row["price"],
        }
        for row in rows
        if str(row["status"]) == BOUGHT_NOTHING
        and str(row["status_against_the_named_reading"]) == BOUGHT_SOMETHING
    ]
    return {
        "columns": [
            "what the admitted boundary bought",
            "what it cost",
            "which results depend on its presence",
        ],
        "decided_against": "the unnamed reading",
        "membership_rule": (
            "a row is in BOUGHT_NOTHING exactly when the control reaches the same "
            "value at the same stated price; in BOUGHT_SOMETHING when either "
            "differs; and in ABSENT when the notion has no statement in one world, "
            "which is evidence for neither bucket"
        ),
        "entries": bought,
        "entries_the_naming_alone_bought": named_only,
        "bought_nothing": [
            row["id"] for row in rows if str(row["status"]) == BOUGHT_NOTHING
        ],
        "bought_something": [
            row["id"] for row in rows if str(row["status"]) == BOUGHT_SOMETHING
        ],
        "by_kind": {
            kind: {
                status: [
                    row["id"]
                    for row in rows
                    if row["kind"] == kind and str(row["status"]) == status
                ]
                for status in (BOUGHT_NOTHING, BOUGHT_SOMETHING, ABSENT)
            }
            for kind in KINDS
        },
        "rows_whose_pinned_field_the_pinned_world_calls_declared_not_computed": [
            row["id"]
            for row in rows
            if bool(row["the_pinned_field_is_declared_not_computed"])
        ],
        "rows_whose_control_field_is_declared_not_computed": [
            row["id"]
            for row in rows
            if bool(row["the_control_field_is_declared_not_computed"])
        ],
        "definition_level_rows": [
            row["id"] for row in rows if bool(row["is_definition_level"])
        ],
        "rows_reading_a_declared_ledger_cell": [
            {
                "row": row["id"],
                "value_columns": row["columns_reading_a_declared_ledger_cell"],
                "price_columns": as_dict(row["price"])[
                    "columns_reading_a_declared_ledger_cell"
                ],
            }
            for row in rows
            if as_list(row["columns_reading_a_declared_ledger_cell"])
            or as_list(
                as_dict(row["price"])["columns_reading_a_declared_ledger_cell"]
            )
        ],
        "why_the_declared_ledger_cells_are_named": (
            "a column that reads a cell this tree's own endowment ledger flags "
            "in its declared_columns is reading a DECLARATION of this tree and "
            "not a measurement taken off a carrier.  It is named for the reason "
            "the pinned world's own declared fields are named: so that a "
            "typed-in value is not read as something either world measured"
        ),
        "why_the_definition_level_rows_are_named": (
            "a row whose pinned column and control column are BOTH declared and "
            "not computed agrees by unfolding two declarations.  That is "
            "DEFINITION-level and is not content, so it is named here and the "
            "verdict reports its tallies with the declared-field rows and "
            "without them"
        ),
        "why_the_kinds_are_reported": (
            "a difference in a world's own bookkeeping -- the size of its "
            "declared space, the tag its serialization key carries -- is not a "
            "capability the primitive bought, and the kinds keep the two apart "
            "without curating which rows are in which bucket"
        ),
        "absent": [
            {"row": row["id"], "item": row["item"], "reason": row["absent_reason"]}
            for row in rows
            if str(row["status"]) == ABSENT
        ],
    }


# ---------------------------------------------------------------------------
# Gates
# ---------------------------------------------------------------------------


def gate_declared_values(
    resolver: Resolver, pinned: Mapping[int, Json], meta: Json
) -> Json:
    """C1: every pinned value a row uses is declared, and agrees.

    Total in both directions.  An undeclared value a row reads fails; a
    declared value no row reads fails.  This is the gate the injection
    exercises: change one boundary value in the manifest and it fails by name.
    """
    block = meta.get("declared_values")
    if not isinstance(block, dict):
        return {
            "gate": "C1",
            "name": "declared_values_agree",
            "declared": 0,
            "used_by_rows": len(set(resolver.used)),
            "checked": 0,
            "problems": ["BOUNDARY_PIN.json carries no declared_values block"],
            "passed": False,
        }
    declared: Json = block
    problems: list[str] = []
    used = sorted(set(resolver.used))
    checked = 0
    for challenge, path in used:
        key = f"{challenge}:{path}"
        if key not in declared:
            problems.append(
                f"row value {key} is read from the pinned bytes but is not "
                f"declared in BOUNDARY_PIN.json"
            )
            continue
        checked += 1
        value = dig(pinned[challenge], path)
        if value != declared[key]:
            problems.append(
                f"declared value {key} is {declared[key]!r}, the pinned bytes "
                f"say {value!r}"
            )
    unused = sorted(key for key in declared if key not in {f"{c}:{p}" for c, p in used})
    for key in unused:
        problems.append(
            f"BOUNDARY_PIN.json declares {key}, which no row of this comparison reads"
        )
    return {
        "gate": "C1",
        "name": "declared_values_agree",
        "declared": len(declared),
        "used_by_rows": len(used),
        "checked": checked,
        "problems": problems,
        "passed": not problems,
    }


def gate_receipt_agrees(record: Json, rows: Sequence[Json]) -> Json:
    """C2: the control's own headline numbers are the ones the rows carry."""
    problems: list[str] = []
    by_id = {str(row["id"]): row for row in rows}
    if dig(record, "control.rows.0.name") != "base":
        problems.append(
            "the record's first control row is not the base row, so the row "
            "that R21 reads by index is not the one it names"
        )
    expected = {
        "R31": dig(record, "decided.side_free_minimum"),
        "R32": dig(record, "decided.side_free_classes"),
        "R33": dig(record, "decided.side_free_unique"),
    }
    for row_id, want in expected.items():
        got = by_id[row_id]["control"]
        if got != want:
            problems.append(f"{row_id}: the row carries {got!r}, the record says {want!r}")
    deltas = {
        "delta_vs_unnamed": (
            int(str(dig(record, "decided.side_free_minimum")))
            - int(str(dig(record, "decided.unnamed_minimum")))
        ),
        "delta_vs_named": (
            int(str(dig(record, "decided.side_free_minimum")))
            - int(str(dig(record, "decided.named_minimum")))
        ),
    }
    for name, recomputed in deltas.items():
        stated = dig(record, f"decided.{name}")
        if stated != recomputed:
            problems.append(
                f"{name}: the record states {stated!r}, recomputing the two "
                f"minima gives {recomputed!r}"
            )
    return {
        "gate": "C2",
        "name": "receipt_agrees",
        "recomputed_deltas": deltas,
        "problems": problems,
        "passed": not problems,
    }


def gate_minimum_join(pinned: Mapping[int, Json], record: Json) -> Json:
    """C3: the two worlds' minima are joined by the declared collapse map."""
    collapse = as_dict(dig(pin_meta(), "collapse_map"))
    pinned_points = [
        str(name)
        for name in as_list(dig(pinned[3], f"readings.{UNNAMED}.minima_by_mu1.points"))
    ]
    collapsed = sorted({str(collapse.get(name, name)) for name in pinned_points})
    stated = [
        str(name)
        for name in as_list(dig(record, "decided.unnamed_minimum_members_collapsed"))
    ]
    problems: list[str] = []
    if collapsed != sorted(stated):
        problems.append(
            f"the collapse of the pinned minima is {collapsed}, the record "
            f"states {sorted(stated)}"
        )
    control_members = [
        str(name) for name in as_list(dig(record, "decided.side_free_minimum_members"))
    ]
    bought = sorted(set(collapsed) - set(control_members))
    stated_bought = sorted(
        str(name)
        for name in as_list(dig(record, "decided.routes_the_admitted_primitive_bought"))
    )
    if bought != stated_bought:
        problems.append(
            f"the routes the pinned world reaches and the control does not are "
            f"{bought}, the record states {stated_bought}"
        )
    return {
        "gate": "C3",
        "name": "minimum_join",
        "pinned_points": pinned_points,
        "collapsed": collapsed,
        "control_members": control_members,
        "routes_only_the_pinned_world_reaches": bought,
        "problems": problems,
        "passed": not problems,
    }


def gate_taxonomy(rows: Sequence[Json]) -> Json:
    """C4: the row ids are distinct and the declared taxonomy is total."""
    ids = [str(row["id"]) for row in rows]
    problems: list[str] = []
    duplicates = sorted({name for name in ids if ids.count(name) > 1})
    if duplicates:
        problems.append(f"duplicate row ids: {duplicates}")
    undeclared = sorted(set(ids) - set(KIND_OF))
    if undeclared:
        problems.append(f"rows with no declared kind: {undeclared}")
    unused = sorted(set(KIND_OF) - set(ids))
    if unused:
        problems.append(f"declared kinds for rows that do not exist: {unused}")
    wrong = sorted({kind for kind in KIND_OF.values() if kind not in KINDS})
    if wrong:
        problems.append(f"kinds outside the declared taxonomy: {wrong}")
    stages = sorted({str(row["stage"]) for row in rows if "stage" in row})
    stray = [stage for stage in stages if stage not in STAGES]
    if stray:
        problems.append(f"stages outside the declared rung order: {stray}")
    return {
        "gate": "C4",
        "name": "taxonomy_total",
        "rows": len(ids),
        "kinds": list(KINDS),
        "stage_order": list(STAGES),
        "problems": problems,
        "passed": not problems,
    }


def gate_bytes(loads: Sequence[Load], rows: Sequence[Json]) -> Json:
    """C0: the pinned bytes are the declared bytes, whichever copy was read."""
    problems: list[str] = [problem for load in loads for problem in load.problems]
    declared = {int(str(row["challenge"])): row for row in rows}
    for load in loads:
        row = declared[load.challenge]
        if int(str(dig(load.data, "challenge"))) != load.challenge:
            problems.append(
                f"challenge {load.challenge}: {row['local_path']} is the receipt "
                f"of challenge {dig(load.data, 'challenge')}"
            )
    return {
        "gate": "C0",
        "name": "pinned_bytes_ok",
        "receipts": [
            {
                "challenge": int(str(row["challenge"])),
                "sha256": row["sha256"],
                "byte_count": row["byte_count"],
            }
            for row in rows
        ],
        "what_it_checks": (
            "the declared sha256, the byte count and the CR refusal of every "
            "vendored copy, that the blob at the pinned commit has the same "
            "sha256 when that commit is reachable, and that each file is the "
            "receipt of the challenge it is filed under"
        ),
        "problems": problems,
        "passed": not problems,
    }


# ---------------------------------------------------------------------------
# The verdict
# ---------------------------------------------------------------------------


def verdict_block(record: Json, rows: Sequence[Json], table: Json, commit: str) -> Json:
    """One computed sentence and its exact scope.  Numbers are computed."""
    nothing = len(as_list(table["bought_nothing"]))
    something = len(as_list(table["bought_something"]))
    absent = len(as_list(table["absent"]))
    by_kind = as_dict(table["by_kind"])
    priced_same = sum(
        len(as_list(as_dict(by_kind[kind])[BOUGHT_NOTHING])) for kind in (VERDICT, PRICE)
    )
    priced_differ = sum(
        len(as_list(as_dict(by_kind[kind])[BOUGHT_SOMETHING]))
        for kind in (VERDICT, PRICE)
    )
    delta_unnamed = dig(record, "decided.delta_vs_unnamed")
    delta_named = dig(record, "decided.delta_vs_named")
    routes = dig(record, "decided.routes_bought_count")
    declared_ids = [
        str(row["id"])
        for row in rows
        if bool(row["the_pinned_field_is_declared_not_computed"])
        or bool(row["the_control_field_is_declared_not_computed"])
    ]
    definition_ids = [str(row["id"]) for row in rows if bool(row["is_definition_level"])]
    kept = [row for row in rows if str(row["id"]) not in set(declared_ids)]
    kept_nothing = len([r for r in kept if str(r["status"]) == BOUGHT_NOTHING])
    kept_something = len([r for r in kept if str(r["status"]) == BOUGHT_SOMETHING])
    kept_priced_same = len(
        [
            r
            for r in kept
            if str(r["status"]) == BOUGHT_NOTHING and str(r["kind"]) in (VERDICT, PRICE)
        ]
    )
    kept_priced_differ = len(
        [
            r
            for r in kept
            if str(r["status"]) == BOUGHT_SOMETHING
            and str(r["kind"]) in (VERDICT, PRICE)
        ]
    )
    return {
        "statement": (
            f"Over {len(rows)} compared items at the pinned rungs, the control "
            f"reaches the unnamed reading's value at the unnamed reading's price "
            f"in {nothing} of them and differs in {something}, with {absent} items "
            f"that have no statement in one world and are therefore evidence for "
            f"neither. Restricted to the items that are verdicts or prices, it "
            f"reaches the same value at the same price in {priced_same} and "
            f"differs in {priced_differ}. Of the {len(rows)} items, "
            f"{len(declared_ids)} read a field one world or the other DECLARES "
            f"rather than computes -- {', '.join(declared_ids)} -- and the subset "
            f"declared on BOTH sides, which agrees by unfolding and is "
            f"DEFINITION-level rather than content, is {', '.join(definition_ids)}. "
            f"Setting all {len(declared_ids)} aside, the control reaches the same "
            f"value at the same price in {kept_nothing} items and differs in "
            f"{kept_something}, and restricted to verdicts and prices in "
            f"{kept_priced_same} and {kept_priced_differ}. "
            f"At the imposed requirement the minimum "
            f"cost differs by {delta_unnamed} from the unnamed reading and by "
            f"{delta_named} from the named reading, and what the admitted "
            f"primitive bought under the unnamed reading is {routes} additional "
            f"routes at the same price."
        ),
        "counts": {
            "rows": len(rows),
            "bought_nothing": nothing,
            "bought_something": something,
            "absent": absent,
            "verdict_or_price_bought_nothing": priced_same,
            "verdict_or_price_bought_something": priced_differ,
        },
        "counts_without_the_declared_field_rows": {
            "set_aside": declared_ids,
            "definition_level": definition_ids,
            "why": (
                "a row that reads a declared field on one side compares a "
                "declaration with a measurement, and a row declared on BOTH sides "
                "agrees by unfolding.  Neither is curated out of the headline: "
                "the tallies are reported both ways so the reader may take "
                "either, and the row-level flags say which is which"
            ),
            "rows": len(kept),
            "bought_nothing": kept_nothing,
            "bought_something": kept_something,
            "verdict_or_price_bought_nothing": kept_priced_same,
            "verdict_or_price_bought_something": kept_priced_differ,
        },
        "decided_value": dig(record, "decided.what_the_admitted_primitive_bought"),
        "scope": (
            f"Challenges 0 to 3 of the pinned world at {commit}, and their "
            f"analogues in this carrier: the three declared coordinates, the "
            f"pinned requirement and prices, the retained two-mark configuration, "
            f"and the measure mu1.  Nothing wider."
        ),
        "does_not_speak_for": (
            "the rungs not yet run in the pinned world, nor for whether the "
            "requirement was the right one to impose, nor for what the admitted "
            "primitive would buy at a rung this comparison does not price"
        ),
        "what_it_may_not_be_read_as": (
            "the sentence that the admitted primitive bought nothing.  What pays "
            "for separation in a world with no container is the ADMISSION ORDER, "
            "and whether an order is itself a container is not answered here"
        ),
    }


OPEN_ITEMS: tuple[Json, ...] = (
    {
        "id": "SF-OPEN-A",
        "inherited": True,
        "statement": (
            "Whether the admission order is itself a container.  What pays for "
            "separation in a world with no container is that order; this "
            "comparison prices the route and does not decide what kind of thing "
            "an order is."
        ),
    },
    {
        "id": "SF-OPEN-B",
        "inherited": True,
        "statement": (
            "The price of re-purchasing a per-mark two-valued datum.  It lies "
            "outside the pinned candidate space and is therefore priced in "
            "neither world."
        ),
    },
    {
        "id": "SF-OPEN-C",
        "inherited": True,
        "statement": (
            "The pinned premise that a candidate's permitted renamings are closed "
            "under composition and inverse is inherited, stated, and checked by "
            "nothing."
        ),
    },
    {
        "id": "SF-OPEN-D",
        "inherited": True,
        "statement": (
            "Whether the requirement should have been declared so as to exclude a "
            "route that satisfies it by unfolding."
        ),
    },
    {
        "id": "SF-OPEN-E",
        "inherited": False,
        "statement": (
            "Record-format limitation remains; the CI bypass is closed. "
            "The sibling record receipts/side_free.json retains its conditional "
            "source check at gates.G1.commit_check as the frozen design requires. "
            "Unavailable source can change diagnostic bytes, so that record is "
            "not claimed clone-independent. The source pin now names its actual "
            "landed merge. Required source verification fails on missing or "
            "differing source or ancestry outside the checked history; CI compares "
            "fresh receipt bytes unconditionally. A clone without the required "
            "source cannot pass the battery. This comparison record retains its "
            "separate clone-independent rendering property."
        ),
    },
)


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


def compare() -> Json:
    """One deterministic record.  VOID if any gate fails, with no difference."""
    man = manifest()
    meta = pin_meta()
    commit = str(man["pinned_commit"])
    loads = [load_pinned(row, commit) for row in vendored_receipts()]
    pinned = {load.challenge: load.data for load in loads}
    record = side_free_record()
    computed = control_computed()
    computed.update(extra_computed(record))
    resolver = Resolver(pinned, record, computed, as_dict(meta["collapse_map"]))
    rows = [build_row(resolver, spec) for spec in specs()]
    table = bought_table(rows)
    gates = {
        "C0": gate_bytes(loads, vendored_receipts()),
        "C1": gate_declared_values(resolver, pinned, meta),
        "C2": gate_receipt_agrees(record, rows),
        "C3": gate_minimum_join(pinned, record),
        "C4": gate_taxonomy(rows),
    }
    passed = all(bool(gate["passed"]) for gate in gates.values())
    gates_block: Json = dict(gates)
    gates_block["all_passed"] = passed
    out: Json = {
        "artifact": "comparison",
        "authority_effect": "None",
        "tree": "side_free",
        "what_this_is": (
            "the price list: what each world can say at the pinned rungs, what "
            "each says it costs, and what the admitted primitive bought.  Every "
            "row is computed from a pinned receipt or from a carrier; no boundary "
            "number is typed in"
        ),
        "pinned_commit": commit,
        "provenance": {
            "receipts": [
                {
                    "challenge": int(str(row["challenge"])),
                    "local_path": row["local_path"],
                    "sha256": row["sha256"],
                    "byte_count": row["byte_count"],
                }
                for row in vendored_receipts()
            ],
            "where_the_pinned_source_paths_are_declared": (
                "SOURCE_MANIFEST.json, which is one of the three files this "
                "tree's source-isolation scan carves for naming the pinned tree. "
                "This record cites the local vendored copies instead, so the "
                "carve stays exactly three files wide"
            ),
            "how_the_bytes_are_read": (
                "the blob at the pinned commit when that commit is reachable, and "
                "the vendored copy otherwise; both are held to the one declared "
                "sha256, so the rows are the same either way"
            ),
            "why_the_reachability_is_not_in_this_record": (
                "a record that carried it would not be the same file in a clone "
                "that cannot reach the pinned commit.  run_comparison.py prints "
                "the reachability report instead, so it is never silent"
            ),
            "control_record": "receipts/side_free.json",
        },
        "gates": gates_block,
        "void": not passed,
    }
    if not passed:
        out["problems"] = [
            f"{name}: {problem}"
            for name, gate in sorted(gates.items())
            for problem in as_list(gate["problems"])
        ]
        return out
    out["rows"] = rows
    out["row_count"] = len(rows)
    present = {str(row["stage"]) for row in rows}
    out["stages"] = [stage for stage in STAGES if stage in present]
    out["bought_table"] = table
    out["boundary_source_census"] = boundary_source_census()
    out["minima_and_the_sides"] = minima_reading_a_side(pinned, record)
    out["pinned_dependence_claims"] = dependence_block(pinned, record)
    out["verdict"] = verdict_block(record, rows, table, commit)
    out["open"] = list(OPEN_ITEMS)
    return out


def render(record: Json) -> bytes:
    """Deterministic bytes: sorted keys, LF only, no timestamp, no environment."""
    text = json.dumps(record, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    return text.encode("utf-8")


def declare_values() -> int:
    """Snapshot the pinned values the rows read into ``BOUNDARY_PIN.json``.

    A DELIBERATE act, exactly as a pin regeneration is elsewhere: it must
    never be run while an injection is live, because doing so adopts the
    injected value as the baseline and destroys the gate it feeds.  The
    snapshot is taken from the vendored bytes, so no number is typed by hand.
    """
    man = manifest()
    commit = str(man["pinned_commit"])
    loads = [load_pinned(row, commit) for row in vendored_receipts()]
    pinned = {load.challenge: load.data for load in loads}
    record = side_free_record()
    computed = control_computed()
    computed.update(extra_computed(record))
    meta = pin_meta()
    resolver = Resolver(pinned, record, computed, as_dict(meta["collapse_map"]))
    for spec in specs():
        build_row(resolver, spec)
    declared = {
        f"{challenge}:{path}": dig(pinned[challenge], path)
        for challenge, path in sorted(set(resolver.used))
    }
    meta["declared_values"] = declared
    PIN_META_PATH.write_bytes(
        (json.dumps(meta, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode(
            "utf-8"
        )
    )
    return len(declared)


# ---------------------------------------------------------------------------
# The document, rendered from the record and carrying nothing else
# ---------------------------------------------------------------------------


def show(value: object) -> str:
    """One table cell: JSON for anything that is not already a plain string."""
    if isinstance(value, str):
        return value.replace("|", "\\|")
    return f"`{json.dumps(value, sort_keys=True)}`".replace("|", "\\|")


def sentence(text: object) -> str:
    """One spliced record sentence, with its first letter raised.

    Presentation only: no word is added, removed or reordered, so the
    document still carries exactly what the record does.
    """
    raw = str(text)
    return raw[:1].upper() + raw[1:]


def difference_text(diff: Json) -> str:
    kind = str(diff["kind"])
    if kind == "absent":
        return f"absent in {diff['absent_in']}"
    if bool(diff["same"]):
        return "same"
    if kind == "count":
        return f"control minus boundary = {diff['control_minus_boundary']}"
    if kind == "set":
        return (
            f"only pinned {show(diff['only_in_the_pinned_world'])}; "
            f"only control {show(diff['only_in_the_control'])}"
        )
    return "differs"


def document(record: Json) -> bytes:
    """``COMPARISON.md``, assembled from the record and adding nothing to it."""
    lines: list[str] = []
    add: Callable[[str], None] = lines.append
    add("# The price list: the pinned world beside the side-free control")
    add("")
    add(
        "Rendered from `receipts/comparison.json` by `run_comparison.py`.  Every "
        "number, name and sentence below is carried by that record; this file "
        "adds nothing to it and is regenerated rather than edited."
    )
    add("")
    add(sentence(record["what_this_is"]) + ".")
    add("")
    provenance = as_dict(record["provenance"])
    add(
        f"Pinned commit `{record['pinned_commit']}`.  "
        + sentence(provenance["how_the_bytes_are_read"])
        + "."
    )
    add("")
    add("| challenge | vendored copy | sha256 | bytes |")
    add("|---|---|---|---|")
    for entry in as_list(provenance["receipts"]):
        row = as_dict(entry)
        add(
            f"| {row['challenge']} | `{row['local_path']}` | "
            f"`{str(row['sha256'])[:12]}` | {row['byte_count']} |"
        )
    add("")
    add(sentence(provenance["where_the_pinned_source_paths_are_declared"]) + ".")
    add("")
    add(sentence(provenance["why_the_reachability_is_not_in_this_record"]) + ".")
    add("")
    add("## Gates")
    add("")
    add("| gate | name | passed |")
    add("|---|---|---|")
    gates = as_dict(record["gates"])
    for name in sorted(key for key in gates if key != "all_passed"):
        gate = as_dict(gates[name])
        add(f"| {name} | `{gate['name']}` | {str(gate['passed']).lower()} |")
    add("")
    add(f"All gates passed: {str(gates['all_passed']).lower()}.")
    add("")
    add("## The rows")
    add("")
    table = as_dict(record["bought_table"])
    add(sentence(table["membership_rule"]) + ".")
    add("")
    for stage in as_list(record["stages"]):
        add(f"### {stage}")
        add("")
        add(
            "| id | kind | item | unnamed reading | named reading | control | "
            "difference vs unnamed | status |"
        )
        add("|---|---|---|---|---|---|---|---|")
        for entry in as_list(record["rows"]):
            row = as_dict(entry)
            if row["stage"] != stage:
                continue
            control = (
                f"ABSENT -- {row['absent_reason']}"
                if bool(row["control_is_absent"])
                else show(row["control"])
            )
            add(
                f"| {row['id']} | {row['kind']} | {row['item']} | "
                f"{show(row['unnamed_reading'])} | "
                f"{show(row['named_reading'])} | {control} | "
                f"{difference_text(as_dict(row['difference_against_the_unnamed_reading']))} | "
                f"{row['status']} |"
            )
        add("")
        for entry in as_list(record["rows"]):
            row = as_dict(entry)
            if row["stage"] == stage and "note" in row:
                add(f"* **{row['id']}.** {sentence(row['note'])}.")
        add("")
    add("## What the admitted boundary bought, what it cost, what depends on it")
    add("")
    add(f"Decided against {table['decided_against']}.")
    add("")
    add(
        "| what the admitted boundary bought | what it cost | "
        "which results depend on its presence |"
    )
    add("|---|---|---|")
    for entry in as_list(table["entries"]):
        item = as_dict(entry)
        bought = as_dict(item["what_the_admitted_boundary_bought"])
        cost = as_dict(item["what_it_cost"])
        depends = as_dict(item["which_results_depend_on_its_presence"])
        cost_text = (
            f"unnamed {show(cost['unnamed'])}, control {show(cost['control'])}"
            if bool(cost["stated"])
            else str(cost["why"])
        )
        add(
            f"| {bought['row']} ({bought['kind']}) {bought['item']}: pinned "
            f"{show(bought['in_the_unnamed_reading'])}, "
            f"control {show(bought['in_the_control'])} | {cost_text} | "
            f"{depends['this_row']} at {depends['stage']}; also "
            f"{show(depends['other_rows_at_this_stage_that_also_move'])} |"
        )
    add("")
    add(f"Bought nothing: {show(table['bought_nothing'])}.")
    add("")
    add(f"Bought something: {show(table['bought_something'])}.")
    add("")
    add(sentence(table["why_the_kinds_are_reported"]) + ".")
    add("")
    add(
        "Rows whose pinned field the pinned world's own receipt calls declared "
        "and not computed: "
        + show(
            table[
                "rows_whose_pinned_field_the_pinned_world_calls_declared_not_computed"
            ]
        )
        + "."
    )
    add("")
    add(
        "Rows whose control field this module declares rather than computes: "
        + show(table["rows_whose_control_field_is_declared_not_computed"])
        + ".  DEFINITION-level, being declared on both sides: "
        + show(table["definition_level_rows"])
        + "."
    )
    add("")
    add(sentence(table["why_the_definition_level_rows_are_named"]) + ".")
    add("")
    add(
        "Rows reading a cell this tree's own endowment ledger flags as declared "
        "and not computed, by value column and by price column: "
        + show(table["rows_reading_a_declared_ledger_cell"])
        + "."
    )
    add("")
    add(sentence(table["why_the_declared_ledger_cells_are_named"]) + ".")
    add("")
    add("| kind | bought nothing | bought something | absent |")
    add("|---|---|---|---|")
    for kind, buckets in sorted(as_dict(table["by_kind"]).items()):
        cell = as_dict(buckets)
        add(
            f"| {kind} | {show(cell[BOUGHT_NOTHING])} | "
            f"{show(cell[BOUGHT_SOMETHING])} | {show(cell[ABSENT])} |"
        )
    add("")
    add("Absent, and therefore evidence for neither bucket:")
    add("")
    for entry in as_list(table["absent"]):
        item = as_dict(entry)
        add(f"* **{item['row']}** {item['item']} -- {item['reason']}.")
    add("")
    add("What the naming alone bought, over the unnamed reading:")
    add("")
    for entry in as_list(table["entries_the_naming_alone_bought"]):
        item = as_dict(entry)
        add(
            f"* **{item['row']}** {item['item']}: named {show(item['in_the_named_reading'])}, "
            f"control {show(item['in_the_control'])}."
        )
    add("")
    add("## Which minima read a side")
    add("")
    minima = as_dict(record["minima_and_the_sides"])
    add(f"By name: {minima['criterion_by_name']}")
    add("")
    add(f"By behaviour: {minima['criterion_by_behaviour']}.")
    add("")
    add(sentence(minima["where_each_criterion_is_evaluated"]) + ".")
    add("")
    add(
        "| whose minimum | reading | minimum | names a side, over pinned text | "
        "reads the placement, computed on a carrier of this tree |"
    )
    add("|---|---|---|---|---|")
    for entry in as_list(minima["rows"]):
        row = as_dict(entry)
        placement = as_dict(row["placement"])
        add(
            f"| {row['whose_minimum']} | {show(row['reading'])} | `{row['point']}` | "
            f"{str(row['names_a_side_in_its_capability_sentence']).lower()} | "
            f"{str(placement['reads_the_placement']).lower()} |"
        )
    add("")
    add(f"The two criteria disagree on: {show(minima['the_two_criteria_disagree_on'])}.")
    add("")
    add("## The pinned world's own dependence claims, read")
    add("")
    dependence = as_dict(record["pinned_dependence_claims"])
    add(sentence(dependence["what_it_is"]) + ".")
    add("")
    add(f"Entries: {dependence['entry_count']}.  By class: {show(dependence['counts_by_class'])}.")
    add("")
    add(f"Classification: {dependence['classification_is_mechanical']}.")
    add("")
    add(f"Selector: {dependence['selector']}.")
    add("")
    adjudication = as_dict(dependence["adjudication"])
    add(f"Selected: {show(adjudication['selected'])}.")
    add("")
    add(f"Evidence: {show(adjudication['evidence'])}.")
    add("")
    add(
        f"Verdict: **{adjudication['verdict']}**.  "
        + sentence(adjudication["what_is_declared_and_what_is_computed"])
        + "."
    )
    add("")
    add("## The verdict")
    add("")
    verdict = as_dict(record["verdict"])
    add(str(verdict["statement"]))
    add("")
    add(f"Decided value: `{verdict['decided_value']}`.")
    add("")
    add(f"**Scope.** {verdict['scope']}")
    add("")
    add(f"**It does not speak for** {verdict['does_not_speak_for']}.")
    add("")
    add(f"**It may not be read as** {verdict['what_it_may_not_be_read_as']}.")
    add("")
    add("## Open, and not closed")
    add("")
    for entry in as_list(record["open"]):
        item = as_dict(entry)
        mark = "inherited" if bool(item["inherited"]) else "opened here"
        add(f"* **{item['id']}** ({mark}) {item['statement']}")
    add("")
    return ("\n".join(lines)).encode("utf-8")
