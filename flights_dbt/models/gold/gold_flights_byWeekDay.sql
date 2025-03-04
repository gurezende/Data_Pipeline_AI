-- gold layer from flights DB

{{ config(materialized='view') }}

-- average price by depart_city and weekday
select
	depart_city,
	wkday_name,
	ROUND( cast( AVG(ticket_prices_brl) as NUMERIC ), 3) as average_ticket_price
from {{ ref('silver_flights') }}
group by depart_city, wkday_name
order by depart_city, average_ticket_price ASC
    
 
