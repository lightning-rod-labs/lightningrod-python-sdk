"""Evaluation metrics — computes per-model accuracy from scored rollouts."""

import math
from collections import defaultdict
from typing import Any, Dict, List, Optional

from lightningrod._generated.models.rollout_parsed_output_type_0 import RolloutParsedOutputType0
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.types import Unset


def _parsed_output_dict(rollout) -> dict:
    """Convert a rollout's parsed_output to a plain dict (or {} if absent)."""
    po = rollout.parsed_output
    if po is None or isinstance(po, Unset):
        return {}
    return po.to_dict() if isinstance(po, RolloutParsedOutputType0) else (po if isinstance(po, dict) else {})


def _get_label(sample) -> Optional[str]:
    """Extract the label string from a sample, or None if missing/unset."""
    if not sample.label or isinstance(sample.label, Unset):
        return None
    lbl = sample.label.label
    return None if lbl is None or isinstance(lbl, Unset) else lbl


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
            parsed = rollout.parsed_output is not None and not isinstance(rollout.parsed_output, Unset)
            correct = False

            if parsed and correct_answer is not None:
                po_dict = _parsed_output_dict(rollout)

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
            po_dict = _parsed_output_dict(rollout)
            if not po_dict:
                continue

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

        label = _get_label(sample)

        results.append({
            "question_text": question_text,
            "predictions": predictions,
            "label": label,
            "spread": spread,
            "all_agree": all_agree,
        })

    results.sort(key=lambda r: r["spread"], reverse=True)
    return results


def _multi_choice_log_score(predicted, correct_answer, multiple_choice_options):
    """Log score for mutually-exclusive multi-choice options."""
    return sum(
        int(v == correct_answer) * math.log(max(0.001, min(0.999, predicted[k])))
        for k, v in multiple_choice_options.items() if k in predicted
    )


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
            po_dict = _parsed_output_dict(rollout)
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
        consensus: Dict[str, float] = {}
        max_spread = 0.0
        for key in multiple_choice_options:
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
        per_model_answers = {
            m: multiple_choice_options.get(max(p, key=p.get), max(p, key=p.get))
            for m, p in predictions.items()
        }

        all_agree = len(set(per_model_answers.values())) == 1

        label = _get_label(sample)

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


def compute_consensus_summary(
    samples: List[Sample],
    multiple_choice_options: Dict[str, str],
) -> Dict[str, Any]:
    """Consensus analysis: averaged prediction vs individual models.

    Returns a dict with:
        model_comparison   – {"averaged": {...}, "model_a": {...}, ...}
                             each with keys: accuracy, mean_log_score, n
        agreement_analysis – {"all": {...}, "agreement_set": {...}, "disagreement_set": {...}}
                             each with keys: n, accuracy, mean_log_score
        n_consensus        – number of samples with 2+ parsed rollouts
        n_agree            – number of samples where all models agree
    """
    consensus_rows = compute_multi_choice_consensus(samples, multiple_choice_options)
    labeled = [r for r in consensus_rows if r["label"] is not None]

    n_consensus = len(consensus_rows)
    n_agree = sum(1 for r in consensus_rows if r["all_agree"])

    # Model comparison: averaged vs each individual model
    model_comparison: Dict[str, Dict[str, Any]] = {}
    if labeled:
        model_comparison["averaged"] = {
            "accuracy": sum(r["consensus_answer"] == r["label"] for r in labeled) / len(labeled),
            "mean_log_score": sum(
                _multi_choice_log_score(r["consensus"], r["label"], multiple_choice_options)
                for r in labeled
            ) / len(labeled),
            "n": len(labeled),
        }
        for model in sorted({m for r in labeled for m in r["predictions"]}):
            ml = [r for r in labeled if model in r["per_model_answers"]]
            if ml:
                model_comparison[model] = {
                    "accuracy": sum(r["per_model_answers"][model] == r["label"] for r in ml) / len(ml),
                    "mean_log_score": sum(
                        _multi_choice_log_score(r["predictions"][model], r["label"], multiple_choice_options)
                        for r in ml if model in r["predictions"]
                    ) / len(ml),
                    "n": len(ml),
                }

    return {
        "model_comparison": model_comparison,
        "n_consensus": n_consensus,
        "n_agree": n_agree,
    }
