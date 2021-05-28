import pandas as pd
import json
import plotly
import plotly.graph_objects as go
from app.data_jhu_csse import DataFromJhuCSSE
from app.data_jhu_cci import DataFromJhuCCI
from app.data_health_and_human_services import DataFromHHS


class GraphData:
    def __init__(self):
        self.case_and_deaths_data_src = DataFromJhuCSSE()
        self.test_and_vaccine_data_src = DataFromJhuCCI()
        self.hospitalizations_data_src = DataFromHHS()

    def graph_cases(self):
        df = self.case_and_deaths_data_src.process_df_csse_data_timeline()

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df['datetime'],
                y=df['daily_confirmed'],
                name="Number of Daily Cases",
                customdata=[
                    df['accu_confirmed'].values,
                    df['seven_avg_daily_cases'].values],
                hovertemplate="%{x}<br>" +
                              "<b>%{y:,.0f} cases</b><br>" +
                              "%{customdata[0]:.0f} cumulative cases<br>" +
                              "%{customdata[1]:.0f}-7 Day average<br>"
                              "<extra></extra>",
            ))

        fig.add_trace(
            go.Scatter(
                x=df['datetime'],
                y=df['seven_avg_daily_cases'],
                name="7-Day Average of Daily Cases",
                mode='lines+markers',
                marker={
                    'size': 9},
                line=dict(
                    color='firebrick',
                    width=3),
                customdata=[
                    df['daily_confirmed'],
                    df['accu_confirmed']],
                hovertemplate="%{x}<br>" + "<b>%{customdata[0]:.0f} cases</b><br>" +
                              "%{customdata[1]:.0f} cumulative cases<br>" +
                              "%{y:.0f}-7 Day average<br>"
                              "<extra></extra>",
            ))

        fig.update_layout(
            plot_bgcolor="rgb(240,240,240)",
            margin=dict(t=50, l=10, b=10, r=10),
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='Number of Daily Cases',
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

    def graph_deaths(self):
        df = self.case_and_deaths_data_src.process_df_csse_data_timeline()

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df['datetime'],
                y=df['daily_deaths'],
                name="Number of Daily Deaths",
                customdata=[
                    df['acc_deaths'].values,
                    df['seven_avg_daily_deaths'].values],
                hovertemplate="%{x}<br>" +
                              "<b>%{y:,.0f} deaths</b><br>" +
                              "%{customdata[0]:.0f} cumulative deaths<br>" +
                              "%{customdata[1]:.0f}-7 Day average<br>" +
                              "<extra></extra>",
            ))

        fig.add_trace(
            go.Scatter(
                x=df['datetime'],
                y=df['seven_avg_daily_deaths'],
                name="7-Day Average of Daily Deaths",
                mode='lines+markers',
                marker={
                    'size': 9},
                line=dict(
                    color='firebrick',
                    width=3),
                customdata=[
                    df['daily_deaths'].values,
                    df['acc_deaths'].values],
                hovertemplate="%{x}<br>" + "<b>%{customdata[0]:.0f} deaths</b><br>" +
                              "%{customdata[1]:.0f} cumulative deaths<br>" +
                              "%{y:.0f}-7 Day average<br>" +
                              "<extra></extra>",
            ))

        fig.update_layout(
            plot_bgcolor="rgb(240,240,240)",
            autosize=False,
            width=1200,
            margin=dict(t=50, l=10, b=10, r=10),
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='Number of Daily Deaths',
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

    def graph_test_positivity(self):
        df = self.test_and_vaccine_data_src.get_df_testing()
        # print(df.head(10))
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df['DateTime'],
                y=df['tests_combined_daily'],
                name="Number of Daily Tests",
                customdata=[df['positivity_daily']],
                hovertemplate="%{x}<br>" + "<b>%{y:,.0f} tests</b><br>" +
                              "%{customdata[0]:.0%} positive" +
                              "<extra></extra>",
            ))

        fig.add_trace(
            go.Scatter(
                x=df['DateTime'],
                y=df['positivity_daily'],
                name="Positivity",
                mode='lines',
                marker={
                    'size': 9},
                line=dict(
                    color='firebrick',
                    width=3),
                # customdata=[df['tests_combined_daily']],
                # hovertemplate="<b>%{customa[0]} tests</b><br>" +
                #               "%{y:.0f}-7 Day average<br>" +
                #               "<extra></extra>",
            ))

        fig.update_layout(
            plot_bgcolor="rgb(240,240,240)",
            autosize=False,
            width=1200,
            margin=dict(t=50, l=10, b=10, r=10),
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='DailyTests+Positivity',
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

    def graph_hospitalizations(self):
        df = self.hospitalizations_data_src.get_df_hospitalizations()
        # print(df.head(10))
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df['DateTime'],
                y=df['inpatient_beds_used_covid'],
                name="Daily COVID-19 Hospitalizations",
                customdata=[df['accumulative_hospitalization'], df['seven_day_avg_covid_hospitalizations']],
                hovertemplate="%{x}<br>" + "<b>%{y:,.0f} hospitalizations</b><br>" +
                              "%{customdata[0]:,.0f} cumulative hospitalizations<br>" +
                              "%{customdata[1]:,.0f} 7-Day Average" +
                              "<extra></extra>",
            ))

        fig.add_trace(
            go.Scatter(
                x=df['DateTime'],
                y=df['seven_day_avg_covid_hospitalizations'],
                name="7-Day Average of Daily COVID-19 Hospitalizations",
                mode='lines',
                marker={
                    'size': 9},
                line=dict(
                    color='firebrick',
                    width=3),
                # customdata=[df['tests_combined_daily']],
                # hovertemplate="<b>%{customa[0]} tests</b><br>" +
                #               "%{y:.0f}-7 Day average<br>" +
                #               "<extra></extra>",
            ))

        fig.update_layout(
            plot_bgcolor="rgb(240,240,240)",
            autosize=False,
            width=1200,
            margin=dict(t=50, l=10, b=10, r=10),
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='Daily COVID-19 Hospitalizations',
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

    def graph_vaccinations(self):
        df = self.test_and_vaccine_data_src.get_df_vaccine_administered()
        # print(df.head(10))
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df['DateTime'],
                y=df['daily_doses'],
                name="Number of Daily Doses",
                customdata=[df['Doses_admin'], df['seven_day_avg_daily_doses']],
                hovertemplate="%{x}<br>" + "<b>%{y:,.0f} doses</b><br>" +
                              "%{customdata[0]:,.0f} cumulative doses<br>" +
                              "%{customdata[1]:,.0f} 7-Day Average" +
                              "<extra></extra>",
            ))

        fig.add_trace(
            go.Scatter(
                x=df['DateTime'],
                y=df['seven_day_avg_daily_doses'],
                name="7-Day Average of Daily Doses",
                mode='lines',
                marker={
                    'size': 9},
                line=dict(
                    color='firebrick',
                    width=3),
                # customdata=[df['tests_combined_daily']],
                # hovertemplate="<b>%{customa[0]} tests</b><br>" +
                #               "%{y:.0f}-7 Day average<br>" +
                #               "<extra></extra>",
            ))

        fig.update_layout(
            plot_bgcolor="rgb(240,240,240)",
            autosize=False,
            width=1200,
            margin=dict(t=50, l=10, b=10, r=10),
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='Number of Daily Doses',
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


# a = GraphData()
# a.graph_test_positivity()
# a.graph_vaccinations()