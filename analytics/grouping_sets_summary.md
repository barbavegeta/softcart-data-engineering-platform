# Grouping Sets Summary

## Source Query

`warehouse/warehouse_queries.sql`

## Purpose

The grouping sets query calculates total sales across two separate dimensions:

- country
- product category

This allows the warehouse to return multiple aggregation levels in a single query instead of running separate queries for each dimension.

## Business Use

This output can support reporting questions such as:

- Which countries generate the highest total sales?
- Which product categories generate the highest total sales?
- How do country-level and category-level totals compare in one analytical result?
