"""
Your test questions.

Milestone 2 asks you to write five questions your system should be able to
answer from your corpus, specific enough to have a right answer.

  ✗ "What are good dining halls?"          — no right answer
  ✓ "What do students say about wait times at Commons during lunch?"

Fill in `QUESTIONS` below. `expects` is a word or short phrase you'd expect a
correct answer to contain — you'll use it in unit 2 when you build a scorer,
and having written it now means you decided what "correct" meant before you saw
any results.

`OUT_OF_SCOPE` holds five questions your documents clearly don't cover. You
need these in Milestone 4 to find where your relevance cutoff belongs, and
again in unit 2, where `run_eval.py` runs them through the gate and writes what
happened into your run log — that's the evidence for criterion 3.

Swap them for your own if you like. Keep five of them either way: criterion 3
names a target of "4 of 5", and four of three is not a thing.
"""

QUESTIONS = [
    # {"question": "...", "expects": "..."},
    {"question": "When is the last day to drop your course without getting a 'W'?", "expects": "week two"},
    {"question": "When do you declare your major?", "expects": "semester two"},
    {"question": "When does the book arrive when ordered through interlibrary system?", "expects": "week"},
    {"question": "When do student permits on west lots usually sell out?", "expects": "three days"},
    {"question": "When do the study abroad applications open up?", "expects": "october"},
]

# Questions from a different world entirely. Your gate should refuse all five.
#
# There are five of these because criterion 3 in criteria.md names a target of
# "at least 4 of 5" — you need five things to try before you can report 4 of 5.
# `run_eval.py` runs these through retrieval and the gate on every eval and
# records what happened, so criterion 3 has evidence in the run log alongside
# the others. They cost no model calls: a refusal never reaches the model.
OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]


def print_distance_groups() -> None:
    """Print best distance for five in-corpus questions and five that are not.

    Milestone 4: the cutoff in config.THRESHOLD goes in the gap between
    these two groups. Retrieval only — no model call.
    """
    from store import search

    print(f"{'Question':<72} {'In corpus?':<12} Best distance")
    print("-" * 100)
    for item in answered():
        results = search(item["question"])
        best = results[0].distance if results else 1.0
        print(f"{item['question']:<72} {'yes':<12} {best:.4f}")
    for question in OUT_OF_SCOPE:
        results = search(question)
        best = results[0].distance if results else 1.0
        print(f"{question:<72} {'no':<12} {best:.4f}")


if __name__ == "__main__":
    print_distance_groups()
