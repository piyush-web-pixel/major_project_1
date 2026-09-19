const API_URL =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
        ? "http://127.0.0.1:8000/api/analyze/"
        : "https://major-project-1-1-diwh.onrender.com/api/analyze/";
// =====================================================
// ELEMENTS
// =====================================================

const fileInput = document.getElementById("fileInput");
const uploadBox = document.getElementById("uploadBox");
const fileName = document.getElementById("fileName");
const analyzeBtn = document.getElementById("analyzeBtn");

const loading = document.getElementById("loading");
const errorBox = document.getElementById("errorBox");
const dashboard = document.getElementById("dashboard");

const datasetFile = document.getElementById("datasetFile");
const kpiContainer = document.getElementById("kpiContainer");

const cleaningContainer =
    document.getElementById("cleaningContainer");

const columnCount =
    document.getElementById("columnCount");

const columnsContainer =
    document.getElementById("columnsContainer");

const chartsContainer =
    document.getElementById("chartsContainer");

const insightsContainer =
    document.getElementById("insightsContainer");


// =====================================================
// FILE SELECT
// =====================================================

fileInput.addEventListener("change", function () {

    if (!this.files.length) {
        return;
    }

    const file = this.files[0];

    fileName.textContent = file.name;

    analyzeBtn.disabled = false;

    uploadBox.classList.add("has-file");

});


// =====================================================
// DRAG OVER
// =====================================================

uploadBox.addEventListener("dragover", function (event) {

    event.preventDefault();

    uploadBox.classList.add("dragging");

});


// =====================================================
// DRAG LEAVE
// =====================================================

uploadBox.addEventListener("dragleave", function () {

    uploadBox.classList.remove("dragging");

});


// =====================================================
// DROP FILE
// =====================================================

uploadBox.addEventListener("drop", function (event) {

    event.preventDefault();

    uploadBox.classList.remove("dragging");

    const files = event.dataTransfer.files;

    if (!files.length) {
        return;
    }

    fileInput.files = files;

    const file = files[0];

    fileName.textContent = file.name;

    analyzeBtn.disabled = false;

    uploadBox.classList.add("has-file");

});


// =====================================================
// ANALYZE BUTTON
// =====================================================

analyzeBtn.addEventListener(
    "click",
    analyzeDataset
);


// =====================================================
// ANALYZE DATASET
// =====================================================

async function analyzeDataset() {

    const file = fileInput.files[0];


    if (!file) {

        showError(
            "Please select a CSV or Excel file first."
        );

        return;
    }


    hideError();

    dashboard.classList.add("hidden");

    loading.classList.remove("hidden");

    analyzeBtn.disabled = true;


    const formData = new FormData();

    formData.append(
        "file",
        file
    );


    try {

        console.log(
            "Uploading:",
            file.name
        );


        const response = await fetch(
            API_URL,
            {
                method: "POST",
                body: formData
            }
        );


        const data =
            await response.json();


        console.log(
            "API Response:",
            data
        );


        if (!response.ok) {

            throw new Error(
                data.message ||
                "Dataset analysis failed."
            );

        }


        if (data.status !== "success") {

            throw new Error(
                data.message ||
                "Analysis failed."
            );

        }


        renderDashboard(data);

    }


    catch (error) {

        console.error(
            "Analysis Error:",
            error
        );


        showError(
            error.message ||
            "Something went wrong."
        );

    }


    finally {

        loading.classList.add("hidden");

        analyzeBtn.disabled = false;

    }

}


// =====================================================
// RENDER DASHBOARD
// =====================================================

function renderDashboard(data) {

    dashboard.classList.remove(
        "hidden"
    );


    renderDatasetInfo(data);

    renderKPIs(data);

    renderCleaning(data);

    renderColumns(data);

    renderCharts(data);

    renderInsights(data);


    dashboard.scrollIntoView({
        behavior: "smooth"
    });

}


// =====================================================
// DATASET INFO
// =====================================================

function renderDatasetInfo(data) {

    datasetFile.textContent =
        data.file_name ||
        "Dataset";

}


// =====================================================
// DYNAMIC BUSINESS KPIs
// =====================================================

