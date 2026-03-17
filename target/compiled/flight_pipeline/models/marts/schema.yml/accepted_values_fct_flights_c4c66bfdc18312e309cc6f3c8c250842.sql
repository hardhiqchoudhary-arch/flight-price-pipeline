
    
    

with all_values as (

    select
        deal_flag as value_field,
        count(*) as n_records

    from "flight_db"."public"."fct_flights"
    group by deal_flag

)

select *
from all_values
where value_field not in (
    'good deal','fair price','overpriced'
)


