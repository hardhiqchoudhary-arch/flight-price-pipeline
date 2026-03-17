
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select origin
from "flight_db"."public"."stg_flights"
where origin is null



  
  
      
    ) dbt_internal_test