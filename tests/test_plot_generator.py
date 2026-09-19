from data_engine.loader import load_file
from data_engine.column_detector import detect_columns
from data_engine.chart_recommender import recommend_charts
from data_engine.plot_generator import (
    generate_recommended_charts
)


# ==========================================
# LOAD DATA
# ==========================================

df = load_file(
    "data/sample.csv"
)

print("\n========== ORIGINAL DATA ==========")

print(df.shape)

print(df.columns.tolist())


# ==========================================
# DETECT COLUMNS
# ==========================================

detected_columns = detect_columns(
    df
)


# ==========================================
# RECOMMEND CHARTS
# ==========================================

recommendations = recommend_charts(
    df,
    detected_columns,
    max_charts=10
)


print(
    "\n========== RECOMMENDATIONS =========="
)

print(
    f"Total Recommendations: "
    f"{len(recommendations)}"
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
        f"   X: "
        f"{recommendation.get('x')}"
    )

    if recommendation.get("y"):

        print(
            f"   Y: "
            f"{recommendation.get('y')}"
        )

    if recommendation.get(
        "aggregation"
    ):

        print(
            f"   Aggregation: "
            f"{recommendation.get('aggregation')}"
        )


# ==========================================
# GENERATE PLOTLY CHARTS
# ==========================================

charts = generate_recommended_charts(
    df,
    recommendations
)


print(
    "\n========== GENERATED CHARTS =========="
)

print(
    f"Total Generated: "
    f"{len(charts)}"
)


for index, chart in enumerate(
    charts,
    start=1
):

    recommendation = chart[
        "recommendation"
    ]

    if chart["figure"] is not None:

        print(
            f"{index}. "
            f"{recommendation['chart_type'].upper()} "
            f"✓ Generated"
        )

    else:

        print(
            f"{index}. "
            f"{recommendation['chart_type'].upper()} "
            f"✗ Failed"
        )

        print(
            f"   Error: "
            f"{chart['error']}"
        )


# ==========================================
# SAVE FIRST CHART
# ==========================================

if charts:

    first_chart = charts[0]["figure"]

    if first_chart is not None:

        first_chart.write_html(
            "first_chart.html"
        )

        print(
            "\nFirst chart saved as:"
        )

        print(
            "first_chart.html"
        )