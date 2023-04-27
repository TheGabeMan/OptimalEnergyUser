""" Determine optimal time of day to run power heavy devices """
import asyncio
import datetime
import uuid
import sys
import os
import matplotlib.pyplot as plt
import numpy
from energyzero import EnergyZero
import plotgraph
import solarforecast
import send_telegram


def main():
    """Main script"""
    # Nog doen: controle op env inhoud en eventueel vragen om input

    # Get EnergyZero prices
    energyprices = asyncio.run(get_energy_prices())

    # Get forecast info
    solar_forecastjson = solarforecast.get_solarforecast()

    # Combine Energy Prices and SolarForcast
    combined_list = get_combined_values(energyprices, solar_forecastjson)
    forecast_date = datetime.datetime.strftime(combined_list[12][0], "%A %d %B %Y")

    # Voor debugging opslaan van combined_list
    # numpy.save('dumpert', combined_list, allow_pickle=True)

    # Plot Graph
    plt = plotgraph.create_plot(combined_list,forecast_date)

    if os.getenv("TMPIMAGEPATH") is None:
        tmp_image_path = "./"
    elif os.getenv("TMPIMAGEPATH")[-1] == "/":
        tmp_image_path = os.getenv("TMPIMAGEPATH")
    else:
        tmp_image_path = os.getenv("TMPIMAGEPATH") + "/"

    # Generate temp file name
    image_name = tmp_image_path + "{}{:-%Y%m%d%H%M%S}.jpeg".format(
        str(uuid.uuid4().hex), datetime.datetime.now()
    )
    plt.savefig(image_name, format="png", dpi=300)

    # Send to Telegram
    telegram_text = send_telegram.create_body_text(energyprices, forecast_date)
    send_telegram.send_telegram_message(telegram_text)
    send_telegram.send_telegram_image(image_name)

    # Remove the temporary file
    os.remove(image_name)


def get_combined_values(energyprices, solar_forecastjson):
    """Combine Energy prices and forecast"""
    combined_list = None
    for electrictytimestamp, electrictyprice in energyprices.prices.items():
        found_forecast = False
        for forecasttime, forecastvalue in solar_forecastjson.items():
            forecast_dt = datetime.datetime.fromisoformat(forecasttime)
            forecast_utc_dt = forecast_dt.astimezone(datetime.timezone.utc)
            if forecast_utc_dt == electrictytimestamp:
                found_forecast = True
                if combined_list is None:
                    combined_list = numpy.array(
                        [
                            [
                                electrictytimestamp,
                                electrictyprice,
                                datetime.datetime.strptime(
                                    forecasttime, "%Y-%m-%dT%H:%M:%S%z"
                                ).replace(tzinfo=datetime.timezone.utc),
                                forecastvalue,
                            ]
                        ]
                    )
                else:
                    combined_list = numpy.append(
                        combined_list,
                        [
                            [
                                electrictytimestamp,
                                electrictyprice,
                                datetime.datetime.strptime(
                                    forecasttime, "%Y-%m-%dT%H:%M:%S%z"
                                ).replace(tzinfo=datetime.timezone.utc),
                                forecastvalue,
                            ]
                        ],
                        axis=0,
                    )
                break

        if found_forecast is False:
            if combined_list is None:
                combined_list = numpy.array(
                    [[electrictytimestamp, electrictyprice, electrictytimestamp, 0]]
                )
            else:
                combined_list = numpy.append(
                    combined_list,
                    [[electrictytimestamp, electrictyprice, electrictytimestamp, 0]],
                    axis=0,
                )
    return combined_list


async def get_energy_prices() -> None:
    """fetching the energy prices from EnergyZero using
    Energyzero package
    https://pypi.org/project/energyzero/"""

    async with EnergyZero(incl_btw="true") as client:
        if datetime.datetime.today().hour <= 6:
            """Since new prices will be available after 15:00, calling them after
            midnight but before 15:00 will result in empty response. But also since it
            is only for debugging that EnergyZero will be queried after midnight,
            I'm using before 6am as time check"""
            end_date = datetime.datetime.today()
        else:
            end_date = datetime.datetime.today() + datetime.timedelta(days=1)

        start_date = end_date  # We only need one day
        energy = await client.energy_prices(start_date, end_date)
        return energy


if __name__ == "__main__":
    sys.exit(main())
