# Task Logic Audit: Weather Prediction Task

## 1. Paradigm Intent

- Task: `weather_prediction`.
- Construct: probabilistic multi-cue category learning.
- Manipulated trial factors:
- cue pattern (`pattern_id` with 4-card on/off vector)
- stochastic outcome sampled from pattern-specific `P(sun)`.
- Primary dependent measures:
- prediction accuracy
- decision RT
- timeout count
- `sun` prediction tendency
- cumulative score.

## 2. Block/Trial Workflow

### Block Structure

- Human profile: `2` blocks x `60` trials.
- QA/sim profiles: `1` block x `20` trials.
- Block initialization: `Controller.start_block(block_idx)` resets block counter.
- Trial specification:
- cue pattern sampled by `Controller.draw_pattern()`.
- actual weather sampled by `Controller.sample_weather(pattern)`.

### Trial State Machine

1. `fixation`
- Stimulus: `fixation`.
- Trigger: `fixation_onset`.
- Keys: none.

2. `cue`
- Stimuli: `cue_title`, `score_text`, 4 rebuilt `cue_card_template` items, `cue_hint`.
- Trigger: `cue_onset`.
- Keys: none.

3. `decision`
- Stimuli: `score_text`, 4 rebuilt `cue_card_template` items, `decision_prompt`, `key_hint`.
- Trigger: `decision_onset`.
- Response triggers: `choice_sun` / `choice_rain`.
- Timeout trigger: `choice_timeout`.

4. `feedback`
- Stimulus branch: `feedback_correct`, `feedback_incorrect`, `feedback_timeout`.
- Trigger branch: `feedback_correct`, `feedback_incorrect`, `feedback_timeout`.
- Keys: none.

5. `inter_trial_interval`
- Stimulus: `fixation`.
- Trigger: `iti_onset`.
- Keys: none.

## 3. Condition Semantics

- Runtime condition ID: `probabilistic_classification`.
- Trial-level semantic factors:
- `pattern_id` and `pattern_cards` encode cue-combination identity.
- `sun_probability` is the pattern-conditioned weather likelihood.
- `actual_weather` is stochastically sampled per trial (`sun` or `rain`).

## 4. Response and Scoring Rules

- Valid decision keys: `sun_key` and `rain_key` (default `f`/`j`).
- Response mapping:
- `sun_key -> sun`
- `rain_key -> rain`
- Timeout sets `is_correct = null` and applies `timeout_delta`.
- Score policy:
- correct: `+1`
- incorrect: `-1`
- timeout: `0`
- QA-required outputs include `condition`, `trial_id`, `pattern_id`, `actual_weather`, `decision_response`, `decision_rt`, `is_correct`, `score_after`.

## 5. Stimulus Layout Plan

- Cue/decision screens:
- title and score in top region (`y=305`, `y=255`).
- four cue cards in horizontal row (`x=-390,-130,130,390`, `y=70`).
- instructional prompt near bottom (`y=-210` to `y=-295`).

- Cue cards:
- active cards use highlight color; inactive cards use muted color.
- each card shows config-driven card label and state label.

All participant-facing text is sourced from config (`stimuli.*`, `task.weather_labels`, `task.card_labels`, `task.card_state_labels`).

## 6. Trigger Plan

| Trigger | Code | Meaning |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `fixation_onset` | 20 | fixation onset |
| `cue_onset` | 30 | cue onset |
| `decision_onset` | 40 | decision onset |
| `choice_sun` | 41 | `sun` response |
| `choice_rain` | 42 | `rain` response |
| `choice_timeout` | 43 | no response before deadline |
| `feedback_correct` | 50 | correct feedback onset |
| `feedback_incorrect` | 51 | incorrect feedback onset |
| `feedback_timeout` | 52 | timeout feedback onset |
| `iti_onset` | 60 | ITI onset |

## 7. Architecture Decisions (Auditability)

- `main.py` uses one standardized execution path for `human|qa|sim` with shared initialization order and runtime context handling.
- `src/run_trial.py` is fully weather-task specific and removes MID leftovers (`anticipation`, generic `target`, `hit/miss` template logic).
- Decision response triggers are emitted after response-key mapping (`choice_sun`/`choice_rain`) while timeout remains capture-policy driven.
- Runtime trial context includes `pattern_id`, `cards`, and `sun_probability`, enabling responder simulation and downstream audit reproducibility.

## 8. Inference Log

- Exact fixation/ITI jitter values are implementation-level inferences constrained by the cited probabilistic-learning workflow, not explicit values mandated by the papers.
- Weighted pattern sampling is implemented as equal weights by default; this is an inference to keep sampling balanced while preserving pattern-conditioned probabilities.
- Card/state display formatting (single text-template cards with color highlighting) is an implementation inference that preserves required cue-visibility semantics.