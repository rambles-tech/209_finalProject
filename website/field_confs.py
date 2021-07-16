import altair as alt
from collections import OrderedDict

### Define Field Selectors ###
density_cuts = [0, 20, 50, 100, 1000, float('inf')]
density_labels = ["0-20", "20-50", "50-100", "100-1000", "1000+"]

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
        ALIAS: "Minimum Population Density"
    }
fields_conf["income_individual_median"] = {
        FIELD_TYPE: "Q",
        COMPARATOR: "ge",
        ALIAS: "Median Individual Income"
    }


def get_conf(vars):
    if vars:
        return {k: v for k, v in fields_conf.items() if k in vars}
    else:
        return fields_conf