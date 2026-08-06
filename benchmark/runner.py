"""
Runs the benchmark suite for Safe Text2SQL Analytics.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.llm import generate_sql
from app.validator import validate_sql
from benchmark.metrics import calculate_metrics
from benchmark.questions import BENCHMARK_QUESTIONS

ROOT_DIR = Path(__file__).resolve().parent.parent

REPORT_PATH = ROOT_DIR / "benchmark" / "benchmark_report.json"


def run_benchmark() -> None:
    """
    Run the benchmark dataset and save the report.
    """

    print("=" * 80)
    print("Running Benchmark...")
    print("=" * 80)

    results = []

    passed = 0
    failed = 0

    safe_total = 0
    safe_correct = 0

    unsafe_total = 0
    unsafe_blocked = 0

    for item in BENCHMARK_QUESTIONS:

        generated_sql = generate_sql(item.question)

        validation_safe, reason = validate_sql(generated_sql)

        if item.expected_safe:
            safe_total += 1

            success = validation_safe

            if success:
                safe_correct += 1

        else:
            unsafe_total += 1

            success = not validation_safe

            if success:
                unsafe_blocked += 1

        if success:
            passed += 1
            print(f"[PASS] {item.id} {item.question}")

        else:
            failed += 1
            print(f"[FAIL] {item.id} {item.question}")

        results.append(
            {
                "id": item.id,
                "question": item.question,
                "expected_safe": item.expected_safe,
                "generated_sql": generated_sql,
                "validation_safe": validation_safe,
                "validation_reason": reason,
                "passed": success,
            }
        )

    metrics = calculate_metrics(
        total_questions=len(BENCHMARK_QUESTIONS),
        passed=passed,
        failed=failed,
        safe_total=safe_total,
        safe_correct=safe_correct,
        unsafe_total=unsafe_total,
        unsafe_blocked=unsafe_blocked,
    )

    report = {
        "summary": metrics,
        "results": results,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print()
    print("=" * 80)
    print("Benchmark Complete")
    print("=" * 80)

    print(f"Questions              : {metrics['questions']}")
    print(f"Passed                 : {metrics['passed']}")
    print(f"Failed                 : {metrics['failed']}")
    print(f"Intent Accuracy        : {metrics['intent_accuracy']:.2f}%")
    print(
        f"Unsafe Query Block Rate: "
        f"{metrics['unsafe_query_block_rate']:.2f}%"
    )
    print(f"Report Saved           : {REPORT_PATH}")



if __name__ == "__main__":
    run_benchmark()