# 29. From model ticks to a clock claim

The uniform Lean rule gives two new fast ticks for each new slow tick.
A team concludes, “Two real clocks will stay synchronized under any
conditions.”

**Predict:** what physical comparison did the theorem perform?

<details><summary>Check your prediction</summary>

None. The ratio follows from additions built into the declared update.
It establishes a relation between model counters, not an observation
about an actual pair of clocks.

</details>

For an application, specify which events count as ticks, which model
updates correspond to device events, how the two records are compared,
and under what operating conditions the proposed rule should hold.
Keep the counter origins and both endpoints of every interval.

Use this blank worksheet for a separately chosen comparison. Do not
replace its entries with generated desk rows and call them observations.

| Item to retain | Your entry |
|---|---|
| Devices or counters actually compared | |
| Meaning of one recorded tick on each | |
| How interval start/end events are associated | |
| Initial counts and final counts | |
| Predicted changes and ratio before comparison | |
| Observed changes, repeats and unclear readings | |
| Conditions, interval lengths and untested cases | |

A short interval may include a pulse in one schedule but not another.
Matching a longer-interval ratio need not identify the complete update
rule. A shifted origin can change total counts without changing elapsed
increments. The examples show why the procedure and interval belong
with the numbers.

### What the execution model assumes

The teaching route uses natural-number fields, exactly the named Python
registers a and b, and the native fixed period labels 1 and 2. Changing
the labels does not tune the native transition: its next step overwrites
them with those fixed values. The raw rate function subtracts two supplied
counter records; it does not establish that one was reached from the other.
The desk instead obtains its endpoints by replaying the chosen rule.

The computer executes these calculations, but no theorem here measures
its scheduling delays or converts update count into seconds. There is
also no assertion that the Python and Lean schedules represent one
physical process. Such a correspondence remains a separate obligation.

Try the [changed practice](CLOCKS_PRACTICE.md) before its
[answers](CLOCKS_ANSWERS.md). The [source guide](CLOCKS_SOURCES.md)
states exactly which owner and book claims were checked.

AuthorityEffect: None. Blank optional worksheet; zero measured durations
or beginner learning scores.
