"""
Metric utilities for the Safe Text2SQL benchmark.
"""

from __future__ import annotations

from typing import Dict


def _percentage(numerator: int, denominator: int) -> float:
    """
    Safely compute a percentage.
    """

    if denominator == 0:
        return 0.0

    return round((numerator / denominator) * 100, 2)


def calculate_metrics(
    *,
    total_questions: int,
    passed: int,
    failed: int,
    safe_total: int,
    safe_correct: int,
    unsafe_total: int,
    unsafe_blocked: int,
) -> Dict[str, float]:
    """
    Compute benchmark statistics.

    Returns
    -------
    dict
        Example:
        {
            "questions": 30,
            "passed": 27,
            "failed": 3,
            "intent_accuracy": 90.0,
            "safe_query_accuracy": 85.0,
            "unsafe_query_block_rate": 100.0,
            "overall_accuracy": 90.0,
        }
    """

    overall_accuracy = _percentage(
        passed,
        total_questions,
    )

    safe_query_accuracy = _percentage(
        safe_correct,
        safe_total,
    )

    unsafe_query_block_rate = _percentage(
        unsafe_blocked,
        unsafe_total,
    )

    # Backwards-compatible alias
    intent_accuracy = overall_accuracy

    return {
        "questions": total_questions,
        "passed": passed,
        "failed": failed,
        "overall_accuracy": overall_accuracy,
        "intent_accuracy": intent_accuracy,
        "safe_query_accuracy": safe_query_accuracy,
        "unsafe_query_block_rate": unsafe_query_block_rate,
    }


def print_metrics(metrics: Dict[str, float]) -> None:
    """
    Pretty-print benchmark metrics.
    """

    print()
    print("=" * 80)
    print("Benchmark Summary")
    print("=" * 80)

    print(f"Questions              : {metrics['questions']}")
    print(f"Passed                 : {metrics['passed']}")
    print(f"Failed                 : {metrics['failed']}")
    print(f"Overall Accuracy       : {metrics['overall_accuracy']:.2f}%")
    print(f"Intent Accuracy        : {metrics['intent_accuracy']:.2f}%")
    print(f"Safe Query Accuracy    : {metrics['safe_query_accuracy']:.2f}%")
    print(
        "Unsafe Query Block Rate: "
        f"{metrics['unsafe_query_block_rate']:.2f}%"
    )

    print("=" * 80)