{{ config(materialized= 'table') }}


SELECT
    id,
    account_id,
    billing_address_id,
    bill_to_contact_id,
    description,
    close_date,
    name,
    ordered_date,
    order_number,
    order_item_ids,
    related_order_id,
    shipping_address_id,
    status,
    total_amount,
    total_tax_amount,
    type
FROM {{ source('public', 'order') }}
