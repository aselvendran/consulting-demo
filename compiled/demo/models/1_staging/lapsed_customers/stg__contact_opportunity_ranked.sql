


SELECT
    contact.*,
    orders.total_amount,
    close_date ::date as close_date,
    FIRST_VALUE(orders.account_id) OVER (PARTITION BY contact.id ORDER BY ordered_date ASC) initial_account_id,
    COUNT(orders.account_id) OVER (PARTITION BY contact.id) count_accounts,
    COUNT(orders.id) OVER (PARTITION BY contact.id) count_gifts,
    ROW_NUMBER () OVER (PARTITION BY contact.id ORDER BY close_date ASC) as ranking_of_purchase,
    AVG(orders.total_amount) OVER (PARTITION BY contact.id) as average_purchase,
    AVG(orders.total_amount) OVER (PARTITION BY contact.id, orders.account_id) as average_purchase_by_account,
    LAG(close_date ::date ,1) OVER (partition by contact.id ORDER BY close_date ::date DESC) as following_gift,


    CASE WHEN orders.total_amount > AVG(orders.total_amount) OVER (PARTITION BY contact.id)
        THEN 'order_greater_than_average' ELSE NULL END as is_gift_greater_than_average,
    floor((close_date ::date - LAG(close_date ::date ,1) OVER (partition by contact.id ORDER BY close_date ::date ASC))/7) as previous_purchase_week_diff,
    floor((close_date ::date - MIN(close_date ::date) OVER (partition by contact.id ))/7) as week_diff_from_first_purchase

FROM "demo"."public_sources"."contact" as contact
    INNER JOIN "demo"."public_sources"."orders" as orders
    ON contact.id = orders.bill_to_contact_id