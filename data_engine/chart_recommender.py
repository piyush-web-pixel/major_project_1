import pandas as pd


# =========================================================
# COLUMN GROUPS
# =========================================================

def get_column_groups(
    df,
    detected_columns
):

    date_columns = []
    numeric_columns = []
    categorical_columns = []
    binary_columns = []

    for column, information in detected_columns.items():

        if column not in df.columns:
            continue

        column_type = information["type"]

        if column_type == "date":
            date_columns.append(column)

        elif column_type == "numeric":
            numeric_columns.append(column)

        elif column_type == "categorical":
            categorical_columns.append(column)

        elif column_type == "binary":
            binary_columns.append(column)

    return (
        date_columns,
        numeric_columns,
        categorical_columns,
        binary_columns
    )


# =========================================================
# VARIATION SCORE
# =========================================================

def calculate_variation_score(series):

    series = series.dropna()

    if len(series) == 0:
        return 0

    unique_ratio = (
        series.nunique() / len(series)
    )

    if unique_ratio >= 0.50:
        return 20

    elif unique_ratio >= 0.20:
        return 15

    elif unique_ratio >= 0.05:
        return 10

    return 5


# =========================================================
# CARDINALITY SCORE
# =========================================================

def calculate_cardinality_score(series):

    unique_count = (
        series.nunique(dropna=True)
    )

    if 2 <= unique_count <= 5:
        return 20

    elif 6 <= unique_count <= 10:
        return 15

    elif 11 <= unique_count <= 20:
        return 8

    return 0


# =========================================================
# TIME CHARTS
# =========================================================

def recommend_time_charts(
    df,
    date_columns,
    numeric_columns
):

    recommendations = []

    for date_column in date_columns:

        for numeric_column in numeric_columns:

            variation_score = (
                calculate_variation_score(
                    df[numeric_column]
                )
            )

            score = 60 + variation_score

            recommendations.append({

                "chart_type": "line",

                "x": date_column,

                "y": numeric_column,

                "aggregation": "mean",

                "score": score,

                "reason": (
                    f"Shows how {numeric_column} "
                    f"changes over time"
                )
            })

    return recommendations


# =========================================================
# CATEGORY CHARTS
# =========================================================

def recommend_category_charts(
    df,
    categorical_columns,
    numeric_columns
):

    recommendations = []

    for categorical_column in categorical_columns:

        cardinality_score = (
            calculate_cardinality_score(
                df[categorical_column]
            )
        )

        if cardinality_score == 0:
            continue

        for numeric_column in numeric_columns:

            variation_score = (
                calculate_variation_score(
                    df[numeric_column]
                )
            )

            score = (
                40
                + cardinality_score
                + variation_score
            )

            recommendations.append({

                "chart_type": "bar",

                "x": categorical_column,

                "y": numeric_column,

                "aggregation": "mean",

                "score": score,

                "reason": (
                    f"Compares average "
                    f"{numeric_column} across "
                    f"{categorical_column}"
                )
            })

    return recommendations


# =========================================================
# SCATTER CHARTS
# =========================================================

def recommend_scatter_charts(
    df,
    numeric_columns
):

    recommendations = []

    if len(numeric_columns) < 2:
        return recommendations

    correlation_matrix = (
        df[numeric_columns].corr()
    )

    for i in range(
        len(numeric_columns)
    ):

        for j in range(
            i + 1,
            len(numeric_columns)
        ):

            column_1 = numeric_columns[i]
            column_2 = numeric_columns[j]

            correlation = (
                correlation_matrix.loc[
                    column_1,
                    column_2
                ]
            )

            if pd.isna(correlation):
                continue

            absolute_correlation = abs(
                float(correlation)
            )

            # Ignore very weak relationships
            if absolute_correlation < 0.20:
                continue

            correlation_score = (
                absolute_correlation * 100
            )

            recommendations.append({

                "chart_type": "scatter",

                "x": column_1,

                "y": column_2,

                "score": round(
                    correlation_score,
                    2
                ),

                "correlation": round(
                    float(correlation),
                    4
                ),

                "reason": (
                    "Shows the relationship "
                    f"between {column_1} "
                    f"and {column_2}"
                )
            })

    return recommendations


# =========================================================
# DISTRIBUTION CHARTS
# =========================================================

