# Data Sources
## US Counties Dataset

## Weather Dataset
The weather dataset is queried and downloaded from Google BigQuery (See queries embedded in `../weather_stations_to_county.ipynb`). 
These datasets are composed off the yearly aggregate metrics for each weather station in the _Global Historical Climatology Network Daily_ table for 2020. 

Once the yearly weather data is pulled for each of the weather stations, the latitude and longitude is used to query the [FCC Block Api](https://geo.fcc.gov/api/census/#!/block/get_block_find) to get the county name, county FIPS, state, and state FIPS which is used to join to the US Counties dataset.

The weather stations are then aggregated at the county level, using median metrics to define a central value for the county. 

The final weather dataset is located in `additional_sources/2020_weather_station_to_county_aggregated_by_county.csv`


| field | description |
| ----- | ----------- |
| county | county name |
| county_fips | county fips code |
| state_id | state 2 letter code | 
| state_name | state full name | 
| state_fips | state fips code | 
| total_precip_mm | cumulative precipitation in mm |
| num_precip_days | number of days in which there was any precipitation |
| num_precip_days_greater_1mm | number of days in which the total precipitation was at least 1mm |
| 0.05\_percentile\_high | 0.05 percentile of daily highs in 2020 (i.e. 18th coldest day of the year) |
| 0.25\_percentile\_high | 0.25 percentile of daily highs in 2020 (i.e. 91st coldest day of the year) |
| 0.50\_percentile\_high | 0.50 percentile of daily highs in 2020 (i.e. 182nd coldest day of the year) |
| 0.75\_percentile\_high | 0.75 percentile of daily highs in 2020 (i.e. 274th coldest day of the year) |
| 0.95\_percentile\_high | 0.95 percentile of daily highs in 2020 (i.e. 347th coldest day of the year) |
| min_high | coldest day of the year |
| max_high | hottest day of the year | 

*note: for multiple weather stations within a county, metrics are centralized using the median value