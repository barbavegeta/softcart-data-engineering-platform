from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from textwrap import fill

ROOT = Path(__file__).resolve().parents[1]
ANALYTICS = ROOT / "analytics"
REPORTS = ROOT / "reports"
WAREHOUSE = ROOT / "data" / "warehouse"

REPORTS.mkdir(exist_ok=True)

country = pd.read_csv(ANALYTICS / "total_sales_per_country.csv")
category = pd.read_csv(ANALYTICS / "total_sales_per_category.csv")
fact = pd.read_csv(WAREHOUSE / "FactSales.csv")
dim_date = pd.read_csv(WAREHOUSE / "DimDate.csv")

# Normalise likely column names
fact.columns = [c.strip() for c in fact.columns]
dim_date.columns = [c.strip() for c in dim_date.columns]

# The warehouse files use these columns from the validated PostgreSQL schema
# FactSales: orderid, dateid, countryid, categoryid, amount
# DimDate: dateid, date, Year, Quarter, Month, Day, etc.
merged = fact.merge(dim_date[["dateid", "Year", "Quarter", "Month"]], on="dateid", how="left")

yearly_sales = (
    merged.groupby("Year", as_index=False)["amount"]
    .sum()
    .rename(columns={"Year": "year", "amount": "total_sales"})
    .sort_values("year")
)

quarterly_sales = (
    merged.groupby(["Year", "Quarter"], as_index=False)["amount"]
    .sum()
    .rename(columns={"Year": "year", "Quarter": "quarter", "amount": "total_sales"})
    .sort_values(["year", "quarter"])
)

monthly_sales = (
    merged.groupby(["Year", "Month"], as_index=False)["amount"]
    .sum()
    .rename(columns={"Year": "year", "Month": "month", "amount": "total_sales"})
    .sort_values(["year", "month"])
)

top_country = country.sort_values("total_sales", ascending=False).head(10)
top_category = category.sort_values("total_sales", ascending=False)

total_revenue = int(fact["amount"].sum())
top_country_name = top_country.iloc[0]["country"]
top_country_sales = int(top_country.iloc[0]["total_sales"])
top_category_name = top_category.iloc[0]["category"]
top_category_sales = int(top_category.iloc[0]["total_sales"])

output_pdf = REPORTS / "softcart_ecommerce_performance_report.pdf"

def money(x):
    return f"{x:,.0f}"

def add_wrapped_text(fig, x, y, text, width=95, fontsize=11):
    fig.text(x, y, fill(text, width=width), fontsize=fontsize, va="top")

with PdfPages(output_pdf) as pdf:

    # Page 1: executive summary
    fig = plt.figure(figsize=(11.69, 8.27))
    fig.text(0.07, 0.88, "SoftCart E-Commerce Performance Report", fontsize=26, weight="bold")
    fig.text(0.07, 0.82, "Warehouse-backed sales analysis from the validated SoftCart dimensional model", fontsize=13)

    fig.text(0.07, 0.72, "Executive Summary", fontsize=17, weight="bold")
    summary = (
        f"The SoftCart warehouse contains 300,000 fact sales records joined to date, country, "
        f"and product-category dimensions. Total recorded sales amount to {money(total_revenue)}. "
        f"The highest-selling country is {top_country_name} with {money(top_country_sales)} in sales, "
        f"while the strongest product category is {top_category_name} with {money(top_category_sales)} in sales. "
        f"The analysis demonstrates a reproducible warehouse workflow: loading dimensional data into PostgreSQL, "
        f"validating table counts, and exporting business-facing analytics outputs."
    )
    add_wrapped_text(fig, 0.07, 0.66, summary, width=100, fontsize=11)

    fig.text(0.07, 0.45, "Validated Warehouse Tables", fontsize=15, weight="bold")
    fig.text(
        0.09, 0.38,
        "FactSales: 300,000 rows\nDimDate: 1,096 rows\nDimCountry: 56 rows\nDimCategory: 5 rows",
        fontsize=12
    )

    fig.text(0.07, 0.22, "Generated Outputs", fontsize=15, weight="bold")
    fig.text(
        0.09, 0.14,
        "total_sales_per_country.csv\n"
        "total_sales_per_category.csv\n"
        "sales_by_year_country_rollup.csv\n"
        "average_sales_cube.csv",
        fontsize=11
    )
    plt.axis("off")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    # Page 2: top countries
    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.barh(top_country["country"], top_country["total_sales"])
    ax.invert_yaxis()
    ax.set_title("Top 10 Countries by Total Sales", fontsize=17, weight="bold")
    ax.set_xlabel("Total sales")
    ax.set_ylabel("Country")

    for i, value in enumerate(top_country["total_sales"]):
        ax.text(value, i, f" {money(value)}", va="center", fontsize=9)

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    # Page 3: category sales
    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.bar(top_category["category"], top_category["total_sales"])
    ax.set_title("Total Sales by Product Category", fontsize=17, weight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Total sales")
    ax.tick_params(axis="x", rotation=25)

    for i, value in enumerate(top_category["total_sales"]):
        ax.text(i, value, money(value), ha="center", va="bottom", fontsize=9, rotation=0)

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    # Page 4: yearly sales
    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.plot(yearly_sales["year"], yearly_sales["total_sales"], marker="o")
    ax.set_title("Total Sales by Year", fontsize=17, weight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total sales")
    ax.set_xticks(yearly_sales["year"].astype(int))

    for _, row in yearly_sales.iterrows():
        ax.text(row["year"], row["total_sales"], money(row["total_sales"]), ha="center", va="bottom", fontsize=9)

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    # Page 5: quarterly sales
    quarterly_sales["period"] = quarterly_sales["year"].astype(int).astype(str) + " Q" + quarterly_sales["quarter"].astype(int).astype(str)

    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.plot(quarterly_sales["period"], quarterly_sales["total_sales"], marker="o")
    ax.set_title("Quarterly Sales Trend", fontsize=17, weight="bold")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total sales")
    ax.tick_params(axis="x", rotation=35)

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    # Page 6: methodology
    fig = plt.figure(figsize=(11.69, 8.27))
    fig.text(0.07, 0.88, "Methodology", fontsize=22, weight="bold")

    methodology = (
        "The report was generated from validated warehouse outputs and dimensional source tables. "
        "Sales facts were joined to the date dimension to calculate yearly and quarterly trends. "
        "Country and category performance were calculated from PostgreSQL warehouse queries exported "
        "to CSV. The report is designed as a reproducible portfolio artefact rather than a static course screenshot."
    )
    add_wrapped_text(fig, 0.07, 0.78, methodology, width=100, fontsize=12)

    fig.text(0.07, 0.55, "Files Used", fontsize=16, weight="bold")
    fig.text(
        0.09, 0.47,
        "analytics/total_sales_per_country.csv\n"
        "analytics/total_sales_per_category.csv\n"
        "data/warehouse/FactSales.csv\n"
        "data/warehouse/DimDate.csv",
        fontsize=11
    )

    fig.text(0.07, 0.28, "Limitations", fontsize=16, weight="bold")
    limitations = (
        "The dataset is course-derived rather than production data. The report demonstrates data engineering "
        "workflow reproducibility, warehouse loading, validation, and analytical reporting, but should not be "
        "presented as a live production BI system."
    )
    add_wrapped_text(fig, 0.09, 0.22, limitations, width=95, fontsize=11)

    plt.axis("off")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

print(f"Created report: {output_pdf}")
