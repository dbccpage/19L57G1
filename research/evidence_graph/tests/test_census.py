"""Population and lexical failure controls. AuthorityEffect: None."""
import pytest

from eg_census import blank_lean_comments, lean_imports, text_blocks
from eg_schema import topological_ranks


def test_comments_and_strings_do_not_supply_imports() -> None:
    source = '/- import Fake.Hidden /- nested -/ -/\nimport Native.Basic -- trailing\n\ndef text := "import Fake.String"\nimport Fake.Late\n'
    assert lean_imports(source) == ["Native.Basic"]
    assert blank_lean_comments('"/- is a string -/"') == '"/- is a string -/"'


def test_multiline_header_and_quoted_names() -> None:
    assert lean_imports('module\nprelude\npublic import\n Native.«odd-name» Native.Second\nnamespace Example\n') == ["Native.«odd-name»", "Native.Second"]


@pytest.mark.parametrize("source", ["/- open", 'def x := "open', "import\n", "import\nimport Other", "import Bad; injected"])
def test_unreadable_header_fails_closed(source: str) -> None:
    with pytest.raises(ValueError):
        lean_imports(source)


def test_every_nonempty_text_line_enters_population() -> None:
    text = '# Heading\n\nFree assertion\ncontinues.\n\n| A | B |\n| 1 | 2 |\n\n- A result\n  and its condition\n\n```text\n# Listing, not heading\n```\n\n> Another claim\n'
    blocks = text_blocks("example.md", text)
    assert [b.kind for b in blocks] == ["heading", "prose", "table_row", "table_row", "list_item", "listing", "prose"]
    actual = {line for b in blocks for line in range(b.start, b.end + 1)}
    assert all(i + 1 in actual for i, line in enumerate(text.splitlines()) if line.strip())


def test_dependency_order_and_disconnected_nodes() -> None:
    result = topological_ranks(["claim", "proof", "premise", "other"], [("claim", "proof"), ("proof", "premise")])
    assert result == {"premise": 0, "other": 0, "proof": 1, "claim": 2}


@pytest.mark.parametrize("nodes,edges,error", [
    (["a"], [("a", "a")], "PROOF_DEPENDENCY_CYCLE"),
    (["a", "b"], [("a", "b"), ("b", "a")], "PROOF_DEPENDENCY_CYCLE"),
    (["a"], [("a", "missing")], "DEPENDENCY_NODE_MISSING"),
    (["a", "a"], [], "DEPENDENCY_NODE_DUPLICATE"),
])
def test_bad_dependency_graph_is_named(nodes: list[str], edges: list[tuple[str, str]], error: str) -> None:
    with pytest.raises(ValueError, match=error):
        topological_ranks(nodes, edges)
