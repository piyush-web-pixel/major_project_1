from pathlib import Path

from data_engine.pipeline import (
    run_autoinsight
)


# ==========================================
# CONFIGURATION
# ==========================================

FILE_PATH = "data/sample.csv"

JSON_REPORT = (
    "reports/autoinsight_report.json"
)

HTML_REPORT = (
    "reports/autoinsight_report.html"
)


# ==========================================
# RUN COMPLETE SYSTEM
# ==========================================

print(
    "\n=========================================="
)

print(
    "        AUTOINSIGHT FULL SYSTEM TEST"
)

print(
    "=========================================="
)


result = run_autoinsight(
    FILE_PATH,
    max_charts=10
)


# ==========================================
# VALIDATION
# ==========================================

validation = result[
    "validation"
]

assert validation["valid"] is True

print(
    "\n[PASS] Dataset validation"
)


# ==========================================
# PROFILE
# ==========================================

profile = result[
    "profile"
]

assert profile["rows"] > 0
assert profile["columns"] > 0

print(
    "[PASS] Dataset profiling"
)


# ==========================================
# COLUMN DETECTION
# ==========================================

detected_columns = result[
    "detected_columns"
]

assert len(
    detected_columns
) == profile["columns"]

print(
    "[PASS] Column detection"
)


# ==========================================
# CLEANING
# ==========================================

cleaning = result[
    "cleaning_report"
]

assert (
    cleaning["final_rows"] > 0
)

print(
    "[PASS] Data cleaning"
)


# ==========================================
# ANALYSIS
# ==========================================

analysis = result[
    "analysis"
]

assert "numeric" in analysis
assert "categorical" in analysis
assert "binary" in analysis
assert "date" in analysis
assert "correlations" in analysis

print(
    "[PASS] Data analysis"
)


# ==========================================
# CHART RECOMMENDATIONS
# ==========================================

recommendations = result[
    "chart_recommendations"
]

assert len(
    recommendations
) > 0

print(
    "[PASS] Chart recommendation"
)


# ==========================================
# CHART GENERATION
# ==========================================

charts = result[
    "charts"
]

successful_charts = sum(
    1
    for chart in charts
    if chart["figure"] is not None
)

assert successful_charts > 0

print(
    "[PASS] Chart generation"
)


# ==========================================
# INSIGHTS
# ==========================================

insights = result[
    "insights"
]

assert len(
    insights
) > 0

print(
    "[PASS] Insight generation"
)


# ==========================================
# REPORT
# ==========================================

report = result[
    "report"
]

assert (
    "dataset_overview"
    in report
)

assert (
    "data_quality"
    in report
)

assert (
    "analysis"
    in report
)

assert (
    "insights"
    in report
)

print(
    "[PASS] Report generation"
)


# ==========================================
# REPORT FILES
# ==========================================

assert Path(
    JSON_REPORT
).exists()

assert Path(
    HTML_REPORT
).exists()

print(
    "[PASS] JSON report file"
)

print(
    "[PASS] HTML report file"
)


# ==========================================
# FINAL SUMMARY
# ==========================================

print(
    "\n=========================================="
)

print(
    "       AUTOINSIGHT SYSTEM TEST PASSED"
)

print(
    "=========================================="
)

print(
    f"Rows              : {profile['rows']:,}"
)

print(
    f"Columns           : {profile['columns']}"
)

print(
    f"Detected Columns  : {len(detected_columns)}"
)

print(
    f"Charts Generated  : {successful_charts}"
)

print(
    f"Insights Generated: {len(insights)}"
)

print(
    f"Correlations      : "
    f"{len(analysis['correlations'])}"
)

print(
    "JSON Report       : READY"
)

print(
    "HTML Report       : READY"
)

print(
    "\nAutoInsight Engine V1 is working successfully."
)