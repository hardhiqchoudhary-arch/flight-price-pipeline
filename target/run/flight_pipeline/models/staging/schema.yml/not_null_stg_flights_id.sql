
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select id
from "flight_db"."public"."stg_flights"
where id is null



  
  
      
    ) dbt_internal_test