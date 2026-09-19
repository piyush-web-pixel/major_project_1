from data_engine.pipeline import (
    run_autoinsight
)

from data_engine.report_generator import (
    create_report,
    save_json_report,
    save_html_report
)


# ==========================================
# RUN PIPELINE
# ==========================================

result = run_autoinsight(
    "data/sample.csv",
    max_charts=10
)


# ==========================================
# CREATE REPORT
# ==========================================

report = create_report(
    result
)


print(
    "\n========== REPORT CREATED =========="
)

print(
    "Dataset rows:",
    report[
        "dataset_overview"
    ]["rows"]
)

print(
    "Dataset columns:",
    report[
        "dataset_overview"
    ]["columns"]
)

print(
    "Outliers:",
    report[
        "data_quality"
    ]["outliers_detected"]
)

print(
    "Insights:",
    len(
        report["insights"]
    )
)

print(
    "Chart recommendations:",
    len(
        report[
            "chart_recommendations"
        ]
    )
)


# ==========================================
# SAVE JSON
# ==========================================

json_path = save_json_report(
    report
)

print(
    "\nJSON report saved:"
)

print(json_path)


# ==========================================
# SAVE HTML
# ==========================================

html_path = save_html_report(
    report
)

print(
    "\nHTML report saved:"
)

print(html_path)