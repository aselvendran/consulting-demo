


SELECT
    id,
    birth_date ::date as birth_date,
    description,
    do_not_call,
    email,
    first_name,
    has_opted_out_of_email,
    home_phone,
    is_email_bounced,
    last_name,
    created_date,
    updated_date,
    address_id,
    middle_name,
    mobile_phone,
    name,
    phone
FROM "demo"."public"."contact"