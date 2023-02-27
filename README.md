# OptimalEnergyUser
What time of the day should you use your heavy devices?

# Goal of this script
Using dynamic energy tarifs, the cost of running heavy machinery can vary per hour. With this script you'll get a daily overview of the upcoming hourly tarifs, combined with the predicted solar panel delivery and the base power usage of your household. This graph will then be send to your family members, so they too know when to run heavy devices like a dishwasher, tumble dryer or washingmashine.

# SolarForecast
To get the forecast of your solarpanels, we're using the https://forecast.solar/ API. Though this is possible for free, please reward the maker by maybe signing up for the 'personal' plan or use the 'buy me a coffee' button on the website.

To make the forecast for your solar panels, you need to:
1- determine your exact location in latitude and longitude
2- determine the declination of your panels
3- determine the azimuth or orientation of your panels.
4- determine the peak watt of your solar panels in kWh (float)

Upon first usage of the script, you'll be asked to give these values, but you can also enter them in the .env file manually like:
LAT=54.9
LON=25.3
DEC=25
AZI=40
KWP=4.4

# Base consumption
If you now the base consumption of your household, this will be used in the calculations as well. You can enter a value in kWh hour to reflect the base consumption or add it manualy in the .env file:
BASE=0.5

# Power Consumption
Next we need to know the power consumption of some heavy devices in your house hold. You'll be asked for these in the first run of the script, but you can also enter and add them manually in the .env file, using the following format:
device01='name',powerusage in kWh for one run, duration in hours
device02='name',powerusage in kWh for one run, duration in hours

If you tumbledryer use 3kWh for one cycle and it will take 1,5hrs for the cycle, this would be:
device01='tumbledryer long program', 3, 1.5
and for the shorter program maybe 1.5kWh for half an hour:
device02='tumbledryver short program',1.5,0.5

# Energy Prices
Currently I can only read information from EnergyZero in the Netherlands.

