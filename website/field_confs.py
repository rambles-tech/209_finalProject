import altair as alt
from collections import OrderedDict

### Define Field Selectors ###
density_cuts = [0, 20, 50, 100, 1000, float('inf')]
density_labels = ["0-20", "20-50", "50-100", "100-1000", "1000+"]

#DP Added
age_labels= ["0-25", "25-50", "50-75", "75-100+"]
## DP End

def create_slider(name, min_val, max_val, step, field_inits):
    slider = alt.binding_range(min=min_val, max=max_val, step=step)
    return alt.selection_single(name=name, fields=[f[0] for f in field_inits],
                                bind=slider, init=dict(field_inits))

def create_dropdown(name, options, field_inits):
    dropdown = alt.binding_select(options=options)
    return alt.selection_single(name=name,
                                fields=[f[0] for f in field_inits],
                                bind=dropdown, init=dict(field_inits))

temp_selector = create_slider("temperature", -30, 120, 0.1, [("low_temp", 10), ("high_temp", 90)])
precip_selector = create_slider("precipitation", 0, 365, 1, [("num_days", 100)])
education_selector = create_slider("education", 0, 100, 1, [("college_or_above", 20)])
income_selector = create_slider("income", 5000, 100000, 5000, [("individual_median", 25000)])
density_selector = create_dropdown("density", density_labels, [("group", "100-1000")])

#DP Added
age_selector = create_dropdown("age_median",age_labels,[("group", "25-50")])
home_value_selector = create_slider("home_value", 0, 2000000,50000, [("home_value", 500000)])
rent_median_selector = create_slider("rent_median", 0, 3000, 100, [("rent_median", 1000)])
unemployment_rate_selector= create_slider("unemployment_rate_average", 0, 100, 5,[("unemployment_rate_average", 5)])
crime_selector= create_slider("crime_rate_per_100000",0, 2000, 50, [("crime_rate_per_100000", 100)])
## DP End

FIELD_TYPE = "field_type"
COMPARATOR = "comparator"
ALIAS = "alias"
SELECTOR = "selector"
SELECTOR_FIELD = "field"

comparators = {
    "g": ">",
    "ge": ">=",
    "l": "<",
    "le": "<=",
    "eq": "=="
}

# this contains a superset of fields to selectors, should only need to append, not delete
fields_to_selectors = {
    "low_temp": {SELECTOR: temp_selector, SELECTOR_FIELD: "low_temp"},
    "high_temp": {SELECTOR: temp_selector, SELECTOR_FIELD: "high_temp"},
    "precip_num_days": {SELECTOR: precip_selector, SELECTOR_FIELD: "num_days"},
    "density_group": {SELECTOR: density_selector, SELECTOR_FIELD: "group"},
    "income_individual_median": {SELECTOR: income_selector, SELECTOR_FIELD: "individual_median"}
    #DP Added
    "age_median": {SELECTOR: age_selector, SELECTOR_FIELD: "age_median"}
    "home_value": {SELECTOR: home_value_selector, SELECTOR_FIELD: "home_value"}
    "rent_median": {SELECTOR: rent_median_selector, SELECTOR_FIELD: "rent_median"}
    "unemployment_rate_average": {SELECTOR: unemployment_rate_selector, SELECTOR_FIELD:"unemployment_rate_average"}
    "crime_rate_per_100000": {SELECTOR: crime_selector, SELECTOR_FIELD:"crime_rate_per_100000"}
    ##DP End
}

# this conf is what determines which fields get added to the selection criteria and plotted in the detailed view
# comment out the ones that you dont want to appear in the vis
fields_conf = OrderedDict()
fields_conf["low_temp"] = {
        FIELD_TYPE: "Q",
        COMPARATOR: "ge",
        ALIAS: "Coldest Daily Temperatures"
    }
fields_conf["high_temp"] = {
        FIELD_TYPE: "Q",
        COMPARATOR: "le",
        ALIAS: "Hottest Daily Temperatures"
    }
fields_conf["precip_num_days"] = {
        FIELD_TYPE: "Q",
        COMPARATOR: "le",
        ALIAS: "Number of Days with Precipitation"
    }
fields_conf["density_group"] = { # we should probably change this to a drop down of low/medium/high
        FIELD_TYPE: "O",
        COMPARATOR: "eq",
        ALIAS: "Population Density"
    }
fields_conf["income_individual_median"] = {
        FIELD_TYPE: "Q",
        COMPARATOR: "ge",
        ALIAS: "Median Individual Income"
    }
#DP Added
fields_conf["home_value"] = {
        FIELD_TYPE: "Q",
        COMPARATOR: "ge",
        ALIAS: "Median Home Value"
    }
fields_conf["rent_median"] = {
        FIELD_TYPE: "Q",
        COMPARATOR: "ge",
        ALIAS: "Median Rent Cost"
    }
fields_conf["age_median"] = {
        FIELD_TYPE: "O",
        COMPARATOR: "eq",
        ALIAS: "Median Age Group"
    }
fields_conf["unemployment_rate_average"] = {
        FIELD_TYPE: "Q",
        COMPARATOR: "ge",
        ALIAS: "Average Unemployment Rate"
    }
fields_conf["crime_rate_per_100000"] = {
        FIELD_TYPE: "Q",
        COMPARATOR: "ge",
        ALIAS: "Crime Rate per 100,000 Population"
    }
##DP End

def get_conf(vars):
    if vars:
        return {k: v for k, v in fields_conf.items() if k in vars}
    else:
        return fields_conf