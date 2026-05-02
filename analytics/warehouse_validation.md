# Warehouse Validation

The SoftCart warehouse was loaded successfully into PostgreSQL and validated using table row counts.

## Loaded Tables

| Table | Row Count |
|---|---:|
| DimDate | 1,096 |
| DimCategory | 5 |
| DimCountry | 56 |
| FactSales | 300,000 |

## Generated Analytics Outputs

| Output | Description |
|---|---|
| `total_sales_per_country.csv` | Total sales aggregated by country |
| `total_sales_per_category.csv` | Total sales aggregated by product category |
| `sales_by_year_country_rollup.csv` | Sales rollup by year and country |
| `average_sales_cube.csv` | Average sales across year/country cube combinations |

## Notes

The warehouse queries were adapted to match the actual schema column names used in the supplied capstone tables.
