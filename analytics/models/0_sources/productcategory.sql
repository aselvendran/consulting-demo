{{ config(materialized= 'table') }}


SELECT
    id,
    currency_iso_code,
    description,
    created_date,
    updated_date,
    name,
    number_of_products
FROM {{ source('public', 'productcategory') }}
