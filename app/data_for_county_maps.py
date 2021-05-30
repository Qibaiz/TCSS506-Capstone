from app.data_jhu_csse import DataFromJhuCSSE
from app.data_racial_data_tracker import DataFromRacialTracker
import pickle
from os import path
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
from app.api import API


class MapData:
    def __init__(self):
        self.api = API()
        self.cases_and_deaths_data_src = DataFromJhuCSSE()
        self.racial_data_src = DataFromRacialTracker()

        self.geojson = self.api.query_api_geojson()

    def map_cumulative_data_total_cases(self):
        # check if the file is stored in the caching directory
        file_is_out_of_date = False
        if not path.exists('./process_df_csse_county_map') or file_is_out_of_date:
            with open('./process_df_csse_county_map', 'wb') as handle:
                pickle.dump(self.cases_and_deaths_data_src.process_df_csse_county_map(),
                            handle, protocol=pickle.HIGHEST_PROTOCOL)
        # load data from caching file
        with open('./process_df_csse_county_map', 'rb') as handle:
            df = pickle.load(handle)

        # add URL to local favourite county
        # Index(['_id', 'uid', 'country_iso2', 'country_iso3', 'country_code', 'fips',
        #        'county', 'state', 'country', 'combined_name', 'population', 'loc',
        #        'date', 'confirmed', 'deaths', 'confirmed_daily', 'deaths_daily'],
        #       dtype='object')
        df["url"] = 'http://10.0.0.8:5000/county_maps?county=' + df["county"]
        print(df["url"])
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
        df = self.cases_and_deaths_data_src.process_df_csse_county_map()

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

    def map_cumulative_cases_and_deaths(self, option='confirmed'):
        df = self.cases_and_deaths_data_src.process_df_csse_county_map()

        color_scale = 'Blues'
        if option == 'deaths':
            color_scale = 'Reds'

        fig = px.choropleth(
            df,
            geojson=self.geojson,
            featureidkey='properties.FIPS',
            locations='fips',
            color=option,
            color_continuous_scale=color_scale,
            hover_name='county',
            hover_data={
                'fips': False,
                option: ': ,'
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

    def map_daily_cases(self):
        df = self.cases_and_deaths_data_src.process_df_csse_county_map()

        fig = px.choropleth(
            df,
            geojson=self.geojson,
            featureidkey='properties.FIPS',
            locations='fips',
            color='confirmed_daily',
            color_continuous_scale='Sunset',
            custom_data=[],
            hover_name='county',
            hover_data={
                'fips': False,
                'confirmed_daily': ': ,'
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

    def map_daily_deaths(self):
        df = self.cases_and_deaths_data_src.process_df_csse_county_map()

        fig = px.choropleth(
            df,
            geojson=self.geojson,
            featureidkey='properties.FIPS',
            locations='fips',
            color='deaths_daily',
            color_continuous_scale='Emrld',
            hover_name='county',
            hover_data={
                'fips': False,
                'deaths_daily': ': ,'
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

    def map_daily_cases_and_deaths(self, option='confirmed_daily'):
        df = self.cases_and_deaths_data_src.process_df_csse_county_map()
        color_scale = 'Sunset'
        if option == 'deaths_daily':
            color_scale = 'Emrld'

        fig = px.choropleth(
            df,
            geojson=self.geojson,
            featureidkey='properties.FIPS',
            locations='fips',
            color=option,
            color_continuous_scale=color_scale,
            hover_name='county',
            hover_data={
                'fips': False,
                option: ': ,'
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

    def graph_racial_breakdown(self):
        cases_data, deaths_data = self.racial_data_src.get_racial_data_of_cases_and_deaths()

        racials = ['White', 'Hispanic', 'Latino', 'Asian', 'Black', 'American Indian<br>Alaska Native',
                   'Native Hawaiian<br>Pacific Islander']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=racials,
            y=cases_data,
            name='Cases per 100,000 people',
            marker_color='#FFBF00',
            texttemplate="%{y:.0f}",
            textposition='outside',
            hoverinfo='none',
        ))
        fig.add_trace(go.Bar(
            x=racials,
            y=deaths_data,
            name='Deaths per 100,000 people',
            marker_color='#9FE2BF',
            texttemplate="%{y:.2f}",
            textposition='outside',
            hoverinfo='none',

        ))

        # Here we modify the tickangle of the xaxis, resulting in rotated labels. /xaxis_tickangle=-45
        fig.update_layout(barmode='group')
        # fig.show()
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


# a = MapData()
# a.graph_racial_breakdown()
# a.process_geojson_file()
# a.map_cumulative_data_total_deaths()
# a.map_daily_data_and_demo_cases()
# a.map_daily_data_and_demo_deaths()
