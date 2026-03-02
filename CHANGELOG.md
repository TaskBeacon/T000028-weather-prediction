# CHANGELOG

All notable development changes for `T000028-weather-prediction` are documented here.

## [v0.2.1-dev] - 2026-03-02

### Changed
- Standardized `main.py` to the single-flow `human|qa|sim` runtime contract with shared initialization and runtime-context handling.
- Replaced `src/run_trial.py` MID-template leftovers with weather-prediction-specific phases (`fixation -> cue -> decision -> feedback -> inter_trial_interval`) driven by controller pattern/outcome sampling.
- Added config-driven localization dictionaries (`task.weather_labels`, `task.card_labels`, `task.card_state_labels`) across all config profiles.
- Added `stimuli.cue_card_template` and updated `stimuli.key_hint` placeholders to keep participant-facing labels configurable.
- Rewrote reference artifacts to current task-build contract schema:
  - `references/references.yaml`
  - `references/references.md`
  - `references/parameter_mapping.md`
  - `references/stimulus_mapping.md`
  - `references/task_logic_audit.md`

### Fixed
- Fixed `references/references.yaml` parse failures caused by unquoted colon-containing fields.
- Restored required reference headings/table columns expected by validators.
- Restored QA-required trial outputs (`condition`, `trial_id`, `pattern_id`, `actual_weather`, `decision_response`, `decision_rt`, `is_correct`, `score_after`).

### Validation
- `python -m py_compile main.py src/run_trial.py`
- `python e:/Taskbeacon/psyflow/skills/task-build/scripts/check_task_standard.py --task-path e:/Taskbeacon/T000028-weather-prediction`
- `psyflow-qa e:/Taskbeacon/T000028-weather-prediction --no-maturity-update`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`
- `python -m psyflow.validate e:/Taskbeacon/T000028-weather-prediction`

## [v0.2.0-dev] - 2026-02-19

### Changed
- Rebuilt the task from zero-base literature logic for a true Weather Prediction paradigm (`fixation -> cue -> decision -> feedback -> iti`).
- Replaced MID-template runtime code in `main.py`, `src/run_trial.py`, and `src/utils.py` with cue-combination probabilistic classification logic.
- Replaced all four config files with clean UTF-8 Chinese participant text and weather-specific triggers/response mapping.
- Replaced sampler logic in `responders/task_sampler.py` with a decision-phase probabilistic policy.
- Regenerated `references/task_logic_audit.md`, `references/stimulus_mapping.md`, `references/parameter_mapping.md`, `references/references.yaml`, and `references/references.md` from task-relevant literature.
- Updated metadata and documentation (`taskbeacon.yaml`, `README.md`, `selected_papers.json`).

### Fixed
- Fixed controller logging call signature in `src/utils.py` to avoid runtime exceptions during QA/sim runs.

## [v0.1.1-dev] - 2026-02-19

### Changed
- Rebuilt literature bundle with task-relevant curated papers and regenerated reference artifacts.
- Replaced corrupted `references/task_logic_audit.md` with a full state-machine audit.
- Updated `references/stimulus_mapping.md` to concrete implemented stimulus IDs per condition.
- Synced metadata (`README.md`, `taskbeacon.yaml`) with current configuration and evidence.

## [0.1.0] - 2026-02-17

### Added
- Added initial PsyFlow/TAPS task scaffold for Weather Prediction Task.
- Added mode-aware runtime (`human|qa|sim`) in `main.py`.
- Added split configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`).
- Added responder trial-context plumbing via `set_trial_context(...)` in `src/run_trial.py`.
- Added generated cue/target image stimuli under `assets/generated/`.
