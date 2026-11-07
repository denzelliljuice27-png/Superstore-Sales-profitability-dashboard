from pathlib import Path
from io import BytesIO
import base64

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc


# ---------------------------------------------------------------------
# Configuration and data loading
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "Sample - Superstore.csv"

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}. "
        "Make sure the data folder contains 'Sample - Superstore.csv'."
    )

df = pd.read_csv(DATA_PATH, encoding="latin1")
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
df["Shipping_Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
df["Profit_Margin"] = (df["Profit"] / df["Sales"].replace(0, pd.NA)) * 100
df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)

REGIONS = sorted(df["Region"].dropna().unique())
CATEGORIES = sorted(df["Category"].dropna().unique())
SEGMENTS = sorted(df["Segment"].dropna().unique())


# ---------------------------------------------------------------------
# Static visualisations (created once when the app starts)
# ---------------------------------------------------------------------
def figure_to_base64(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=140)
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close(fig)
    return encoded


def create_profit_distribution():
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["Profit"], kde=True, ax=ax)
    ax.axvline(0, color="red", linestyle="--", label="Break-even")
    ax.set(title="Profit Distribution", xlabel="Profit", ylabel="Frequency")
    ax.legend()
    return figure_to_base64(fig)


def create_subcategory_chart():
    average_profit = (
        df.groupby("Sub-Category")["Profit"]
        .mean()
        .sort_values()
    )
    bar_colors = ["#dc3545" if value < 0 else "#198754" for value in average_profit]

    fig, ax = plt.subplots(figsize=(9, 6))
    average_profit.plot(kind="barh", color=bar_colors, ax=ax)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set(title="Average Profit by Sub-Category", xlabel="Average Profit", ylabel="")
    return figure_to_base64(fig)


def create_correlation_heatmap():
    correlation = df[["Sales", "Quantity", "Discount", "Profit"]].corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(correlation, annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=ax)
    ax.set_title("Correlation Heatmap")
    return figure_to_base64(fig)


profit_image = create_profit_distribution()
subcategory_image = create_subcategory_chart()
heatmap_image = create_correlation_heatmap()


# ---------------------------------------------------------------------
# Dash application layout
# ---------------------------------------------------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Superstore Sales & Profitability Dashboard"

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H1(
                        "Superstore Dashboard",
                        className="text-center text-primary mt-4",
                    ),
                    html.P(
                        "Retail Sales and Profitability Analysis",
                        className="text-center lead",
                    ),
                ]
            )
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select Region"),
                        dcc.Dropdown(
                            id="region_filter",
                            options=[{"label": r, "value": r} for r in REGIONS],
                            value=REGIONS,
                            multi=True,
                            placeholder="Choose one or more regions",
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.Label("Select Category"),
                        dcc.Dropdown(
                            id="category_filter",
                            options=[{"label": c, "value": c} for c in CATEGORIES],
                            value=CATEGORIES,
                            multi=True,
                            placeholder="Choose one or more categories",
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.Label("Select Segment"),
                        dcc.RadioItems(
                            id="segment_filter",
                            options=[{"label": s, "value": s} for s in SEGMENTS],
                            value=SEGMENTS[0] if SEGMENTS else None,
                            labelStyle={"display": "block", "marginBottom": "8px"},
                        ),
                    ],
                    md=4,
                ),
            ],
            className="g-3",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody([html.H5("Total Sales"), html.H2(id="sales_kpi")])) , md=3),
                dbc.Col(dbc.Card(dbc.CardBody([html.H5("Total Profit"), html.H2(id="profit_kpi")])) , md=3),
                dbc.Col(dbc.Card(dbc.CardBody([html.H5("Average Profit Margin"), html.H2(id="margin_kpi")])) , md=3),
                dbc.Col(dbc.Card(dbc.CardBody([html.H5("Orders"), html.H2(id="orders_kpi")])) , md=3),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(dbc.Col(dcc.Graph(id="scatter_plot"))),
        dbc.Row(dbc.Col(dcc.Graph(id="time_series"))),
        dbc.Row(dbc.Col(dcc.Graph(id="regional_chart"))),
        html.Hr(),
        html.H3("Additional Analysis", className="mb-3"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Profit Distribution"),
                        html.Img(
                            src=f"data:image/png;base64,{profit_image}",
                            className="img-fluid",
                        ),
                        html.P("Shows the spread of transaction profit values."),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.H5("Average Profit by Sub-Category"),
                        html.Img(
                            src=f"data:image/png;base64,{subcategory_image}",
                            className="img-fluid",
                        ),
                        html.P("Negative average-profit values are shown in red."),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.H5("Correlation Heatmap"),
                        html.Img(
                            src=f"data:image/png;base64,{heatmap_image}",
                            className="img-fluid",
                        ),
                        html.P("Summarises linear relationships between numeric variables."),
                    ],
                    md=4,
                ),
            ],
            className="g-4",
        ),
        html.Footer(
            "Built with Python, Pandas, Plotly, Dash, Matplotlib and Seaborn.",
            className="text-center text-muted py-4",
        ),
    ],
    fluid=True,
)


