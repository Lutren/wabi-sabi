# 13‑Layer Editorial System

**Quality‑control framework for long fiction.**

Developed and tested in the MEDIOEVO saga (~70,000 words per book).

## Principle

Editorial revision has two enemies: the wrong order and the lack of metrics.  Fixing voice before fixing structure doubles your work; editing without counting tics produces intuition, not control.  This system solves both problems: **a fixed order of execution plus quantifiable deliverables per layer**.

## Meta‑rule

```
IF THE SCENE WORKS, THE RULE LOSES.
Verify canon afterwards, do not paralyse before.
BUT: “Works” requires technical justification, not “I liked it”.
```

## Estimated time

Each layer usually takes 2–3 hours per ~70,000 words.

## Layers

### Layer 1: Technical clean‑up

**Goal:** Remove noise that distorts later diagnoses.

Tasks:

- Fix hyphens/en‑dashes, mojibake and Pandoc artefacts.
- Normalise titles and headers for table of contents.
- Remove visible editorial placeholders (`[FILL]`, `[SEE NOTE]`).
- Fix mechanical typos: double spaces, repeated punctuation, curly quotes.

**Deliverable:** Clean text without technical noise, with a diff of changes.

### Layer 2: Code saturation (motifs and tics)

**Goal:** Detect and reduce mechanical repetition that the eye no longer sees.

Count repeated motifs using simple tools like `grep`.  Recommended maximums per ~70k words (adjust proportionally to length):

| Element                          | Suggested maximum |
|----------------------------------|------------------|
| Unique recurring number/symbol   | 5 per book       |
| Second recurring symbol          | 20 per book      |
| Sensory synaesthesia (e.g. “hum”)| 20 per book      |
| Central character’s name         | 60 per book      |
| “something that” (vague)         | 70 per book      |
| “as if” + abstract concept       | 15 per book      |
| “the type of” (decorative)       | 10 per book      |
| “It wasn't X. It was Y.”         | 10 per book      |
| Decorative “silence”             | 30 per book      |

**Deliverable:** Counts before/after for each intervened motif.

### Layer 3: Anti‑insistence

**Goal:** Cut phrases that explain what the scene already shows.

Examples to remove:

- “It was evident that …”
- “She had no choice.”
- “The weight of what had just happened …”

Exception: cold data from an analytic character (e.g. “Third time in twelve days”) which is characterisation, not insistence.

**Deliverable:** List of cuts with ≤20‑word quote and justification.

### Layer 4: Protagonist’s motor

**Goal:** Ensure the protagonist acts from desire rather than simply reacts.

Per chapter, ask: **Does the protagonist DO something or merely RECEIVE events?**

Identify chapters where they are 100% reactive and insert at least one active decision per chapter.  Each decision must cost something irreversible (a relationship, information, a possibility).

**Deliverable:** Map of active vs reactive decisions per chapter.

### Layer 5: Exposition → scene

**Goal:** Turn informational blocks into dramatic experience.

Signs of trouble:

- Paragraphs listing world data
- Dialogues that sound like lectures
- Blocks where the narrator explains the system instead of showing its effect

**Conversion technique:** (1) Show a concrete human effect first; (2) Provide partial explanation afterwards (only what the character needs to know); (3) Let the reader reconstruct the system – do not dump it fully.

**Deliverable:** Before/after of each converted block.

### Layer 6: Anti‑inventory + anti‑baroque

**Goal:** Each detail justified, not accumulated.

Rules:

- Maximum two details per paragraph; a third only if it contradicts or surprises.
- POV filter: Would this character notice this detail at this moment?  If not, cut it.
- Condense descriptions of four or more lines down to two.
- Remove documentary camera‑style description (inventory without perspective).

**Deliverable:** List of intervened blocks.

### Layer 7: Idiolect + structure

**Goal:** Each character should sound different; structure should serve meaning.

For each character, identify 2–3 unique speech patterns (vocabulary, sentence length, what they avoid saying) and verify that in long dialogues the voices are distinguishable without tags.  Check paratextual spoilers (glossaries, epigraphs), weak closing scenes and include at least one short circuit per secondary character per book (a non‑utilitarian gesture that reveals without explaining).

**Deliverable:** Voice guide per character and list of structural fixes.

### Layer 8: Anti‑analogy + anti‑teleology

