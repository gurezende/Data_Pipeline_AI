-- gold layer from flights DB

{{ config(materialized='view') }}

-- Which routes are more popular
select
	flight_numbers, depart_city, depart_time, 
	COUNT(id) as number_of_flights
from {{ ref('silver_flights') }}
group by 1,2,3
order by depart_city, number_of_flights DESC 
 
