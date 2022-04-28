from flask import Flask, render_template
import pandas as pd
import geopandas as gpd
import requests
import json
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def home_page():

   return render_template('index.html')

@app.route('/circuits')
def circuits():
   response = requests.get("http://ergast.com/api/f1/circuits.json?limit=100").json()

   # get down to correct level of dictionary
   response_clean = response["MRData"]["CircuitTable"]["Circuits"]

   # convert to dataframe
   df = pd.json_normalize(response_clean)

   # convert dataframe into geo dataframe
   geo_df = gpd.GeoDataFrame(
      df, geometry=gpd.points_from_xy(df['Location.long'], df['Location.lat']))

   fig = px.scatter_geo(geo_df,
                        lat=geo_df.geometry.y,
                        lon=geo_df.geometry.x,
                        hover_name="circuitName")

   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

   return render_template('circuits.html', graphJSON=graphJSON)
