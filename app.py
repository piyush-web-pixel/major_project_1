import streamlit as st
import pandas as pd
import tempfile
from pathlib import Path

from data_engine.pipeline import run_autoinsight


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AutoInsight",
    page_icon="📊",
    layout="wide"
)


# =====================================================
# TITLE
# =====================================================

st.title("📊 AutoInsight")

st.markdown(
    """
    **Automated Data Analysis & Business Intelligence Platform**

    Upload a CSV or Excel file and AutoInsight will automatically:
    
    - Profile your dataset
    - Detect column types
    - Clean the data
    - Analyze numerical and categorical patterns
    - Detect correlations
    - Recommend charts
    - Generate insights
    - Create reports
    """
)


# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx", "xls"]
)


# =====================================================
# ANALYZE
# =====================================================

if uploaded_file is not None:

    st.success(
        f"File uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🚀 Analyze Dataset",
        use_container_width=True
    ):

        with st.spinner(
            "AutoInsight is analyzing your dataset..."
        ):

            try:

                # -------------------------------------
                # SAVE TEMPORARY FILE
                # -------------------------------------

                suffix = Path(
                    uploaded_file.name
                ).suffix

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    temp_path = temp_file.name


                # -------------------------------------
                # RUN PIPELINE
                # -------------------------------------

                result = run_autoinsight(
                    temp_path,
                    max_charts=10
                )


                st.session_state[
                    "result"
                ] = result


                st.success(
                    "Analysis completed successfully!"
                )


            except Exception as error:

                st.error(
                    f"Analysis failed: {error}"
                )


# =====================================================
# DISPLAY RESULTS
# =====================================================

if "result" in st.session_state:

    result = st.session_state[
        "result"
    ]


    # =================================================
    # DATASET OVERVIEW
    # =================================================

    st.header("📌 Dataset Overview")

    profile = result[
        "profile"
    ]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rows",
        f"{profile['rows']:,}"
    )

    col2.metric(
        "Columns",
        profile["columns"]
    )

    col3.metric(
        "Duplicate Rows",
        f"{profile['duplicate_rows']:,}"
    )

    col4.metric(
        "Missing Columns",
        len(
            profile["missing_values"]
        )
    )


    # =================================================
    # DETECTED COLUMNS
    # =================================================

    st.header("🔍 Column Detection")

    detected = result[
        "detected_columns"
    ]

    detection_data = []

    for column, information in detected.items():

        detection_data.append({

            "Column":
                column,

            "Type":
                information["type"],

            "Confidence":
                f"{information['confidence']}%",

            "Unique Values":
                information["unique_values"],

            "Missing Values":
                information["missing_values"]

        })

    detection_df = pd.DataFrame(
        detection_data
    )

    st.dataframe(
        detection_df,
        use_container_width=True,
        hide_index=True
    )


    # =================================================
    # CLEANING REPORT
    # =================================================

    st.header("🧹 Data Cleaning")

    cleaning = result[
        "cleaning_report"
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Rows Removed",
        cleaning["rows_removed"]
    )

    col2.metric(
        "Columns Removed",
        cleaning["columns_removed"]
    )

    col3.metric(
        "Outliers Detected",
        f"{cleaning['outliers']['total']:,}"
    )


    # =================================================
    # ANALYSIS
    # =================================================

    st.header("📈 Analysis")

    analysis = result[
        "analysis"
    ]

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Numeric",
            "Categorical",
            "Dates",
            "Correlations"
        ]
    )


    # -----------------------------------------------
    # NUMERIC
    # -----------------------------------------------

    with tab1:

        numeric_data = []

        for column, stats in analysis[
            "numeric"
        ].items():

            numeric_data.append({

                "Column": column,
                "Mean": stats["mean"],
                "Median": stats["median"],
                "Min": stats["min"],
                "Max": stats["max"],
                "Std": stats["std"]

            })

        if numeric_data:

            st.dataframe(
                pd.DataFrame(
                    numeric_data
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No numeric columns detected."
            )


    # -----------------------------------------------
    # CATEGORICAL
    # -----------------------------------------------

    with tab2:

        categorical_data = []

        for column, stats in analysis[
            "categorical"
        ].items():

            categorical_data.append({

                "Column": column,

                "Unique Values":
                    stats["unique_values"],

                "Top Value":
                    stats["top_value"],

                "Top Value Count":
                    stats["top_value_count"]

            })

        if categorical_data:

            st.dataframe(
                pd.DataFrame(
                    categorical_data
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No categorical columns detected."
            )


    # -----------------------------------------------
    # DATES
    # -----------------------------------------------

    with tab3:

        date_data = []

        for column, stats in analysis[
            "date"
        ].items():

            date_data.append({

                "Column": column,

                "Start Date":
                    stats["start_date"],

                "End Date":
                    stats["end_date"],

                "Unique Dates":
                    stats["unique_dates"],

                "Days":
                    stats["days"]

            })

        if date_data:

            st.dataframe(
                pd.DataFrame(
                    date_data
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No date columns detected."
            )


    # -----------------------------------------------
    # CORRELATIONS
    # -----------------------------------------------

    with tab4:

        correlations = analysis[
            "correlations"
        ]

        if correlations:

            correlation_data = []

            for item in correlations:

                correlation_data.append({

                    "Column 1":
                        item["column_1"],

                    "Column 2":
                        item["column_2"],

                    "Correlation":
                        item["correlation"],

                    "Absolute Correlation":
                        item[
                            "absolute_correlation"
                        ]

                })

            st.dataframe(
                pd.DataFrame(
                    correlation_data
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Not enough numeric columns "
                "for correlation analysis."
            )


    # =================================================
    # CHARTS
    # =================================================

    st.header("📊 Recommended Charts")

    charts = result[
        "charts"
    ]

    successful_charts = [

        chart

        for chart in charts

        if chart["figure"] is not None

    ]

    for index, chart in enumerate(
        successful_charts,
        start=1
    ):

        recommendation = chart[
            "recommendation"
        ]

        st.subheader(
            f"{index}. "
            f"{recommendation['chart_type'].title()}"
        )

        st.plotly_chart(
            chart["figure"],
            use_container_width=True
        )


    # =================================================
    # INSIGHTS
    # =================================================

    st.header("💡 Automated Insights")

    insights = result[
        "insights"
    ]

    for index, insight in enumerate(
        insights,
        start=1
    ):

        st.write(
            f"**{index}.** {insight}"
        )


    # =================================================
    # REPORT
    # =================================================

    st.header("📄 Reports")

    report = result[
        "report"
    ]

    col1, col2 = st.columns(2)


    # -----------------------------------------------
    # JSON DOWNLOAD
    # -----------------------------------------------

    import json

    json_data = json.dumps(
        report,
        indent=4,
        ensure_ascii=False
    )

    col1.download_button(
        label="⬇️ Download JSON Report",
        data=json_data,
        file_name="autoinsight_report.json",
        mime="application/json",
        use_container_width=True
    )


    # -----------------------------------------------
    # HTML DOWNLOAD
    # -----------------------------------------------

    html_path = (
        "reports/autoinsight_report.html"
    )

    if Path(html_path).exists():

        with open(
            html_path,
            "r",
            encoding="utf-8"
        ) as file:

            html_data = file.read()

        col2.download_button(
            label="⬇️ Download HTML Report",
            data=html_data,
            file_name="autoinsight_report.html",
            mime="text/html",
            use_container_width=True
        )