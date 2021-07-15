import altair as alt

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

temp_selector = create_slider("temperature", -30, 60, 0.1, [("low_temp", 10), ("high_temp", 90)])
precip_selector = create_slider("precipitation", 0, 365, 1, [("num_days", 100)])
education_selector = create_slider("education", 0, 100, 1, [("college_or_above", 20)])
income_selector = create_slider("income", 5000, 100000, 5000, [("individual_median", 25000)])
density_selector = create_dropdown("density", density_labels, [("group", "100-1000")])