# ---------------------------------------------------------------------
# Callback: filter the data and refresh KPIs and interactive charts
# ---------------------------------------------------------------------
@app.callback(
    [
        Output("sales_kpi", "children"),
        Output("profit_kpi", "children"),
        Output("margin_kpi", "children"),
        Output("orders_kpi", "children"),
        Output("scatter_plot", "figure"),
        Output("time_series", "figure"),
        Output("regional_chart", "figure"),
    ],
    [
        Input("region_filter", "value"),
        Input("category_filter", "value"),
        Input("segment_filter", "value"),
    ],
)
def update_dashboard(selected_regions, selected_categories, selected_segment):
    selected_regions = selected_regions or []
    selected_categories = selected_categories or []

    filtered = df[
        df["Region"].isin(selected_regions)
        & df["Category"].isin(selected_categories)
        & (df["Segment"] == selected_segment)
    ]

    if filtered.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="No data matches the selected filters")
        return "—", "—", "—", "0", empty_fig, empty_fig, empty_fig

    total_sales = filtered["Sales"].sum()
    total_profit = filtered["Profit"].sum()
    average_margin = filtered["Profit_Margin"].mean()
    order_count = filtered["Order ID"].nunique()

    scatter_fig = px.scatter(
        filtered,
        x="Sales",
        y="Profit",
        color="Segment",
        size="Quantity",
        hover_data=["Product Name", "Category", "Sub-Category", "Discount", "Region"],
        title="Sales vs Profit",
    )
    scatter_fig.add_hline(y=0, line_dash="dash", line_color="red")

    monthly = (
        filtered.groupby("YearMonth", as_index=False)["Sales"]
        .sum()
        .sort_values("YearMonth")
    )
    time_fig = px.line(
        monthly,
        x="YearMonth",
        y="Sales",
        title="Monthly Sales Trend",
        markers=True,
    )
    time_fig.update_layout(xaxis_rangeslider_visible=True)

    regional = (
        filtered.groupby("Region", as_index=False)[["Sales", "Profit"]]
        .sum()
    )
    regional_fig = go.Figure()
    regional_fig.add_trace(go.Bar(x=regional["Region"], y=regional["Sales"], name="Sales"))
    regional_fig.add_trace(go.Bar(x=regional["Region"], y=regional["Profit"], name="Profit"))
    regional_fig.update_layout(
        barmode="group",
        title="Regional Performance",
        xaxis_title="Region",
        yaxis_title="Amount",
    )

    return (
        f"${total_sales:,.2f}",
        f"${total_profit:,.2f}",
        f"{average_margin:.2f}%" if pd.notna(average_margin) else "—",
        f"{order_count:,}",
        scatter_fig,
        time_fig,
        regional_fig,
    )


if __name__ == "__main__":
    app.run(debug=True)
