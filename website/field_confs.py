import altair as alt
from collections import OrderedDict

### Define Field Selectors ###
density_cuts = [0, 20, 50, 100, 1000, float('inf')]
density_labels = ["0-20", "20-50", "50-100", "100-1000", "1000+"]
age_cuts = [18, 25, 35, 45, 55, 65, float('inf')]
age_labels = ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]

def create_slider(name, min_val, max_val, step, field_inits):
    slider = alt.binding_range(min=min_val, max=max_val, step=step)
    return alt.selection_single(name=name, fields=[f[0] for f in field_inits],
                                bind=slider, init=dict(field_inits))

def create_dropdown(name, options, field_inits):
    dropdown = alt.binding_select(options=options)
    return alt.selection_single(name=name,
                                fields=[f[0] for f in field_inits],
                                bind=dropdown, init=dict(field_inits))

low_temp_selector = create_slider("temperature_low", -30, 120, 0.1, [("temp", 10)])
high_temp_selector = create_slider("temperature_high", -30, 120, 0.1, [("temp", 90)])
precip_selector = create_slider("precipitation", 0, 365, 1, [("num_days", 100)])
education_selector = create_slider("education", 0, 100, 1, [("college_or_above", 20)])
income_selector = create_slider("income", 5000, 100000, 5000, [("individual_median", 25000)])
density_selector = create_dropdown("density", density_labels, [("group", "100-1000")])

age_selector = create_dropdown("age_median", age_labels, [("group", "25-50")])
home_value_selector = create_slider("home", 0, 2000000, 50000, [("value", 500000)])
rent_median_selector = create_slider("rent", 0, 3000, 100, [("median", 1000)])
unemployment_rate_selector = create_slider("unemployment", 0, 100, 5, [("rate", 5)])
crime_selector = create_slider("crime", 0, 500, 0.5, [("rate_per_100000", 20)])

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
    "low_temp": {SELECTOR: low_temp_selector, SELECTOR_FIELD: "temp"},
    "high_temp": {SELECTOR: high_temp_selector, SELECTOR_FIELD: "temp"},
    "precip_num_days": {SELECTOR: precip_selector, SELECTOR_FIELD: "num_days"},
    "density_group": {SELECTOR: density_selector, SELECTOR_FIELD: "group"},
    "income_individual_median": {SELECTOR: income_selector, SELECTOR_FIELD: "individual_median"},
    "age_median_group": {SELECTOR: age_selector, SELECTOR_FIELD: "group"},
    "home_value": {SELECTOR: home_value_selector, SELECTOR_FIELD: "value"},
    "rent_median": {SELECTOR: rent_median_selector, SELECTOR_FIELD: "median"},
    "unemployment_rate_average": {SELECTOR: unemployment_rate_selector, SELECTOR_FIELD: "rate"},
    "crime_rate_per_100000": {SELECTOR: crime_selector, SELECTOR_FIELD: "rate_per_100000"}
}

# this conf is what determines which fields get added to the selection criteria and plotted in the detailed view
# comment out the ones that you dont want to appear in the vis
fields_conf = OrderedDict()
fields_conf["low_temp"] = {
        FIELD_TYPE: "Q",
        COMPARATOR: "ge",
        ALIAS: "Coldest Daily Temperature"
    }
fields_conf["high_temp"] = {
        FIELD_TYPE: "Q",
        COMPARATOR: "le",
        ALIAS: "Hottest Daily Temperature"
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
fields_conf["age_median_group"] = {
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


def get_conf(vars):
    if vars:
        new_dict = OrderedDict()
        for k, v in fields_conf.items():
            if k in vars:
                new_dict[k] = v
        return new_dict
    else:
        return fields_conf