"""Evaluation metrics — computes per-model accuracy from scored rollouts."""

import math
from collections import defaultdict
from typing import Any, Dict, List, Optional

from lightningrod._generated.models.rollout_parsed_output_type_0 import RolloutParsedOutputType0
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.types import Unset


def compute_metrics_summary(
    samples: List[Sample],
    multiple_choice_options: Optional[Dict[str, str]] = None,
) -> Dict[str, Dict[str, Any]]:
    """Compute per-model evaluation metrics from scored samples.

    Returns dict keyed by model_name with accuracy, parse_rate, mean_reward,
    n_correct, n_parsed, n_total.
    """
    model_data: Dict[str, list] = defaultdict(list)

    for sample in samples:
        if not sample.label:
            continue
        correct_answer = sample.label.label

        for rollout in sample.rollouts or []:
            parsed_output = rollout.parsed_output
            parsed = (
                parsed_output is not None
                and not isinstance(parsed_output, Unset)
            )
            correct = False

            if parsed and correct_answer is not None:
                # Convert RolloutParsedOutputType0 to a plain dict
                if isinstance(parsed_output, RolloutParsedOutputType0):
                    po_dict = parsed_output.to_dict()
                else:
                    po_dict = parsed_output if isinstance(parsed_output, dict) else {}

                if multiple_choice_options and po_dict:
                    predicted_key = max(po_dict, key=po_dict.get)
                    predicted_value = multiple_choice_options.get(predicted_key)
                    correct = predicted_value == str(correct_answer)
                elif po_dict:
                    parsed_value = po_dict.get("value")
                    correct = str(parsed_value) == str(correct_answer)

            reward = rollout.reward
            if isinstance(reward, Unset):
                reward = None

            model_data[rollout.model_name].append({
                "correct": correct,
                "parsed": parsed,
                "reward": reward,
            })

    summary: Dict[str, Dict[str, Any]] = {}
    for model_name, entries in model_data.items():
        n_total = len(entries)
        n_parsed = sum(1 for e in entries if e["parsed"])
        n_correct = sum(1 for e in entries if e["correct"])
        rewards = [e["reward"] for e in entries if e["reward"] is not None]

        summary[model_name] = {
            "accuracy": n_correct / n_parsed if n_parsed else 0.0,
            "n_correct": n_correct,
            "n_parsed": n_parsed,
            "n_total": n_total,
            "parse_rate": n_parsed / n_total if n_total else 0.0,
            "mean_reward": sum(rewards) / len(rewards) if rewards else 0.0,
        }

    return summary


def compute_consensus(samples: List[Sample]) -> List[Dict[str, Any]]:
    """Compute model consensus for each sample with 2+ parsed rollouts.

    For each question, extracts each model's predicted probability and measures
    disagreement across models.

    Returns a list of dicts sorted by spread (most disagreement first), each with:
        question_text, predictions (model_name → float), label, spread, all_agree
    """
    results = []

    for sample in samples:
        predictions: Dict[str, float] = {}

        for rollout in sample.rollouts or []:
            parsed_output = rollout.parsed_output
            if parsed_output is None or isinstance(parsed_output, Unset):
                continue

            if isinstance(parsed_output, RolloutParsedOutputType0):
                po_dict = parsed_output.to_dict()
            else:
                po_dict = parsed_output if isinstance(parsed_output, dict) else {}

            value = po_dict.get("value")
            if value is not None:
                try:
                    predictions[rollout.model_name] = float(value)
                except (TypeError, ValueError):
                    continue

        if len(predictions) < 2:
            continue

        probs = list(predictions.values())
        spread = max(probs) - min(probs)
        all_agree = all(p >= 0.5 for p in probs) or all(p < 0.5 for p in probs)

        question_text = ""
        if sample.question and not isinstance(sample.question, Unset):
            qt = getattr(sample.question, "question_text", None)
            if qt and not isinstance(qt, Unset):
                question_text = qt

        label = None
        if sample.label and not isinstance(sample.label, Unset):
            lbl = sample.label.label
            if lbl is not None and not isinstance(lbl, Unset):
                label = lbl

        results.append({
            "question_text": question_text,
            "predictions": predictions,
            "label": label,
            "spread": spread,
            "all_agree": all_agree,
        })

    results.sort(key=lambda r: r["spread"], reverse=True)
    return results


