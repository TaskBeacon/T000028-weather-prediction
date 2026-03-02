# CHANGELOG

All notable development changes for `T000028-weather-prediction` are documented here.

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
