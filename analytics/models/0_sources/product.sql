{{ config(materialized= 'table') }}


SELECT
    id,
    description,
    product_class,
    is_active,
    is_deleted,
    created_date,
    updated_date,
    name,
    product_category_id,
    cost,
    stock_keeping_unit
FROM {{ source('public', 'product2') }}
