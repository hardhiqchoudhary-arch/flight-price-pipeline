
  create view "flight_db"."public"."stg_flights__dbt_tmp"
    
    
  as (
    -- models/staging/stg_flights.sql
-- Layer 1: Clean and standardize raw flight data

with source as (
    select * from flights
),

staged as (
    select
        -- identifiers
        id,
        
        -- route info
        upper(trim(origin))      as origin,
        upper(trim(destination)) as destination,
        
        -- flight details
        flight_date,
        airline,
        price::numeric(10,2)     as price_usd,
        duration                 as duration_minutes,
        stops,
        
        -- derived columns
        case 
            when stops = 0 then 'direct'
            when stops = 1 then '1 stop'
            else 'multi-stop'
        end as stop_type,

        -- metadata
        current_timestamp as ingested_at

    from source
    where price is not null
      and flight_date >= current_date
)

select * from staged
  );