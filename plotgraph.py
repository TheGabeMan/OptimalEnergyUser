import matplotlib.pyplot as plt
import numpy
import datetime


def create_plot(combined_list):
    # combined_list = numpy.load("dumpert.npy", allow_pickle=True)

    xas = None
    prices = None
    solar = None
    for row in combined_list:
        if xas is None:
            xas = [datetime.datetime.strftime(row[0], "%H:%m")]
            prices = [row[1]]
            solar = [row[3]]
        else:
            xas = xas + [datetime.datetime.strftime(row[0], "%H:%m")]
            prices = prices + [row[1]]
            solar = solar + [row[3]]

    fig, ax = plt.subplots()
    ax.bar(xas, prices, color="red", label="Price per KWh")
    ax.set_xlabel("Time")
    ax.set_ylabel("Solar Wh")
    ax.set_ylim(ymax=max(prices) * 1.5, ymin=0)
    plt.legend()

    ax2 = ax.twinx()
    ax2.plot(xas, solar, color="green", label="Solar Wh")
    ax2.set_ylabel("Price KWh")
    plt.legend()

    return plt
