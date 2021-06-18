# W209 Final Project - Life Locator

## Dataset description

### US Counties Dataset
A collection of data from simplemaps.com, sourced from the U.S. Bureau of Labor Statistics and the 2019 American Community Survey which is hosted by the United States Census Bureau.


| field | description |
|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| county                      | The name of the county.                                                                                                                                              |
| county_ascii                | county as an ASCII string.                                                                                                                                           |
| county_fips                 | The 5-digit FIPS code of the county. The first two digits correspond to the state's FIPS code.                                                                       |
| state_id                    | The state or territory's USPS postal abbreviation.                                                                                                                   |
| state_name                  | The name of the state or territory that contains the county.                                                                                                         |
| lat                         | The latitude of the county.                                                                                                                                          |
| lng                         | The longitude of the county.                                                                                                                                         |
| population                  | An estimate of the county's population.                                                                                                                              |
| density                     | The estimated population per square kilometer.                                                                                                                       |
| timezone                    | The county's primary timezone in the tz database format. (e.g. America/Los_Angeles)                                                                                  |
| zips                        | A string containing all five-digit zip codes in the county, delimited by a space.                                                                                    |
| age_median                  | The median age of residents in the county.                                                                                                                           |
| male                        | The percentage of residents who report being male (e.g. 55.1).                                                                                                       |
| female                      | The percentage of residents who report being female (e.g. 44.9).                                                                                                     |
| married                     | The percentage of residents who report being married (e.g. 44.9).                                                                                                    |
| family_size                 | The average size of resident families (e.g. 3.22).                                                                                                                   |
| income_household_median     | Median household income in USD.                                                                                                                                      |
| income_household_six_figure | Percentage of households that earn at least $100,000 (e.g. 25.3)                                                                                                     |
| home_ownership              | Percentage of households that own (rather than rent) their residence.                                                                                                |
| home_value                  | The median value of homes that are owned by residents.                                                                                                               |
| rent_median                 | The median rent paid by renters.                                                                                                                                     |
| education_college_or_above  | The percentage of residents with at least a 4-year degree.                                                                                                           |
| labor_force_participation   | The percentage of residents 16 and older in the labor force.                                                                                                         |
| labor_force                 | The number of people in the labor force. Updated monthly with a lag as of bls_date.                                                                                  |
| unemployment_rate           | The percentage of residents unemployed. Updated monthly with a lag as of bls_date.                                                                                   |
| bls_date                    | The date (MM-YYYY) when labor_force, labor_force_average, unemployment_rate, and unemployment_rate_average data was colleced by the U.S. Bureau of Labor Statistics. |
| race_white                  | The percentage of residents who report their race White.                                                                                                             |
| race_black                  | The percentage of residents who report their race as Black or African American.                                                                                      |
| race_asian                  | The percentage of residents who report their race as Asian.                                                                                                          |
| race_native                 | The percentage of residents who report their race as American Indian and Alaska Native.                                                                              |
| race_pacific                | The percentage of residents who report their race as Native Hawaiian and Other Pacific Islander.                                                                     |
| race_other                  | The percentage of residents who report their race as Some other race.                                                                                                |
| race_multiple               | The percentage of residents who report their race as Two or more races.                                                                                              |
| age_under_10                | The percentage of residents aged 0-9.                                                                                                                                |
| age_10_to_19                | The percentage of residents aged 10-19.                                                                                                                              |
| age_20s                     | The percentage of residents aged 20-29.                                                                                                                              |
| age_30s                     | The percentage of residents aged 30-39.                                                                                                                              |
| age_40s                     | The percentage of residents aged 40-49.                                                                                                                              |
| age_50s                     | The percentage of residents aged 50-59.                                                                                                                              |
| age_60s                     | The percentage of residents aged 60-69.                                                                                                                              |
| age_70s                     | The percentage of residents aged 70-79.                                                                                                                              |
| age_over_80                 | The percentage of residents aged over 80.                                                                                                                            |
| divorced                    | The percentage of residents divorced.                                                                                                                                |
| never_married               | The percentage of residents never married.                                                                                                                           |
| widowed                     | The percentage of residents never widowed.                                                                                                                           |
| family_dual_income          | The percentage of families with dual income earners.                                                                                                                 |
| income_household_under_5    | The percentage of households with income under $5,000.                                                                                                               |
| income_household_5_to_10    | The percentage of households with income from $5,000-$10,000.                                                                                                        |
| income_household_10_to_15   | The percentage of households with income from $10,000-$15,000.                                                                                                       |
| income_household_15_to_20   | The percentage of households with income from $15,000-$20,000.                                                                                                       |
| income_household_20_to_25   | The percentage of households with income from $20,000-$25,000.                                                                                                       |
| income_household_25_to_35   | The percentage of households with income from $25,000-$35,000.                                                                                                       |
| income_household_35_to_50   | The percentage of households with income from $35,000-$50,000.                                                                                                       |
| income_household_50_to_75   | The percentage of households with income from $50,000-$75,000.                                                                                                       |
| income_household_75_to_100  | The percentage of households with income from $75,000-$100,000.                                                                                                      |
| income_household_100_to_150 | The percentage of households with income from $100,000-$150,000.                                                                                                     |
| income_household_150_over   | The percentage of households with income over $150,000.                                                                                                              |
| income_individual_median    | The median income of individuals in the county.                                                                                                                      |
| home_value                  | The median value of owner occupied homes.                                                                                                                            |
| rent_burden                 | The median rent as a percentage of the median renter's household income.                                                                                             |
| education_less_highschool   | The percentage of residents with less than a high school education.                                                                                                  |
| education_highschool        | The percentage of residents with a high school diploma but no more.                                                                                                  |
| education_some_college      | The percentage of residents with some college but no more.                                                                                                           |
| education_bachelors         | The percentage of residents with a bachelor's degree (or equivalent) but no more.                                                                                    |
| education_graduate          | The percentage of residents with a graduate degree.                                                                                                                  |
| education_stem_degree       | The percentage of residents with a Bachelor's degree or higher in a Science and Engineering (or related) field.                                                      |
| disabled                    | The percentage of residents who report a disability.                                                                                                                 |
| limited_english             | The percentage of residents who only speak limited English.                                                                                                          |
| commute_time                | The median commute time of resident workers in minutes.                                                                                                              |
| health_uninsured            | The percentage of residents who report not having health insurance.                                                                                                  |
| veteran                     | The percentage of residents who are veterans.                                                                                                                        |
| labor_force_average         | The number of people in the labor force, averaged over the last 12 months. Updated monthly with a lag as of bls_date.                                                |
| unemployment_rate_average   | The percentage of residents unemployed, averaged over the last 12 months. Updated monthly with a lag as of bls_date.                                                 |
| timezone_all                | Some counties are in multiple timezones. This fields lists every timezone delimited by a '\|'.                                                                       |


### Weather Dataset
The weather dataset is queried and downloaded from Google BigQuery (See queries embedded in `../weather_stations_to_county.ipynb`).
These datasets are composed off the yearly aggregate metrics for each weather station in the _Global Historical Climatology Network Daily_ table for 2020.

Once the yearly weather data is pulled for each of the weather stations, the latitude and longitude is used to query the [FCC Block Api](https://geo.fcc.gov/api/census/#!/block/get_block_find) to get the county name, county FIPS, state, and state FIPS which is used to join to the US Counties dataset.

The weather stations are then aggregated at the county level, using median metrics to define a central value for the county.

The final weather dataset is located in `additional_sources/2020_weather_station_to_county_aggregated_by_county.csv`

The fields included in the overall dataset include:

| field | description |
| ----- | ----------- |
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

### Crime Rate

The Crime Rate dataset was sourced from the [United States crime rates by county](https://www.kaggle.com/mikejohnsonjr/united-states-crime-rates-by-county) Kaggle competition.  It provides Crime Rate data from 2016.

The fields included in the overall dataset include:


| field | description |
| ----- | ----------- |
| crime_rate_per_100000 | The rate of all victimized and non-victimized crime per 100,000 population |
