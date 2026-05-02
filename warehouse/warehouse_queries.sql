-- Grouping sets: total sales by country and by category

SELECT
    T.country,
    C.category,
    SUM(F.amount) AS total_sales
FROM public."FactSales" AS F
LEFT JOIN public."DimCountry" AS T
    ON F.countryid = T.countryid
LEFT JOIN public."DimCategory" AS C
    ON F.categoryid = C.categoryid
GROUP BY GROUPING SETS (
    (T.country),
    (C.category)
);


-- Rollup: total sales by year and country, including subtotals

SELECT
    D.Year,
    T.country,
    SUM(F.amount) AS total_sales
FROM public."FactSales" AS F
LEFT JOIN public."DimDate" AS D
    ON F.dateid = D.dateid
LEFT JOIN public."DimCountry" AS T
    ON F.countryid = T.countryid
GROUP BY ROLLUP (D.Year, T.country);


-- Cube: average sales across all year/country combinations

SELECT
    D.Year,
    T.country,
    AVG(F.amount) AS average_sales
FROM public."FactSales" AS F
LEFT JOIN public."DimDate" AS D
    ON F.dateid = D.dateid
LEFT JOIN public."DimCountry" AS T
    ON F.countryid = T.countryid
GROUP BY CUBE (D.Year, T.country);


-- Materialized view: precomputed total sales per country

DROP MATERIALIZED VIEW IF EXISTS total_sales_per_country;

CREATE MATERIALIZED VIEW total_sales_per_country AS
SELECT
    T.country,
    SUM(F.amount) AS total_sales
FROM public."FactSales" AS F
LEFT JOIN public."DimCountry" AS T
    ON F.countryid = T.countryid
GROUP BY T.country;

REFRESH MATERIALIZED VIEW total_sales_per_country;

SELECT * FROM total_sales_per_country;
