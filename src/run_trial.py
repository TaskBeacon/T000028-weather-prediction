from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, set_trial_context


def _deadline_s(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def _as_duration(controller, value: Any, default_value: float) -> float:
    if hasattr(controller, "sample_duration"):
        return float(controller.sample_duration(value, default_value))
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return float(default_value)
    return float(default_value)


def _as_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list:
    return list(value) if isinstance(value, (list, tuple)) else []


def _add_cue_cards(
    unit: StimUnit,
    stim_bank,
    cards: tuple[int, int, int, int],
    card_labels: list[str],
    on_label: str,
    off_label: str,
) -> None:
    positions = [(-390, 70), (-130, 70), (130, 70), (390, 70)]
    for idx, card_state in enumerate(cards):
        card_label = card_labels[idx] if idx < len(card_labels) else f"Card {idx + 1}"
        state_label = on_label if int(card_state) == 1 else off_label
        card_color = [0.97, 0.88, 0.46] if int(card_state) == 1 else [0.66, 0.66, 0.66]
        unit.add_stim(
            stim_bank.rebuild(
                "cue_card_template",
                text=f"{card_label}\n{state_label}",
                pos=positions[idx],
                color=card_color,
            )
        )


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one weather-prediction trial with probabilistic cue pattern and outcome."""
    condition_name = str(condition).strip().lower()
    trial_id = int(controller.next_trial_id()) if hasattr(controller, "next_trial_id") else 1
    block_idx_val = int(block_idx) if block_idx is not None else 0

    pattern = controller.draw_pattern()
    actual_weather = str(controller.sample_weather(pattern)).strip().lower()
    cards = tuple(int(v) for v in pattern.cards)
    card_code = "".join(str(v) for v in cards)

    sun_key = str(getattr(settings, "sun_key", "f")).strip().lower()
    rain_key = str(getattr(settings, "rain_key", "j")).strip().lower()
    response_keys = [sun_key, rain_key]

    weather_labels = _as_dict(getattr(settings, "weather_labels", {}))
    sun_label = str(weather_labels.get("sun", "sun"))
    rain_label = str(weather_labels.get("rain", "rain"))
    actual_weather_label = sun_label if actual_weather == "sun" else rain_label

    card_labels = [str(item) for item in _as_list(getattr(settings, "card_labels", []))]
    if len(card_labels) < 4:
        card_labels = ["Card 1", "Card 2", "Card 3", "Card 4"]

    card_state_labels = _as_dict(getattr(settings, "card_state_labels", {}))
    on_label = str(card_state_labels.get("on", "on"))
    off_label = str(card_state_labels.get("off", "off"))

    fixation_duration = _as_duration(controller, settings.fixation_duration, 0.45)
    cue_duration = float(settings.cue_duration)
    decision_deadline = float(settings.decision_deadline)
    feedback_duration = float(settings.feedback_duration)
    iti_duration = _as_duration(controller, settings.iti_duration, 0.45)

    current_score = int(getattr(controller, "current_score", 0))
    trial_data = {
        "condition": condition_name,
        "trial_id": trial_id,
        "block_id": str(block_id) if block_id is not None else "block_0",
        "block_idx": block_idx_val,
        "pattern_id": str(pattern.pattern_id),
        "pattern_cards": card_code,
        "card_1": cards[0],
        "card_2": cards[1],
        "card_3": cards[2],
        "card_4": cards[3],
        "sun_probability": float(pattern.sun_probability),
        "actual_weather": actual_weather,
        "actual_weather_cn": actual_weather_label,
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    fixation = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fixation,
        trial_id=trial_id,
        phase="fixation",
        deadline_s=_deadline_s(fixation_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=condition_name,
        task_factors={
            "stage": "fixation",
            "pattern_id": pattern.pattern_id,
            "cards": list(cards),
            "sun_probability": float(pattern.sun_probability),
            "block_idx": block_idx_val,
        },
        stim_id="fixation",
    )
    fixation.show(
        duration=fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    cue = make_unit(unit_label="cue")
    cue.add_stim(stim_bank.get("cue_title"))
    cue.add_stim(stim_bank.get_and_format("score_text", current_score=current_score))
    _add_cue_cards(cue, stim_bank, cards, card_labels, on_label=on_label, off_label=off_label)
    cue.add_stim(stim_bank.get("cue_hint"))
    set_trial_context(
        cue,
        trial_id=trial_id,
        phase="cue",
        deadline_s=_deadline_s(cue_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=condition_name,
        task_factors={
            "stage": "cue",
            "pattern_id": pattern.pattern_id,
            "cards": list(cards),
            "sun_probability": float(pattern.sun_probability),
            "current_score": current_score,
            "block_idx": block_idx_val,
        },
        stim_id="cue_title+score_text+cue_card_template*4+cue_hint",
    )
    cue.show(
        duration=cue_duration,
        onset_trigger=settings.triggers.get("cue_onset"),
    ).to_dict(trial_data)

    decision = make_unit(unit_label="decision")
    decision.add_stim(stim_bank.get_and_format("score_text", current_score=current_score))
    _add_cue_cards(decision, stim_bank, cards, card_labels, on_label=on_label, off_label=off_label)
    decision.add_stim(stim_bank.get("decision_prompt"))
    decision.add_stim(
        stim_bank.get_and_format(
            "key_hint",
            sun_key=sun_key.upper(),
            rain_key=rain_key.upper(),
            sun_label=sun_label,
            rain_label=rain_label,
        )
    )
    set_trial_context(
        decision,
        trial_id=trial_id,
        phase="decision",
        deadline_s=_deadline_s(decision_deadline),
        valid_keys=response_keys,
        block_id=trial_data["block_id"],
        condition_id=condition_name,
        task_factors={
            "stage": "decision",
            "pattern_id": pattern.pattern_id,
            "cards": list(cards),
            "sun_probability": float(pattern.sun_probability),
            "sun_key": sun_key,
            "rain_key": rain_key,
            "block_idx": block_idx_val,
        },
        stim_id="score_text+cue_card_template*4+decision_prompt+key_hint",
    )
    decision.capture_response(
        keys=response_keys,
        duration=decision_deadline,
        onset_trigger=settings.triggers.get("decision_onset"),
        response_trigger=None,
        timeout_trigger=settings.triggers.get("choice_timeout"),
    )
    decision.to_dict(trial_data)

    response_key = str(decision.get_state("response", "")).strip().lower()
    timed_out = response_key not in response_keys
    if response_key == sun_key:
        trigger_runtime.send(settings.triggers.get("choice_sun"))
    elif response_key == rain_key:
        trigger_runtime.send(settings.triggers.get("choice_rain"))

    if timed_out:
        predicted_weather = "none"
        predicted_weather_label = "none"
    else:
        predicted_weather = "sun" if response_key == sun_key else "rain"
        predicted_weather_label = sun_label if predicted_weather == "sun" else rain_label

    is_correct: bool | None = None if timed_out else (predicted_weather == actual_weather)
    score_update = controller.apply_score(is_correct)

    if timed_out:
        feedback_stim_id = "feedback_timeout"
        feedback_onset = "feedback_timeout"
        feedback_stim = stim_bank.get_and_format(
            feedback_stim_id,
            actual_weather_cn=actual_weather_label,
            score_after=score_update["score_after"],
        )
    else:
        feedback_stim_id = "feedback_correct" if bool(is_correct) else "feedback_incorrect"
        feedback_onset = feedback_stim_id
        feedback_stim = stim_bank.get_and_format(
            feedback_stim_id,
            predicted_weather_cn=predicted_weather_label,
            actual_weather_cn=actual_weather_label,
            score_delta=score_update["score_delta"],
            score_after=score_update["score_after"],
        )

    feedback = make_unit(unit_label="feedback").add_stim(feedback_stim)
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="feedback",
        deadline_s=_deadline_s(feedback_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=condition_name,
        task_factors={
            "stage": "feedback",
            "pattern_id": pattern.pattern_id,
            "actual_weather": actual_weather,
            "predicted_weather": predicted_weather,
            "timed_out": timed_out,
            "is_correct": is_correct,
            "score_after": score_update["score_after"],
            "block_idx": block_idx_val,
        },
        stim_id=feedback_stim_id,
    )
    feedback.show(
        duration=feedback_duration,
        onset_trigger=settings.triggers.get(feedback_onset),
    ).to_dict(trial_data)

    iti = make_unit(unit_label="inter_trial_interval").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=_deadline_s(iti_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=condition_name,
        task_factors={"stage": "inter_trial_interval", "block_idx": block_idx_val},
        stim_id="fixation",
    )
    iti.show(
        duration=iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    rt = decision.get_state("rt", None)
    key_press = decision.get_state("key_press", None)
    rt_s = float(rt) if isinstance(rt, (int, float)) else None

    trial_data.update(
        {
            "response_key": response_key if not timed_out else "",
            "decision_response": response_key if not timed_out else "",
            "decision_key_press": bool(key_press) if key_press is not None else not timed_out,
            "decision_rt": rt_s,
            "decision_rt_s": rt_s,
            "decision_timed_out": bool(timed_out),
            "predicted_weather": predicted_weather,
            "predicted_weather_cn": predicted_weather_label,
            "is_correct": bool(is_correct) if is_correct is not None else None,
            "score_before": score_update["score_before"],
            "score_after": score_update["score_after"],
            "score_delta": score_update["score_delta"],
        }
    )

    controller.record_trial(trial_data)
    return trial_data