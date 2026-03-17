
  create view "flight_db"."public"."int_flights_enriched__dbt_tmp"
    
    
  as (
    -- models/intermediate/int_flights_enriched.sql
-- Layer 2: Enrich staged data with business logic and price analytics

with staged as (
    select * from "flight_db"."public"."stg_flights"
),

enriched as (
    select
        *,

        -- price buckets
        case
            when price_usd < 300  then 'budget'
            when price_usd < 500  then 'moderate'
            when price_usd < 800  then 'expensive'
            else 'premium'
        end as price_category,

        -- day of week (useful for ML later)
        to_char(flight_date, 'Day')     as day_of_week,
        extract(dow from flight_date)   as day_of_week_num,
        extract(month from flight_date) as flight_month,

        -- days until departure
        (flight_date - current_date)    as days_until_departure,

        -- price vs route average
        avg(price_usd) over (
            partition by origin, destination
        ) as avg_route_price,

        -- price rank within route (1 = cheapest)
        rank() over (
            partition by origin, destination
            order by price_usd asc
        ) as price_rank

    from staged
)

select * from enriched
  );