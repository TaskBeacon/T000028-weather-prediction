# Weather Prediction Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Weather Prediction Task |
| Version | v0.2.0-dev |
| URL / Repository | https://github.com/TaskBeacon/T000028-weather-prediction |
| Short Description | Probabilistic category learning task using multi-cue card combinations to predict weather outcomes. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-19 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (voice disabled by default) |

## 1. Task Overview

This implementation follows the Weather Prediction paradigm as a probabilistic multiple-cue classification task. Each trial presents a combination of four cue cards, and participants predict whether the weather will be `sun` or `rain`.

Outcome feedback is probabilistic and contingent on the sampled cue pattern (`P(sun | pattern)`), supporting gradual strategy learning instead of deterministic rule execution.

## 2. Task Flow

![Task Flow](task_flow.png)

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Block init | Controller resets block trial counter and keeps cumulative score continuity. |
| 2. Trial loop | `run_trial(...)` executes fixation, cue exposure, decision, feedback, and ITI. |
| 3. Block summary | Show block accuracy, timeout count, mean RT, prediction tendency, and score. |
| 4. Final summary | Show session-level performance and final cumulative score. |

### Trial-Level Flow

| Step | Description |
|---|---|
| `fixation` | Jittered fixation baseline. |
| `cue` | Show 4-card cue pattern with active/inactive card states. |
| `decision` | Collect weather prediction (`F=晴天`, `J=雨天`) under deadline. |
| `feedback` | Show correct/incorrect/timeout feedback with actual weather and score update. |
| `iti` | Jittered inter-trial fixation before next trial. |

### Controller Logic

| Component | Description |
|---|---|
| Cue pattern library | 14 cue-card patterns, each with explicit `sun_probability`. |
| Outcome sampling | Bernoulli weather outcome sampled from pattern-specific `P(sun)`. |
| Score update | Correct `+1`, incorrect `-1`, timeout `0`. |
| Metrics | Tracks trial history, cumulative score, and block/session summaries. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `fixation` | Pre-trial baseline. |
| `cue` | Non-response cue observation stage. |
| `decision` | Active weather prediction response window. |
| `feedback` | Outcome feedback stage. |
| `iti` | Inter-trial transition stage. |

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | 3-digit participant identifier. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `[0.07, 0.10, 0.14]` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Stimulus Group | Description |
|---|---|
| `cue_title`, `cue_hint`, runtime cue-card rectangles/text | Trial-wise visual cue-combination display. |
| `decision_prompt`, `key_hint` | Binary weather prediction prompt and key mapping. |
| `feedback_correct`, `feedback_incorrect`, `feedback_timeout` | Outcome-specific feedback with score update. |
| `instruction_text`, `block_break`, `good_bye`, `score_text`, `fixation` | Envelope and progress stimuli. |

### d. Timing

| Stage | Duration |
|---|---|
| fixation | jittered (`[0.3, 0.6] s`) |
| cue | fixed (`0.8 s`) |
| decision | deadline (`2.5 s`) |
| feedback | fixed (`1.0 s`) |
| iti | jittered (`[0.3, 0.6] s`) |

### e. Triggers

| Trigger | Code |
|---|---:|
| `exp_onset` | 1 |
| `exp_end` | 2 |
| `block_onset` | 10 |
| `block_end` | 11 |
| `fixation_onset` | 20 |
| `cue_onset` | 30 |
| `decision_onset` | 40 |
| `choice_sun` | 41 |
| `choice_rain` | 42 |
| `choice_timeout` | 43 |
| `feedback_correct` | 50 |
| `feedback_incorrect` | 51 |
| `feedback_timeout` | 52 |
| `iti_onset` | 60 |

### f. Adaptive Controller

| Parameter Group | Description |
|---|---|
| `patterns` | 14-card-pattern probability table (`pattern_id`, `cards`, `sun_probability`, `weight`). |
| `score deltas` | `correct_delta`, `incorrect_delta`, `timeout_delta`. |
| `random_seed` | Reproducible probabilistic sampling in QA/sim when set. |

## 4. Methods (for academic publication)

Participants performed a probabilistic weather prediction task in which each trial displayed a subset of four cue cards and required binary weather classification (`sun` vs `rain`). Trial outcomes were sampled probabilistically based on cue-pattern-specific weather likelihoods, and immediate feedback was provided to support gradual learning.

Primary behavioral endpoints include response accuracy, timeout rate, decision latency, prediction tendency, and cumulative score trajectory. The implementation emits trigger-aligned phase events (`fixation`, `cue`, `decision`, `feedback`, `iti`) for reproducible behavioral and synchronized acquisition workflows.
