from flask import Flask, render_template, url_for, request
import json
import os
import altair_visualization as alt_vis
 
app = Flask(__name__)      

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/country/')
def country():
  return country_spec(None)

@app.route('/country/spec/<vars_list>')
def country_spec(vars_list):
  data_url = "/~skylerroh/w209/static/data_sources/final_transformed_data.csv"
  var_names = vars_list.split(';') if vars_list else None
  kwargs = {s: request.args.get(s) for s in ["reference_county", "reference_state"]}
  county = kwargs["reference_county"]
  state = kwargs["reference_state"]
  vega_spec = alt_vis.country_view(data_url, var_names, **kwargs)
  return render_template('country.html', vega_spec=vega_spec, Kwargs=kwargs, vars_list=vars_list,
                         reference_for_title = f"{county}, {state}" if county and state else "None; no reference county selected, initilizing with default values")

@app.route('/state/')
def state():
  return state_spec(None)

@app.route('/state/spec/<vars_list>')
def state_spec(vars_list):
  data_url = "/~skylerroh/w209/static/data_sources/final_transformed_data.csv"
  var_names = vars_list.split(';') if vars_list else None
  kwargs = {s: request.args.get(s) for s in ["reference_county", "reference_state"]}
  county = kwargs["reference_county"]
  state = kwargs["reference_state"]
  vega_spec = alt_vis.state_view(data_url, var_names, **kwargs)
  return render_template('state.html', vega_spec=vega_spec,
                         reference_for_title = f"{county}, {state}" if county and state else "None; no reference county selected, initilizing with default values")

@app.route('/compare/')
def compare():
  return render_template('compare.html', vega_spec=None)

@app.route('/compare/spec/<vars_list>')
def compare_spec(vars_list):
  data_url = "/~skylerroh/w209/static/data_sources/final_transformed_data.csv"
  var_names = vars_list.split(';') if vars_list else None
  counties_list = request.args.get("counties_list")
  if counties_list:
    vega_spec = alt_vis.comp_view(data_url,
                                  counties_list=[c.split(",") for c in counties_list.split("|")],
                                  vars_list=var_names)
  else:
    vega_spec = None
  return render_template('compare.html', vega_spec=vega_spec)

if __name__ == '__main__':
  app.run(debug=False)
