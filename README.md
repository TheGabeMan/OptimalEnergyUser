![GitHub all releases](https://img.shields.io/github/downloads/thegabeman/OptimalEnergyUser/total?logo=Github&style=plastic)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/thegabeman/OptimalEnergyUser?style=plastic)
![GitHub](https://img.shields.io/github/license/thegabeman/OptimalEnergyUser?style=plastic)
![GitHub issues](https://img.shields.io/github/issues/thegabeman/OptimalEnergyUser?style=plastic)

# OptimalEnergyUser
Send daily update to family members for the most optimal time to run heavy devices as cheap as possible.

# Goal of this script
Using dynamic energy tarifs, the cost of running heavy machinery can vary per hour. With this script you'll get a daily overview of the upcoming hourly tarifs, combined with the predicted solar panel delivery and the base power usage of your household. This graph will then be send to a Telegram Group chat, so the group members (family) now knows when to run heavy devices like a dishwasher, tumble dryer or washingmashine.

# SolarForecast
To get the forecast of your solarpanels, we're using the https://forecast.solar/ API. Though this is possible for free, please reward the maker by maybe signing up for the 'personal' plan or use the 'buy me a coffee' button on the website.

To make the forecast for your solar panels, you need to determine:
1. your exact location in latitude and longitude
2. the declination of your panels
3. the azimuth or orientation of your panels.
4. the peak watt of your solar panels in kWh (float)
5. Your timezone, for example 'Europe/Amsterdam'

Add these values to the .env file manually like:
```
LAT=54.9
LON=25.3
DEC=25
AZI=40
KWP=4.4
TIMEZONE=Europe/Amsterdam
```

# Telegram Token and chat ID
To be able to send messages to Telegram, you'll need to have a Telegram API Token and chat ID. There are many guides to be found on how to get those details. Add them to your .env file like this:
```
TELEGRAMAPI=<Your telefgram API key>
TELEGRAMCHANNELID=<Channel ID telefgram>
```
Note: my chat ID started with a minus sign, be sure to include it aswell if that is the case for you.

# Energy Prices
Currently I can only read information from EnergyZero in the Netherlands who's prices are also the prices for ANWB Energie, MijnDomein Energie, Energie van Ons, GroeneStroomLokaal.


# Use of EnergyZero and Solar.Forecast
This project makes use of the following other projects:
- [EnergyZero by Klaas Schoute](https://github.com/klaasnicolaas/python-energyzero)
- [Forecast.Solar by Knut Kohl](https://forecast.solar/) Though the use of his API is for free, please reward the maker by signing up for the 'personal' plan or use the 'buy me a coffee' button on the website.


# Changes
- March 22nd, 2023: Added TIMEZONE=Europe/Amsterdam to the .env, you should add this as well (with your timezone) to prevent the script from failing.
- April 21st, 2023: Added TMPIMAGEPATH=/home/OptimalEnergyUser to the .env. This points to the temp directory for the image generated. If not specified it will use the directory of the script.
- April 21st, 2023: Show the BASICHOUSEUSAGEWATT (Basic House Usage in WATT) in the image as third graph