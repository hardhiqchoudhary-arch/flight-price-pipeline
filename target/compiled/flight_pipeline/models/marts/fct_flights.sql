-- models/marts/fct_flights.sql
-- Layer 3: Final analytics-ready table — Power BI connects here

with enriched as (
    select * from "flight_db"."public"."int_flights_enriched"
),

final as (
    select
        -- identifiers
        id,

        -- route
        origin,
        destination,
        origin || ' → ' || destination as route,

        -- flight info
        flight_date,
        day_of_week,
        flight_month,
        days_until_departure,
        airline,
        duration_minutes,
        round(duration_minutes / 60.0, 1) as duration_hours,
        stops,
        stop_type,

        -- pricing
        price_usd,
        price_category,
        price_rank,
        round(avg_route_price, 2)               as avg_route_price,
        round(price_usd - avg_route_price, 2)   as price_vs_avg,

        -- is this a good deal?
        case
            when price_usd < avg_route_price * 0.9 then 'good deal'
            when price_usd > avg_route_price * 1.1 then 'overpriced'
            else 'fair price'
        end as deal_flag,

        -- metadata
        ingested_at

    from enriched
)

select * from final