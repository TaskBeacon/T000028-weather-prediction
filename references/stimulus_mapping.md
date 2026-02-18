# Stimulus Mapping

Task: `Weather Prediction Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `sun` | `sun_cue`, `sun_target` | `W2110781393` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for SUN; target token for condition-specific response context. |
| `rain` | `rain_cue`, `rain_target` | `W2110781393` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for RAIN; target token for condition-specific response context. |
| `snow` | `snow_cue`, `snow_target` | `W2110781393` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for SNOW; target token for condition-specific response context. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
