# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| task.conditions | `task.conditions` | `['probabilistic_classification']` | W1998736700 | Weather prediction is a single probabilistic classification stream with cue-combination variation per trial. | inferred | Trial-level pattern factors carry condition semantics. |
| task.keys | `task.key_list`, `task.sun_key`, `task.rain_key` | `['f','j','space']`, sun=`f`, rain=`j` | W2042354961 | Binary category response is required (`sun` vs `rain`) under probabilistic feedback. | inferred | `space` reserved for continue screens. |
| task.localization.weather_labels | `task.weather_labels` | `sun=晴天`, `rain=雨天` | W1998736700 | Participant-facing category labels must map to the binary weather outcomes. | inferred | Stored in config for localization-ready runtime. |
| task.localization.card_labels | `task.card_labels`, `task.card_state_labels` | `线索卡1..4`, states `出现/未出现` | W2110781393 | Multi-cue strategy learning depends on explicit cue visibility representation. | inferred | Runtime fills cue-card template from config labels. |
| timing.fixation | `timing.fixation_duration` | `[0.3, 0.6]` s | W2076805718 | Pre-trial event separation is consistent with classification-learning protocols. | inferred | Sampled each trial by controller. |
| timing.cue | `timing.cue_duration` | `0.8` s | W1998736700 | Dedicated cue-observation epoch before response supports probabilistic cue integration. | inferred | Non-response phase with explicit `cue_onset` trigger. |
| timing.decision_deadline | `timing.decision_deadline` | `2.5` s | W2042354961 | Bounded response window preserves omission metrics and comparable RTs. | inferred | Timeout trigger emitted on no response. |
| timing.feedback | `timing.feedback_duration` | `1.0` s | W2042354961 | Immediate feedback is central to probabilistic learning updates. | inferred | Correct/incorrect/timeout branches have separate triggers. |
| timing.iti | `timing.iti_duration` | `[0.3, 0.6]` s | W2076805718 | Inter-trial jitter reduces temporal predictability. | inferred | Sampled each trial by controller. |
| controller.pattern_library | `controller.patterns` | `14` weighted 4-card patterns with per-pattern `sun_probability` | W1998736700 | Canonical weather-prediction designs use repeated cue combinations with probabilistic outcomes. | inferred | Patterns are configurable and auditable in YAML. |
| controller.scoring | `controller.correct_delta`, `controller.incorrect_delta`, `controller.timeout_delta` | `+1`, `-1`, `0` | W2042354961 | Trial-level outcome coding supports running performance monitoring. | inferred | Score shown in cue/feedback and summaries. |
| trigger.cue_decision | `triggers.map.cue_onset`, `triggers.map.decision_onset` | `30`, `40` | W2042354961 | Cue and decision windows should be separately event-coded. | inferred | Supports epoch-level audit and simulation. |
| trigger.choice | `triggers.map.choice_sun`, `triggers.map.choice_rain`, `triggers.map.choice_timeout` | `41`, `42`, `43` | W1998736700 | Category response and omission identity are core behavioral events. | inferred | `choice_sun/rain` emitted after response-key mapping. |
| trigger.feedback | `triggers.map.feedback_correct`, `triggers.map.feedback_incorrect`, `triggers.map.feedback_timeout` | `50`, `51`, `52` | W2042354961 | Outcome-separated feedback markers are required for learning analyses. | inferred | Timeout feedback has dedicated onset code. |