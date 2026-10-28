# Reproduce the search lab

AuthorityEffect: None. All generated teaching records live under
`textbook/search_lab/`, outside the sealed paths.

Run from the repository root with an available Python:

```text
python textbook/search_lab/run_lab.py
python textbook/checks/u17_search_lab.py
python -m unittest discover -s textbook/search_lab -p test_lab.py
```

The first command recomputes both readings at arity bounds 1, 2, 3 and
compares every allowed candidate of zero to two items using the naive
validity path with the optimized minimum search under both price rules.
It also checks the protection examples, stop reasons, explicit class
maps, brute-force class partitions, and the longer exported graph.
The source-map population table is compared with those computed cases.
The existing textbook runner automatically discovers the second command.
The unit tests also require rejection of a dropped tie, a forged export
price, and stale numbers in the lesson table, and check the self-contained
bundle's data and downloadable-record links.

To regenerate the two teaching records after an intentional source change:

```text
python textbook/search_lab/run_lab.py --write
```

Review the difference. Do not regenerate a record merely to make a
source disagreement disappear. The current records are deterministic
within the declared inputs and source normalization mode.

For the separate replay path, without running candidate search:

```text
python -c "import sys,json; sys.path.insert(0,'code'); from derivation.export import verify_full_export; p=json.load(open('textbook/search_lab/reading_L_mu1_rounds5.json',encoding='utf-8')); ok=verify_full_export(p); print(ok); sys.exit(0 if ok else 1)"
```

The replay checker is separate from the search, sharing the admitted
kernel. Its limited scope is demonstrated in Lesson 07.

For the repository's entire local textbook job under its required Python
version and pinned dependencies:

```text
uv run --isolated --no-project --python 3.14.7 --with-requirements requirements.txt python ci/run_gates.py --job textbook --receipt artifacts2/search_lab/textbook_gates_314.json
```

An existing uv-managed Python 3.14.7 ran this job successfully. Its five
selected steps include the library build, 97 Python checks, and 71
book-Lean checks. This is the textbook job only, not all twelve local gate
families. The earlier bundled-Python 3.12 setup failure is historical.

Build and preview the results desk:

```text
python textbook/search_lab/build_results.py
python -m http.server 8766 --bind 127.0.0.1 --directory textbook/search_lab
```

Open `http://127.0.0.1:8766/results.html`. It is also a self-contained file
that can be opened directly from disk. It makes no runtime data requests,
stores no reader data, and displays the source-backed recorded outcomes.
Changing a control selects a recorded case; it does not execute a Python
search or replay verifier in the browser. The interface calls its button
“Reveal recorded result” to keep that distinction visible.

The Wiki copy rewrites reading and downloadable-record links to their
published locations. Browser review should cover changed price rules,
all arity settings, protected/unprotected cases and both item budgets,
prediction gating, recorded replay outcomes, keyboard controls, and a
narrow viewport. Reader comprehension remains a separate evaluation.
