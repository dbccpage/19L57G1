"""The prose watchlist census (``ci/check_prose_watchlist.py``).

The identifier firewall cannot see prose.  This gate pins every whole-word
hit of a digest-stored term list per tracked file and fails in both
directions.  These tests use NEUTRAL probe words only: the real terms live
as digests in ``ci/prose_watchlist.json`` and must not be written here as
prose, which is the whole point of storing them as digests.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "ci"))

import check_prose_watchlist as cpw  # noqa: E402


def _watched(*terms: str) -> dict[str, str]:
    return {cpw.digest(t): "probe" for t in terms}


# -- normalization and tokenization -------------------------------------


def test_normalize_strips_case_and_combining_marks() -> None:
    assert cpw.normalize("ÄpFel") == "apfel"
    assert cpw.normalize(cpw.normalize("Éclair")) == cpw.normalize("Éclair")


def test_digest_is_sha256_of_normalized_form() -> None:
    want = hashlib.sha256(b"apfel").hexdigest()
    assert cpw.digest("ÄPFEL") == want
    assert cpw.digest("apfel") == want


def test_tokens_skip_identifiers_and_split_on_hyphen() -> None:
    # snake_case and digit-bearing names are single \w runs: no \b inside,
    # so they yield nothing.  camelCase lowercases to one token.  A hyphen
    # is a separator.
    assert cpw.tokens("alpha_beta gammaDelta eps-iota k9x") == [
        "gammadelta", "eps", "iota"]


def test_stems_offer_singular_forms() -> None:
    # both de-pluralizations are offered; over-generation is harmless
    # because a form only counts when its digest is watched
    assert cpw.stems("boxes") == ["boxes", "box", "boxe"]
    assert cpw.stems("zzprobes") == ["zzprobes", "zzprob", "zzprobe"]
    assert cpw.stems("zzprobe") == ["zzprobe"]
    assert cpw.stems("abs") == ["abs"]


# -- matching -------------------------------------------------------------


def test_unigram_hits_count_plurals_and_case_not_prefixes() -> None:
    watched = _watched("zzprobe")
    hits = cpw.scan_text("zzprobes zzprobe ZZPROBE\nzzprobed zzprobe_x", watched)
    assert [(h.line, h.surface) for h in hits] == [
        (1, "zzprobes"), (1, "zzprobe"), (1, "zzprobe")]


def test_bigram_hits_adjacent_tokens_only() -> None:
    watched = _watched("zz probe")
    assert len(cpw.scan_text("a zz probe here", watched)) == 1
    assert len(cpw.scan_text("a zz-probe here", watched)) == 1
    assert len(cpw.scan_text("a zz probes here", watched)) == 1
    assert cpw.scan_text("probe zz", watched) == []
    assert cpw.scan_text("zz\nprobe", watched) == []


# -- scope ----------------------------------------------------------------


def test_scope_excludes_seed_inputs_quarantine_and_self() -> None:
    assert not cpw.in_scope("prompt/prompt.md")
    assert not cpw.in_scope("prompt\\seed_prompt.md")
    assert not cpw.in_scope("contact/analysis/anything.md")
    assert not cpw.in_scope(cpw.WATCHLIST_REL)
    assert cpw.in_scope("prompt/other.md")
    assert cpw.in_scope("research/x/STATUS.md")


def test_read_text_skips_nul_and_falls_back_to_latin1(tmp_path: Path) -> None:
    binary = tmp_path / "b.bin"
    binary.write_bytes(b"ab\x00cd")
    assert cpw.read_text(binary) is None
    latin = tmp_path / "l.txt"
    latin.write_bytes(b"zzprobe caf\xe9")
    assert cpw.read_text(latin) == "zzprobe café"


# -- census and comparison ------------------------------------------------


def test_census_and_compare_in_both_directions(tmp_path: Path) -> None:
    watched = _watched("zzprobe")
    (tmp_path / "a.md").write_text("zzprobe once\nzzprobe twice\n", "utf-8")
    (tmp_path / "b.md").write_text("nothing here\n", "utf-8")
    (tmp_path / "contact").mkdir()
    (tmp_path / "contact" / "analysis").mkdir()
    (tmp_path / "contact" / "analysis" / "q.md").write_text("zzprobe", "utf-8")
    files = ["a.md", "b.md", "contact/analysis/q.md"]
    hits = cpw.scan_repo(tmp_path, watched, files)
    census = cpw.census_of(hits)
    d = cpw.digest("zzprobe")
    assert census == {"a.md": {d: 2}}
    assert cpw.compare(census, census) == []
    # injection: one more hit -> NEW HIT naming the file and the token
    (tmp_path / "a.md").write_text(
        "zzprobe once\nzzprobe twice\nzzprobe thrice\n", "utf-8")
    hits2 = cpw.scan_repo(tmp_path, watched, files)
    fails = cpw.compare(census, cpw.census_of(hits2), hits2)
    assert len(fails) == 1
    assert fails[0].startswith("FAIL: NEW HIT: a.md:")
    assert "line 3 'zzprobe'" in fails[0]
    # other direction: a removed hit -> STALE PIN naming the file
    (tmp_path / "a.md").write_text("zzprobe once\n", "utf-8")
    hits3 = cpw.scan_repo(tmp_path, watched, files)
    fails3 = cpw.compare(census, cpw.census_of(hits3), hits3)
    assert len(fails3) == 1
    assert fails3[0].startswith("FAIL: STALE PIN: a.md:")
    # a new file with a hit is a NEW HIT too
    (tmp_path / "c.md").write_text("zzprobe\n", "utf-8")
    hits4 = cpw.scan_repo(tmp_path, watched, files + ["c.md"])
    assert any(f.startswith("FAIL: NEW HIT: c.md:")
               for f in cpw.compare(census, cpw.census_of(hits4), hits4))


def test_run_reports_clean_and_failing(tmp_path: Path) -> None:
    watched = _watched("zzprobe")
    (tmp_path / "a.md").write_text("zzprobe\n", "utf-8")
    d = cpw.digest("zzprobe")
    data: dict[str, object] = {"watched": watched, "baseline": {"a.md": {d: 1}}}
    code, msgs, _ = cpw.run(tmp_path, data, ["a.md"])
    assert code == 0 and msgs[0].startswith("prose watchlist clean")
    data["baseline"] = {}
    code, msgs, _ = cpw.run(tmp_path, data, ["a.md"])
    assert code == 1 and msgs[0].startswith("FAIL: NEW HIT: a.md:")


def test_load_rejects_malformed_watchlists(tmp_path: Path) -> None:
    p = tmp_path / "w.json"
    p.write_text(json.dumps({"watched": {}, "baseline": {}}), "utf-8")
    with pytest.raises(ValueError):
        cpw.load(p)
    p.write_text(json.dumps({"watched": {"nothex": "c"}, "baseline": {}}), "utf-8")
    with pytest.raises(ValueError):
        cpw.load(p)
    d = cpw.digest("zzprobe")
    p.write_text(json.dumps(
        {"watched": {d: "c"}, "baseline": {"a.md": {"0" * 64: 1}}}), "utf-8")
    with pytest.raises(ValueError):
        cpw.load(p)
    p.write_text(json.dumps(
        {"watched": {d: "c"}, "baseline": {"a.md": {d: 0}}}), "utf-8")
    with pytest.raises(ValueError):
        cpw.load(p)


def test_probe_answers_under_scanner_stemming() -> None:
    watched = _watched("zzprobe", "zz probe")
    out = cpw.probe(["zzprobe", "ZZPROBES", "zz-probes", "other", "a b c"],
                    watched)
    assert out[0].startswith("'zzprobe': WATCHED (probe)")
    assert out[1].startswith("'ZZPROBES': WATCHED (probe)")
    assert out[2].startswith("'zz-probes': WATCHED (probe)")
    assert out[3].startswith("'other': not watched")
    assert out[4].startswith("'a b c': not watched")


def test_add_registers_a_digest_and_repins(tmp_path: Path) -> None:
    if shutil.which("git") is None:
        pytest.skip("git unavailable")
    import subprocess
    (tmp_path / "a.md").write_text("zznew zznew\n", "utf-8")
    (tmp_path / "ci").mkdir()
    path = tmp_path / cpw.WATCHLIST_REL
    cpw.dump(path, {"about": [], "watched": _watched("zzprobe"),
                    "baseline": {}})
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    data = cpw.load(path)
    lines = cpw.add(tmp_path, path, data, "zznew", "probe class")
    assert lines[0] == f"added digest {cpw.digest('zznew')} tagged 'probe class'"
    assert lines[-1] == "regen: baseline rewritten: 1 files, 2 hits"
    text = path.read_text("utf-8")
    assert "zznew" not in text  # the word never reaches the file
    reloaded = cpw.load(path)
    assert cpw.run(tmp_path, reloaded)[0] == 0
    again = cpw.add(tmp_path, path, reloaded, "zznew", "probe class")
    assert again[0].startswith("already watched (probe class)")


def test_regen_rewrites_pin_deterministically(tmp_path: Path) -> None:
    watched = _watched("zzprobe")
    (tmp_path / "a.md").write_text("zzprobe\n", "utf-8")
    (tmp_path / "ci").mkdir()
    (tmp_path / "prompt").mkdir()
    (tmp_path / "prompt" / "prompt.md").write_text("zzprobe\n", "utf-8")
    path = tmp_path / cpw.WATCHLIST_REL
    cpw.dump(path, {"about": [], "watched": watched, "baseline": {}})
    # regen uses git ls-files at tmp_path, so give it a repository
    if shutil.which("git") is None:
        pytest.skip("git unavailable")
    import subprocess
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    data = cpw.load(path)
    lines = cpw.regen(tmp_path, path, data)
    assert lines[-1] == "regen: baseline rewritten: 1 files, 1 hits"
    first = path.read_bytes()
    assert b"\r" not in first and first.endswith(b"\n")
    cpw.regen(tmp_path, path, cpw.load(path))
    assert path.read_bytes() == first
    # the seed input under prompt/ was excluded even though it is tracked
    assert "prompt/prompt.md" not in cpw.load(path)["baseline"]  # type: ignore[operator]


# -- the live gate --------------------------------------------------------


def test_committed_watchlist_is_well_formed() -> None:
    data = cpw.load(REPO / cpw.WATCHLIST_REL)
    watched = data["watched"]
    assert isinstance(watched, dict) and len(watched) >= 40
    about = data["about"]
    assert isinstance(about, list) and about
    raw = (REPO / cpw.WATCHLIST_REL).read_bytes()
    assert b"\r" not in raw and raw.endswith(b"\n")
    # the file never carries a watched term as prose: its own text, scanned,
    # yields no hits (digests are hex; the about-block is written to pass)
    assert cpw.scan_text(raw.decode("ascii"), watched) == []


def test_live_census_matches_its_pin() -> None:
    if shutil.which("git") is None:
        pytest.skip("git unavailable")
    data = cpw.load(REPO / cpw.WATCHLIST_REL)
    code, messages, hits = cpw.run(REPO, data)
    assert code == 0, "\n".join(messages)
    baseline = data["baseline"]
    assert isinstance(baseline, dict)
    tracked = set(cpw.tracked_files(REPO))
    for rel in baseline:
        assert rel in tracked, rel
        assert cpw.in_scope(rel), rel
    assert set(hits) == set(baseline)
