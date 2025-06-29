# File: eval/eval_metrics.py
"""Evaluate agent outputs using RAGAS and basic metrics."""

from ragas import evaluate
from ragas.metrics import context_precision, context_recall, faithfulness, answer_relevancy
from datasets import Dataset

# Prepare RAGAS Dataset
# Each entry should include: question, answer, contexts, ground_truth

def run_ragas_eval(entries: list[dict]):
    ds = Dataset.from_list(entries)
    result = evaluate(
        ds,
        metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
    )
    return result.to_pandas()