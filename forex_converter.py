# Script to convert BRL to USD
from currency_converter import CurrencyConverter
# Get rate

def get_usd_rate():
    """
    Get the current conversion rate from BRL to USD.
    
    Returns
    -------
    float
        The current conversion rate from BRL to USD.
    """
    c = CurrencyConverter()
    rate = c.convert(1, 'BRL', 'USD')
    return rate