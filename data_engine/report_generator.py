import json
from pathlib import Path


def make_json_serializable(data):
    """
    Convert nested AutoInsight results into
    JSON-serializable Python objects.
    """

    if isinstance(data, dict):

        return {
            str(key): make_json_serializable(value)
            for key, value in data.items()
            if key != "figure"
        }

    if isinstance(data, list):

        return [
            make_json_serializable(item)
            for item in data
        ]

    if hasattr(data, "item"):

        try:
            return data.item()
        except Exception:
            pass

    if hasattr(data, "isoformat"):

        try:
            return data.isoformat()
        except Exception:
            pass

    return data


def create_report(result):
    """
    Create a clean report structure from
    the complete AutoInsight pipeline result.
    """

    profile = result["profile"]
    cleaning = result["cleaning_report"]
    analysis = result["analysis"]

    report = {

        "dataset_overview": {

            "rows": profile["rows"],

            "columns": profile["columns"],

            "column_names":
                profile["column_names"]

        },

        "data_quality": {

            "duplicate_rows":
                profile["duplicate_rows"],

            "missing_values":
                profile["missing_values"],

            "rows_removed":
                cleaning["rows_removed"],

            "columns_removed":
                cleaning["columns_removed"],

            "outliers_detected":
                cleaning["outliers"]["total"]

        },

        "column_summary": {

            "numeric":
                profile["numeric_columns"],

            "categorical":
                profile["categorical_columns"],

            "date":
                [
                    column
                    for column, information
                    in result["detected_columns"].items()
                    if information["type"] == "date"
                ],

            "binary":
                [
                    column
                    for column, information
                    in result["detected_columns"].items()
                    if information["type"] == "binary"
                ],

            "identifier":
                [
                    column
                    for column, information
                    in result["detected_columns"].items()
                    if information["type"] == "identifier"
                ]

        },

        "analysis": analysis,

        "chart_recommendations":
            result["chart_recommendations"],

        "insights":
            result["insights"]

    }

    return report


def save_json_report(
    report,
    output_path="reports/autoinsight_report.json"
):
    """
    Save AutoInsight report as JSON.
    """

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    serializable_report = (
        make_json_serializable(report)
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            serializable_report,
            file,
            indent=4,
            ensure_ascii=False
        )

    return str(output_path)


def save_html_report(
    report,
    output_path="reports/autoinsight_report.html"
):
    """
    Save a simple HTML version of the report.
    """

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    overview = report[
        "dataset_overview"
    ]

    quality = report[
        "data_quality"
    ]

    columns = report[
        "column_summary"
    ]

    insights = report[
        "insights"
    ]

    recommendations = report[
        "chart_recommendations"
    ]

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>AutoInsight Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    background: #f5f7fa;
    color: #222;
}}

h1 {{
    margin-bottom: 5px;
}}

h2 {{
    margin-top: 35px;
}}

.card-container {{
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}}

.card {{
    background: white;
    padding: 20px;
    border-radius: 10px;
    min-width: 150px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

.card h3 {{
    margin: 0;
    font-size: 14px;
    color: #666;
}}

.card p {{
    font-size: 24px;
    font-weight: bold;
    margin: 10px 0 0;
}}

.section {{
    background: white;
    padding: 20px;
    margin-top: 20px;
    border-radius: 10px;
}}

li {{
    margin-bottom: 10px;
}}

table {{
    border-collapse: collapse;
    width: 100%;
}}

th, td {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}}

</style>

</head>

<body>

<h1>AutoInsight Report</h1>

<p>Automated Dataset Analysis Report</p>


<h2>Dataset Overview</h2>

<div class="card-container">

<div class="card">
<h3>Rows</h3>
<p>{overview["rows"]:,}</p>
</div>

<div class="card">
<h3>Columns</h3>
<p>{overview["columns"]}</p>
</div>

<div class="card">
<h3>Duplicates</h3>
<p>{quality["duplicate_rows"]:,}</p>
</div>

<div class="card">
<h3>Outliers</h3>
<p>{quality["outliers_detected"]:,}</p>
</div>

</div>


<h2>Column Summary</h2>

<div class="section">

<p>
<b>Numeric:</b>
{len(columns["numeric"])}
</p>

<p>
<b>Categorical:</b>
{len(columns["categorical"])}
</p>

<p>
<b>Binary:</b>
{len(columns["binary"])}
</p>

<p>
<b>Date:</b>
{len(columns["date"])}
</p>

<p>
<b>Identifier:</b>
{len(columns["identifier"])}
</p>

</div>


<h2>Insights</h2>

<div class="section">

<ul>
"""

    for insight in insights:

        html += (
            f"<li>{insight}</li>\n"
        )

    html += """
</ul>

</div>


<h2>Recommended Charts</h2>

<div class="section">

<table>

<tr>
<th>#</th>
<th>Chart</th>
<th>X</th>
<th>Y</th>
<th>Score</th>
</tr>
"""

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        chart_type = recommendation[
            "chart_type"
        ]

        x = recommendation.get(
            "x",
            "-"
        )

        y = recommendation.get(
            "y",
            "-"
        )

        score = recommendation.get(
            "score",
            "-"
        )

        html += f"""
<tr>
<td>{index}</td>
<td>{chart_type}</td>
<td>{x}</td>
<td>{y}</td>
<td>{score}</td>
</tr>
"""

    html += """
</table>

</div>

</body>

</html>
"""

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)

    return str(output_path)