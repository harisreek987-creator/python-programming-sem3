# ================================================================
# RETAIL SALES ANALYTICS DASHBOARD
# Individual Python Mini-Project | Google Colab
# Libraries: Pandas, NumPy, Matplotlib, IPyWidgets
# Dataset: Sample Superstore (public sample retail transactions)
# ================================================================

# If running in Google Colab, run this cell as-is.
# If the automatic dataset download fails, the script will ask you
# to upload the CSV file manually.

# ------------------------------
# 1. IMPORT REQUIRED LIBRARIES
# ------------------------------
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets

from IPython.display import display, HTML, clear_output

# Enable interactive IPyWidgets when running inside Google Colab.
try:
    from google.colab import output
    output.enable_custom_widget_manager()
except ImportError:
    pass

plt.rcParams["figure.figsize"] = (15, 9)
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10
plt.rcParams["font.size"] = 9
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "#F8FAFC"

print("Libraries imported successfully.")

# ------------------------------
# 2. LOAD THE DATASET
# ------------------------------
DATASET_URL = (
    "https://raw.githubusercontent.com/"
    "leonism/sample-superstore/master/data/superstore.csv"
)

try:
    df = pd.read_csv(DATASET_URL, encoding="latin-1")
    print("Dataset downloaded successfully.")
except Exception as error:
    print("Automatic download failed.")
    print("Please upload the Sample - Superstore.csv file.")
    try:
        from google.colab import files
        uploaded = files.upload()
        csv_file = next(iter(uploaded))
        df = pd.read_csv(csv_file, encoding="latin-1")
    except Exception:
        raise RuntimeError(
            "Could not load the dataset. Upload the Sample Superstore CSV "
            "or check your internet connection and try again."
        )

