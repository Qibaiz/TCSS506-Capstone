from app.data_jhu_csse import DataFromJhuCSSE
from urllib.request import urlopen
import plotly
import plotly.express as px
import pandas as pd
import json


class MapData:
    def __init__(self):
        self.data_src = DataFromJhuCSSE()
        self.geojson = {}

        self.process_geojson_file()

    def process_geojson_file(self):
        with urlopen(
                'https://raw.githubusercontent.com/loganpowell/census-geojson/master/GeoJSON/20m/2019/county.json') \
                as json_file:
            data = json.load(json_file)

        # print(type(data))
        fips = {}

        for value in data['features']:
            id = value['properties']['COUNTYNS']
            if id not in fips:
                fips[id] = ''
            fips[id] = value['properties']['STATEFP'] + value['properties']['COUNTYFP']

        for value in data['features']:
            for key, fip_data in fips.items():
                if key == value['properties']['COUNTYNS']:
                    value['properties'].update({"FIPS": fip_data})

        self.geojson = data


    def map_cumulative_data_total_cases(self):
        df = self.data_src.process_county_maps_cases_and_deaths_data()

        fig = px.choropleth(
            df,
            geojson=self.geojson,
            featureidkey='properties.FIPS',
            locations='fips',
            color='confirmed',
            color_continuous_scale='Blues',
            hover_name='county',
            hover_data={
                'fips': False,
                'confirmed': ': ,'
            },

        )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            width=1100,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )
        # fig.show()
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    def map_cumulative_data_total_deaths(self):
        df = self.data_src.process_county_maps_cases_and_deaths_data()

        fig = px.choropleth(
            df,
            geojson=self.geojson,
            featureidkey='properties.FIPS',
            locations='fips',
            color='deaths',
            color_continuous_scale='Reds',
            hover_name='county',
            hover_data={
                'fips': False,
                'deaths': ': ,'
            },

        )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            width=1100,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )
        # fig.show()
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    def map_daily_data_and_demo_cases(self):
        pass

    def map_daily_data_and_demo_deaths(self):
        pass


a = MapData()
# a.process_geojson_file()
a.map_cumulative_data_total_deaths()
