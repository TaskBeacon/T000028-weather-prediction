# Task Logic Audit: Weather Prediction Task

## 1. Paradigm Intent

- Task: `weather_prediction`
- Primary construct: probabilistic category learning from multiple visual cues.
- Manipulated factors:
  - cue-card combination pattern (4-card display, subset active per trial)
  - probabilistic weather outcome conditional on cue pattern (`P(sun | pattern)`)
- Dependent measures:
  - prediction accuracy (responded trials)
  - timeout count
  - response latency
  - prediction tendency (`sun` response rate)
  - cumulative score trajectory
- Key citations:
  - `W1998736700`
  - `W2042354961`
  - `W2110781393`
  - `W2076805718`
  - `W2136211925`

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: `2` (human baseline), `1` (QA/sim profiles).
- Trials per block: `60` (human baseline), `20` (QA/sim profiles).
- Randomization/counterbalancing:
  - each trial samples one cue pattern from a 14-pattern library
  - sampled pattern determines Bernoulli weather outcome using configured `sun_probability`

### Trial State Machine

1. `fixation`
   - Onset trigger: `fixation_onset`
   - Stimuli shown: central fixation cross.
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after jittered fixation duration.
   - Next state: `cue`.

2. `cue`
   - Onset trigger: `cue_onset`
   - Stimuli shown together:
     - cue title and current score text
     - four card slots with active/inactive status labels
     - cue hint text
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after fixed cue exposure.
   - Next state: `decision`.

3. `decision`
   - Onset trigger: `decision_onset`
   - Stimuli shown together:
     - same four cue cards
     - decision prompt
     - key hint (`F=晴天`, `J=雨天`)
   - Valid keys: `[sun_key, rain_key]`.
   - Response triggers:
     - `choice_sun`
     - `choice_rain`
   - Timeout trigger: `choice_timeout`
   - Timeout behavior: no prediction response recorded; trial continues to feedback.
   - Next state: `feedback`.

4. `feedback`
   - Onset trigger (outcome-dependent):
     - `feedback_correct`, or
     - `feedback_incorrect`, or
     - `feedback_timeout`
   - Stimuli shown:
     - correctness feedback with predicted vs actual weather and score update, or
     - timeout feedback with actual weather and current score.
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after feedback duration.
   - Next state: `iti`.

5. `iti`
   - Onset trigger: `iti_onset`
   - Stimuli shown: fixation cross.
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after jittered ITI.
   - Next state: next trial.

## 3. Condition Semantics

- Condition ID: `probabilistic_classification`
  - Participant-facing meaning: use the currently visible cue-card combination to predict weather.
  - Concrete stimulus realization:
    - four horizontally aligned cue cards (`卡片1`-`卡片4`)
    - active cards highlighted with gold fill and status `出现`
    - inactive cards dimmed with status `未出现`
  - Outcome rules:
    - each cue pattern has configured `sun_probability`
    - actual weather sampled stochastically each trial (`sun` or `rain`)
    - response scored against sampled weather outcome

## 4. Response and Scoring Rules

- Response mapping:
  - `F -> 晴天`
  - `J -> 雨天`
- Missing-response policy:
  - if no decision response before deadline, emit `choice_timeout`
  - timeout trial score change uses `timeout_delta` (configured `0`)
- Correctness logic:
  - `is_correct = (predicted_weather == actual_weather)` when response exists
- Reward/penalty updates:
  - correct prediction: `+1`
  - incorrect prediction: `-1`
  - timeout: `0`
- Running metrics:
  - block/session accuracy, timeout count, mean decision RT, sun prediction rate, cumulative score

## 5. Stimulus Layout Plan

- Cue/decision multi-stimulus layout:
  - `cue_title`: top center (`0, 305`)
  - `score_text`: upper center (`0, 255`)
  - 4 cue cards: horizontal row at `x = [-390, -130, 130, 390], y = 20`
  - card state labels (`出现/未出现`): lower inside each card
  - cue and decision prompts: lower middle (`y=-210` to `y=-295`)
- Visual hierarchy:
  - score/context first, cue cards as primary perceptual objects, response hint near bottom.
- Readability constraints:
  - participant-facing text uses `font: SimHei`
  - wrap widths and spacing prevent overlap at `1280x720`

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `fixation_onset` | 20 | fixation onset |
| `cue_onset` | 30 | cue display onset |
| `decision_onset` | 40 | decision screen onset |
| `choice_sun` | 41 | `sun` key response |
| `choice_rain` | 42 | `rain` key response |
| `choice_timeout` | 43 | no response before deadline |
| `feedback_correct` | 50 | correct feedback onset |
| `feedback_incorrect` | 51 | incorrect feedback onset |
| `feedback_timeout` | 52 | timeout feedback onset |
| `iti_onset` | 60 | ITI onset |

## 7. Inference Log

- Decision: use a single runtime condition (`probabilistic_classification`) and encode cue variation at trial level via explicit pattern factors.
- Why inference was required: weather prediction paradigms manipulate cue combinations within one task stream rather than as separate block conditions.
- Citation-supported rationale: selected papers analyze strategy/learning as functions of cue combinations and probabilistic outcomes.

- Decision: represent 14 cue patterns with configurable `sun_probability` values and equal sampling weights.
- Why inference was required: publications often describe cue-probability structure conceptually and vary in exact pattern frequencies across implementations.
- Citation-supported rationale: this preserves core probabilistic-category-learning mechanics while keeping phase/trigger behavior explicit and reproducible.