**Goal:** Remove two common crutches of genre prose.

**Anti‑analogy:**

- Remove “as if” + abstract or philosophical concept.
- Keep “as if” + concrete physical image.
- Replace always with direct physical description.

**Anti‑teleology:**

- Remove: “He didn’t know it would be the last time …”
- Remove: “He would soon understand that …”
- Remove any phrase that reveals the narrator knows the future.

**Deliverable:** Before/after for each instance.

### Layer 9: Chapter endings + anti‑solemnity

**Goal:** Chapters should end in action, image or silence – not summary.

Check that no chapter ends with the protagonist reflecting on what just happened.  If there are three or more pages of consecutive solemnity with no relief, insert humour, absurdity or the mundane interrupting the serious.

Types of humour that do not break the tone:

1. Bureaucracy with perfect logic → ridiculous result
2. The mundane interrupting the grave (someone is hungry during a cosmic revelation)
3. A character doing something absurd without knowing it is funny

**Deliverable:** List of corrected chapter endings and inserted relief moments.

### Layer 10: Encyclopaedic blocks

**Goal:** Condense what remains of exposition after Layer 5.

- For inventories of stations/locations/systems: cut to a minimal functional description.
- Verify that every world rule shown has a consequence also shown.
- Remove enumerations of future events with proper names (“In year X, Y would do Z”).

**Deliverable:** Condensed blocks with word counts before/after.

### Layer 11: Emotions + reconciliations

**Goal:** Motives should be a mixture, not pure; emotional closures should cost something.

- Remove clean reconciliations (conflict should leave a mark).
- Check that no hug or reunion functions as a reward without cost.
- Cut decorative “the type of” phrases.
- Cut vague “something that” phrases.
- Ensure no emotion is named if it has already been shown physically.

**Deliverable:** Metrics of intervened tics and list of emotional corrections.

### Layer 12: Final clean‑up

**Goal:** Diagnose length and global coherence.

- Remove residual mechanical repetition such as decorative “It wasn’t X. It was Y.”
- Replace weak verbs in expository blocks (to be/to have) with action.
- Check entropy versus purpose: Does each scene change something irreversibly?
- Final word count per chapter; verify that length reflects tension.

**Deliverable:** Final metrics and length diagnosis per chapter.

### Layer 13: Production

**Goal:** Complete publication package.

- Generate EPUB (metadata, CSS, table of contents).
- Generate PDF Paperback (6×9″, KDP margins).
- Generate PDF Hardcover (6.14×9.21″).
- Generate DOCX for editors.
- Marketing: short/long synopsis, keywords, BISAC codes, cover prompts.

**Deliverable:** Complete package ready to upload to KDP.

## Execution order

```
Layers 1–3:   Mechanical (quick; can be done in a single session)
Layers 4–6:   Structural (require author decisions)
Layers 7–8:   Voice and style (more time per layer)
Layers 9–11:  Fine tone and emotion
Layer 12:     Final diagnosis
Layer 13:     Production
```

## Unified checklist

```
L1:  [ ] Clean encoding  [ ] Normalised headers  [ ] No placeholders
L2:  [ ] Tics counted  [ ] Thresholds respected  [ ] Counts before/after
L3:  [ ] No post‑scene explanations  [ ] No “It was evident”
L4:  [ ] Active protagonist  [ ] Decisions have a cost
L5:  [ ] No pure info dumps  [ ] Human effect first
L6:  [ ] ≤2 details/paragraph  [ ] POV filter applied
L7:  [ ] Distinguishable voices  [ ] Short circuit per secondary
L8:  [ ] No abstract “as if”  [ ] No teleology
L9:  [ ] Ends with action/image/silence  [ ] Humour inserted when needed
L10: [ ] No inventories  [ ] Each rule has a consequence
L11: [ ] Mixed motives  [ ] No clean reconciliations
L12: [ ] Calibrated length  [ ] Entropy checked
L13: [ ] EPUB  [ ] PDF Paperback  [ ] PDF Hardcover  [ ] Marketing
```

## Threshold notes

The thresholds in Layer 2 are suggestions calibrated for books of about 70,000 words.  They scale linearly.  For a 35,000‑word book, divide the numbers by two.  The exact number is less important than the habit of **counting before editing**.

*Developed in production — not in theory.  Tested in MEDIOEVO Books I, II and III.  MIT licensed.*