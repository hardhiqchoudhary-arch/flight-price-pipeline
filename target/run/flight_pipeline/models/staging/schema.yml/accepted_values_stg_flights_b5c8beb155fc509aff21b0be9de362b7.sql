
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        stop_type as value_field,
        count(*) as n_records

    from "flight_db"."public"."stg_flights"
    group by stop_type

)

select *
from all_values
where value_field not in (
    'direct','1 stop','multi-stop'
)



  
  
      
    ) dbt_internal_test