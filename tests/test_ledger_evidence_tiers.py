"""The two pinned Lean tiers of the ledger evidence gate (gate 9).

``ci/check_ledger_evidence.py`` resolves a Lean-side citation by its final
name segment.  Two weak results used to count as ordinary passes:

* a bare name that more than one declaration or report answers to.  At
  ``827bf983`` CL-PROGRESS cited bare ``getD_append_lt``, which means the
  ``Progress.lean`` theorem, and the suffix tier matched the report of a
  different theorem, ``Attachment.getD_append_lt``;
* a cited ``theorem`` that has no axiom report and passed only because a
  declaration of that name exists.

They are now ``lean-ambiguous`` and ``lean-theorem-unreported``, pinned by
(entry id, token) and failing in both directions.  These tests drive
``classify()`` on synthetic tokens and ``main()`` on scratch copies of the
ledger.  The copies live under ``tmp_path``; nothing here writes the
sealed ledger.
"""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "ci"))

import check_ledger_evidence as gate  # noqa: E402


@pytest.fixture(autouse=True)
def _cwd(monkeypatch: pytest.MonkeyPatch) -> None:
    """The gate resolves its inputs relative to the repository root."""
    monkeypatch.chdir(REPO)


# -- helpers ---------------------------------------------------------------


def _decl(name: str, head: str, path: str = "lean4/Derivation/A.lean",
          line: int = 1) -> gate.Decl:
    return gate.Decl(name, head, path, line)


def _classify(
    norm: str,
    *,
    side: str = "lean",
    axioms: Iterable[str] = (),
    counted: Mapping[str, Sequence[gate.Decl]] | None = None,
    names: Iterable[str] | None = None,
) -> gate.Verdict:
    counted = counted or {}
    index = gate.DeclIndex(
        frozenset(counted if names is None else names),
        {key: tuple(value) for key, value in counted.items()},
    )
    token = gate.Token("CL-SYN", side, 1, norm, norm)
    return gate.classify(
        token, frozenset({"CL-SYN"}), frozenset(axioms), index,
        frozenset(), frozenset(), {}, frozenset(), "", "",
    )


def _live_verdicts(ledger: Path) -> list[gate.Verdict]:
    """Every verdict for ``ledger``, built the way ``main`` builds them."""
    text = ledger.read_text(encoding="utf-8")
    entry_ids = frozenset(
        m.group("id")
        for m in (gate.ENTRY.match(ln) for ln in text.splitlines())
        if m
    )
    axioms = gate.load_axiom_names()
    decls = gate.load_lean_decls()
    tests = gate.load_test_defs()
    codedefs = gate.load_code_defs()
    parsed, art_keys, art_text = gate.load_artifacts()
    code_text = "\n".join(
        p.read_text(encoding="utf-8")
        for root in gate.CODE_DIRS
        for p in sorted(root.rglob("*.py"))
    )
    out = []
    for entry, side, line, chunk in gate.evidence_chunks(text):
        for m in gate.TOKEN.finditer(chunk):
            at = line + chunk[: m.start()].count("\n")
            token = gate.Token(entry, side, at, m.group(1),
                               gate.normalize(m.group(1)))
            out.append(
                gate.classify(token, entry_ids, axioms, decls, tests,
                              codedefs, parsed, art_keys, art_text, code_text)
            )
    return out


def _scratch(tmp_path: Path, old: str, new: str) -> Path:
    """A copy of the ledger with exactly one occurrence of ``old``
    replaced by ``new``.  The replacement must stay on the same line so
    the rest of the ledger keeps its line numbers."""
    text = gate.LEDGER.read_text(encoding="utf-8")
    assert text.count(old) == 1, old
    assert "\n" not in old and "\n" not in new
    path = tmp_path / "ledger.md"
    path.write_bytes(text.replace(old, new).encode("utf-8"))
    return path


def _line_of(path: Path, needle: str) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    hits = [i for i, ln in enumerate(lines, 1) if needle in ln]
    assert len(hits) == 1, (needle, hits)
    return hits[0]


