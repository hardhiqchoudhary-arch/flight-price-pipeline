
    
    

select
    id as unique_field,
    count(*) as n_records

from "flight_db"."public"."stg_flights"
where id is not null
group by id
having count(*) > 1


