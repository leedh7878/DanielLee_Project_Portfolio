# NOOAA Shiny App: Project Overview

* Develop a Shiny app to access and efficiently present precipitation data for weather stations in Washington State, sourced from the NOAA API

* Allow users to select any year within the range of 2000 to 2003 and provide the option to choose from all available months.

* Provide an interactive interface to visualize the monthly precipitation data for the selected year.

* Implement a bar graph that highlights the top 5 areas (stations) with the highest recorded precipitation levels.

# Data Collections


This API is for developers looking to create their own scripts or programs that use the CDO database of weather and climate data.
https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted


# Data Visualization

* The Leaflet library was utilized to create an interactive map for visualizing precipitation values.

* The colors of circles on the map represent precipitation values, with variations depicted by a palette shown alongside the Leaflet map.


# App publication

* Utilizing the rsconnect library, publish the Shiny app on shinyapps.io to make it publicly accessible