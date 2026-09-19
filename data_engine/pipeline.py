from data_engine.loader import load_file
from data_engine.profiler import profile_data
from data_engine.column_detector import detect_columns
from data_engine.cleaner import clean_data
from data_engine.analyzer import analyze_data
from data_engine.chart_recommender import recommend_charts
from data_engine.plot_generator import (
    generate_recommended_charts
)
from data_engine.insight_generator import (
    generate_insights
)

from data_engine.validator import (
    validate_file_path,
    validate_dataset
)

from data_engine.report_generator import (
    create_report
)

def run_autoinsight(
    file_path,
    max_charts=10
):
    # ==========================================
    # 1. VALIDATE FILE
    # ==========================================

    validate_file_path(file_path)


    # ==========================================
    # 2. LOAD DATA
    # ==========================================

    df = load_file(file_path)


    # ==========================================
    # 3. VALIDATE DATASET
    # ==========================================

    validation_report = validate_dataset(df)


    # ==========================================
    # 4. PROFILE DATA
    # ==========================================

    profile = profile_data(df)


    # ==========================================
    # 5. DETECT COLUMNS
    # ==========================================

    detected_columns = detect_columns(df)


    # ==========================================
    # 6. CLEAN DATA
    # ==========================================

    cleaned_df, cleaning_report = clean_data(
        df,
        detected_columns
    )


    # ==========================================
    # 7. ANALYZE DATA
    # ==========================================

    analysis = analyze_data(
        cleaned_df,
        detected_columns
    )


    # ==========================================
    # 8. RECOMMEND CHARTS
    # ==========================================

    chart_recommendations = recommend_charts(
        cleaned_df,
        detected_columns,
        max_charts=max_charts
    )


    # ==========================================
    # 9. GENERATE CHARTS
    # ==========================================

    charts = generate_recommended_charts(
        cleaned_df,
        chart_recommendations
    )


    # ==========================================
    # 10. GENERATE INSIGHTS
    # ==========================================

    insights = generate_insights(
        profile,
        analysis
    )


    # ==========================================
    # 11. BUILD RESULT
    # ==========================================

    result = {

        "validation": validation_report,

        "profile": profile,

        "detected_columns":
            detected_columns,

        "cleaning_report":
            cleaning_report,

        "analysis":
            analysis,

        "chart_recommendations":
            chart_recommendations,

        "charts":
            charts,

        "insights":
            insights

    }


    # ==========================================
    # 12. CREATE REPORT
    # ==========================================

    report = create_report(
        result
    )

    result["report"] = report


    return result