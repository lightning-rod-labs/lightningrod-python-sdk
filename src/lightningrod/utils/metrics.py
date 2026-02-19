"""Evaluation metrics — computes per-model accuracy from scored rollouts."""

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
