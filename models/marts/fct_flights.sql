-- models/marts/fct_flights.sql
-- Layer 3: Final analytics-ready table — Power BI connects here

with enriched as (
    select * from {{ ref('int_flights_enriched') }}
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
```

**Cmd + S** to save.

---

This is the **money layer** — it's what Power BI will query directly. Notice the `deal_flag` column — that's what will drive the dashboard insights: *"Is this flight a good deal right now?"*

Here's what we've built so far:
```
Raw flights table
      ↓
stg_flights.sql       (clean & standardize)
      ↓
int_flights_enriched.sql  (add business logic)
      ↓
fct_flights.sql       (Power BI connects here)