print(f"Original dataset shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# ------------------------------
# 3. DATA CLEANING & PREPROCESSING
# ------------------------------
df.columns = df.columns.str.strip()

required_columns = [
    "Order ID", "Order Date", "Customer ID", "Region",
    "Category", "Sub-Category", "Product Name",
    "Sales", "Quantity", "Discount", "Profit"
]

missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Dataset is missing required columns: {missing_columns}")

# Remove exact duplicate records.
duplicate_count = int(df.duplicated().sum())
df = df.drop_duplicates().copy()

# Convert dates and numeric fields.
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
for column in ["Sales", "Quantity", "Discount", "Profit"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove rows that cannot be used for sales analysis.
before_invalid_removal = len(df)
df = df.dropna(subset=["Order Date", "Sales", "Quantity", "Profit"]).copy()
invalid_rows_removed = before_invalid_removal - len(df)

# Replace missing categorical values with an explicit label.
categorical_columns = [
    "Region", "Category", "Sub-Category", "Product Name",
    "Segment", "Ship Mode"
]
for column in categorical_columns:
    if column in df.columns:
        df[column] = df[column].fillna("Unknown").astype(str).str.strip()

# Add analysis columns.
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
df["Month Name"] = df["Order Date"].dt.strftime("%b")
df["Profit Margin (%)"] = np.where(
    df["Sales"] != 0, (df["Profit"] / df["Sales"]) * 100, 0
)

print("\nDATA CLEANING SUMMARY")
print("-" * 45)
print(f"Duplicate rows removed : {duplicate_count:,}")
print(f"Invalid rows removed   : {invalid_rows_removed:,}")
print(f"Clean dataset shape    : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Date range             : {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")

# ------------------------------
# 4. DATASET OVERVIEW
# ------------------------------
print("\nDATASET PREVIEW")
display(df.head())

print("\nNUMERICAL SUMMARY")
display(df[["Sales", "Quantity", "Discount", "Profit"]].describe().round(2))

print("\nMISSING VALUES")
display(df.isnull().sum().to_frame("Missing Values"))

# ------------------------------
# 5. FILTER OPTIONS
# ------------------------------
def dropdown_options(column):
    values = sorted(df[column].dropna().unique().tolist())
    return [("All", "All")] + [(str(value), str(value)) for value in values]

date_min = df["Order Date"].min().date()
date_max = df["Order Date"].max().date()

start_date = widgets.DatePicker(
    description="Start date",
    value=date_min,
    style={"description_width": "initial"},
    layout=widgets.Layout(width="230px")
)

end_date = widgets.DatePicker(
    description="End date",
    value=date_max,
    style={"description_width": "initial"},
    layout=widgets.Layout(width="230px")
)

region_filter = widgets.Dropdown(
    options=dropdown_options("Region"),
    value="All",
    description="Region:",
    style={"description_width": "initial"},
    layout=widgets.Layout(width="220px")
)

category_filter = widgets.Dropdown(
    options=dropdown_options("Category"),
    value="All",
    description="Category:",
    style={"description_width": "initial"},
    layout=widgets.Layout(width="220px")
)

segment_filter = widgets.Dropdown(
    options=dropdown_options("Segment") if "Segment" in df.columns
    else [("All", "All")],
    value="All",
    description="Customer segment:",
    style={"description_width": "initial"},
    layout=widgets.Layout(width="250px")
)

ship_filter = widgets.Dropdown(
    options=dropdown_options("Ship Mode") if "Ship Mode" in df.columns
    else [("All", "All")],
    value="All",
    description="Ship mode:",
    style={"description_width": "initial"},
    layout=widgets.Layout(width="220px")
)

# ------------------------------
# 6. DASHBOARD HELPER FUNCTIONS
# ------------------------------
def format_currency(value):
    return f"${value:,.2f}"

def get_filtered_data(start, end, region, category, segment, ship_mode):
    filtered = df.copy()

    if start is not None:
        filtered = filtered[filtered["Order Date"].dt.date >= start]
    if end is not None:
        filtered = filtered[filtered["Order Date"].dt.date <= end]
    if region != "All":
        filtered = filtered[filtered["Region"] == region]
    if category != "All":
        filtered = filtered[filtered["Category"] == category]
    if segment != "All" and "Segment" in filtered.columns:
        filtered = filtered[filtered["Segment"] == segment]
    if ship_mode != "All" and "Ship Mode" in filtered.columns:
        filtered = filtered[filtered["Ship Mode"] == ship_mode]

    return filtered

def show_kpi_cards(data):
    total_sales = data["Sales"].sum()
    total_profit = data["Profit"].sum()
    total_orders = data["Order ID"].nunique()
    total_quantity = data["Quantity"].sum()
    avg_order_value = total_sales / total_orders if total_orders else 0
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0

    cards = [
        ("TOTAL SALES", format_currency(total_sales)),
        ("TOTAL PROFIT", format_currency(total_profit)),
        ("PROFIT MARGIN", f"{profit_margin:.2f}%"),
        ("TOTAL ORDERS", f"{total_orders:,}"),
        ("UNITS SOLD", f"{total_quantity:,.0f}"),
        ("AVERAGE ORDER VALUE", format_currency(avg_order_value))
    ]

    card_html = """
    <div style="display:grid;grid-template-columns:repeat(3,minmax(150px,1fr));
                gap:12px;margin:12px 0 18px 0;">
    """
    for label, value in cards:
        card_html += f"""
        <div style="background:#EFF6FF;border-left:4px solid #2563EB;
                    padding:14px;border-radius:8px;">
            <div style="font-size:11px;color:#475569;font-weight:600;">{label}</div>
            <div style="font-size:21px;color:#0F172A;font-weight:700;margin-top:5px;">
                {value}
            </div>
        </div>
        """
    card_html += "</div>"
    display(HTML(card_html))

# ------------------------------
# 7. AUTOMATED BUSINESS INSIGHTS
# ------------------------------
def generate_business_insights(data):
    if data.empty:
        display(HTML("<p>No data available for the selected filters.</p>"))
        return

    total_sales = data["Sales"].sum()
    total_profit = data["Profit"].sum()
    margin = (total_profit / total_sales * 100) if total_sales else 0

    category_sales = data.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    region_sales = data.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    category_profit = data.groupby("Category")["Profit"].sum().sort_values()
    subcategory_profit = data.groupby("Sub-Category")["Profit"].sum().sort_values()

    insights = []

    if not category_sales.empty:
        insights.append(
            f"<b>Leading category:</b> {category_sales.index[0]} "
            f"generates the highest sales ({format_currency(category_sales.iloc[0])})."
        )

    if not region_sales.empty:
        insights.append(
            f"<b>Leading region:</b> {region_sales.index[0]} "
            f"has the highest sales ({format_currency(region_sales.iloc[0])})."
        )

    if not category_profit.empty:
        insights.append(
            f"<b>Profit performance:</b> {category_profit.index[-1]} "
            f"has the highest total profit ({format_currency(category_profit.iloc[-1])})."
        )

    if not subcategory_profit.empty and subcategory_profit.iloc[0] < 0:
        insights.append(
            f"<b>Potential concern:</b> {subcategory_profit.index[0]} "
            f"has the largest total loss "
            f"({format_currency(subcategory_profit.iloc[0])})."
        )

    insights.append(
        f"<b>Overall profit margin:</b> {margin:.2f}% for the currently selected data."
    )

    average_discount = data["Discount"].mean() * 100
    insights.append(
        f"<b>Average discount:</b> {average_discount:.1f}% across the filtered transactions."
    )

    html = """
    <div style="background:#F8FAFC;padding:16px;border-radius:10px;
                border:1px solid #CBD5E1;margin-top:12px;">
      <h3 style="margin:0 0 10px 0;color:#0F172A;">Business Insights</h3>
      <ul style="margin:0;padding-left:20px;line-height:1.8;color:#334155;">
    """
    for insight in insights:
        html += f"<li>{insight}</li>"
    html += "</ul></div>"
    display(HTML(html))

# ------------------------------
# 8. MAIN INTERACTIVE DASHBOARD
# ------------------------------
def render_dashboard(start, end, region, category, segment, ship_mode):
    clear_output(wait=True)

    data = get_filtered_data(start, end, region, category, segment, ship_mode)

    display(HTML("""
    <div style="background:#0F172A;color:white;padding:18px;border-radius:10px;">
      <h1 style="margin:0;color:white;">RETAIL SALES ANALYTICS DASHBOARD</h1>
      <p style="margin:6px 0 0 0;color:#CBD5E1;">
        Interactive analysis of sales, profitability, products and regions
      </p>
    </div>
    """))

    if data.empty:
        display(HTML(
            "<h3 style='color:#B91C1C;'>No records match the selected filters. "
            "Please change the filters.</h3>"
        ))
        return

    show_kpi_cards(data)

    # Create a 2 x 3 visualization layout.
    fig, axes = plt.subplots(2, 3, figsize=(19, 11))
    fig.suptitle("Retail Sales Performance Overview",
                 fontsize=17, fontweight="bold", y=1.01)

    # Chart 1: Monthly sales trend.
    monthly_sales = data.groupby("Month")["Sales"].sum().sort_index()
    axes[0, 0].plot(
        monthly_sales.index, monthly_sales.values,
        marker="o", linewidth=2, color="#2563EB"
    )
    axes[0, 0].set_title("Monthly Sales Trend", fontweight="bold")
    axes[0, 0].set_ylabel("Sales ($)")
    axes[0, 0].grid(alpha=0.25)
    axes[0, 0].tick_params(axis="x", rotation=35)

    # Chart 2: Sales by category.
    category_sales = data.groupby("Category")["Sales"].sum().sort_values()
    axes[0, 1].barh(
        category_sales.index, category_sales.values, color="#0D9488"
    )
    axes[0, 1].set_title("Sales by Category", fontweight="bold")
    axes[0, 1].set_xlabel("Sales ($)")
    axes[0, 1].grid(axis="x", alpha=0.25)

    # Chart 3: Profit by region.
    region_profit = data.groupby("Region")["Profit"].sum().sort_values()
    axes[0, 2].bar(
        region_profit.index, region_profit.values, color="#7C3AED"
    )
    axes[0, 2].set_title("Profit by Region", fontweight="bold")
    axes[0, 2].set_ylabel("Profit ($)")
    axes[0, 2].tick_params(axis="x", rotation=20)
    axes[0, 2].axhline(0, color="black", linewidth=0.8)
    axes[0, 2].grid(axis="y", alpha=0.25)

    # Chart 4: Top 10 products by sales.
    top_products = (
        data.groupby("Product Name")["Sales"]
        .sum().nlargest(10).sort_values()
    )
    axes[1, 0].barh(
        [name[:34] + ("..." if len(name) > 34 else "")
         for name in top_products.index],
        top_products.values,
        color="#D97706"
    )
    axes[1, 0].set_title("Top 10 Products by Sales", fontweight="bold")
    axes[1, 0].set_xlabel("Sales ($)")
    axes[1, 0].grid(axis="x", alpha=0.25)

    # Chart 5: Discount vs profit.
    axes[1, 1].scatter(
        data["Discount"] * 100, data["Profit"],
        alpha=0.35, s=22, color="#DB2777"
    )
    axes[1, 1].set_title("Discount vs Profit", fontweight="bold")
    axes[1, 1].set_xlabel("Discount (%)")
    axes[1, 1].set_ylabel("Profit ($)")
    axes[1, 1].axhline(0, color="black", linewidth=0.8)
    axes[1, 1].grid(alpha=0.25)

    # Chart 6: Sales contribution by customer segment.
    if "Segment" in data.columns:
        segment_sales = data.groupby("Segment")["Sales"].sum()
        axes[1, 2].pie(
            segment_sales.values,
            labels=segment_sales.index,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"edgecolor": "white"}
        )
        axes[1, 2].set_title("Sales by Customer Segment", fontweight="bold")
    else:
        axes[1, 2].text(0.5, 0.5, "Segment data unavailable",
                        ha="center", va="center")
        axes[1, 2].set_axis_off()

    plt.tight_layout()
    plt.show()

    # Business insights below the charts.
    generate_business_insights(data)

    # Display a small summary table.
    display(HTML("<h3 style='color:#0F172A;'>Category Performance Summary</h3>"))
    summary = (
        data.groupby("Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Units_Sold=("Quantity", "sum"),
            Orders=("Order ID", "nunique")
        )
        .sort_values("Total_Sales", ascending=False)
    )
    summary["Profit_Margin_%"] = np.where(
        summary["Total_Sales"] != 0,
        summary["Total_Profit"] / summary["Total_Sales"] * 100,
        0
    )
    display(summary.style.format({
        "Total_Sales": "${:,.2f}",
        "Total_Profit": "${:,.2f}",
        "Units_Sold": "{:,.0f}",
        "Orders": "{:,.0f}",
        "Profit_Margin_%": "{:.2f}%"
    }))

# ------------------------------
# 9. DISPLAY INTERACTIVE FILTERS
# ------------------------------
display(HTML("""
<h2 style="color:#0F172A;">Dashboard Filters</h2>
<p style="color:#475569;">
Select a date range, region, category, customer segment or shipping mode.
The dashboard updates automatically when a filter changes.
</p>
"""))

filter_row_1 = widgets.HBox([start_date, end_date])
filter_row_2 = widgets.HBox([region_filter, category_filter])
filter_row_3 = widgets.HBox([segment_filter, ship_filter])

controls = {
    "start": start_date,
    "end": end_date,
    "region": region_filter,
    "category": category_filter,
    "segment": segment_filter,
    "ship_mode": ship_filter
}

dashboard_output = widgets.interactive_output(
    render_dashboard,
    controls
)

display(widgets.VBox([
    filter_row_1,
    filter_row_2,
    filter_row_3,
    dashboard_output
]))

# ------------------------------
# 10. PROJECT CONCLUSION
# ------------------------------
print("""
PROJECT: RETAIL SALES ANALYTICS DASHBOARD

The project uses Python to load, clean, analyse and visualize retail
transaction data from a CSV file. Interactive filters allow users to
explore sales performance across different time periods, regions,
categories, customer segments and shipping modes.

The dashboard presents key performance indicators, sales trends,
category and regional comparisons, product performance and automated
business observations.

Note: The dataset is a public sample dataset. The analysis describes
the records contained in that dataset and should not be interpreted
as current market data or as information from a live retailer.
""")
