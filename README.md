# SoftCart Data Engineering Platform

End-to-end data engineering project based on an e-commerce analytics scenario. The project covers operational data ingestion, relational and NoSQL querying, data warehouse design, ETL automation, BI reporting, and Spark-based large-scale analytics.

## Project Scope

- Modelled sales and product data for transactional analysis
- Queried semi-structured product data using MongoDB commands
- Designed a dimensional data warehouse for reporting
- Built ETL scripts for data extraction, transformation, and loading
- Created an e-commerce analytics report
- Used Apache Spark notebooks for scalable analytics and model workflow practice

## Tools

Python, SQL, Bash, MySQL, PostgreSQL/Db2-style warehouse SQL, MongoDB, Apache Spark, Jupyter Notebook, BI reporting.

## Repository Structure

```text
softcart-data-engineering-platform/
├── README.md
├── analytics/
│   ├── average_sales_cube.csv
│   ├── cube_summary.md
│   ├── grouping_sets_summary.md
│   ├── materialized_view_summary.md
│   ├── rollup_summary.md
│   ├── sales_by_year_country_rollup.csv
│   ├── total_sales_per_category.csv
│   ├── total_sales_per_country.csv
│   ├── warehouse_analytics_overview.md
│   └── warehouse_validation.md
├── architecture/
│   └── architecture.png
├── data/
│   ├── raw/
│   │   ├── ecommerce.csv
│   │   ├── electronics.csv
│   │   ├── oltpdata.csv
│   │   ├── sales.csv
│   │   └── searchterms.csv
│   └── warehouse/
│       ├── DimCategory.csv
│       ├── DimCountry.csv
│       ├── DimDate.csv
│       └── FactSales.csv
├── docs/
│   ├── data_dictionary.md
│   ├── limitations.md
│   ├── project_summary.md
│   └── runbook.md
├── etl/
│   ├── automation.py
│   ├── datadump.sh
│   ├── import.sh
│   ├── mysql_connect.py
│   ├── postgresql_connect.py
│   └── process_web_log.py
├── nosql/
│   └── mongodb_commands.sh
├── reports/
│   └── ecommerce_report.pdf
├── spark/
│   └── model_saving_loading.ipynb
├── sql/
│   ├── etl_sales.sql
│   └── oltp_sales_data.sql
└── warehouse/
    ├── create_warehouse_schema.sql
    ├── load_warehouse_data.sql
    └── warehouse_queries.sql
```
