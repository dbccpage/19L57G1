# Catalog schema (plan — not a live database)

**Do not run this SQL in this PR.** It is the target shape for
review. Status words below are library lifecycle, not FDA
standing, and not house AuthorityStatus.

Target: practical EKNF. Foreign keys on.

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE repo (
  repo_id     INTEGER PRIMARY KEY,
  code        TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL
);

CREATE TABLE visibility (
  visibility_id INTEGER PRIMARY KEY,
  code          TEXT NOT NULL UNIQUE
);

CREATE TABLE track (
  track_id    INTEGER PRIMARY KEY,
  code        TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL
);

CREATE TABLE program_node (
  program_id INTEGER PRIMARY KEY,
  parent_id  INTEGER REFERENCES program_node(program_id),
  level      INTEGER NOT NULL CHECK (level BETWEEN 1 AND 3),
  code       TEXT NOT NULL,
  name       TEXT NOT NULL,
  UNIQUE (parent_id, code)
);

CREATE TABLE paper (
  paper_id      INTEGER PRIMARY KEY,
  bit_key       BLOB NOT NULL UNIQUE
                  CHECK (length(bit_key) = 16),
  repo_id       INTEGER NOT NULL REFERENCES repo(repo_id),
  visibility_id INTEGER NOT NULL REFERENCES visibility(visibility_id),
  track_id      INTEGER NOT NULL REFERENCES track(track_id),
  program_id    INTEGER NOT NULL REFERENCES program_node(program_id),
  paper_seq     INTEGER NOT NULL,
  slug          TEXT NOT NULL,
  title         TEXT NOT NULL,
  status        TEXT NOT NULL CHECK (status IN (
                  'draft', 'sealed_negative', 'active',
                  'withdrawn', 'promoted')),
  created_at    TEXT NOT NULL,
  sealed_at     TEXT,
  UNIQUE (repo_id, track_id, program_id, paper_seq)
);

CREATE TABLE claim (
  claim_id  INTEGER PRIMARY KEY,
  bit_key   BLOB NOT NULL UNIQUE
              CHECK (length(bit_key) = 16),
  paper_id  INTEGER NOT NULL REFERENCES paper(paper_id),
  claim_seq INTEGER NOT NULL,
  prefix    TEXT NOT NULL,
  statement TEXT NOT NULL,
  class     TEXT NOT NULL CHECK (class IN (
              'definition', 'theorem', 'bounded_theorem',
              'counterexample', 'declared_metatheory',
              'finite_computation', 'open', 'withdrawn')),
  status    TEXT NOT NULL CHECK (status IN (
              'live', 'withdrawn', 'superseded', 'open')),
  UNIQUE (paper_id, claim_seq)
);

CREATE TABLE claim_dep (
  claim_id   INTEGER NOT NULL REFERENCES claim(claim_id),
  depends_on INTEGER NOT NULL REFERENCES claim(claim_id),
  PRIMARY KEY (claim_id, depends_on),
  CHECK (claim_id <> depends_on)
);

CREATE TABLE paper_file (
  paper_id    INTEGER NOT NULL REFERENCES paper(paper_id),
  kind        TEXT NOT NULL CHECK (kind IN (
                'paper', 'claim_ledger', 'change_log')),
  rel_path    TEXT NOT NULL,
  content_sha TEXT NOT NULL,
  PRIMARY KEY (paper_id, kind)
);

CREATE TABLE change_event (
  event_id    INTEGER PRIMARY KEY,
  paper_id    INTEGER NOT NULL REFERENCES paper(paper_id),
  claim_id    INTEGER REFERENCES claim(claim_id),
  event_type  TEXT NOT NULL CHECK (event_type IN (
                'admit', 'withdraw', 'repair', 'supersede',
                'promote', 'seal_negative', 'status_change')),
  reason      TEXT NOT NULL,
  actor       TEXT NOT NULL,
  at          TEXT NOT NULL,
  prev_status TEXT,
  new_status  TEXT
);

CREATE TABLE external_code (
  paper_id INTEGER NOT NULL REFERENCES paper(paper_id),
  scheme   TEXT NOT NULL CHECK (scheme IN (
             'MSC2020', 'arXiv', 'PACS', 'LoC', 'HEP',
             'custom')),
  code     TEXT NOT NULL,
  PRIMARY KEY (paper_id, scheme, code)
);

CREATE VIRTUAL TABLE claim_fts USING fts5(
  statement,
  prefix,
  content='claim',
  content_rowid='claim_id'
);
```

## House-law notes (must hold before CREATE)

- `promoted` is a human act. Agents must not write it.
- SQL `status` is library lifecycle. Do not collapse it with
  AuthorityStatus, LifecycleStatus, or GtocTerminal.
- `sealed_negative` is for the `0N/00-null` pointer to the
  existing sealed derivation, not a new origin proof.
- `content_sha` is integrity, not truth.
- A search hit is not standing.

## Option A vs B (prune later)

- A: committed YAML/JSONL; generated SQLite. Better diffs.
- B: committed SQLite as the catalog. Needs a YAML dump for
  review.

Recommendation to prune toward: A for OER, B as a generated
artifact. Do not import `omega_engine_databases/*.db`.