def recommend_distribution_charts(
    df,
    categorical_columns,
    binary_columns
):

    recommendations = []

    # Categorical distributions
    for column in categorical_columns:

        cardinality_score = (
            calculate_cardinality_score(
                df[column]
            )
        )

        if cardinality_score == 0:
            continue

        score = (
            30
            + cardinality_score
        )

        recommendations.append({

            "chart_type": "count",

            "x": column,

            "score": score,

            "reason": (
                f"Shows distribution "
                f"of {column}"
            )
        })

    # Binary distributions
    for column in binary_columns:

        recommendations.append({

            "chart_type": "count",

            "x": column,

            "score": 45,

            "reason": (
                f"Shows distribution "
                f"of {column}"
            )
        })

    return recommendations


# =========================================================
# REMOVE DUPLICATES
# =========================================================

def remove_duplicate_charts(
    recommendations
):

    unique = {}

    for recommendation in recommendations:

        key = (
            recommendation["chart_type"],
            recommendation.get("x"),
            recommendation.get("y")
        )

        if (
            key not in unique
            or
            recommendation["score"]
            > unique[key]["score"]
        ):

            unique[key] = recommendation

    return list(
        unique.values()
    )


# =========================================================
# DIVERSITY-AWARE SELECTION
# =========================================================

def select_diverse_charts(
    recommendations,
    max_charts=10
):

    selected = []

    used_chart_types = set()

    used_pairs = set()

    # -----------------------------------------------------
    # STEP 1
    # Sort by score
    # -----------------------------------------------------

    recommendations = sorted(
        recommendations,
        key=lambda x: x["score"],
        reverse=True
    )

    # -----------------------------------------------------
    # STEP 2
    # Select high quality + diverse charts
    # -----------------------------------------------------

    for recommendation in recommendations:

        if len(selected) >= max_charts:
            break

        chart_type = (
            recommendation["chart_type"]
        )

        x = recommendation.get("x")
        y = recommendation.get("y")

        pair = (
            x,
            y
        )

        # -------------------------------------------------
        # Avoid too many same chart types initially
        # -------------------------------------------------

        chart_type_count = sum(
            1
            for item in selected
            if item["chart_type"]
            == chart_type
        )

        # Maximum same chart type = 4
        if chart_type_count >= 4:
            continue

        # -------------------------------------------------
        # Avoid duplicate x/y combinations
        # -------------------------------------------------

        if pair in used_pairs:
            continue

        # -------------------------------------------------
        # Prefer diversity
        # -------------------------------------------------

        if (
            len(selected) < 4
            and chart_type in used_chart_types
        ):

            continue

        selected.append(
            recommendation
        )

        used_chart_types.add(
            chart_type
        )

        used_pairs.add(
            pair
        )

    # -----------------------------------------------------
    # STEP 3
    # Fill remaining slots
    # -----------------------------------------------------

    if len(selected) < max_charts:

        for recommendation in recommendations:

            if len(selected) >= max_charts:
                break

            if recommendation in selected:
                continue

            x = recommendation.get("x")
            y = recommendation.get("y")

            pair = (
                x,
                y
            )

            if pair in used_pairs:
                continue

            selected.append(
                recommendation
            )

            used_pairs.add(
                pair
            )

    return selected


# =========================================================
# MAIN RECOMMENDER
# =========================================================

def recommend_charts(
    df,
    detected_columns,
    max_charts=10
):

    (
        date_columns,
        numeric_columns,
        categorical_columns,
        binary_columns
    ) = get_column_groups(
        df,
        detected_columns
    )

    recommendations = []

    # -----------------------------------------------------
    # TIME
    # -----------------------------------------------------

    recommendations.extend(
        recommend_time_charts(
            df,
            date_columns,
            numeric_columns
        )
    )

    # -----------------------------------------------------
    # CATEGORY
    # -----------------------------------------------------

    recommendations.extend(
        recommend_category_charts(
            df,
            categorical_columns,
            numeric_columns
        )
    )

    # -----------------------------------------------------
    # SCATTER
    # -----------------------------------------------------

    recommendations.extend(
        recommend_scatter_charts(
            df,
            numeric_columns
        )
    )

    # -----------------------------------------------------
    # DISTRIBUTION
    # -----------------------------------------------------

    recommendations.extend(
        recommend_distribution_charts(
            df,
            categorical_columns,
            binary_columns
        )
    )

    # -----------------------------------------------------
    # REMOVE DUPLICATES
    # -----------------------------------------------------

    recommendations = (
        remove_duplicate_charts(
            recommendations
        )
    )

    # -----------------------------------------------------
    # DIVERSITY-AWARE SELECTION
    # -----------------------------------------------------

    recommendations = (
        select_diverse_charts(
            recommendations,
            max_charts
        )
    )

    return recommendations