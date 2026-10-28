# Authoring and checking the first-steps route

AuthorityEffect: None. This directory is explanatory apparatus outside the
sealed derivation. It changes no sealed definition and introduces no new
research-tree registration.

## Local reading and preview

Read `README.md`, then Lessons 00–04. Keep `PRACTICE.md` and
`READER_CHECK.md` separate from their answer files while trying the tasks.

Serve the explorer from the repository root with an available Python:

```text
python textbook/first_steps/serve.py
```

Open `http://127.0.0.1:8765/explorer.html`. The explorer uses local module
and JSON files, and makes no external requests. It stores no responses or
personal information. Reloading or Reset restores the supplied example.
The preview server supplies explicit JavaScript MIME types so Windows
file associations cannot prevent the modules from loading.

For a single HTML file that also opens directly from disk:

```text
python textbook/first_steps/build.py --output artifacts2/first_steps/explorer.html
```

This bundles the declared answer table and local CSS/JavaScript. The source
files remain separate for inspection and testing.

The Markdown lessons remain complete without the interactive controls.
The Wiki mirrors each lesson and supplies a hosted launch URL for the
self-contained explorer at `media/first_steps/explorer.html`.

## Checks

```text
python textbook/checks/u00_first_steps.py
node --test textbook/first_steps/test_model.mjs
python -m unittest discover -s textbook/media -p test_research_population.py
python -m unittest discover -s textbook/first_steps -p test_build.py
```

The first command is discovered automatically by the existing textbook
Python check runner. It independently encodes all 64 two-question boolean
tables on three items through the sealed Python admission and observation
modules, for all four selected-question subsets. It checks contexts,
positive derivability, profiles, separations, and witnesses.

The JavaScript checks compare recovery with independent enumeration of
possible lookup rules on each observed pattern. They also exercise the
loss example, the empty question list, and malformed inputs. Node is
needed for this authoring check, not for reading the Markdown lessons or
running the existing Python/Lean gate jobs.

Browser inspection must cover prediction gating, all question subsets,
renaming, reset, a successful recovery lookup, a blocking pair, keyboard
focus, narrow viewports, and a failed asset load. Geometry, calculations,
and interface operation are different checks from reader comprehension.

## Learning criteria and next work

The assessment asks for names versus answers, groups of distinct entries,
a separation witness, the hypothesis for refinement, and a blocking pair.
The provisional target is four fully explained tasks plus a transfer
explanation. Record actual reading time and the reader's own responses;
no learning outcome or twenty-minute guarantee is claimed yet.

This route supplies the first five small lessons. Later work still needs
the rest of the sealed-development learning route, source-audited research
lessons, complete search and replay laboratories, additional visual
explanations, novice feedback, and delayed transfer checks. The full
thread goal remains open.
