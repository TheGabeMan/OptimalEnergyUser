''' Determine optimal time of day to run power heavy devices '''
import asyncio
import datetime
import uuid
import sys
import os
import matplotlib.pyplot as plt
import numpy
import plotgraph
# import pytz
from energyzero import EnergyZero
import solarforecast
import send_telegram

def main():
    ''' Main script'''
    # Nog doen: controle op env inhoud en eventueel vragen om input

    # Inlezen EnergyZero
    energyprices = asyncio.run(get_energy_prices())

    # Inlezen forecast
    solar_forecastjson = solarforecast.get_solarforecast()

    combined_list = get_combined_values(energyprices,solar_forecastjson)

    # Voor debugging opslaan van combined_list
    # numpy.save('dumpert', combined_list, allow_pickle=True)
    # Controle waar voldoende stroom opgevangen wordt om een apparaat te draaien
    # Nog doen: uitzoeken welk moment 't meest gunstig is

    # Grafiek plotten
    plt = plotgraph.create_plot(combined_list)

    # Generate temp file name
    image_name = '{}{:-%Y%m%d%H%M%S}.jpeg'.format(str(uuid.uuid4().hex), datetime.datetime.now())
    plt.savefig( image_name, format='png', dpi=300)

    # Grafiek verzenden
    send_telegram.send_telegram_message('Energy prices and solar forecast for tomorrow')
    send_telegram.send_telegram_image(image_name)
   

    # Remove the temporary file
    os.remove(image_name)

    # Verwerken forecast, energtzero, zware apparaten tot 1 overzicht



def get_combined_values(energyprices,solar_forecastjson):
    ''' Combine Energy prices and forecast'''
    # tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    # tomorrow = datetime.datetime.strptime(tomorrow, ("%Y-%m-%d"))
    # utcstamp = tomorrow.astimezone(pytz.utc)
    # targettimezone = pytz.timezone('Europe/Amsterdam')
    combined_list = None
    for electrictytimestamp, electrictyprice in energyprices.prices.items():
        found_forecast = False
        for forecasttime,forecastvalue  in solar_forecastjson["result"].items():
            if datetime.datetime.strptime(forecasttime,"%Y-%m-%dT%H:%M:%S%z") == electrictytimestamp:
                found_forecast = True
                if combined_list is None:
                    combined_list = numpy.array( [[electrictytimestamp,
                                                   electrictyprice,
                                                   datetime.datetime.strptime(forecasttime,"%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=datetime.timezone.utc),
                                                   forecastvalue]])
                else:
                    combined_list = numpy.append( combined_list, 
                                                  [[electrictytimestamp,
                                                    electrictyprice,
                                                    datetime.datetime.strptime(forecasttime,"%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=datetime.timezone.utc),
                                                    forecastvalue]],
                                                    axis=0 )
                break

        if found_forecast is False:
            if combined_list is None:
                combined_list = numpy.array([[electrictytimestamp,
                                              electrictyprice,
                                              electrictytimestamp,
                                              0]])
            else:
                combined_list = numpy.append(combined_list,
                                             [[electrictytimestamp,
                                               electrictyprice,
                                               electrictytimestamp,
                                               0]],
                                               axis=0)
             
    # print('************     COMBINED LIST    *********')
    # for row in combined_list:
    #     print( row )

    return combined_list

async def get_energy_prices() -> None:
    """fetching the energy prices from EnergyZero using
    Energyzero package
    https://pypi.org/project/energyzero/ """

    async with EnergyZero(incl_btw="true") as client:
        start_date = datetime.datetime.today()
        end_date = start_date + datetime.timedelta(days=1)
        energy = await client.energy_prices(start_date, end_date)
        return energy

if __name__ == "__main__":
    sys.exit(main())
