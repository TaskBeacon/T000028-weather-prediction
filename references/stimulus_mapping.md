# Stimulus Mapping

Task: `Weather Prediction Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `probabilistic_classification` | `cue_title`, runtime 4-card cue array (`cue_card_1..4`), `cue_hint`, `decision_prompt`, `key_hint`, `feedback_correct`, `feedback_incorrect`, `feedback_timeout`, `fixation` | `W1998736700` | Weather prediction uses cue-card combinations to drive probabilistic category predictions with trial-wise feedback. | `psychopy_builtin` | Cue cards are concrete visual rectangles with active/inactive state labels; weather responses are binary (`sun/rain`). |
| `pattern_probability_logic` | per-trial pattern factor (`pattern_id`, `sun_probability`) and sampled outcome (`actual_weather`) | `W2042354961` | Probabilistic classification learning relies on outcome uncertainty contingent on cue combinations. | `psychopy_builtin` | Outcome generation is implemented in controller and surfaced in feedback text. |
| `all_conditions` | `instruction_text`, `block_break`, `good_bye`, `score_text` | `W2110781393` | Multi-cue learning tasks include instructions, repeated trial feedback, and session-level performance summaries. | `psychopy_builtin` | Participant-facing text is UTF-8 Chinese with `SimHei` font. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config or runtime drawing.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
