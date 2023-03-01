""" Read Solar forecast from forecast.solar """
import logging
import sys
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_solarforecast():
    """Read forecast for tomorrow"""

    logging.info("Reading location information from .env")
    forecast_lat = os.getenv("LAT")
    forecast_lon = os.getenv("LON")
    forecast_dec = os.getenv("DEC")
    forecast_azi = os.getenv("AZI")
    forecast_kwp = os.getenv("KWP")
    # Nog doen: Missing some error checking

    # Example URL = https://api.forecast.solar/estimate/:lat/:lon/:dec/:az/:kwp
    # Example URL = "https://api.forecast.solar/estimate/50.82172/5.72486/25/40/4.4"
    url = (
        f"https://api.forecast.solar/estimate/watt_hours_period/{forecast_lat}/"
        f"{forecast_lon}/{forecast_dec}/{forecast_azi}/{forecast_kwp}"
        "?time=utc&no_sun=1"
    )
    # no_sun parameter to prevent last timestamp to be in middle of an hour block
    # see: https://doc.forecast.solar/api
    logging.info("Retrieve info from forecast.solar")
    response = requests.get(url=url, timeout=10)
    if response.status_code != 200:
        logging.error(
            "Error while retrieving info from forecast API. %s", response.status_code
        )
        sys.exit()
    forecast_json = response.json()
    return forecast_json
