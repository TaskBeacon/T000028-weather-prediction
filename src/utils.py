
from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

from psychopy import logging


@dataclass(frozen=True)
class PatternSpec:
    pattern_id: str
    cards: tuple[int, int, int, int]
    sun_probability: float
    weight: float


DEFAULT_PATTERNS: tuple[PatternSpec, ...] = (
    PatternSpec("P01", (1, 0, 0, 0), 0.76, 1.0),
    PatternSpec("P02", (0, 1, 0, 0), 0.57, 1.0),
    PatternSpec("P03", (0, 0, 1, 0), 0.43, 1.0),
    PatternSpec("P04", (0, 0, 0, 1), 0.20, 1.0),
    PatternSpec("P05", (1, 1, 0, 0), 0.67, 1.0),
    PatternSpec("P06", (1, 0, 1, 0), 0.60, 1.0),
    PatternSpec("P07", (1, 0, 0, 1), 0.48, 1.0),
    PatternSpec("P08", (0, 1, 1, 0), 0.50, 1.0),
    PatternSpec("P09", (0, 1, 0, 1), 0.38, 1.0),
    PatternSpec("P10", (0, 0, 1, 1), 0.32, 1.0),
    PatternSpec("P11", (1, 1, 1, 0), 0.59, 1.0),
    PatternSpec("P12", (1, 1, 0, 1), 0.51, 1.0),
    PatternSpec("P13", (1, 0, 1, 1), 0.46, 1.0),
    PatternSpec("P14", (0, 1, 1, 1), 0.40, 1.0),
)


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, float(value)))


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


def _safe_int(value: Any, default: int) -> int:
    try:
        return int(round(float(value)))
    except Exception:
        return int(default)


def _coerce_cards(raw_cards: Any) -> tuple[int, int, int, int] | None:
    if not isinstance(raw_cards, (list, tuple)) or len(raw_cards) != 4:
        return None
    cards: list[int] = []
    for token in raw_cards:
        cards.append(1 if str(token).strip() in {"1", "true", "True"} or token == 1 else 0)
    if sum(cards) <= 0:
        return None
    return (cards[0], cards[1], cards[2], cards[3])


def _parse_patterns(raw_patterns: Any) -> list[PatternSpec]:
    if not isinstance(raw_patterns, list):
        return list(DEFAULT_PATTERNS)

    parsed: list[PatternSpec] = []
    for idx, item in enumerate(raw_patterns):
        if not isinstance(item, dict):
            continue
        cards = _coerce_cards(item.get("cards"))
        if cards is None:
            continue
        pattern_id = str(item.get("pattern_id", f"P{idx + 1:02d}")).strip() or f"P{idx + 1:02d}"
        sun_probability = _clamp(_safe_float(item.get("sun_probability", 0.5), 0.5), 0.0, 1.0)
        weight = max(1e-6, _safe_float(item.get("weight", 1.0), 1.0))
        parsed.append(
            PatternSpec(
                pattern_id=pattern_id,
                cards=cards,
                sun_probability=sun_probability,
                weight=weight,
            )
        )

    return parsed if parsed else list(DEFAULT_PATTERNS)


