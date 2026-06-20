Use case: infographic-diagram
Asset type: TaskBeacon task flow diagram
Primary request: Create a clean, publication-ready task flow diagram as a timeline collection for the behavioral task described below.

Task: Weather Prediction Task
Construct: probabilistic category learning / feedback-based learning
Rows/conditions:
- Sun-favoring pattern: cue-card pattern with higher P(sun).
- Ambiguous pattern: cue-card pattern near chance P(sun).
- Rain-favoring pattern: cue-card pattern with lower P(sun).

Timeline phases:
- Sun-favoring pattern: Fixation (300-600 ms; no response; +) -> Cue cards (800 ms; no response; 4 cards active/inactive; higher P(sun)) -> Decision (2500 ms; press F=sun / J=rain) -> Feedback (1000 ms; no response; correct / incorrect / timeout; actual weather; score update) -> ITI (300-600 ms; no response; +)
- Ambiguous pattern: Fixation (300-600 ms; no response; +) -> Cue cards (800 ms; no response; 4 cards active/inactive; near chance P(sun)) -> Decision (2500 ms; press F=sun / J=rain) -> Feedback (1000 ms; no response; correct / incorrect / timeout; actual weather; score update) -> ITI (300-600 ms; no response; +)
- Rain-favoring pattern: Fixation (300-600 ms; no response; +) -> Cue cards (800 ms; no response; 4 cards active/inactive; lower P(sun)) -> Decision (2500 ms; press F=sun / J=rain) -> Feedback (1000 ms; no response; correct / incorrect / timeout; actual weather; score update) -> ITI (300-600 ms; no response; +)

Visual requirements:
- White background, landscape orientation, crisp dark text, restrained condition accent colors.
- One horizontal row per evidence type.
- Each row contains 5 participant-screen snapshots connected by a subtle arrow.
- Each screen snapshot shows participant-visible screen content only.
- Use gray participant-screen boxes, thin black arrows, consistent row spacing, and subtle row separators.
- Place timing labels under each screen in compact text.
- Place evidence labels at the left of each row.
- Use short labels only; avoid paragraphs inside the image.
- Make all text legible at normal document preview size.
- Leave a clean blank header band across the top 18-20% of the image.

Accuracy constraints:
- Do not invent phases, stimuli, condition names, keys, rewards, or timings.
- Do not add people, lab equipment, decorative scenes, logos, or unrelated icons.
- Do not draw the task title, construct subtitle, any logo, watermark, brand mark, or `TaskBeacon` text inside the generated image.
- Draw only the timeline content below the blank header band.
- Preserve these exact terms where used: Sun-favoring pattern, Ambiguous pattern, Rain-favoring pattern, P(sun), F=sun, J=rain, 300-600 ms, 800 ms, 2500 ms, 1000 ms.

Style:
TaskBeacon scientific infographic style: clean vector-like raster image, organized spacing, gray screen boxes, restrained color accents, and a blank header-safe area.
