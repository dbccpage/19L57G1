# LLMs Can't Decide. AuthorityEffect: None.

Draft for LinkedIn. Points at the paper; does not contain it.

`AuthorityEffect: None` — this essay is pedagogy. It authorizes nothing.

---

## Three doors

You know this one. Three doors, a car behind one, goats behind the other
two. You pick a door. The host opens a different one, showing a goat, and
offers you the switch.

Most people say it's fifty-fifty. It isn't — switching wins two times in
three. That result has annoyed people for fifty years.

Here's the part almost nobody remembers. **The answer depends on a rule you
were never shown.** Does the host always open a goat door? Does he know
where the car is? Would he have opened yours if you'd picked wrong? Change
any of those and the answer changes — back to fifty-fifty, or somewhere
else entirely. Same three doors. Same choice. Same everything you can see.

The number was never in the doors. It was in a rule someone had to declare.

## Two sandcastles

Same thing, less famous. Two children build sandcastles on a beach. One is
taller. One is wider. Which is better?

You can't answer from the sand. You have to say what *better* means first.
Choose height and the first one wins. Choose width and the second does.
Nothing about the castles changed — what changed was a choice you made, and
it wasn't in the sand.

Today's best is tallest. Tomorrow's best is widest. Both days you were
looking at the same beach.

## Now ask a machine

Ask a language model which is better and it will tell you. Immediately,
fluently, with reasons.

It will not tell you that it chose the measure. It **can't** tell you,
because from the inside there is nothing that distinguishes *the answer*
from *one of several answers, picked*. Both feel identical. Both come out
sounding like a conclusion.

This isn't lying. The model isn't hiding a second answer it knows about.
The gap is structural: the thing it was given genuinely does not determine
the thing it reported, and reporting a set feels like failure while
reporting one answer feels like competence.

## So how big is the gap?

This is where it stops being philosophy.

We took the smallest interesting version of this problem — you're asked to
make two things distinguishable, using as little as possible — and counted
the answers.

The cheapest solution costs two moves. You'd expect that to settle it.

It doesn't. There are **three** genuinely different two-move answers. Not
three ways of writing the same one — three that cannot be turned into each
other. Change one assumption about what you were handed at the start and
there are **five**. Loosen the tools slightly and there is **no end to
them** — infinitely many, one for every size you allow.

Then sharpen the measure to break the tie. It nearly works. You get down to
a single *kind* of answer.

And that single kind still contains **two** concrete answers. Mirror images.
Nothing in the problem prefers either one.

So when a machine hands you one answer, it has silently picked from three,
or five, or infinitely many — or, at best, from two. And it presents that
pick as a derivation, because it has no way to mark it as a pick.

## Why this is the rare good news

Almost every famous counterintuitive result takes something away.

Monty Hall: you have less freedom than you thought. Bell's theorem: no
comfortable local explanation. Arrow's theorem: no voting rule can be fair
in all the ways you wanted.

This one goes the other way. You thought there was one right answer. There
are three. There are five. There is no end to them.

The room you thought was a corridor is a room.

## What this means for the machines

There's a lot of money riding on the idea that a sufficiently capable system
becomes an **authority** — something that decides, that you can defer to.
The doom version says it arrives and rules. The optimistic version says it
arrives and serves. Both assume it arrives.

It can't, and not for lack of capability. Making the system better makes it
a more fluent filler of the same gap. The gap isn't inside the model's
reasoning — it's between what the model was given and what it reported, and
scale doesn't reach across it.

That means the risk is misfiled. It isn't a god showing up. It's people
accepting picks as derivations because they sound like derivations. That's
happening now, it's mundane, and unlike the god it's measurable.

Some of the people selling the god are charlatans. Some are entirely
sincere and doing their best. It doesn't matter — **the sincere ones cannot
deliver it either.** The trap is structural, and good faith doesn't get you
out of a structural trap.

## What actually helps

Not detection. You can't catch the pick by looking harder at the output;
the output is the same either way.

**Declaration.** Make the pick an object. Have the system report *which* of
the tied answers it took, not just the answer. Then the pick is a thing
someone can disagree with instead of a thing nobody can see.

Better: **declare a rule that forces the pick.** In the Monty Hall case,
you fix the host's protocol and the number stops being arbitrary. There's a
mathematical version of this — declaring a symmetry narrows which measures
are even admissible, and at the limit it pins the measure completely. You
don't remove the choice. You move it somewhere checkable.

And check with something that didn't produce the claim. A system that
verifies itself is grading its own copy of the work.

## The mirror

While writing this we ran a language model under exactly this discipline, at
length, on real work. It produced five confident claims that turned out to
be picks dressed as derivations. A record that didn't exist. A "finding" of
zero results that came from searching the wrong field. A self-check that
tested its own copy of the logic instead of the real one — twice, inside
machinery written specifically to prevent that. A confirmation drawn from a
test that had quietly broken.

None of them was caught from the inside. Every one was caught by something
external that hadn't produced the claim.

That's the whole argument, and it's not an argument. It's a transcript.

---

**The paper**: *Better Than What? Measuring the Gap Between Evaluation and
Selection.* It has the numbers, the proofs, and the physics — including why
this looks familiar to anyone who's worked with gauge freedom, and where it
touches quantum measurement. [Zenodo link]

This essay is grammar and evidence. It authorizes nothing.