class Controller:
    """State controller for Weather Prediction probabilistic classification trials."""

    def __init__(
        self,
        *,
        patterns: list[PatternSpec] | None = None,
        initial_score: int = 0,
        correct_delta: int = 1,
        incorrect_delta: int = -1,
        timeout_delta: int = 0,
        enable_logging: bool = True,
    ) -> None:
        self.patterns: list[PatternSpec] = list(patterns or DEFAULT_PATTERNS)

        self.initial_score = int(initial_score)
        self.correct_delta = int(correct_delta)
        self.incorrect_delta = int(incorrect_delta)
        self.timeout_delta = int(timeout_delta)
        self.enable_logging = bool(enable_logging)

        self.current_score = int(initial_score)
        self.trial_count_total = 0
        self.trial_count_block = 0
        self.block_idx = -1
        self.histories: list[dict[str, Any]] = []

    @classmethod
    def from_dict(cls, config: dict) -> "Controller":
        if not isinstance(config, dict):
            config = {}
        return cls(
            patterns=_parse_patterns(config.get("patterns")),
            initial_score=_safe_int(config.get("initial_score", 0), 0),
            correct_delta=_safe_int(config.get("correct_delta", 1), 1),
            incorrect_delta=_safe_int(config.get("incorrect_delta", -1), -1),
            timeout_delta=_safe_int(config.get("timeout_delta", 0), 0),
            enable_logging=bool(config.get("enable_logging", True)),
        )

    def start_block(self, block_idx: int) -> None:
        self.block_idx = int(block_idx)
        self.trial_count_block = 0

    def apply_score(self, is_correct: bool | None) -> dict[str, int]:
        score_before = int(self.current_score)
        if is_correct is None:
            delta = int(self.timeout_delta)
        elif is_correct:
            delta = int(self.correct_delta)
        else:
            delta = int(self.incorrect_delta)
        score_after = int(score_before + delta)
        self.current_score = score_after
        return {"score_before": score_before, "score_after": score_after, "score_delta": int(delta)}

    def record_trial(self, record: dict[str, Any]) -> None:
        self.trial_count_total += 1
        self.trial_count_block += 1
        self.histories.append(dict(record))
        if self.enable_logging:
            logging.data(
                "[WeatherPrediction] "
                f"block={self.block_idx} "
                f"trial_block={self.trial_count_block} "
                f"trial_total={self.trial_count_total} "
                f"pattern={record.get('pattern_id', '')} "
                f"p_sun={_safe_float(record.get('sun_probability', 0.5), 0.5):.2f} "
                f"actual={record.get('actual_weather', '')} "
                f"pred={record.get('predicted_weather', '')} "
                f"correct={record.get('is_correct', None)} "
                f"score={record.get('score_after', self.current_score)}"
            )


def generate_weather_conditions(
    n_trials: int,
    condition_labels: list[Any] | None = None,
    *,
    seed: int = 0,
    patterns: list[PatternSpec] | tuple[PatternSpec, ...] | None = None,
) -> list[tuple[str, str, tuple[int, int, int, int], float, str]]:
    """Build concrete cue-pattern and weather outcomes during block scheduling."""
    labels = [str(label).strip().lower() for label in (condition_labels or ["probabilistic_classification"])]
    if not labels:
        labels = ["probabilistic_classification"]
    pattern_list = list(patterns or DEFAULT_PATTERNS)
    rng = random.Random(int(seed))
    weights = [max(1e-6, float(pattern.weight)) for pattern in pattern_list]

    scheduled: list[tuple[str, str, tuple[int, int, int, int], float, str]] = []
    for trial_index in range(int(n_trials)):
        condition_name = labels[trial_index % len(labels)]
        pattern = rng.choices(pattern_list, weights=weights, k=1)[0]
        actual_weather = "sun" if rng.random() < float(pattern.sun_probability) else "rain"
        scheduled.append(
            (
                condition_name,
                str(pattern.pattern_id),
                tuple(int(v) for v in pattern.cards),
                float(pattern.sun_probability),
                actual_weather,
            )
        )
    return scheduled


def weather_condition_to_trial_info(condition: Any) -> dict[str, Any]:
    """Decode a scheduled weather-prediction condition tuple."""
    if isinstance(condition, (tuple, list)) and len(condition) >= 5:
        condition_name, pattern_id, cards, sun_probability, actual_weather = condition[:5]
        parsed_cards = _coerce_cards(cards)
        if parsed_cards is None:
            raise ValueError(f"Invalid weather card pattern in condition: {condition!r}")
        return {
            "condition": str(condition_name).strip().lower(),
            "pattern_id": str(pattern_id),
            "cards": parsed_cards,
            "sun_probability": float(sun_probability),
            "actual_weather": str(actual_weather).strip().lower(),
        }
    raise ValueError(f"Expected scheduled weather condition tuple, got {condition!r}")
