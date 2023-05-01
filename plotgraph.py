"""Generate the data for the Graph"""
import os
import datetime
import matplotlib.pyplot as plt
import numpy
from dotenv import load_dotenv
import main

load_dotenv()


def create_plot(combined_list,forecast_date):
    """Generate the data for the Graph"""
    main.debuglog('Create Graphs')

    forecast_kwp = float(os.getenv("KWP")) * 1000
    if float( os.getenv("BASICHOUSEUSAGEWATT")) > 0:
        basic_house_usage = float(os.getenv("BASICHOUSEUSAGEWATT"))
    else:
        basic_house_usage = 0

    rows = len(combined_list)
    prices = combined_list[0 : rows + 1, 1:2]
    solar = combined_list[0 : rows + 1, 3:4]

    xas = [(str(combined_list[i][0].hour) + ":00") for i in range(rows)]
    max_prices = max(prices.flatten()) * 1.5
    if min(prices.flatten()) * 1.25 >0:
        min_prices = 0
    else:
        min_prices = min(prices.flatten()) * 1.25

    fig, ax = plt.subplots()
    ax.bar(xas, prices.flatten(), color="#76ff7b", label="Price per KWh")
    ax.set_xticks(xas, xas, rotation=45, fontsize=5)
    ax.set_xlabel("Time of day")
    ax.set_ylabel("Price in Euro's")
    ax.set_ylim(ymax=max_prices, ymin=min_prices)
    ax.legend()

    ax2 = ax.twinx()
    ax2.plot(solar, color="green", label="Solar Forecast in Wh")
    ax2.set_ylabel("Wh")
    ax2.set_ylim(ymax=forecast_kwp, ymin=0)
    ax2.legend()

    plt.axhline(basic_house_usage,xmin=0, xmax=forecast_kwp, color="orange" )
    ax2.plot(basic_house_usage,
             color="orange",
             label=f"Basic House Usage {basic_house_usage} Watt")
    plt.title("Forecast for " + forecast_date)
    plt.legend(loc="upper left")

    return plt
