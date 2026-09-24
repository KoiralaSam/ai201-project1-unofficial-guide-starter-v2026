# The Unofficial Guide

Samarpan Koirala — corpus: `campus_life`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This is a search system over the `campus_life` corpus: about 88 short student posts on how things actually work on campus, not the official handbook. You ask a plain question and get an answer drawn only from those posts, with the source file named. It is built for factual “when / how does this work” questions — add/drop without a W, when to declare a major, how long interlibrary books take, when west-lot permits sell out, when study-abroad applications open — not opinions like “what’s the best dining hall.” If nothing in the posts is close enough to the question, it says it doesn’t have enough information instead of guessing.

## Chunking Strategy

**Chunk size:** 550 characters (the longest file in `campus_life/documents`)
**Overlap:** 0

`campus_life` posts average about 317 characters; the longest is 550 and the shortest is 178. The starter’s 800-character window never split anything (88 documents became 88 chunks). I first thought about shrinking the window, then dropped that: a 200–400 cut would slice a one-sentence fact in half. These posts are already one thought, so `split_documents` keeps each file as one chunk and does not slide a window. Overlap is 0 because there is no neighbouring piece to share text with. `config.py` records the same numbers so `fallback_split` would use them if I compared against it; the live path is `chunker.py::split_documents`.

## Sample Chunks

Printed with `python app.py chunks -n 5`. All five produced by `chunker.py::split_documents`.

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

**Question:** When do you declare your major?

**Answer:**

```
  (best distance 0.283, cutoff 0.5)

You declare your major at the end of your second semester, or later if you need to (admin_declaring_a_major.txt).

Sources retrieved: admin_declaring_a_major.txt, admin_graduation_requirements.txt, admin_pass_fail_option.txt
```

An off-topic question (`What is the capital of Mongolia?`) hits best distance 0.825 and the gate returns: I don't have enough information about that.

**My relevance cutoff:** 0.50 (`THRESHOLD` in `config.py`)

In-corpus best distances sat between 0.23 and 0.36. Out-of-scope best distances sat between 0.82 and 0.93. The gap is about 0.36 to 0.82. I put the cutoff at 0.50, in that gap: low enough to refuse Mongolia / diesel / World Cup, high enough that the interlibrary question (0.36) still passes. 0.30 would have been too tight; 0.80 would have been too loose.

| Question                                                            | In corpus? | Best distance |
| ------------------------------------------------------------------- | ---------- | ------------- |
| When is the last day to drop your course without getting a 'W'?     | yes        | 0.2782        |
| When do you declare your major?                                     | yes        | 0.2826        |
| When does the book arrive when ordered through interlibrary system? | yes        | 0.3623        |
| When do student permits on west lots usually sell out?              | yes        | 0.2332        |
| When do the study abroad applications open up?                      | yes        | 0.2347        |
| What is the capital of Mongolia?                                    | no         | 0.8246        |
| How do I change the oil in a diesel engine?                         | no         | 0.9340        |
| Who won the 1994 World Cup?                                         | no         | 0.8859        |
| What is the recommended dosage of ibuprofen for a headache?         | no         | 0.8442        |
| How do I write a for loop in Rust?                                  | no         | 0.8960        |

## How I Used AI

**1.** I asked why `split_documents` and `fallback_split` were the same if I only changed `CHUNK_SIZE` in `config.py`, and whether a chunk size just above the longest file was about keeping a complete thought. It said yes: `campus_life` is already one thought per file, so a window smaller than the post would cut a sentence, and a character check inside `split_documents` would not change any chunk. I had already written `max_corpus_characters()` (longest file 550) and set overlap to 0. I used that explanation to keep one post as one chunk instead of shrinking the starter window.

**2.** I asked what Milestone 2 wanted for the extra criteria and whether criterion 5 had to be about chunk size. It said one of the two I write has to be about chunks, with a number someone else could check. I wrote criterion 4 myself (retrieval under 10 seconds) and criterion 5 as 4 of 5 sampled chunks standing alone. For the cutoff I asked how to use the five in-corpus and five out-of-scope questions. It said put `THRESHOLD` in the gap. I ran those ten questions, got 0.23–0.36 vs 0.82–0.93, and set 0.50 myself instead of leaving the starter at 0.60.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion                              | Target | Run 1 | Run 2 | Run 3 | Verdict |
| -------------------------------------- | ------ | ----- | ----- | ----- | ------- |
| 1. Retrieved chunk contains the answer | 4 of 5 |       |       |       |         |
| 2. Every answer names a source         | 5 of 5 |       |       |       |         |
| 3. Gate stops out-of-corpus questions  | 4 of 5 |       |       |       |         |
| 4.                                     |        |       |       |       |         |
| 5.                                     |        |       |       |       |         |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| #   | Criterion | Verdict | How I decided |
| --- | --------- | ------- | ------------- |
| 1   |           |         |               |
| 2   |           |         |               |
| 3   |           |         |               |
| 4   |           |         |               |
| 5   |           |         |               |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion                              | Target | Run 1 | Run 2 | Run 3 | Verdict |
| -------------------------------------- | ------ | ----- | ----- | ----- | ------- |
| 1. Retrieved chunk contains the answer | 4 of 5 |       |       |       |         |
| 2. Every answer names a source         | 5 of 5 |       |       |       |         |
| 3. Gate stops out-of-corpus questions  | 4 of 5 |       |       |       |         |
| 4.                                     |        |       |       |       |         |
| 5.                                     |        |       |       |       |         |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
