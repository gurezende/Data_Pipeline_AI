# Script to validate the data with pandera

import streamlit as st
from datetime import datetime
from pandera import Column, Check, DataFrameSchema
from pandera.errors import SchemaError


# Define a Schema
Schema = DataFrameSchema({
    "dt": Column(str),
    "depart_city": Column(str),
    "depart_time": Column(str),
    "city_arrival": Column(str),
    "time_arrival": Column(str),
    "flight_numbers": Column(str),
    "n_stops": Column(str),
    "flight_lengths": Column(float, Check.greater_than(0)),
    "ticket_prices": Column(float, Check.greater_than_or_equal_to(0)),
    "days_before_flight": Column(int, Check.greater_than(0))
})


# Define a function to validate the data
def validate_data(data):# Validate data
    """
    Validate a DataFrame against a predefined schema.

    Parameters
    ----------
    data : DataFrame
        DataFrame to validate.

    Returns
    -------
    bool
        True if the DataFrame validates successfully, False otherwise.
    """
    try:
        validated_df = Schema.validate(data)
        st.write(":heavy_check_mark: DataFrame validated SUCCESSFULLY!")
        return True
    except SchemaError as e:
        st.error(f"DataFrame validation FAILED: {e}",
                 icon="❌")
        return False
    