import pandas as pd
import numpy as np


# =========================================================
# NUMERIC ANALYSIS
# =========================================================

def analyze_numeric_columns(df, detected_columns):

    result = {}

    for column, information in detected_columns.items():

        if column not in df.columns:
            continue

        if information["type"] != "numeric":
            continue

        series = df[column].dropna()

        if len(series) == 0:
            continue

        result[column] = {

            "count": int(series.count()),

            "mean": round(
                float(series.mean()),
                4
            ),

            "median": round(
                float(series.median()),
                4
            ),

            "std": round(
                float(series.std()),
                4
            ),

            "min": round(
                float(series.min()),
                4
            ),

            "max": round(
                float(series.max()),
                4
            ),

            "q1": round(
                float(series.quantile(0.25)),
                4
            ),

            "q3": round(
                float(series.quantile(0.75)),
                4
            )
        }

    return result


# =========================================================
# KPI ANALYSIS
# =========================================================

def generate_kpis(df, detected_columns):

    kpis = []

    # -----------------------------------------------------
    # Keywords used to identify business-important columns
    # -----------------------------------------------------

    metric_rules = {

        "sum": [
            "sales",
            "revenue",
            "amount",
            "profit",
            "income",
            "quantity",
            "units sold",
            "units_sold",
            "demand",
            "orders",
            "order",
            "transactions",
            "transaction"
        ],

        "average": [
            "price",
            "discount",
            "rating",
            "score",
            "age",
            "salary",
            "cost",
            "margin"
        ],

        "inventory": [
            "inventory",
            "stock"
        ]
    }


    # -----------------------------------------------------
    # Get numeric columns
    # -----------------------------------------------------

    numeric_columns = []

    for column, information in detected_columns.items():

        if column not in df.columns:
            continue

        if information["type"] == "numeric":
            numeric_columns.append(column)


    # -----------------------------------------------------
    # Generate KPIs
    # -----------------------------------------------------

    for column in numeric_columns:

        series = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if series.empty:
            continue


        column_lower = column.lower().replace("_", " ")


        # =============================================
        # Decide KPI aggregation
        # =============================================

        aggregation = None
        title = None


        # Inventory / Stock
        if any(
            keyword in column_lower
            for keyword in metric_rules["inventory"]
        ):

            aggregation = "sum"
            title = f"Total {column}"


        # SUM metrics
        elif any(
            keyword in column_lower
            for keyword in metric_rules["sum"]
        ):

            aggregation = "sum"
            title = f"Total {column}"


        # AVERAGE metrics
        elif any(
            keyword in column_lower
            for keyword in metric_rules["average"]
        ):

            aggregation = "average"
            title = f"Average {column}"


        # Unknown numeric column
        else:

            aggregation = "average"
            title = f"Average {column}"


        # =============================================
        # Calculate value
        # =============================================

        if aggregation == "sum":

            value = series.sum()

        else:

            value = series.mean()


        # =============================================
        # Add KPI
        # =============================================

        kpis.append({

            "title": title,

            "column": column,

            "aggregation": aggregation,

            "value": round(
                float(value),
                2
            ),

            "formatted_value": format_kpi_value(
                value
            )

        })


    # -----------------------------------------------------
    # Limit KPIs
    # -----------------------------------------------------

    return kpis[:6]


# =========================================================
# KPI VALUE FORMATTER
# =========================================================

def format_kpi_value(value):

    value = float(value)

    absolute_value = abs(value)


    if absolute_value >= 1_000_000_000:

        return f"{value / 1_000_000_000:.2f}B"


    if absolute_value >= 1_000_000:

        return f"{value / 1_000_000:.2f}M"


    if absolute_value >= 1_000:

        return f"{value / 1_000:.2f}K"


    if value.is_integer():

        return f"{int(value):,}"


    return f"{value:,.2f}"




# =========================================================
# CATEGORICAL ANALYSIS
# =========================================================

def analyze_categorical_columns(
    df,
    detected_columns
):

    result = {}

    for column, information in detected_columns.items():

        if column not in df.columns:
            continue

        if information["type"] != "categorical":
            continue

        series = df[column].dropna()

        if len(series) == 0:
            continue

        value_counts = (
            series
            .value_counts()
            .head(10)
        )

        top_value = value_counts.index[0]

        result[column] = {

            "unique_values": int(
                series.nunique()
            ),

            "top_value": str(
                top_value
            ),

            "top_value_count": int(
                value_counts.iloc[0]
            ),

            "distribution": {
                str(key): int(value)
                for key, value
                in value_counts.items()
            }
        }

    return result


# =========================================================
# BINARY ANALYSIS
# =========================================================

def analyze_binary_columns(
    df,
    detected_columns
):

    result = {}

    for column, information in detected_columns.items():

        if column not in df.columns:
            continue

        if information["type"] != "binary":
            continue

        series = df[column].dropna()

        if len(series) == 0:
            continue

        value_counts = series.value_counts()

        result[column] = {

            "unique_values": int(
                series.nunique()
            ),

            "distribution": {
                str(key): int(value)
                for key, value
                in value_counts.items()
            }
        }

    return result


# =========================================================
# DATE ANALYSIS
# =========================================================

def analyze_date_columns(
    df,
    detected_columns
):

    result = {}

    for column, information in detected_columns.items():

        if column not in df.columns:
            continue

        if information["type"] != "date":
            continue

        series = pd.to_datetime(
            df[column],
            errors="coerce"
        ).dropna()

        if len(series) == 0:
            continue

        start_date = series.min()
        end_date = series.max()

        result[column] = {

            "start_date": str(
                start_date.date()
            ),

            "end_date": str(
                end_date.date()
            ),

            "unique_dates": int(
                series.nunique()
            ),

            "days": int(
                (end_date - start_date).days
            )
        }

    return result


# =========================================================
# CORRELATION ANALYSIS
# =========================================================
def analyze_correlations(df, detected_columns):

    numeric_columns = []

    for column, information in detected_columns.items():

        if column not in df.columns:
            continue

        if information["type"] == "numeric":
            numeric_columns.append(column)

    if len(numeric_columns) < 2:
        return []

    correlation_matrix = (
        df[numeric_columns]
        .corr()
    )

    relationships = []

    # Only take upper triangle
    for i in range(len(numeric_columns)):

        for j in range(i + 1, len(numeric_columns)):

            column_1 = numeric_columns[i]
            column_2 = numeric_columns[j]

            correlation = correlation_matrix.loc[
                column_1,
                column_2
            ]

            if pd.isna(correlation):
                continue

            relationships.append({

                "column_1": column_1,

                "column_2": column_2,

                "correlation": round(
                    float(correlation),
                    4
                ),

                "absolute_correlation": round(
                    abs(float(correlation)),
                    4
                )
            })

    # Strongest relationships first
    relationships.sort(
        key=lambda x: x["absolute_correlation"],
        reverse=True
    )

    return relationships


# =========================================================
# MAIN ANALYZER
# =========================================================
def analyze_data(
    df,
    detected_columns
):

    analysis = {

        "numeric": analyze_numeric_columns(
            df,
            detected_columns
        ),

        "categorical": analyze_categorical_columns(
            df,
            detected_columns
        ),

        "binary": analyze_binary_columns(
            df,
            detected_columns
        ),

        "date": analyze_date_columns(
            df,
            detected_columns
        ),

        "correlations": analyze_correlations(
            df,
            detected_columns
        ),

        "kpis": generate_kpis(
            df,
            detected_columns
        )
    }

    return analysis