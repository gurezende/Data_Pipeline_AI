-- gold layer from flights DB

{{ config(materialized='view') }}

-- Average price by depart_city and month
select
	depart_city,
	month_number,
	ROUND( cast( AVG(ticket_prices_brl) as NUMERIC ), 3) as average_ticket_price
from {{ ref('silver_flights') }}
group by depart_city, month_number
order by depart_city, average_ticket_price asc
 
