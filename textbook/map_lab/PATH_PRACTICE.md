# Path practice: a different recorder

Try these before the [separate answers](PATH_ANSWERS.md). Explain each
answer in your own words; a correct guess is not the whole task.

Supply a three-state dial with states A, B, C. The event next follows
A → B → C → A; stay keeps the current state. This is a new model, not
a measured device or a consequence of the switch table.

1. Start at B. Replay next, stay, next. Give every intermediate state.
   Compare its history with next, next from B: what agrees and differs?
2. Encode A/B/C as empty live passage states with budgets 2/5/8.
   What budget writes translate next, stay, next from B? Explain why
   repeating the first translated write would fail.
3. Are those three state codes injective? Does the passage's specified
   native observation recover the dial state? Name a blocking pair.
4. Change the target observation to read budget. Give a decoding rule on
   the three used values. Must that rule have a uniquely determined answer
   on unused value 3? What changes in the earlier obstruction's premises?
5. The source instead reports only “is this an allowed dial state?”
   Explain how a constant observation map can now be faithful on the
   source's actual observation values. Why did the same trick fail for
   the source-state question?
6. A log has two rows. The first correctly records initial passage state
   → admit occurrence 0 → state with occurrence [0]. The second correctly
   records initial passage state → halt → halted empty state. Are these
   consecutive actual steps? Repair the log by changing only the second
   row's before- and after-states, keeping its event label halt.

Transfer: a claimed translation passes every step square and has distinct
state codes. Someone concludes “it preserves every fact we can observe.”
Specify the missing observation requirements and give the switch or dial
as a counterexample. Then describe a change that would make the particular
state question recoverable. Do not infer a physical law from either model.

AuthorityEffect: None. These are supplied changed-label/three-state tasks.
They measure learning only if an actual reader attempts them and a response
is recorded; no such outcome is asserted here.
