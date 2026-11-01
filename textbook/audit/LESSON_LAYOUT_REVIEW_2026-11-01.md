# Shared Wiki layout: reach the worked lesson first

AuthorityEffect: None. Review date: 2026-11-01 UTC (October 31 locally).

## Reading problem

Each generated Unit previously put repeated claim summaries, a video,
two generated reminder tables and generic prediction/diagram/boundary
disclosures before the actual lesson. This made the concrete first pass
harder to reach and repeated selected fragments without their full context.
The stock prediction also asked about “the proof” on Units whose principal
contribution is a supplied definition rather than a theorem.

The shared renderer now places the complete lesson after short navigation
and a First pass reading instruction. The Act video, five general reading questions
and source-edition record are separate disclosures after the lesson.
There is no generated mathematical summary or generic dependency diagram.
The source lesson retains its own predictions, examples, classifications,
conditions, diagrams, proofs, limits and practice links in their source order.
The navigation still crosses from U74 to I00 and exits I17 to the coverage map.
Lesson position is an ordinal, not an understanding or mastery score.

## Custody before the change

All 93 live Unit pages matched the earlier renderer exactly at their
individual published source revisions. This checks that no separate
Wiki-only Unit edit is silently overwritten. All 75 Part 1 and eighteen
institution source files remain unchanged. Their 601 fenced blocks remain
the same, including source quotations, examples and diagrams. The two
separately author-edited beginner pages remain outside this publication.

## Source and layout verification

The existing Wiki verifier now checks each complete Unit body against its
source, rather than checking only that the page and sidebar link exist.
Relative links are resolved using that page's own source edition. The
full body must occur once before its folded Act video; both expected media
links and a unique First pass heading must be present. The source-edition link
names the exact file and full commit, with a matching twelve-digit label.

A Git batch read retrieves every pinned file. UTF-8 source text is
compared with line endings normalized to LF; a plausible URL alone does
not establish custody. A missing object, mismatched source text or absent
pin fails. A generated fragment shortcut before the lesson is also
refused. This verifies source text and placement, not the meaning of
every theorem, the proof checker or a claim about a physical device.

The thirteen-test Wiki authoring suite passes. Its new population check
visits all 93 Units and checks full text once, before optional media, with
the exact original fenced-block population. Eight disposable page faults
are refused: dropping a scope sentence, moving a video before the lesson,
opening the video by default, changing its GIF destination, introducing either of two unverified fragment
shortcuts, inventing an
unavailable source commit, and naming a real older commit whose source
differs from the displayed lesson. Unchanged pages recover after each fault.
The checks use scratch output; no source Unit is mutated.

## Limits and reproduction

Run `python -m unittest discover -s textbook/media -p test_wiki_textbook.py`
and the existing `ci/run_gates.py --job textbook` from the repository root.
The source-custody check is part of the existing Wiki verification step;
no gate family or allowed vocabulary population is added.

Selective publication, original page/source hashes and named live desktop,
phone, keyboard-disclosure and navigation samples are retained under
`artifacts2/lesson-layout-2026-11-01`. Corrected video bytes, all interactive
desks and figures remain unchanged. No new video is rendered for this
layout change. Complete semantic coverage, general accessibility and
observed beginner comprehension, transfer and retention remain open.
This review is not full twelve-family merge clearance; the author merges.

Live phone checks found that same-page fragments changed the address
without reliably moving the heading into view in the in-app browser.
Both the ordinary and actual GitHub heading-ID forms were tried. The
final layout therefore uses a plain First pass reading instruction and
begins with the lesson itself; it requires no generated scroll shortcut.
The initial publication, attempted fragment correction and their receipts
are retained separately from the final publication and its UI samples.
