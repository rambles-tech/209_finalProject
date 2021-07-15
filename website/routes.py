from flask import Flask, render_template, url_for
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
  var_names = vars_list.split('&') if vars_list else None
  vega_spec = alt_vis.country_view(data_url, var_names)
  return render_template('country.html', vega_spec=vega_spec) 


@app.route('/state/')
def state():
  return state_spec(None)

@app.route('/state/spec/<vars_list>')
def state_spec(vars_list):
  data_url = "/~skylerroh/w209/static/data_sources/final_transformed_data.csv"
  var_names = vars_list.split('&') if vars_list else None
  vega_spec = alt_vis.state_view(data_url, var_names)
  return render_template('state.html', vega_spec=vega_spec) 

if __name__ == '__main__':
  app.run(debug=False)
