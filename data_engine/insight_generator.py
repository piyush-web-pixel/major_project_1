import pandas as pd


def generate_dataset_insight(profile):
    """
    Generate basic dataset-level insights.
    """

    insights = []

    rows = profile.get("rows", 0)
    columns = profile.get("columns", 0)

    insights.append(
        f"Dataset contains {rows:,} rows and "
        f"{columns} columns."
    )

    duplicate_rows = profile.get(
        "duplicate_rows", 0
    )

    if duplicate_rows > 0:
        insights.append(
            f"Dataset contains {duplicate_rows:,} "
            f"duplicate rows."
        )
    else:
        insights.append(
            "Dataset contains no duplicate rows."
        )

    return insights


def generate_missing_value_insights(profile):
    """
    Generate insights about missing values.
    """

    insights = []

    missing_values = profile.get(
        "missing_values", {}
    )

    if not missing_values:

        insights.append(
            "No missing values were detected."
        )

        return insights

    total_missing = sum(
        missing_values.values()
    )

    insights.append(
        f"Dataset contains {total_missing:,} "
        f"missing values across "
        f"{len(missing_values)} columns."
    )

    return insights


def generate_numeric_insights(analysis):
    """
    Generate insights from numeric statistics.
    """

    insights = []

    numeric_data = analysis.get(
        "numeric", {}
    )

    for column, stats in numeric_data.items():

        mean = stats["mean"]
        median = stats["median"]
        minimum = stats["min"]
        maximum = stats["max"]

        insights.append(
            f"Average {column} is "
            f"{mean:.2f}, with values ranging "
            f"from {minimum:.2f} to {maximum:.2f}."
        )

        if mean > median * 1.10:

            insights.append(
                f"{column} appears to be "
                f"right-skewed because its mean "
                f"is noticeably higher than its median."
            )

    return insights


def generate_categorical_insights(analysis):
    """
    Generate insights from categorical columns.
    """

    insights = []

    categorical_data = analysis.get(
        "categorical", {}
    )

    for column, stats in categorical_data.items():

        unique_values = stats[
            "unique_values"
        ]

        top_value = stats[
            "top_value"
        ]

        top_count = stats[
            "top_value_count"
        ]

        insights.append(
            f"{column} contains "
            f"{unique_values} unique categories. "
            f"The most frequent value is "
            f"'{top_value}' with "
            f"{top_count:,} records."
        )

    return insights


def generate_binary_insights(analysis):
    """
    Generate insights from binary columns.
    """

    insights = []

    binary_data = analysis.get(
        "binary", {}
    )

    for column, stats in binary_data.items():

        distribution = stats.get(
            "distribution", {}
        )

        if not distribution:
            continue

        top_value = max(
            distribution,
            key=distribution.get
        )

        top_count = distribution[
            top_value
        ]

        insights.append(
            f"{column} has "
            f"{stats['unique_values']} "
            f"unique values. "
            f"Value '{top_value}' appears "
            f"{top_count:,} times."
        )

    return insights


def generate_date_insights(analysis):
    """
    Generate insights from date columns.
    """

    insights = []

    date_data = analysis.get(
        "date", {}
    )

    for column, stats in date_data.items():

        insights.append(
            f"{column} covers the period from "
            f"{stats['start_date']} to "
            f"{stats['end_date']} "
            f"({stats['days']} days)."
        )

    return insights


def generate_correlation_insights(analysis):
    """
    Generate insights from correlations.
    """

    insights = []

    correlations = analysis.get(
        "correlations", []
    )

    for relationship in correlations:

        correlation = relationship[
            "correlation"
        ]

        column_1 = relationship[
            "column_1"
        ]

        column_2 = relationship[
            "column_2"
        ]

        absolute_correlation = abs(
            correlation
        )

        if absolute_correlation >= 0.80:

            strength = "very strong"

        elif absolute_correlation >= 0.60:

            strength = "strong"

        elif absolute_correlation >= 0.40:

            strength = "moderate"

        elif absolute_correlation >= 0.20:

            strength = "weak"

        else:

            strength = "very weak"

        direction = (
            "positive"
            if correlation > 0
            else "negative"
        )

        insights.append(
            f"{column_1} and {column_2} "
            f"have a {strength} {direction} "
            f"relationship "
            f"(correlation: {correlation:.4f})."
        )

    return insights


def generate_insights(
    profile,
    analysis
):
    """
    Generate complete dataset insights.
    """

    insights = []

    insights.extend(
        generate_dataset_insight(
            profile
        )
    )

    insights.extend(
        generate_missing_value_insights(
            profile
        )
    )

    insights.extend(
        generate_numeric_insights(
            analysis
        )
    )

    insights.extend(
        generate_categorical_insights(
            analysis
        )
    )

    insights.extend(
        generate_binary_insights(
            analysis
        )
    )

    insights.extend(
        generate_date_insights(
            analysis
        )
    )

    insights.extend(
        generate_correlation_insights(
            analysis
        )
    )

    return insights