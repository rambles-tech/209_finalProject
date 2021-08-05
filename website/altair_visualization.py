import pandas as pd
import altair as alt
import os
from field_confs import *

from vega_datasets import data

DIST_METHOD = "clipped_l1"  # [l1, l2, binary]

WIDTH = 800
HEIGHT = 500
dataFilePath = os.path.dirname(os.path.abspath(__file__)) + "/static/data_sources/final_transformed_data.csv"

counties_boundaries = alt.topo_feature(data.us_10m.url, 'counties')
state_boundaries = alt.topo_feature(data.us_10m.url, 'states')

outline = alt.Chart(state_boundaries).mark_geoshape(stroke='darkslategrey', fillOpacity=0).project(
    type='albersUsa'
).properties(
    width=WIDTH,
    height=HEIGHT
)

# define state selection
county = pd.read_csv(dataFilePath)

# get the standard deviations
stddevs = county.std().to_dict()

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

def create_similarity(fields_conf, selectors):
    n_fields = len(fields_conf)
    formula = []
    for f, conf in fields_conf.items():
        selector = f"{selectors.get(f).get(SELECTOR).name}.{selectors.get(f).get(SELECTOR_FIELD)}"
        comp = comparators.get(conf.get(COMPARATOR))
        if comp == "==":
            formula.append(f"(1 - (datum.{f} {comp} {selector}))")
        else:
            sd = stddevs.get(f)
            formula.append(f"(abs(datum.{f} - {selector})/{sd})")

    if DIST_METHOD == "clipped_l1":
        added = "(" + " + ".join([f"min({field}, 1)" for field in formula]) + ")"
        return f"(1-({added} / {n_fields}))"

    elif DIST_METHOD == "l1":
        # average l1
        added = "(" + " + ".join(formula) + ")"
        return f"(1-({added} / {n_fields}))"

    elif DIST_METHOD == "l2":
        #l2
        added = "(1-(sqrt(" + " + ".join(["pow(f, 2)" for f in formula]) + ")))"
        return added

