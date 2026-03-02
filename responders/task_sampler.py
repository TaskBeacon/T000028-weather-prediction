from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import random as _py_random

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Sampler responder for Weather Prediction decision phase."""

    quality_rate: float = 0.75
    miss_rate: float = 0.08
    sun_bias: float = 0.0
    rt_mean_s: float = 0.55
    rt_sd_s: float = 0.12
    rt_min_s: float = 0.18

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.quality_rate = max(0.0, min(1.0, float(self.quality_rate)))
        self.miss_rate = max(0.0, min(1.0, float(self.miss_rate)))
        self.sun_bias = max(-0.5, min(0.5, float(self.sun_bias)))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _sample_normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _sample_random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def _continue_action(self, valid_keys: list[str], phase: str) -> Action:
        key = "space" if "space" in valid_keys else valid_keys[0]
        rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))
        return Action(
            key=key,
            rt_s=rt,
            meta={"source": "task_sampler", "phase": phase, "outcome": "continue"},
        )

    def act(self, obs: Observation) -> Action:
        valid_keys = [str(k).strip().lower() for k in list(obs.valid_keys or []) if str(k).strip()]
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        if self._rng is None:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "rng_missing"})

        phase = str(obs.phase or "")
        if phase != "decision":
            return self._continue_action(valid_keys, phase)

        if self._sample_random() < self.miss_rate:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "outcome": "timeout"})

        factors = dict(obs.task_factors or {})
        sun_key = str(factors.get("sun_key", "f")).strip().lower()
        rain_key = str(factors.get("rain_key", "j")).strip().lower()
        if sun_key not in valid_keys:
            sun_key = valid_keys[0]
        if rain_key not in valid_keys:
            rain_key = valid_keys[-1] if len(valid_keys) > 1 else valid_keys[0]

        p_sun = float(factors.get("sun_probability", 0.5))
        p_sun = max(0.0, min(1.0, p_sun))
        p_sun = max(0.0, min(1.0, p_sun + self.sun_bias))

        optimal_key = sun_key if p_sun >= 0.5 else rain_key
        alternative_key = rain_key if optimal_key == sun_key else sun_key
        choose_optimal = self._sample_random() < self.quality_rate
        chosen = optimal_key if choose_optimal else alternative_key

        rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))
        return Action(
            key=chosen,
            rt_s=rt,
            meta={
                "source": "task_sampler",
                "outcome": "choose_weather",
                "quality_rate": self.quality_rate,
                "p_sun": p_sun,
            },
        )
