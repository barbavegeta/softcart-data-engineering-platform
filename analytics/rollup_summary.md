# Rollup Summary

## Source Query

`warehouse/warehouse_queries.sql`

## Purpose

The rollup query calculates total sales by year and country, while also producing subtotal and grand-total rows.

## Business Use

This output supports hierarchical sales reporting, for example:

- sales by country within each year
- yearly total sales across all countries
- overall sales across the full dataset

Rollups are useful when reports need both detailed and summarised totals.
