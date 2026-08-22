"""Expected values for the blind-restart stages, read from the sealed artifacts.

No derivation result is hard-coded in this file. Every expected value is
resolved from ``artifacts/`` at run time, through the same committed
exports the paper cites. A value cannot drift from the derivation without
the pinned hashes in ``SOURCE_PINS.json`` failing first.

That is deliberate. ``paper/anti_skill_inbox.md`` records "verify through
a parallel path instead of the production one" as a failure mode observed
twice inside one pull request: a check that exercises its own
re-implementation certifies the copy, and is most convincing exactly when
it is most wrong. A key that restated the numbers would be that mistake.

Scope of the stages below: genesis through the tie, plus closure
termination. The proposal this tree answers also asked for a stage about
an unjoinable overlap in the rewrite system and a stage about a residual
with a rational dual certificate. Neither is here, and neither is
deferred -- see STATUS.md for why both are refused.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any, NamedTuple

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
ARTIFACTS = REPO / "artifacts"


class Field(NamedTuple):
    """One value a submitted packet must supply for a stage."""

    name: str
    artifact: str
    pointer: tuple[str, ...]


class Stage(NamedTuple):
    """One demand put to the solver, and what its packet must contain."""

    stage_id: str
    demand: str
    ledger: tuple[str, ...]
    fields: tuple[Field, ...]


def _c(*pointer: str) -> tuple[str, ...]:
    return pointer


STAGES: tuple[Stage, ...] = (
    Stage(
        stage_id="inertia",
        demand=(
            "The initial inscription is presented and no operation or "
            "transition rule is admitted. State what follows, what does "
            "not, and whether any successor is internally forced."
        ),
        ledger=("CL-0-INERTIA",),
        fields=(
            Field("context_count", "challenges.json", _c("challenge0", "context_count")),
            Field(
                "derivable_instances",
                "challenges.json",
                _c("challenge0", "derivable_instances"),
            ),
            Field(
                "internally_forced_successor",
                "challenges.json",
                _c("challenge0", "internally_forced_successor"),
            ),
            Field(
                "supply_changes_state",
                "challenges.json",
                _c("challenge0", "supply_changes_state"),
            ),
        ),
    ),
    Stage(
        stage_id="supply_not_admission",
        demand=(
            "A further inscription is supplied. Decide whether this is a "
            "new external presentation, a new admitted state, a new "
            "internally observable distinction, or some combination. Do "
            "not conflate supply, mention, admission, retention, "
            "observation and equality."
        ),
        ledger=("CL-1-SUPPLY-NOT-ADMISSION",),
        fields=(
            Field(
                "new_external_presentation",
                "challenges.json",
                _c("challenge1", "new_external_presentation"),
            ),
            Field(
                "internal_observable_distinction",
                "challenges.json",
                _c("challenge1", "internal_observable_distinction"),
            ),
            Field(
                "admitted_without_admission_event",
                "challenges.json",
                _c("challenge1", "admitted_without_admission_event"),
            ),
        ),
    ),
    Stage(
        stage_id="collapse",
        demand=(
            "Both opaque wholes are retained. Declare the sense in which "
            "two data are internally separable, then report how many "
            "observational classes the retained data fall into, and "
            "whether admission increased what is internally expressible."
        ),
        ledger=("CL-2-COLLAPSED", "CL-2-NONINCREASE"),
        fields=(
            Field(
                "observational_classes.L",
                "challenges.json",
                _c("challenge2", "readings", "L", "observational_classes"),
            ),
            Field(
                "observational_classes.F",
                "challenges.json",
                _c("challenge2", "readings", "F", "observational_classes"),
            ),
            Field(
                "expressive_increase.L",
                "challenges.json",
                _c("challenge2", "readings", "L", "expressive_increase_over_challenge0"),
            ),
            Field(
                "expressive_increase.F",
                "challenges.json",
                _c("challenge2", "readings", "F", "expressive_increase_over_challenge0"),
            ),
        ),
    ),
    Stage(
        stage_id="regime_fails",
        demand=(
            "Separation of the retained pair is now required. Decide "
            "whether the current regime already satisfies the sense of "
            "internal separability you declared."
        ),
        ledger=("CL-3-FAIL-CURRENT",),
        fields=(
            Field(
                "current_regime_satisfies.L",
                "challenges.json",
                _c("challenge3", "L", "current_regime_satisfies"),
            ),
            Field(
                "current_regime_satisfies.F",
                "challenges.json",
                _c("challenge3", "F", "current_regime_satisfies"),
            ),
        ),
    ),
    Stage(
        stage_id="cost_floor",
        demand=(
            "Under the declared item grammar and the first declared cost "
            "measure, report the cost of a minimum valid response, and "
            "whether every candidate strictly below that cost fails. "
            "Count every capability each candidate uses; reject any "
            "candidate called one item that silently bundles others."
        ),
        ledger=("CL-3-MIN-TWO", "CL-3-COST1-IMPOSSIBLE"),
        fields=(
            Field(
                "minimum_cost.L",
                "challenges.json",
                _c("challenge3", "L", "mu1", "minimum_cost"),
            ),
            Field(
                "minimum_cost.F",
                "challenges.json",
                _c("challenge3", "F", "mu1", "minimum_cost"),
            ),
            Field(
                "below_minimum_all_fail.L",
                "challenges.json",
                _c("challenge3", "L", "mu1", "cost_below_minimum_all_fail"),
            ),
            Field(
                "below_minimum_all_fail.F",
                "challenges.json",
                _c("challenge3", "F", "mu1", "cost_below_minimum_all_fail"),
            ),
        ),
    ),
    Stage(
        stage_id="tie_under_first_measure",
        demand=(
            "Within the declared candidate bounds, and quotienting only "
            "by an isomorphism relation you state, report how many "
            "non-isomorphic minimum responses survive under the first "
            "measure. Retain all tied minima unless uniqueness is proved."
        ),
        ledger=("CL-3-NONUNIQUE-MU1", "CL-3-TIE-CLASSES"),
        fields=(
            Field("tie_classes.L", "claims.json", _c("CL-3-NONUNIQUE-MU1", "L")),
            Field("tie_classes.F", "claims.json", _c("CL-3-NONUNIQUE-MU1", "F")),
        ),
    ),
    Stage(
        stage_id="second_measure",
        demand=(
            "Apply the second declared cost measure to the survivors. "
            "Report how many non-isomorphic minima remain. Do not assume "
            "in advance that a measure either does or does not resolve a "
            "tie."
        ),
        ledger=("CL-3-UNIQUE-MU2-L", "CL-3-UNIQUE-MU2-F"),
        fields=(
            Field("tie_classes.L", "claims.json", _c("CL-3-UNIQUE-MU2", "L")),
            Field("tie_classes.F", "claims.json", _c("CL-3-UNIQUE-MU2", "F")),
        ),
    ),
    Stage(
        stage_id="closure_terminates",
        demand=(
            "Under a declared pair-separation closure policy and no "
            "external continuation, report whether every maximal branch "
            "terminates, and how many rounds were used."
        ),
        ledger=("CL-CLOSURE-TERMINATION",),
        fields=(
            Field(
                "every_maximal_branch_terminates.L",
                "claims.json",
                _c(
                    "CL-CLOSURE-TERMINATION",
                    "L",
                    "branch_report",
                    "every_maximal_branch_terminates",
                ),
            ),
            Field(
                "every_maximal_branch_terminates.F",
                "claims.json",
                _c(
                    "CL-CLOSURE-TERMINATION",
                    "F",
                    "branch_report",
                    "every_maximal_branch_terminates",
                ),
            ),
            Field(
                "rounds_used.L",
                "claims.json",
                _c("CL-CLOSURE-TERMINATION", "L", "rounds_used"),
            ),
            Field(
                "rounds_used.F",
                "claims.json",
                _c("CL-CLOSURE-TERMINATION", "F", "rounds_used"),
            ),
        ),
    ),
)


def artifact_names() -> tuple[str, ...]:
    """Every artifact the key reads, in sorted order."""

    return tuple(sorted({f.artifact for s in STAGES for f in s.fields}))


def load_artifact(name: str) -> dict[str, Any]:
    path = ARTIFACTS / name
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot read artifact {name}: {exc}") from exc
    payload: object = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError(f"artifact {name} is not a JSON object")
    return payload


def resolve(payload: dict[str, Any], field: Field) -> Any:
    """Walk a pointer, failing by name rather than returning a default.

    A missing field is an error, never a ``None``. The sibling export
    surface makes the same distinction: a hash pin proves the source did
    not move, and it does not prove the document names anything real.
    """

    node: Any = payload
    walked: list[str] = []
    for key in field.pointer:
        walked.append(key)
        if not isinstance(node, dict):
            raise ValueError(
                f"{field.artifact}:{'/'.join(walked)} is not reachable: "
                f"{'/'.join(walked[:-1]) or '<root>'} is not an object"
            )
        if key not in node:
            raise ValueError(
                f"{field.artifact}:{'/'.join(walked)} names no field "
                f"(field {field.name!r})"
            )
        node = node[key]
    return node


def expected() -> dict[str, dict[str, Any]]:
    """Expected packet contents, stage id -> field name -> value."""

    if not STAGES:
        raise ValueError("the stage population is empty; the key is broken")
    cache: dict[str, dict[str, Any]] = {}
    out: dict[str, dict[str, Any]] = {}
    for stage in STAGES:
        if not stage.fields:
            raise ValueError(f"stage {stage.stage_id} declares no fields")
        values: dict[str, Any] = {}
        for field in stage.fields:
            if field.artifact not in cache:
                cache[field.artifact] = load_artifact(field.artifact)
            values[field.name] = resolve(cache[field.artifact], field)
        out[stage.stage_id] = values
    return out
