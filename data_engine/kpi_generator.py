import pandas as pd


def generate_kpis(df):

    kpis = []

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns


    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) == 0:
            continue


        total = series.sum()
        average = series.mean()
        maximum = series.max()


        kpis.append({

            "title": f"Total {column}",

            "value": total,

            "formatted_value":
                format_number(total),

            "metric": "sum",

            "column": column

        })


    return kpis


def format_number(value):

    value = float(value)


    if abs(value) >= 1_000_000_000:

        return f"{value / 1_000_000_000:.2f}B"


    if abs(value) >= 1_000_000:

        return f"{value / 1_000_000:.2f}M"


    if abs(value) >= 1_000:

        return f"{value / 1_000:.2f}K"


    return f"{value:,.2f}"