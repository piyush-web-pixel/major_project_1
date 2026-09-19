
from data_engine.loader import load_file
from data_engine.column_detector import detect_columns
from data_engine.cleaner import clean_data
from data_engine.chart_recommender import recommend_charts


# =========================================================
# LOAD
# =========================================================

df = load_file("data/sample.csv")

# df = load_file('data/retail_sales_dataset.xlsx')

# =========================================================
# DETECT
# =========================================================

detected_columns = detect_columns(df)


# =========================================================
# CLEAN
# =========================================================

cleaned_df, cleaning_report = clean_data(
    df,
    detected_columns
)


# =========================================================
# RECOMMEND CHARTS
# =========================================================

recommendations = recommend_charts(
    cleaned_df,
    detected_columns
)


# =========================================================
# PRINT RESULTS
# =========================================================

print("\n========== CHART RECOMMENDATIONS ==========\n")

print(
    "Total Recommendations:",
    len(recommendations)
)


for index, recommendation in enumerate(
    recommendations,
    start=1
):

    print(
        f"\n{index}. "
        f"{recommendation['chart_type'].upper()}"
    )

    print(
        "   X:",
        recommendation["x"]
    )

    if "y" in recommendation:

        print(
            "   Y:",
            recommendation["y"]
        )

    if "aggregation" in recommendation:

        print(
            "   Aggregation:",
            recommendation["aggregation"]
        )

    print(
        "   Score:",
        recommendation["score"]
    )

    if "correlation" in recommendation:

        print(
            "   Correlation:",
            recommendation["correlation"]
        )

    print(
        "   Reason:",
        recommendation["reason"]
    )