# The CL-PROGRESS Lean field, first line.  Injections append to it.
PROGRESS_FIELD = "- **Lean**: `mark_progress` (with `derivable_extend`,"


# -- the committed ledger ----------------------------------------------------


def test_gate_passes_and_prints_both_counts(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert gate.main() == 0
    out = capsys.readouterr().out
    assert out.startswith("ledger evidence resolves: ")
    assert f"{len(gate.PINNED_AMBIGUOUS)} lean-ambiguous," in out
    assert f"{len(gate.PINNED_UNREPORTED)} lean-theorem-unreported," in out
    assert "match their pins" in out


def test_live_populations_equal_the_pins() -> None:
    verdicts = _live_verdicts(gate.LEDGER)
    ambiguous = {(v.token.entry, v.token.norm) for v in verdicts
                 if v.category == "lean-ambiguous"}
    unreported = {(v.token.entry, v.token.norm) for v in verdicts
                  if v.category == "lean-theorem-unreported"}
    assert ambiguous == gate.PINNED_AMBIGUOUS
    assert unreported == gate.PINNED_UNREPORTED
    assert not ambiguous & unreported


def test_the_pinned_members_are_the_measured_ones() -> None:
    """The frozen sets as measured at 827bf983, written out so a change
    to either pin is a visible edit to this file too."""
    assert gate.PINNED_AMBIGUOUS == frozenset(
        {("CL-PROGRESS", "getD_append_lt"), ("CL-RP-PRODUCTIVITY", "admitTok")}
    )
    assert gate.PINNED_UNREPORTED == frozenset(
        {
            ("CL-PROGRESS", "derivable_extend"),
            ("CL-PROGRESS", "getD_concat_self"),
            ("CL-TOKEN-ERASURE", "mem_insertNew"),
            ("CL-TOKEN-ERASURE", "insertNew_of_not_mem"),
            ("CL-TOKEN-ERASURE", "insertNew_of_mem"),
            ("CL-TOKEN-ERASURE", "replayT_cons"),
            ("CL-TOKEN-ERASURE", "replayE_cons"),
        }
    )


def test_bare_getD_append_lt_no_longer_passes_on_another_theorems_report() -> None:
    """The defect itself: the only report ends in ``.getD_append_lt`` but
    belongs to Attachment.lean's theorem.  The verdict names both
    declarations and the one report."""
    by_key = {(v.token.entry, v.token.norm): v
              for v in _live_verdicts(gate.LEDGER)}
    verdict = by_key[("CL-PROGRESS", "getD_append_lt")]
    assert verdict.category == "lean-ambiguous"
    assert "report Attachment.getD_append_lt" in verdict.detail
    assert "lean4/Derivation/Attachment.lean:" in verdict.detail
    assert "lean4/Derivation/Progress.lean:" in verdict.detail
    admit = by_key[("CL-RP-PRODUCTIVITY", "admitTok")]
    assert admit.category == "lean-ambiguous"
    assert "constructor REvent.admitTok at lean4/Derivation/Refusal.lean:" in admit.detail
    assert "constructor Event.admitTok at lean4/Derivation/Represented.lean:" in admit.detail


# -- classify() on synthetic tokens ------------------------------------------


def test_two_declarations_make_a_bare_name_ambiguous() -> None:
    counted = {"foo": [_decl("foo", "theorem", "lean4/Derivation/A.lean", 3),
                       _decl("foo", "theorem", "lean4/Derivation/B.lean", 7)]}
    verdict = _classify("foo", axioms={"A.foo"}, counted=counted)
    assert verdict.category == "lean-ambiguous"
    assert verdict.detail == (
        "candidates: report A.foo; theorem foo at lean4/Derivation/A.lean:3; "
        "theorem foo at lean4/Derivation/B.lean:7"
    )


def test_two_reports_make_a_bare_name_ambiguous() -> None:
    counted = {"foo": [_decl("foo", "theorem")]}
    verdict = _classify("foo", axioms={"A.foo", "B.foo"}, counted=counted)
    assert verdict.category == "lean-ambiguous"
    assert "report A.foo; report B.foo" in verdict.detail


def test_an_exact_and_a_suffix_report_are_two_reports() -> None:
    verdict = _classify("foo", axioms={"foo", "A.foo"},
                        counted={"foo": [_decl("foo", "theorem")]})
    assert verdict.category == "lean-ambiguous"


def test_a_leading_dot_token_counts_as_bare() -> None:
    counted = {"foo": [_decl("foo", "def"), _decl("foo", "def", line=9)]}
    assert _classify(".foo", counted=counted).category == "lean-ambiguous"


def test_a_qualified_token_is_never_ambiguous() -> None:
    counted = {"foo": [_decl("foo", "theorem"), _decl("foo", "theorem", line=9)]}
    verdict = _classify("A.foo", axioms={"A.foo", "B.foo"}, counted=counted)
    assert verdict.category == "lean-theorem"
    assert verdict.detail == "exact"


def test_one_declaration_and_one_report_is_a_theorem_pass() -> None:
    verdict = _classify("foo", axioms={"Derivation.foo"},
                        counted={"foo": [_decl("foo", "theorem")]})
    assert verdict.category == "lean-theorem"
    assert verdict.detail == "suffix"


def test_ambiguity_is_decided_before_the_unreported_tier() -> None:
    counted = {"foo": [_decl("foo", "theorem"), _decl("foo", "def", line=9)]}
    assert _classify("foo", counted=counted).category == "lean-ambiguous"


@pytest.mark.parametrize("head", ["theorem", "lemma"])
def test_a_theorem_without_a_report_is_unreported(head: str) -> None:
    verdict = _classify("foo", counted={"foo": [_decl("foo", head, line=4)]})
    assert verdict.category == "lean-theorem-unreported"
    assert verdict.detail == (
        "declared as a theorem, no axiom report; candidates: "
        f"{head} foo at lean4/Derivation/A.lean:4"
    )


def test_a_qualified_theorem_without_a_report_is_unreported() -> None:
    verdict = _classify("A.foo", counted={"foo": [_decl("foo", "theorem")]})
    assert verdict.category == "lean-theorem-unreported"


@pytest.mark.parametrize("head", ["def", "structure", "inductive", "abbrev",
                                  "instance", "class", gate.CONSTRUCTOR])
def test_a_non_theorem_without_a_report_stays_a_declaration(head: str) -> None:
    verdict = _classify("foo", counted={"foo": [_decl("foo", head)]})
    assert verdict.category == "lean-decl"


def test_existence_without_a_counted_declaration_stays_a_declaration() -> None:
    """A name the over-broad index sees only in a match arm or a comment
    has no counted head, so it cannot be called a theorem."""
    verdict = _classify("foo", counted={}, names={"foo"})
    assert verdict.category == "lean-decl"


def test_the_python_side_is_untouched() -> None:
    counted = {"foo": [_decl("foo", "theorem"), _decl("foo", "theorem", line=9)]}
    verdict = _classify("foo", side="python", counted=counted)
    assert verdict.category == "UNRESOLVED"


def test_an_unknown_bare_name_is_still_unresolved() -> None:
    assert _classify("nowhere").category == "UNRESOLVED"


# -- the counted declaration index -------------------------------------------


def test_comments_and_strings_are_handled_by_the_stripper() -> None:
    text = (
        "/-! doc\ntheorem hidden : True := trivial\n-/\n"
        "/- outer /- inner -/ still comment\ntheorem hidden2 -/\n"
        "def shown := \"-- not a comment\" -- a comment\n"
    )
    lines = gate.strip_lean_comments(text)
    assert len(lines) == len(text.splitlines())
    assert "hidden" not in "".join(lines)
    assert lines[-1] == 'def shown := "-- not a comment" '


def test_counting_keeps_heads_and_scopes_constructors_to_inductives() -> None:
    text = "\n".join(
        [
            "/-- theorem inComment is prose, not a declaration -/",
            "inductive Ev where",
            "  | admit (t : Nat)",
            "  | stop | halt",
            "deriving Repr",
            "  | notACtor",
            "def run : Ev → Nat",
            "  | .admit t => t",
            "  | stop => 0",
            "  | halt => 1",
            "theorem run_stop : run .stop = 0 := rfl",
            "inductive Tri where | t0 | t1",
        ]
    )
    decls = gate.count_decls(Path("lean4/Derivation/X.lean"), text)
    got = [(d.name, d.head, d.line) for d in decls]
    assert got == [
        ("Ev", "inductive", 2),
        ("Ev.admit", "constructor", 3),
        ("Ev.stop", "constructor", 4),
        ("Ev.halt", "constructor", 4),
        ("run", "def", 7),
        ("run_stop", "theorem", 11),
        ("Tri", "inductive", 12),
        ("Tri.t0", "constructor", 12),
        ("Tri.t1", "constructor", 12),
    ]


def test_match_arms_are_not_counted_on_the_real_tree() -> None:
    """Measured, not assumed: the over-broad pattern sees ``newRuleAll`` on
    24 ``|`` lines, and only one of them is a constructor.  Counting the
    other 23 made it ambiguous in the first measurement."""
    index = gate.load_lean_decls()
    assert "newRuleAll" in index
    assert [d.describe() for d in index.counted["newRuleAll"]] == [
        "constructor Item.newRuleAll at lean4/Derivation/Basic.lean:175"
    ]
    assert sorted(d.describe() for d in index.counted["admitTok"]) == [
        "constructor Event.admitTok at lean4/Derivation/Represented.lean:165",
        "constructor REvent.admitTok at lean4/Derivation/Refusal.lean:45",
    ]


# -- main() on scratch ledgers -------------------------------------------------


def test_an_unchanged_copy_passes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    scratch = _scratch(tmp_path, PROGRESS_FIELD, PROGRESS_FIELD)
    assert gate.main(scratch) == 0
    assert "match their pins" in capsys.readouterr().out


def test_new_members_fail_naming_entry_line_token_and_candidates(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The injection: a theorem with no report (``applyDelta_single``,
    Minimality.lean) and a bare name declared twice
    (``refusal_object_inert``, the docstring's withdrawn example)."""
    scratch = _scratch(
        tmp_path,
        PROGRESS_FIELD,
        PROGRESS_FIELD + " `applyDelta_single`, `refusal_object_inert`,",
    )
    line = _line_of(scratch, "`applyDelta_single`")
    assert gate.main(scratch) == 1
    out = capsys.readouterr().out
    assert "FAIL: lean-ambiguous citations in" in out
    assert "FAIL: lean-theorem-unreported citations in" in out
    assert (
        f"  NEW lean-ambiguous: {scratch}:{line}: CL-PROGRESS [lean] "
        "`refusal_object_inert`: candidates: "
        "report Completion.refusal_object_inert; "
        "report PrimitivePassage.refusal_object_inert; "
        "theorem refusal_object_inert at lean4/Derivation/Completion.lean:"
    ) in out
    assert "lean4/Derivation/PrimitivePassage.lean:" in out
    assert (
        f"  NEW lean-theorem-unreported: {scratch}:{line}: CL-PROGRESS [lean] "
        "`applyDelta_single`: declared as a theorem, no axiom report; "
        "candidates: theorem applyDelta_single at "
        "lean4/Derivation/Minimality.lean:"
    ) in out
    assert "STALE PIN" not in out


def test_a_new_member_reports_its_own_line_in_a_wrapped_field(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    old = "  `getD_concat_self`, `getD_append_lt`)."
    scratch = _scratch(tmp_path, old, old[:-2] + ", `applyDelta_single`).")
    line = _line_of(scratch, "`applyDelta_single`")
    opener = _line_of(scratch, PROGRESS_FIELD)
    assert line == opener + 1
    assert gate.main(scratch) == 1
    out = capsys.readouterr().out
    assert f"{scratch}:{line}: CL-PROGRESS [lean] `applyDelta_single`" in out


def test_a_vanished_member_fails_as_a_stale_pin(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    scratch = _scratch(tmp_path, "`getD_append_lt`)", "getD_append_lt)")
    assert gate.main(scratch) == 1
    out = capsys.readouterr().out
    assert (
        "  STALE PIN: (CL-PROGRESS, `getD_append_lt`) is in PINNED_AMBIGUOUS "
        "as lean-ambiguous but is no longer cited in an evidence field; "
        "remove it from PINNED_AMBIGUOUS"
    ) in out
    assert "NEW " not in out


def test_a_requalified_citation_fails_as_a_stale_pin(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Qualifying the citation to the report it matched is not a silent
    fix: the pin still has to be removed on purpose."""
    scratch = _scratch(
        tmp_path, "`getD_append_lt`)", "`Attachment.getD_append_lt`)"
    )
    assert gate.main(scratch) == 1
    out = capsys.readouterr().out
    assert (
        "STALE PIN: (CL-PROGRESS, `getD_append_lt`) is in PINNED_AMBIGUOUS "
        "as lean-ambiguous but is no longer cited in an evidence field"
    ) in out


def test_a_stale_pin_names_what_the_member_is_now(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A report arriving for a pinned theorem closes that residual.  The
    gate then fails until the pin is removed, and says what the citation
    has become."""
    real = gate.load_axiom_names()
    monkeypatch.setattr(
        gate, "load_axiom_names",
        lambda: real | {"Derivation.derivable_extend"},
    )
    assert gate.main() == 1
    out = capsys.readouterr().out
    assert (
        "  STALE PIN: (CL-PROGRESS, `derivable_extend`) is in "
        "PINNED_UNREPORTED as lean-theorem-unreported but now classifies "
        "as lean-theorem; remove it from PINNED_UNREPORTED"
    ) in out
    assert "PINNED_AMBIGUOUS" not in out


def test_an_unreported_member_that_vanishes_fails_too(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    scratch = _scratch(tmp_path, "`replayT_cons`", "replayT_cons")
    assert gate.main(scratch) == 1
    out = capsys.readouterr().out
    assert "FAIL: lean-theorem-unreported citations in" in out
    assert "STALE PIN: (CL-TOKEN-ERASURE, `replayT_cons`) is in PINNED_UNREPORTED" in out


def test_unresolved_and_pin_failures_are_reported_together(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    scratch = _scratch(
        tmp_path,
        PROGRESS_FIELD,
        PROGRESS_FIELD + " `zzz_probe_absent`, `refusal_object_inert`,",
    )
    assert gate.main(scratch) == 1
    out = capsys.readouterr().out
    assert "FAIL: 1 unresolved evidence citation(s)" in out
    assert "`zzz_probe_absent`" in out
    assert "NEW lean-ambiguous" in out


def test_a_missing_ledger_fails_by_name(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    absent = tmp_path / "absent.md"
    assert gate.main(absent) == 1
    assert f"FAIL: {absent} not found" in capsys.readouterr().out


# -- the command line ------------------------------------------------------------


def test_parse_args_reads_the_ledger_override() -> None:
    assert gate.parse_args([]) is None
    assert gate.parse_args(["--ledger", "x.md"]) == Path("x.md")


def test_the_cli_override_reaches_main(tmp_path: Path) -> None:
    scratch = _scratch(
        tmp_path, PROGRESS_FIELD, PROGRESS_FIELD + " `refusal_object_inert`,"
    )
    proc = subprocess.run(
        [sys.executable, "ci/check_ledger_evidence.py", "--ledger", str(scratch)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1, proc.stdout
    assert "NEW lean-ambiguous" in proc.stdout
    assert "`refusal_object_inert`" in proc.stdout
