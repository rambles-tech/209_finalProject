import pandas as pd
import altair as alt
import os
from field_confs import *

from vega_datasets import data

WIDTH = 800
HEIGHT = 500
dataFilePath = os.path.dirname(os.path.abspath(__file__)) + "/static/data_sources/final_transformed_data.csv"

counties_boundaries = alt.topo_feature(data.us_10m.url, 'counties')
state_boundaries = alt.topo_feature(data.us_10m.url, 'states')

outline = alt.Chart(state_boundaries).mark_geoshape(stroke='black', fillOpacity=0).project(
    type='albersUsa'
).properties(
    width=WIDTH,
    height=HEIGHT
)

# define state selection
county = pd.read_csv(dataFilePath)
state_dropdown = alt.binding_select(options=sorted(county.state_id.dropna().unique().tolist()))
state_selector = alt.selection_single(name="state", fields=['state_id'], bind=state_dropdown, init={"state_id": "CA"})

def create_match_pct(fields_conf, selectors):
    n_fields = len(fields_conf)
    formula = []
    for f, conf in fields_conf.items():
        selector = f"{selectors.get(f).get(SELECTOR).name}.{selectors.get(f).get(SELECTOR_FIELD)}"
        formula.append("(datum.{f} {comp} {selector})".format(f=f, 
                                                              comp=comparators.get(conf.get(COMPARATOR)), 
                                                              selector=selector))
    added = "(" + " + ".join(formula) + ")"
    return added + f" / {n_fields}"

def build_chart(data_url, fields_conf, selectors, width=800, height=500):
    base_chart = alt.Chart(
        counties_boundaries
    ).mark_geoshape(
        stroke='black',
        strokeWidth=0.1
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(data_url, 'id', ['county', 'state_id'] + list(fields_conf.keys()))
    ).project(
        type='albersUsa'
    )
    
    selectors = set([selectors.get(f).get(SELECTOR) for f in fields_conf.keys()])
    for s in selectors: 
        base_chart = base_chart.add_selection(s)
    
    base_chart = base_chart.transform_calculate(
        matchPct = create_match_pct(fields_conf, fields_to_selectors)
    ).encode(
        color=alt.Color("matchPct:Q", scale=alt.Scale(domain=[0, 1])),
        tooltip=["county:N", "state_id:N"] + [f"{f}:{conf.get(FIELD_TYPE)}" for f, conf in fields_conf.items()],
    ).properties(
        width=width,
        height=height
    )

    return base_chart

# fields: dict from field_name to new init value
def override_inits(chart, fields):
	chart_dict = chart.to_dict() if not isinstance(chart, dict) else chart
	for f, init_val in fields.items():
		if 'selection' in chart_dict:
			inits = chart_dict['selection'] \
				.get(fields_to_selectors[f][SELECTOR].name) \
				.get("init")
			inits.update({fields_to_selectors[f][SELECTOR_FIELD]: init_val})
	del chart_dict["$schema"]
	del chart_dict["config"]
	return alt.Chart.from_dict(chart_dict) if not isinstance(chart, dict) else chart

def get_overrides(reference_county, reference_state, vars_list):
	df = county[(county.county == reference_county) & (county.state_id == reference_state)].iloc[0].to_dict()
	return {f: df[f] for f in vars_list.keys()}

def country_base(data_url, vars_list=None, reference_county=None, reference_state=None):
	conf = get_conf(vars_list)
	do_override = reference_county and reference_state
	county_value_overrides = get_overrides(reference_county, reference_state, conf) if do_override else {}
	base = build_chart(data_url, conf, fields_to_selectors, WIDTH, HEIGHT)
	if do_override:
		base = base.encode(
        color=alt.condition(f'datum.county == "{reference_county}" && datum.state_id == "{reference_state}"',
        					alt.value("Grey"),
        					alt.Color("matchPct:Q", scale=alt.Scale(domain=[0, 1]))))
		base = override_inits(base, county_value_overrides)
	return base

def country_view(data_url, vars_list=None, reference_county=None, reference_state=None):
	base = country_base(data_url, conf, reference_county, reference_state)
	
	return country_view.to_dict()

def state_view(data_url, vars_list=None, reference_county=None, reference_state=None):
	conf = get_conf(vars_list)
	base = country_base(data_url, conf, reference_county, reference_state)

	print(type(base))
	state_specific = alt.layer(
		base.add_selection(state_selector).transform_filter(state_selector), 
	    outline.transform_filter(
        	state_selector
    	)
	)

	bars = [alt.vconcat(), alt.vconcat()]
	n_fields = len(conf)
	for i, field in enumerate(conf.keys()):
	    field_bars = alt.Chart(data_url).mark_bar(tooltip=True).encode(
	        x=f"{field}:{conf.get(field).get(FIELD_TYPE)}",
	        y="county:N",
	        color="county:N"
	    ).add_selection(
	        state_selector
	    ).transform_filter(
	        state_selector
	    ).transform_window(
	        rank='rank(county)',
	        sort=[alt.SortField("matchPct", order="descending"), alt.SortField('county', order='ascending')]
	    ).transform_filter(
	        alt.datum.rank <= 10
	    ).properties(
	        width=WIDTH / 2,
	        height=HEIGHT / 2
    	)
        
	    bars[i%2] &= field_bars


	state_view = (state_specific & (bars[0] | bars[1])).resolve_scale(
	    color='independent'
	)

	return state_view.to_dict()