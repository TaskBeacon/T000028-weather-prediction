# Weather Prediction Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Weather Prediction Task |
| Version | v0.1.1-dev |
| URL / Repository | https://github.com/TaskBeacon/T000028-weather-prediction |
| Short Description | Probabilistic category learning with cue-combination weather outcomes. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-19 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (voice disabled by default) |

## 1. Task Overview

This task implements a Weather Prediction paradigm with probabilistic category outcomes across `sun`, `rain`, and `snow` conditions. Participants respond during the target interval and receive outcome feedback.

The design supports condition-resolved performance analysis under uncertainty and includes trigger-tagged trial stages for reproducible behavioral or synchronized acquisition runs.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Initialize block | Condition schedule is loaded into `BlockUnit`. |
| 2. Execute trials | `run_trial(...)` handles cue, anticipation, target, and feedback. |
| 3. Block report | Block accuracy and score summary are shown. |
| 4. Task completion | Final total score is displayed. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Cue | Weather cue corresponding to current condition is shown. |
| Anticipation | Fixation interval before target. |
| Target | Condition target appears with response capture. |
| Pre-feedback fixation | Brief interstitial fixation stage. |
| Feedback | Hit/miss feedback and score delta are presented. |

### Controller Logic

| Component | Description |
|---|---|
| Adaptive duration | Controller updates target duration toward configured accuracy target. |
| Condition history | Trial outcomes are stored per condition. |
| Trial scoring | Hit/miss state determines trial delta for cumulative score. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `anticipation` | Pre-target response-monitoring interval. |
| `target` | Main target response window. |

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
| `bg_color` | `gray` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `sun_cue`, `rain_cue`, `snow_cue` | text | Condition-specific cue prompts. |
| `sun_target`, `rain_target`, `snow_target` | text | Condition targets for response capture. |
| `*_hit_feedback`, `*_miss_feedback` | text | Condition-specific feedback screens. |
| `fixation`, `block_break`, `good_bye` | text | Shared fixation and summary displays. |

### d. Timing

| Phase | Duration |
|---|---|
| cue | 0.5 s |
| anticipation | 1.0 s |
| prefeedback | 0.4 s |
| feedback | 0.8 s |
| target | adaptive via controller (`0.08`-`0.40` s bounds) |

## 4. Methods (for academic publication)

Participants completed a probabilistic category-learning task with weather-labeled condition streams. Each trial included cueing, anticipation, target response capture, and immediate feedback, allowing quantification of learning performance by condition.

Adaptive response-window control was used to maintain task difficulty around a target accuracy level. Trial records include response timing, hit/miss outcomes, condition labels, and score deltas.

The implementation emits condition-specific trigger events for all major trial stages, supporting reproducible behavioral and synchronized recording pipelines.
