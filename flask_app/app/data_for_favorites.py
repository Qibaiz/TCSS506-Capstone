from app.data_jhu_csse import DataFromJhuCSSE
import json
import plotly
import plotly.graph_objects as go


class FavoriteData:
    def __init__(self):
        self.case_and_deaths_data_src = DataFromJhuCSSE()

    def get_county_name(self):
        df = self.case_and_deaths_data_src.process_df_csse_favorites_list()
        # print(df.columns)
        counties = sorted(df['county'].tolist())
        return counties

    def get_one_county_list_data(self, county):
        df = self.case_and_deaths_data_src.process_df_csse_favorites_list()
        df = df[df["county"] == county]
        # print(df)
        # county  population  confirmed  deaths  confirmed_daily deaths_daily
        data = {
            'population': f'{df.iloc[0, 1]:,.0f}',
            'total_cases': f'{df.iloc[0, 2]:,.0f}',
            'total_deaths': f'{df.iloc[0, 3]:,.0f}',
            'past_day_cases': f'{df.iloc[0, 4]:,.0f}',
            'past_day_deaths': f'{df.iloc[0, 5]:,.0f}',
        }

        return data


    def get_one_county_line_data(self, county):
        df = self.case_and_deaths_data_src.process_df_csse_favorites_line()
        df = df[df['county'] == county]

        # print(df.columns)
        # print(df.tail(10))

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df['date'],
                y=df['deaths'],
                name="Total deaths",
                # Index(['_id', 'uid', 'country_iso2', 'country_iso3', 'country_code', 'fips',
                #        'county', 'state', 'country', 'combined_name', 'population', 'loc',
                #        'date', 'confirmed', 'deaths', 'confirmed_daily', 'deaths_daily'],
                #       dtype='object')
                customdata=df.to_numpy(),
                hovertemplate="%{x}<br>" +
                              "<b>%{y:,.0f} accumulative deaths</b><br>" +
                              "%{customdata[15]:,.0f} daily cases<br>" +
                              "%{customdata[13]:,.0f} accumulative cases<br>"
                              "<extra></extra>",
            ))

        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['confirmed'],
                name="Total Cases",
                mode='lines',
                marker={
                    'size': 9},
                line=dict(
                    color='firebrick',
                    width=3),
                customdata=df.to_numpy(),
                # Index(['_id', 'uid', 'country_iso2', 'country_iso3', 'country_code', 'fips',
                #        'county', 'state', 'country', 'combined_name', 'population', 'loc',
                #        'date', 'confirmed', 'deaths', 'confirmed_daily', 'deaths_daily'],
                #       dtype='object')
                hovertemplate="%{x}<br>" + "<b>%{y:,.0f} accumulative cases</b><br>" +
                              "%{customdata[15]:,.0f} daily cases<br>" +
                              "%{customdata[14]:,.0f} accumulative deaths<br>"
                              "<extra></extra>",
            ))

        fig.update_layout(
            plot_bgcolor="rgb(240,240,240)",
            margin=dict(t=10, l=10, b=10, r=10),
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='Total Cases',
                titlefont_size=16,
                tickfont_size=14,
            ),
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            bargap=0.15,

        )
        fig.update_traces(texttemplate='%{text:.2s}')
        # fig.show()
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# a = FavoriteData()
# a.get_one_county_line_data('King')
# b = a.get_one_county_data('Yakima')
# print(b)