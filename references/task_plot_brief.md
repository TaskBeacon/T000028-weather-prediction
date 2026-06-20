# Task Plot Brief

## Task

- Title: Weather Prediction Task
- Construct: probabilistic category learning / feedback-based learning
- Paradigm: multi-cue probabilistic classification with weather outcome feedback.

## Rows

- Sun-favoring pattern: cue-card pattern with higher `P(sun)`.
- Ambiguous pattern: cue-card pattern near chance `P(sun)`.
- Rain-favoring pattern: cue-card pattern with lower `P(sun)`.

## Trial Timeline

1. Fixation: 300-600 ms jittered fixation, no response.
2. Cue: 800 ms. Show four cue cards as active/inactive, no response.
3. Decision: 2500 ms. Predict weather. Press F for sun, J for rain.
4. Feedback: 1000 ms. Show correct, incorrect, or timeout feedback with actual weather and score update.
5. ITI: 300-600 ms jittered fixation, no response.

## Notes

- The controller uses 14 cue-card patterns with explicit `sun_probability` values.
- Outcome feedback is probabilistically sampled from the pattern-specific `P(sun)`.
- Scoring is correct +1, incorrect -1, timeout 0.
