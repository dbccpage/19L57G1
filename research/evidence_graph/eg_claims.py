"""Ledger parsing, separate from the complete public-block census.

Source assertions remain OPEN until an explicit scope review is applied.
AuthorityEffect: None.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re
from typing import Any

from eg_census import public_paths
from eg_sources import Snapshot, SourceRef

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
PUBLIC_ID = re.compile(r"\b(?:[A-Z][A-Z0-9_]*(?:-[A-Za-z0-9_.]+)+|[A-Z]{1,10}[0-9]+)\b")
FIELD = re.compile(r"^\s*[-*]\s+\*\*([^*]+)\*\*\s*:\s*(.*)$")


def context_heading(text: str) -> bool:
    title = re.sub(r"^#+\s*", "", text.strip()).strip().lower()
    return title in {"claim ledger", "claims", "contents", "table of contents", "commands", "references", "tests",
                     "verification", "usage", "frozen inputs", "evidence", "files", "scope", "definitions", "status",
                     "nonclaims", "what it supports", "what it does not support"}


@dataclass(frozen=True)
class LedgerEntry:
    public_id: str
    source: SourceRef
    statement: SourceRef
    fields: dict[str, SourceRef]


def ledger_entries(snapshot: Snapshot, path: str) -> list[LedgerEntry]:
    """Headings and ledger-table IDs; no dependency on the headline tokenizer."""
    lines = snapshot.text(path).splitlines()
    headers = [(index, match) for index, line in enumerate(lines) if (match := HEADING.match(line))]
    result = []
    for index, header in headers:
        match = PUBLIC_ID.search(header[2])
        if match is None:
            continue
        stop = next((other for other, candidate in headers if other > index and len(candidate[1]) <= len(header[1])), len(lines))
        starts = [(n, field[1].strip().lower()) for n in range(index + 1, stop) if (field := FIELD.match(lines[n]))]
        fields = {}
        for number, (start, name) in enumerate(starts):
            end = starts[number + 1][0] if number + 1 < len(starts) else stop
            while end > start + 1 and not lines[end - 1].strip():
                end -= 1
            fields[name] = snapshot.reference(path, start + 1, end)
        if "statement" in fields:
            result.append(LedgerEntry(match[0], snapshot.reference(path, index + 1, stop), fields["statement"], fields))
    if "claim" in path.lower():
        occupied = {line for entry in result for line in range(entry.source["start_line"], entry.source["end_line"] + 1)}
        for index, line in enumerate(lines, 1):
            if index in occupied or not line.strip().startswith("|"):
                continue
            first = line.strip().split("|")[1].strip().strip("` *")
            if PUBLIC_ID.fullmatch(first):
                source = snapshot.reference(path, index, index)
                result.append(LedgerEntry(first, source, source, {}))
    return result


def source_classification(snapshot: Snapshot, entry: LedgerEntry) -> str | None:
    reference = entry.fields.get("class")
    if reference is None:
        return None
    text = snapshot.resolve(reference).lower()
    choices = [("metatheory", "metatheory apparatus"), ("definition", "derived definition"),
               ("finite computation", "deterministic computation"), ("theorem", "proved theorem"),
               ("conjecture", "conjecture"), ("unresolved", "open obstruction"),
               ("counterexample", "countermodel"), ("countermodel", "countermodel")]
    found = {value for word, value in choices if word in text}
    return next(iter(found)) if len(found) == 1 else None


def claim_inventory(snapshot: Snapshot, config: dict[str, Any], headlines: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, LedgerEntry]]:
    entries: dict[str, LedgerEntry] = {}
    by_path: dict[str, list[str]] = {}
    claims: dict[str, dict[str, Any]] = {}
    for path in public_paths(snapshot, config):
        parsed = ledger_entries(snapshot, path)
        occurrences = Counter(entry.public_id for entry in parsed)
        for entry in parsed:
            identifier = f"claim:{path}::{entry.public_id}"
            if occurrences[entry.public_id] > 1:
                identifier += "@" + entry.statement["span_sha256"][:16]
            if identifier in entries:
                raise ValueError("LEDGER_STATEMENT_DUPLICATE: " + identifier)
            entries[identifier] = entry
            by_path.setdefault(path, []).append(identifier)
            claims[identifier] = {"id": identifier, "public_id": entry.public_id, "statement": entry.statement,
                "source_class": source_classification(snapshot, entry), "status": "OPEN",
                "lineage": "unresolved", "bounds": [],
                "assumption_ids": [], "parent_bridge_ids": [], "evidence_ids": [],
                "gap": "Ledger assertion is inventoried. Its cited evidence has no accepted same-scope review for this entire statement at the captured source head. Empty scope fields are unreviewed, not assertions that assumptions, bounds or parent bridges are absent."}
    for headline in headlines:
        source = headline["source"]
        identifier = headline["id"]
        if headline["kind"] == "heading" and context_heading(snapshot.resolve(source)):
            headline.update(scope_verdict="CONTEXT", review={"scope_statement": "Document heading; every nonblank substantive block is inventoried separately."}, gap=None)
            continue
        matching = [key for key in by_path.get(source["path"], []) if entries[key].source["start_line"] <= source["start_line"]
                    and source["end_line"] <= entries[key].source["end_line"]]
        if not matching:
            key = "claim:" + identifier.removeprefix("headline:")
            claims[key] = {"id": key, "public_id": None, "statement": source, "source_class": None,
                "status": "OPEN", "lineage": "unresolved", "bounds": [], "assumption_ids": [],
                "parent_bridge_ids": [], "evidence_ids": [],
                "gap": "Unindexed public text has no declared same-scope evidence contract. The complete block is retained for review; names, links and neighboring ledger entries do not prove it."}
            matching = [key]
        headline["claim_ids"] = matching
        headline["gap"] = ("This exact public span has no accepted same-scope review. Its linked source claim remains unresolved; "
                           "a compiled name or a passing neighboring receipt cannot settle the wording.")
        headline["review"] = {"scope_statement": "Unresolved source assertion or apparatus text; conservative coverage includes code listings and historical prose.",
                              "disposition": "explicit_scope_review_required"}
    return sorted(claims.values(), key=lambda row: row["id"]), entries
