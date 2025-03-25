-- gold layer from flights DB

{{ config(materialized='view') }}

-- Average price by depart_city and days_ahead
select
	depart_city,
	days_before_flight ,
	ROUND( cast( AVG(ticket_prices) as NUMERIC ), 3) as average_ticket_price
from {{ ref('silver_flights') }}
group by depart_city, days_before_flight
order by depart_city, average_ticket_price asc
    
 
