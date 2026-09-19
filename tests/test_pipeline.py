from data_engine.pipeline import (
    run_autoinsight
)


# ==========================================
# RUN AUTOINSIGHT
# ==========================================

result = run_autoinsight(
    "data/sample.csv",
    max_charts=10
)


# ==========================================
# PROFILE
# ==========================================

print(
    "\n========== PROFILE =========="
)

profile = result["profile"]

print(
    f"Rows: {profile['rows']}"
)

print(
    f"Columns: {profile['columns']}"
)


# ==========================================
# DETECTED COLUMNS
# ==========================================

print(
    "\n========== DETECTED COLUMNS =========="
)

for column, information in result[
    "detected_columns"
].items():

    print(
        f"{column} → "
        f"{information['type']} "
        f"({information['confidence']}%)"
    )


# ==========================================
# CLEANING REPORT
# ==========================================

print(
    "\n========== CLEANING REPORT =========="
)

cleaning = result[
    "cleaning_report"
]

print(
    f"Original Rows: "
    f"{cleaning['original_rows']}"
)

print(
    f"Final Rows: "
    f"{cleaning['final_rows']}"
)

print(
    f"Rows Removed: "
    f"{cleaning['rows_removed']}"
)

print(
    f"Columns Removed: "
    f"{cleaning['columns_removed']}"
)

print(
    f"Total Outliers Detected: "
    f"{cleaning['outliers']['total']}"
)


# ==========================================
# ANALYSIS
# ==========================================

print(
    "\n========== ANALYSIS =========="
)

analysis = result[
    "analysis"
]

print(
    f"Numeric Columns: "
    f"{len(analysis['numeric'])}"
)

print(
    f"Categorical Columns: "
    f"{len(analysis['categorical'])}"
)

print(
    f"Binary Columns: "
    f"{len(analysis['binary'])}"
)

print(
    f"Date Columns: "
    f"{len(analysis['date'])}"
)

print(
    f"Correlations Found: "
    f"{len(analysis['correlations'])}"
)


# ==========================================
# CHARTS
# ==========================================

print(
    "\n========== CHARTS =========="
)

charts = result[
    "charts"
]

successful_charts = sum(
    1
    for chart in charts
    if chart["figure"] is not None
)

failed_charts = len(charts) - successful_charts

print(
    f"Total Charts: {len(charts)}"
)

print(
    f"Successful: {successful_charts}"
)

print(
    f"Failed: {failed_charts}"
)


# ==========================================
# INSIGHTS
# ==========================================

print(
    "\n========== INSIGHTS =========="
)

insights = result[
    "insights"
]

print(
    f"Total Insights: {len(insights)}"
)

for index, insight in enumerate(
    insights[:10],
    start=1
):

    print(
        f"{index}. {insight}"
    )