def build_chart(data_url, fields_conf, selectors, width=800, height=500):
    base_chart = alt.Chart(
        counties_boundaries
    ).mark_geoshape(
        stroke='black',
        strokeWidth=0.1
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(data_url, 'id', ['county', 'state_id', 'city_largest'] + list(fields_conf.keys()))
    ).project(
        type='albersUsa'
    )
    
    selectors = set([selectors.get(f).get(SELECTOR) for f in fields_conf.keys()])
    for s in selectors: 
        base_chart = base_chart.add_selection(s)
    
    base_chart = base_chart.transform_calculate(
        Similarity=create_match_pct(fields_conf, fields_to_selectors) if DIST_METHOD == "binary" else create_similarity(fields_conf, fields_to_selectors)
    ).encode(
        color=alt.Color("Similarity:Q", scale=alt.Scale(scheme="yellowgreenblue", domain=[0, 1], bins=[0.1*n for n in range(0,11)]),
                        legend=alt.Legend(title='Similarity (Higher is more similar)')),
        tooltip=["county:N", "state_id:N", "city_largest:N"] +
                [alt.Tooltip(f"{f}:{conf.get(FIELD_TYPE)}", title=conf.get(ALIAS)) for f, conf in fields_conf.items()] +
                [alt.Tooltip("Similarity:Q", format=",.2f")],
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
    print(reference_county, reference_state)
    do_override = reference_county and reference_state
    county_value_overrides = get_overrides(reference_county, reference_state, conf) if do_override else {}
    base = build_chart(data_url, conf, fields_to_selectors, WIDTH, HEIGHT)
    if do_override:
        base = base.encode(
            color=alt.condition(f"datum.county == '{reference_county}' && datum.state_id == '{reference_state}'",
                                alt.value("Grey"),
                                alt.Color("Similarity:Q", scale=alt.Scale(scheme="yellowgreenblue", domain=[0, 1], bins=[0.1*n for n in range(0,11)]),
                                          legend=alt.Legend(title='Similarity (Higher is more similar)'))))
        base = override_inits(base, county_value_overrides)
    return base

def bars_base(data_url, fields_conf, state_selector=None):
    bars = alt.Chart(data_url).mark_bar(tooltip=True).encode(
        y=alt.Y("county:N"),
        color="county:N"
    ).transform_calculate(
        Similarity=create_match_pct(fields_conf, fields_to_selectors) if DIST_METHOD == "binary" else create_similarity(fields_conf, fields_to_selectors)
    )
    if state_selector:
        bars = bars.add_selection(
            state_selector
        ).transform_filter(
            "state.filter == datum.state_id"
        )

    return bars.transform_calculate("County", "datum.county + ', ' + datum.state_id"
    ).transform_window(
        rank='rank(Similarity)',
        sort=[alt.SortField("Similarity", order="descending"), alt.SortField('county', order='ascending')]
    ).transform_filter(
        alt.datum.rank <= 10
    ).properties(
        width=WIDTH / 2,
        height=HEIGHT / 3
    )

def country_view(data_url, vars_list=None, reference_county=None, reference_state=None):
    conf = get_conf(vars_list)
    base = alt.layer(country_base(data_url, vars_list, reference_county, reference_state), outline)
    bars = bars_base(data_url, conf) \
        .encode(x=alt.X("Similarity:Q", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(title='Similarity (Higher is more similar)')),
                y=alt.Y("County:N", sort="-x"),
                tooltip=alt.Tooltip('Similarity:Q', format=",.2f")) \
        .properties(title={"text": "Top 10 Most Similar Counties:", "subtitle": "based on above selected criteria"})
    base &= (bars)
    return base.to_dict()

def state_view(data_url, vars_list=None, reference_county=None, reference_state=None):
    state_dropdown = alt.binding_select(options=sorted(county.state_id.dropna().unique().tolist()))
    state_selector = alt.selection_single(name="state", fields=['filter'], bind=state_dropdown, init={"filter": reference_state if reference_state else "CA"})

    conf = get_conf(vars_list)
    base = country_base(data_url, conf, reference_county, reference_state)

    state_specific = alt.layer(
        base.add_selection(state_selector).transform_filter("state.filter == datum.state_id"),
        outline.transform_filter(state_selector)
    )

    bars_base_chart = bars_base(data_url, conf, state_selector)

    bars = [alt.vconcat(
        bars_base_chart.encode(
            x=alt.X("Similarity:Q", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(title='Similarity (Higher is more similar)')),
            y=alt.Y("county:N", sort=alt.SortField("Similarity", order="descending"))
        ).properties(
            title={"text": "Top 10 Most Similar Counties:", "subtitle": "based on above selected criteria"}
        )),
        alt.vconcat()]
    for i, field in enumerate(conf.keys()):
        field_bars = bars_base_chart\
            .encode(x=alt.X(f"{field}:{conf.get(field).get(FIELD_TYPE)}", axis=alt.Axis(title=conf.get(field).get(ALIAS))),
                    y=alt.Y("county:N", sort=alt.SortField("Similarity", order="descending")))
        # selector = fields_to_selectors.get(field).get(SELECTOR)
        #
        # selector_line = alt.Chart()\
        #     .mark_rule()\
        #     .add_selection(selector)\
        #     .encode(y=f"{selector.name}.{selector.get(SELECTOR_FIELD)}")
        bars[(i+1)%2] &= field_bars


    state_view = (state_specific & (bars[0] | bars[1])).resolve_scale(
        color='independent'
    )

    return state_view.to_dict()

def comp_view(data_url, counties_list, vars_list=None):
    conf = get_conf(vars_list)
    # base = country_base(data_url, conf, reference_county, reference_state)

    # state_specific = alt.layer(
    #     base,
    #     outline
    # )
    condition = [f"((datum.county == '{c[0]}') & (datum.state_id == '{c[1]}'))" for c in counties_list]
    bars_base_chart = alt.Chart(data_url
        ).mark_bar(tooltip=True
        ).transform_calculate("County", "datum.county + ', ' + datum.state_id"
        ).encode(
            y="County:N",
            color="County:N"
        ).transform_filter(
            " | ".join(condition)
        ).properties(
            width=WIDTH / 2,
            height=HEIGHT / 3
        )

    bars = [alt.vconcat(), alt.vconcat()]

    for i, field in enumerate(conf.keys()):
        field_bars = bars_base_chart\
            .encode(x=f"{field}:{conf.get(field).get(FIELD_TYPE)}",
                    y=alt.Y("County:N", sort=alt.SortField("County", order="ascending")))
        # selector = fields_to_selectors.get(field).get(SELECTOR)
        #
        # selector_line = alt.Chart()\
        #     .mark_rule()\
        #     .add_selection(selector)\
        #     .encode(y=f"{selector.name}.{selector.get(SELECTOR_FIELD)}")
        bars[i%2] &= field_bars

    return (bars[0] | bars[1]).to_dict()
