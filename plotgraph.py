"""Generate the data for the Graph"""
import datetime
import matplotlib.pyplot as plt
import numpy


def create_plot(combined_list):
    """Generate the data for the Graph"""
    # DEBUG: combined_list = numpy.load("dumpert.npy", allow_pickle=True)
    rows = len(combined_list)
    prices = combined_list[0 : rows + 1, 1:2]
    solar = combined_list[0 : rows + 1, 3:4]

    xas = [(str(combined_list[i][0].hour) + ":00") for i in range(rows)]
    forecastdate = datetime.datetime.strftime(combined_list[12][0], "%A %d %B %Y")
    max_prices = max(prices.flatten()) * 1.5

    fig, ax = plt.subplots()
    ax.bar(xas, prices.flatten(), color="#76ff7b", label="Price per KWh")
    ax.set_xticks(xas, xas, rotation=45, fontsize=5)
    ax.set_xlabel("Time of day")
    ax.set_ylabel("Price in Euro's")
    ax.set_ylim(ymax=max_prices, ymin=0)
    ax.legend()

    ax2 = ax.twinx()
    ax2.plot(solar, color="green", label="Solar Forecast in Wh")
    ax2.set_ylabel("Wh")
    ax2.legend()

    plt.title("Forecast for " + forecastdate)
    plt.legend(loc="upper left")

    return plt, forecastdate
