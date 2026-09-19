from data_engine.loader import load_file
from data_engine.profiler import profile_data
from data_engine.column_detector import detect_columns
from data_engine.analyzer import analyze_data
from data_engine.insight_generator import (
    generate_insights
)


# ==========================================
# LOAD DATA
# ==========================================

df = load_file(
    "data/sample.csv"
)


# ==========================================
# PROFILE
# ==========================================

profile = profile_data(
    df
)


# ==========================================
# DETECT COLUMNS
# ==========================================

detected_columns = detect_columns(
    df
)


# ==========================================
# ANALYZE
# ==========================================

analysis = analyze_data(
    df,
    detected_columns
)


# ==========================================
# GENERATE INSIGHTS
# ==========================================

insights = generate_insights(
    profile,
    analysis
)


# ==========================================
# PRINT RESULTS
# ==========================================

print(
    "\n========== GENERATED INSIGHTS =========="
)

print(
    f"Total Insights: {len(insights)}"
)


for index, insight in enumerate(
    insights,
    start=1
):

    print(
        f"\n{index}. {insight}"
    )