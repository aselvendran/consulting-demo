{{ config(materialized= 'table') }}


SELECT
    id,
    product2_id,
    quantity,
    description
FROM {{ source('public', 'orderitem') }}
