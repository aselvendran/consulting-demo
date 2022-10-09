{{ config(materialized= 'table') }}


SELECT
    id,
    account_source,
    billing_address_id,
    description,
    industry,
    created_date,
    updated_date,
    name,
    phone,
    shipping_address_id
FROM {{ source('public', 'account') }}
