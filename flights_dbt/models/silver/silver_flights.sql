
{{ config(materialized='view') }}

-- clean silver layer
select
	id,
	dt,
	depart_city,
	depart_time,
	(CAST(LEFT(depart_time, 2) AS INTEGER)) as depart_hour, -- add depart_hour
	TO_CHAR(TO_DATE(dt, 'DD/MM/YYYY'), 'Day') AS wkday_name, -- add column wkday name
	EXTRACT(DAY FROM TO_DATE(dt, 'DD/MM/YYYY')) AS daynumber, -- add column day number
	EXTRACT(MONTH FROM TO_DATE(dt, 'DD/MM/YYYY')) AS mth,-- add column mthday
	city_arrival,
	LEFT(time_arrival,5) as time_arrival, -- strip values from  time_arrival
	flight_numbers,
	n_stops AS connex,
	case 
		WHEN n_stops = 'Direto' THEN 0
		ELSE cast(LEFT(n_stops, 1) as INTEGER)
	END as stops, -- make n_stops integer (Direto = 0)
	ROUND(CAST(flight_lengths AS NUMERIC), 2) as flight_lengths, -- flight_length with 2 decimals
	ticket_prices as ticket_prices_BRL,
	days_before_flight
from {{ ref('bronze_flights') }}



/*
source(source file name, table name in Postgres)
*/