function renderKPIs(data) {

    const kpis =
        data.analysis?.kpis || [];


    // -----------------------------------------------
    // No business KPI available
    // -----------------------------------------------

    if (!kpis.length) {

        kpiContainer.innerHTML = `

            <div class="empty-state">

                <h3>
                    No Business KPIs Found
                </h3>

                <p>
                    No suitable business metrics
                    were detected in this dataset.
                </p>

            </div>

        `;

        return;
    }


    // -----------------------------------------------
    // Render KPI cards
    // -----------------------------------------------

    kpiContainer.innerHTML =
        kpis.map(
            (kpi, index) => {

                const title =
                    kpi.title ||
                    kpi.column ||
                    "KPI";


                const value =
                    kpi.formatted_value ??
                    formatNumber(
                        kpi.value
                    );


                const column =
                    kpi.column ||
                    "";


                const aggregation =
                    kpi.aggregation ||
                    "value";


                // -----------------------------------
                // Aggregation label
                // -----------------------------------

                let aggregationLabel = "";


                if (
                    aggregation === "sum"
                ) {

                    aggregationLabel =
                        "Total";

                }

                else if (
                    aggregation === "mean" ||
                    aggregation === "average"
                ) {

                    aggregationLabel =
                        "Average";

                }

                else if (
                    aggregation === "max"
                ) {

                    aggregationLabel =
                        "Maximum";

                }

                else if (
                    aggregation === "min"
                ) {

                    aggregationLabel =
                        "Minimum";

                }


                // -----------------------------------
                // Subtitle
                // -----------------------------------

                const subtitle =
                    kpi.subtitle ||
                    (
                        aggregationLabel
                            ? `${aggregationLabel} of ${column}`
                            : column
                    );


                return `

                    <div class="kpi-card">

                        <div class="kpi-top">

                            <div class="kpi-label">

                                ${escapeHTML(
                                    title
                                )}

                            </div>


                            <div class="kpi-icon">

                                ${getKPIIcon(
                                    index
                                )}

                            </div>

                        </div>


                        <div class="kpi-value">

                            ${escapeHTML(
                                value
                            )}

                        </div>


                        <div class="kpi-description">

                            ${escapeHTML(
                                subtitle
                            )}

                        </div>

                    </div>

                `;

            }
        ).join("");

}


// =====================================================
// KPI ICON
// =====================================================

function getKPIIcon(index) {

    const icons = [

        "↗",
        "▣",
        "◈",
        "◉",
        "◆",
        "★"

    ];


    return icons[
        index % icons.length
    ];

}


// =====================================================
// CLEANING REPORT
// =====================================================

function renderCleaning(data) {

    const report =
        data.cleaning_report || {};


    const rowsRemoved =
        getValue(
            report,
            [
                "rows_removed",
                "removed_rows",
                "rows_deleted"
            ],
            0
        );


    const columnsRemoved =
        getValue(
            report,
            [
                "columns_removed",
                "removed_columns",
                "columns_deleted"
            ],
            0
        );


    const outliers =
        getValue(
            report,
            [
                "outliers",
                "outliers_detected",
                "total_outliers"
            ],
            0
        );


    const missingHandled =
        getValue(
            report,
            [
                "missing_values_handled",
                "missing_handled",
                "missing_filled"
            ],
            0
        );


    cleaningContainer.innerHTML = `

        <div class="health-item">

            <span>
                Rows Removed
            </span>

            <strong>
                ${formatNumber(
                    rowsRemoved
                )}
            </strong>

        </div>


        <div class="health-item">

            <span>
                Columns Removed
            </span>

            <strong>
                ${formatNumber(
                    columnsRemoved
                )}
            </strong>

        </div>


        <div class="health-item">

            <span>
                Missing Values Handled
            </span>

            <strong>
                ${formatNumber(
                    missingHandled
                )}
            </strong>

        </div>


        <div class="health-item">

            <span>
                Outliers Detected
            </span>

            <strong>
                ${formatNumber(
                    outliers
                )}
            </strong>

        </div>

    `;

}


// =====================================================
// DETECTED COLUMNS
// =====================================================

