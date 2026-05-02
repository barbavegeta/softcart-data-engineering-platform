# Materialized View Summary

## Source Query

`warehouse/warehouse_queries.sql`

## Purpose

The materialized view stores total sales per country as a precomputed result.

## Business Use

This improves reporting efficiency for repeated country-level sales queries because the aggregated result can be refreshed and queried directly instead of recomputing the join and aggregation every time.

## Output

The materialized view is named:

`total_sales_per_country`
