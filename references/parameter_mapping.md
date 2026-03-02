# Parameter Mapping

| Parameter | Implemented Value | Source Paper ID | Confidence | Rationale |
|---|---|---|---|---|
| `task.conditions` | `['probabilistic_classification']` | `W1998736700` | `supported` | Weather prediction is a single probabilistic classification stream with trial-wise cue combinations. |
| `task.key_list` | `['f', 'j', 'space']` | `W1998736700` | `inferred` | Two-choice weather prediction requires binary response mapping; keys adapted to local keyboard standard. |
| `task.total_blocks` | `2` | `W2136211925` | `inferred` | Multi-block structure preserves sustained learning while keeping run length manageable. |
| `task.trial_per_block` | `60` | `W2136211925` | `inferred` | Trial volume supports measurable learning progression under probabilistic feedback. |
| `timing.fixation_duration` | `[0.3, 0.6]` | `W2076805718` | `inferred` | Jittered pre-trial baseline separates events and avoids fixed temporal expectancy. |
| `timing.cue_duration` | `0.8` | `W1998736700` | `inferred` | Brief cue-view phase presents card pattern before response stage. |
| `timing.decision_deadline` | `2.5` | `W2042354961` | `inferred` | Bounded response window enables timeout metric while preserving deliberate choice behavior. |
| `timing.feedback_duration` | `1.0` | `W2042354961` | `inferred` | Immediate explicit feedback supports trial-wise probabilistic learning. |
| `controller.patterns` | `14 cue patterns with per-pattern P(sun)` | `W1998736700` | `inferred` | Canonical weather prediction implementations use repeated cue-combination patterns with probabilistic outcomes. |
| `controller.correct_delta` | `+1` | `W2110781393` | `inferred` | Simple signed score updates provide transparent performance feedback without changing core choice mechanics. |
| `controller.incorrect_delta` | `-1` | `W2110781393` | `inferred` | Symmetric penalty keeps cumulative score sensitive to prediction quality. |
| `controller.timeout_delta` | `0` | `W2076805718` | `inferred` | Timeouts are logged behaviorally without adding reward bias. |
| `triggers.map.cue_onset` | `30` | `W2042354961` | `inferred` | Distinct cue-stage marker for reproducible event timing. |
| `triggers.map.decision_onset` | `40` | `W2042354961` | `inferred` | Separates response epoch from cue-only viewing epoch. |
| `triggers.map.choice_sun` | `41` | `W2042354961` | `inferred` | Encodes weather-choice response category. |
| `triggers.map.choice_rain` | `42` | `W2042354961` | `inferred` | Encodes weather-choice response category. |
| `triggers.map.feedback_correct` | `50` | `W2042354961` | `inferred` | Outcome-specific feedback marker for learning analysis. |
| `triggers.map.feedback_incorrect` | `51` | `W2042354961` | `inferred` | Outcome-specific feedback marker for learning analysis. |
| `triggers.map.feedback_timeout` | `52` | `W2042354961` | `inferred` | Explicit timeout feedback marker. |