function renderColumns(data) {

    const detected =
        data.detected_columns || {};


    let rows = [];


    // -----------------------------------------------
    // Array response
    // -----------------------------------------------

    if (Array.isArray(detected)) {

        rows = detected;

    }


    // -----------------------------------------------
    // Object response
    // -----------------------------------------------

    else {

        Object.entries(detected)
            .forEach(
                ([column, info]) => {

                    if (
                        typeof info === "string"
                    ) {

                        rows.push({

                            column: column,

                            type: info,

                            confidence: "-"

                        });

                    }

                    else {

                        rows.push({

                            column: column,

                            type:
                                info?.type ||
                                info?.detected_type ||
                                "Unknown",

                            confidence:
                                info?.confidence ??
                                info?.score ??
                                "-"

                        });

                    }

                }
            );

    }


    columnCount.textContent =
        `${rows.length} columns`;


    columnsContainer.innerHTML = `

        <table class="data-table">

            <thead>

                <tr>

                    <th>
                        Column
                    </th>

                    <th>
                        Detected Type
                    </th>

                    <th>
                        Confidence
                    </th>

                </tr>

            </thead>


            <tbody>

                ${rows.map(
                    row => `

                    <tr>

                        <td>

                            ${escapeHTML(
                                row.column ||
                                row.name ||
                                "-"
                            )}

                        </td>


                        <td>

                            <span class="type-badge">

                                ${escapeHTML(
                                    row.type ||
                                    row.detected_type ||
                                    "-"
                                )}

                            </span>

                        </td>


                        <td>

                            ${formatConfidence(
                                row.confidence
                            )}

                        </td>

                    </tr>

                `
                ).join("")}

            </tbody>

        </table>

    `;

}


// =====================================================
// CHARTS
// =====================================================

function renderCharts(data) {

    chartsContainer.innerHTML = "";


    const charts =
        data.charts || [];


    // -----------------------------------------------
    // No charts
    // -----------------------------------------------

    if (!charts.length) {

        chartsContainer.innerHTML = `

            <div class="empty-state">

                <h3>
                    No charts generated
                </h3>

                <p>
                    No suitable visualizations
                    were found.
                </p>

            </div>

        `;

        return;
    }


    // -----------------------------------------------
    // Render charts
    // -----------------------------------------------

    charts.forEach(
        (chart, index) => {

            if (
                !chart ||
                !chart.figure
            ) {

                return;

            }


            const chartId =
                `chart-${index}`;


            const recommendation =
                chart.recommendation ||
                {};


            const title =
                recommendation.title ||
                recommendation.chart_type ||
                `Visualization ${
                    index + 1
                }`;


            const description =
                recommendation.description ||
                recommendation.reason ||
                "Automatically generated visualization.";


            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "chart-card";


            card.innerHTML = `

                <div class="chart-header">

                    <div>

                        <div class="chart-number">

                            CHART ${
                                String(
                                    index + 1
                                ).padStart(
                                    2,
                                    "0"
                                )
                            }

                        </div>


                        <h3>

                            ${escapeHTML(
                                title
                            )}

                        </h3>


                        <p>

                            ${escapeHTML(
                                description
                            )}

                        </p>

                    </div>

                </div>


                <div
                    id="${chartId}"
                    class="plot-container"
                ></div>

            `;


            chartsContainer.appendChild(
                card
            );


            renderPlot(
                chartId,
                chart.figure
            );

        }
    );

}


// =====================================================
// PLOTLY
// =====================================================
function renderPlot(
    elementId,
    figure
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {
        return;
    }


    const oldLayout =
        figure.layout || {};


    // =================================================
    // LAYOUT
    // =================================================

    const layout = {

        ...oldLayout,

        autosize: true,

        paper_bgcolor:
            "rgba(0,0,0,0)",

        plot_bgcolor:
            "#ffffff",

        font: {

            ...(oldLayout.font || {}),

            family:
                "Inter, Arial, sans-serif",

            color:
                "#374151",

            size:
                12

        },

        margin: {

            ...(oldLayout.margin || {}),

            l: 55,

            r: 25,

            t: 25,

            b: 55

        },

        xaxis: {

            ...(oldLayout.xaxis || {}),

            gridcolor:
                "#eef0f4",

            zerolinecolor:
                "#e5e7eb",

            linecolor:
                "#dfe3e8",

            tickfont: {

                color:
                    "#6b7280",

                size:
                    11

            }

        },

        yaxis: {

            ...(oldLayout.yaxis || {}),

            gridcolor:
                "#eef0f4",

            zerolinecolor:
                "#e5e7eb",

            linecolor:
                "#dfe3e8",

            tickfont: {

                color:
                    "#6b7280",

                size:
                    11

            }

        },

        hoverlabel: {

            bgcolor:
                "#111827",

            bordercolor:
                "#111827",

            font: {

                color:
                    "#ffffff",

                size:
                    13

            },

            align:
                "left"

        }

    };


    // =================================================
    // TRACES
    // =================================================

    const traces =
        (figure.data || []).map(
            trace => {

                const updated = {
                    ...trace
                };


                // -------------------------------------
                // BAR CHART
                // -------------------------------------

                if (
                    trace.type === "bar"
                ) {

                    updated.textposition =
                        trace.textposition ||
                        "auto";


                    updated.hovertemplate =
                        trace.hovertemplate ||
                        "<b>%{x}</b><br>" +
                        "Value: %{y:,}" +
                        "<extra></extra>";

                }


                // -------------------------------------
                // SCATTER / LINE CHART
                // -------------------------------------

                else if (
                    trace.type === "scatter" ||
                    trace.type === "scattergl"
                ) {

                    updated.marker = {

                        ...(trace.marker || {}),

                        size:
                            trace.marker?.size ||
                            7

                    };


                    updated.hovertemplate =
                        trace.hovertemplate ||
                        "<b>%{x}</b><br>" +
                        "Value: %{y:,}" +
                        "<extra></extra>";

                }


                // -------------------------------------
                // PIE CHART
                // -------------------------------------

                else if (
                    trace.type === "pie"
                ) {

                    updated.hovertemplate =
                        trace.hovertemplate ||
                        "<b>%{label}</b><br>" +
                        "Value: %{value:,}<br>" +
                        "Share: %{percent}" +
                        "<extra></extra>";

                }


                // -------------------------------------
                // OTHER CHART TYPES
                // -------------------------------------

                else {

                    updated.hovertemplate =
                        trace.hovertemplate ||
                        "<b>%{x}</b><br>" +
                        "Value: %{y:,}" +
                        "<extra></extra>";

                }


                return updated;

            }
        );


    // =================================================
    // PLOTLY
    // =================================================

    Plotly.newPlot(

        element,

        traces,

        layout,

        {

            responsive: true,

            displaylogo: false,

            displayModeBar:
                "hover",

            modeBarButtonsToRemove: [

                "lasso2d",

                "select2d",

                "autoScale2d"

            ]

        }

    );

}

