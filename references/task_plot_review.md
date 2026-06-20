# Task Plot Review

## Evidence Match

- Pass: title and construct match the Weather Prediction Task.
- Pass: rows summarize the 14 cue-card probability table as sun-favoring, ambiguous, and rain-favoring evidence types.
- Pass: phase order matches README and `src/run_trial.py`: Fixation -> Cue -> Decision -> Feedback -> ITI.
- Pass: timing labels match config: 300-600 ms fixation, 800 ms cue, 2500 ms decision, 1000 ms feedback, 300-600 ms ITI.
- Pass: decision mapping shows F=sun and J=rain.
- Pass: feedback shows correct, incorrect, or timeout with actual weather and score update.
- Pass: no deterministic rule, extra response keys, or extra phases are shown.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