def multi_choice_log_score(
    predicted: Dict[str, float],
    correct_answer: str,
    multiple_choice_options: Dict[str, str],
) -> float:
    """Compute multi-choice log score matching the back-end formula.

    ``sum(actual * log(clamp(predicted)))`` for mutually-exclusive options,
    where *actual* is a one-hot vector built from *correct_answer*.

    Args:
        predicted: option_key → predicted probability (e.g. {"option_0": 0.8, …}).
        correct_answer: the correct option **value** (e.g. "letter").
        multiple_choice_options: option_key → option value mapping.

    Returns:
        The log score (always ≤ 0; higher is better).
    """
    resolution: Dict[str, int] = {}
    for key, value in multiple_choice_options.items():
        resolution[key] = 1 if value == correct_answer else 0

    log_scores: List[float] = []
    for key in multiple_choice_options:
        actual = resolution.get(key, 0)
        pred = predicted.get(key)
        if pred is None:
            continue
        clamped = max(0.001, min(0.999, pred))
        log_scores.append(actual * math.log(clamped))

    return sum(log_scores)


def compute_multi_choice_consensus(
    samples: List[Sample],
    multiple_choice_options: Dict[str, str],
) -> List[Dict[str, Any]]:
    """Compute model consensus for multiple-choice samples with 2+ parsed rollouts.

    For each sample, averages the probability dicts across models and measures
    agreement / spread.

    Returns a list of dicts (one per qualifying sample) with:
        consensus          – averaged probability dict across models
        consensus_answer   – option *value* with highest avg probability
        per_model_answers  – model_name → predicted option value
        all_agree          – bool, all models pick the same top answer
        max_spread         – largest range of any option's probs across models
        label              – ground-truth label (str or None)
        predictions        – model_name → raw probability dict
    """
    results: List[Dict[str, Any]] = []

    for sample in samples:
        predictions: Dict[str, Dict[str, float]] = {}

        for rollout in sample.rollouts or []:
            parsed_output = rollout.parsed_output
            if parsed_output is None or isinstance(parsed_output, Unset):
                continue

            if isinstance(parsed_output, RolloutParsedOutputType0):
                po_dict = parsed_output.to_dict()
            else:
                po_dict = parsed_output if isinstance(parsed_output, dict) else {}

            if not po_dict:
                continue

            # Only keep dicts that look like option probability maps
            if any(k in multiple_choice_options for k in po_dict):
                predictions[rollout.model_name] = {
                    k: float(v) for k, v in po_dict.items()
                    if k in multiple_choice_options
                }

        if len(predictions) < 2:
            continue

        # Average probabilities across models
        option_keys = list(multiple_choice_options.keys())
        consensus: Dict[str, float] = {}
        max_spread = 0.0
        for key in option_keys:
            values = [pred[key] for pred in predictions.values() if key in pred]
            if values:
                consensus[key] = sum(values) / len(values)
                spread = max(values) - min(values)
                if spread > max_spread:
                    max_spread = spread

        # Consensus answer = option value with highest avg probability
        consensus_key = max(consensus, key=consensus.get)
        consensus_answer = multiple_choice_options.get(consensus_key, consensus_key)

        # Per-model top answers
        per_model_answers: Dict[str, str] = {}
        for model_name, pred in predictions.items():
            top_key = max(pred, key=pred.get)
            per_model_answers[model_name] = multiple_choice_options.get(top_key, top_key)

        all_agree = len(set(per_model_answers.values())) == 1

        label = None
        if sample.label and not isinstance(sample.label, Unset):
            lbl = sample.label.label
            if lbl is not None and not isinstance(lbl, Unset):
                label = lbl

        results.append({
            "consensus": consensus,
            "consensus_answer": consensus_answer,
            "per_model_answers": per_model_answers,
            "all_agree": all_agree,
            "max_spread": max_spread,
            "label": label,
            "predictions": predictions,
        })

    return results
