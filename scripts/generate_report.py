import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYTICS = ROOT / "analytics"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

country = pd.read_csv(ANALYTICS / "total_sales_per_country.csv")
category = pd.read_csv(ANALYTICS / "total_sales_per_category.csv")
rollup = pd.read_csv(ANALYTICS / "sales_by_year_country_rollup.csv")
cube = pd.read_csv(ANALYTICS / "average_sales_cube.csv")

output_pdf = REPORTS / "softcart_ecommerce_analytics_report.pdf"

with PdfPages(output_pdf) as pdf:

    # Page 1: title
    fig = plt.figure(figsize=(11.69, 8.27))
    fig.text(0.08, 0.72, "SoftCart E-Commerce Analytics Report", fontsize=26, weight="bold")
    fig.text(0.08, 0.63, "PostgreSQL warehouse outputs generated from dimensional sales data", fontsize=14)
    fig.text(0.08, 0.53, "Includes total sales by country, total sales by category, year-country rollups, and cube-based average sales.", fontsize=11)
    fig.text(0.08, 0.43, "Warehouse validation:", fontsize=13, weight="bold")
    fig.text(0.10, 0.37, "FactSales: 300,000 rows\nDimDate: 1,096 rows\nDimCountry: 56 rows\nDimCategory: 5 rows", fontsize=11)
    plt.axis("off")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    # Page 2: top countries
    top_country = country.head(10)
    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.barh(top_country["country"], top_country["total_sales"])
    ax.invert_yaxis()
    ax.set_title("Top 10 Countries by Total Sales", fontsize=16, weight="bold")
    ax.set_xlabel("Total sales")
    ax.set_ylabel("Country")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    # Page 3: category sales
    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.bar(category["category"], category["total_sales"])
    ax.set_title("Total Sales by Product Category", fontsize=16, weight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Total sales")
    ax.tick_params(axis="x", rotation=30)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    # Page 4: yearly sales trend
    yearly = rollup.dropna(subset=["year"]).groupby("year", as_index=False)["total_sales"].sum()

    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.plot(yearly["year"], yearly["total_sales"], marker="o")
    ax.set_title("Total Sales by Year", fontsize=16, weight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total sales")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    # Page 5: average sales by year
    avg_year = cube.dropna(subset=["year"]).groupby("year", as_index=False)["average_sales"].mean()

    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.plot(avg_year["year"], avg_year["average_sales"], marker="o")
    ax.set_title("Average Sales by Year", fontsize=16, weight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average sales")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

print(f"Report created: {output_pdf}")
