# Runbook

This document explains how to reproduce the warehouse analytics layer of the SoftCart data engineering project.

## 1. Start PostgreSQL

```bash
sudo service postgresql start
```

## 2. Reset the warehouse database

Use this when running the workflow from scratch.

```bash
sudo -u postgres dropdb --if-exists softcart_dw
sudo -u postgres createdb softcart_dw
```

## 3. Create warehouse tables

```bash
sudo -u postgres psql -d softcart_dw -f warehouse/create_warehouse_schema.sql
```

## 4. Load warehouse data

```bash
sudo -u postgres psql -d softcart_dw -f warehouse/load_warehouse_data.sql
```

Expected row counts:

- `DimDate`: 1,096 rows
- `DimCategory`: 5 rows
- `DimCountry`: 56 rows
- `FactSales`: 300,000 rows

## 5. Run warehouse analytical queries

```bash
sudo -u postgres psql -d softcart_dw -f warehouse/warehouse_queries.sql
```

## 6. Export analytics outputs

The generated CSV outputs are stored in:

- `analytics/total_sales_per_country.csv`
- `analytics/total_sales_per_category.csv`
- `analytics/sales_by_year_country_rollup.csv`
- `analytics/average_sales_cube.csv`

These outputs are generated from dimensional warehouse queries using joins, rollups, cubes, and grouped aggregations.

## Notes

If the load step is run twice without resetting the database, PostgreSQL will return duplicate primary key errors. That is expected because the warehouse tables already contain the loaded rows.
