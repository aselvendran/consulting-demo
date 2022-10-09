


SELECT
    *,
    CASE WHEN is_gift_greater_than_average IS NOT NULL
        AND MIN(CASE WHEN is_gift_greater_than_average
                    IS NOT NULL THEN ranking_of_purchase END) OVER (PARTITION BY id)  = ranking_of_purchase
    THEN true END as purchase_greater_than_average



FROM "demo"."public_staging"."stg__contact_opportunity_ranked"