// =====================================================
// INSIGHTS
// =====================================================

function renderInsights(data) {

    const insights =
        data.insights || [];


    // -----------------------------------------------
    // No insights
    // -----------------------------------------------

    if (!insights.length) {

        insightsContainer.innerHTML =
            "<p>No insights available.</p>";

        return;
    }


    // -----------------------------------------------
    // Render insights
    // -----------------------------------------------

    insightsContainer.innerHTML =
        insights.map(
            (insight, index) => {

                let text;


                if (
                    typeof insight === "string"
                ) {

                    text = insight;

                }

                else {

                    text =
                        insight.text ||
                        insight.insight ||
                        insight.message ||
                        JSON.stringify(
                            insight
                        );

                }


                return `

                    <div class="insight-card">

                        <div class="insight-number">

                            ${String(
                                index + 1
                            ).padStart(
                                2,
                                "0"
                            )}

                        </div>


                        <div class="insight-text">

                            ${escapeHTML(
                                text
                            )}

                        </div>

                    </div>

                `;

            }
        ).join("");

}


// =====================================================
// GET VALUE
// =====================================================

function getValue(
    object,
    keys,
    fallback = 0
) {

    for (
        const key of keys
    ) {

        if (
            object &&
            object[key] !== undefined &&
            object[key] !== null
        ) {

            return object[key];

        }

    }


    return fallback;

}


// =====================================================
// FORMAT NUMBER
// =====================================================

function formatNumber(value) {

    const number =
        Number(value);


    if (
        Number.isNaN(number)
    ) {

        return String(
            value ?? "-"
        );

    }


    return number.toLocaleString(
        "en-IN"
    );

}


// =====================================================
// FORMAT CONFIDENCE
// =====================================================

function formatConfidence(value) {

    if (
        value === null ||
        value === undefined ||
        value === "-"
    ) {

        return "-";

    }


    const number =
        Number(value);


    if (
        Number.isNaN(number)
    ) {

        return escapeHTML(
            String(value)
        );

    }


    const percentage =
        number <= 1
            ? number * 100
            : number;


    return `

        <div class="confidence">

            <div class="confidence-track">

                <div
                    class="confidence-fill"
                    style="width:${Math.min(
                        Math.max(
                            percentage,
                            0
                        ),
                        100
                    )}%"
                ></div>

            </div>


            <span>

                ${percentage.toFixed(0)}%

            </span>

        </div>

    `;

}


// =====================================================
// ESCAPE HTML
// =====================================================

function escapeHTML(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );

}


// =====================================================
// SHOW ERROR
// =====================================================

function showError(message) {

    errorBox.textContent =
        message;


    errorBox.classList.remove(
        "hidden"
    );

}


// =====================================================
// HIDE ERROR
// =====================================================

function hideError() {

    errorBox.classList.add(
        "hidden"
    );

}