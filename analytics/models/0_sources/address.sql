{{ config(materialized= 'table') }}


SELECT
    id,
    address,
    address_type,
    city,
    country,
    description,
    geocode_accuracy,
    latitude,
    longitude,
    postal_code,
    state,
    street,
    time_zone
FROM {{ source('public', 'address') }}
