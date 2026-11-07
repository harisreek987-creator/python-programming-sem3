# Retail Sales Analytics Dashboard
**Module V | Individual Python mini-project | Completed**

An interactive retail sales analytics dashboard built with Python, Pandas, NumPy, Matplotlib and IPyWidgets. It loads transaction data from a CSV dataset, prepares the data, calculates key performance indicators, visualizes sales and profitability, and generates business insights.

## Features
- CSV dataset loading with manual upload fallback
- Data validation, duplicate removal and missing-value handling
- KPI cards for sales, profit, profit margin, orders, units sold and average order value
- Interactive filters for date range, region, category, customer segment and shipping mode
- Visualizations for monthly sales, category, region, products, discount and customer segments
- Automated business insights

## Run in Google Colab
Open `Retail_Sales_Analytics_Dashboard.ipynb` in Google Colab and select **Runtime → Run all**. Upload the Sample Superstore CSV if automatic retrieval fails.

## Run locally
```bash
pip install -r requirements.txt
python retail_sales_dashboard.py
```

The interactive widgets are best experienced in Google Colab or Jupyter Notebook. The dataset contains historical sample records, not live retail data.
