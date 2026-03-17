
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select destination
from "flight_db"."public"."stg_flights"
where destination is null



  
  
      
    ) dbt_internal_test