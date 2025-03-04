
{{ config(materialized='view') }}

select *
from {{ source('flights_raw', 'flight_prices') }}


/*
source(source file name, table name in Postgres)
*/