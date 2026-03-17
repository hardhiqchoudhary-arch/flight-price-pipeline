
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select route
from "flight_db"."public"."fct_flights"
where route is null



  
  
      
    ) dbt_internal_test