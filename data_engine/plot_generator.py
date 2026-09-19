import pandas as pd
import plotly.express as px


def aggregate_data(df, x, y, aggregation="mean"):
    """
    Aggregate numeric data for bar/line charts.
    """

    if aggregation == "sum":
        result = df.groupby(x, as_index=False)[y].sum()

    elif aggregation == "median":
        result = df.groupby(x, as_index=False)[y].median()

    elif aggregation == "count":
        result = df.groupby(x, as_index=False)[y].count()

    else:
        result = df.groupby(x, as_index=False)[y].mean()

    return result


def generate_line_chart(
    df,
    x,
    y,
    aggregation="mean"
):
    """
    Generate a line chart.
    """

    chart_data = aggregate_data(
        df,
        x,
        y,
        aggregation
    )

    chart_data = chart_data.sort_values(
        by=x
    )

    fig = px.line(
        chart_data,
        x=x,
        y=y,
        title=f"{y} over {x}",
        markers=True
    )

    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        template="plotly_white"
    )

    return fig


def generate_bar_chart(
    df,
    x,
    y,
    aggregation="mean"
):
    """
    Generate a bar chart.
    """

    chart_data = aggregate_data(
        df,
        x,
        y,
        aggregation
    )

    fig = px.bar(
        chart_data,
        x=x,
        y=y,
        title=f"{y} by {x}"
    )

    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        template="plotly_white"
    )

    return fig

def generate_scatter_chart(
    df,
    x,
    y
):
    """
    Generate an interactive scatter plot.
    """

    fig = px.scatter(
        df,
        x=x,
        y=y,
        title=f"{y} vs {x}"
    )

    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        template="plotly_white"
    )

    return fig
def generate_count_chart(
    df,
    x
):
    """
    Generate a count/distribution chart.
    """

    fig = px.histogram(
        df,
        x=x,
        title=f"Distribution of {x}"
    )

    fig.update_layout(
        xaxis_title=x,
        yaxis_title="Count",
        template="plotly_white"
    )

    return fig


def generate_chart(
    df,
    recommendation
):
    """
    Generate a Plotly chart from
    a chart recommendation.
    """

    chart_type = recommendation["chart_type"]

    x = recommendation.get("x")
    y = recommendation.get("y")

    aggregation = recommendation.get(
        "aggregation",
        "mean"
    )

    if x not in df.columns:
        raise ValueError(
            f"Column '{x}' not found in dataframe."
        )

    if y is not None and y not in df.columns:
        raise ValueError(
            f"Column '{y}' not found in dataframe."
        )

    if chart_type == "line":

        return generate_line_chart(
            df,
            x,
            y,
            aggregation
        )

    elif chart_type == "bar":

        return generate_bar_chart(
            df,
            x,
            y,
            aggregation
        )

    elif chart_type == "scatter":

        return generate_scatter_chart(
            df,
            x,
            y
        )

    elif chart_type == "count":

        return generate_count_chart(
            df,
            x
        )

    else:
        raise ValueError(
            f"Unsupported chart type: {chart_type}"
        )


def generate_recommended_charts(
    df,
    recommendations
):
    """
    Generate Plotly figures for
    all recommended charts.
    """

    charts = []

    for recommendation in recommendations:

        try:

            fig = generate_chart(
                df,
                recommendation
            )

            charts.append({
                "recommendation": recommendation,
                "figure": fig
            })

        except Exception as error:

            charts.append({
                "recommendation": recommendation,
                "figure": None,
                "error": str(error)
            })

    return charts