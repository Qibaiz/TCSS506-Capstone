from app.data_jhu_csse import DataFromJhuCSSE
from app.data_jhu_cci import DataFromJhuCCI
from app.data_health_and_human_services import DataFromHHS

import plotly
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class StateData:

    def __init__(self):
        self.case_and_deaths_data_src = DataFromJhuCSSE()
        self.test_and_vaccine_data_src = DataFromJhuCCI()
        self.hospitalization_data_src = DataFromHHS()

    # filter by state, county and date
    def query_all_time_cases_and_deaths(self):
        min_date, max_date = self.case_and_deaths_data_src.get_state_overview_all_time_date()
        all_time_data = self.case_and_deaths_data_src.query_state_overview_data(min_date, max_date)

        all_time_confirmed_cases = 0
        all_time_deaths = 0
        uids = {}
        for value in all_time_data:
            uid = value["uid"]
            if uid in uids:
                continue
            uids[uid] = 1
            all_time_confirmed_cases += int(value['confirmed'])
            all_time_deaths += int(value['deaths'])

        return all_time_confirmed_cases, all_time_deaths

    def query_past_day_cases_and_deaths(self):

        min_date, max_date = self.case_and_deaths_data_src.get_state_overview_past_day_date()
        past_day_data = self.case_and_deaths_data_src.query_state_overview_data(min_date, max_date)
        new_cases = 0
        new_deaths = 0
        uids = {}
        for value in past_day_data:
            uid = value['uid']
            if uid in uids:
                continue
            uids[uid] = 1
            new_cases += int(value['confirmed_daily'])
            new_deaths += int(value['deaths_daily'])
        return new_cases, new_deaths

    def query_past_week_cases_and_deaths(self):
        min_date, max_date = self.case_and_deaths_data_src.get_state_overview_past_week_date()
        past_week_data = self.case_and_deaths_data_src.query_state_overview_data(min_date, max_date)

        new_cases = 0
        new_deaths = 0
        uids = {}
        for value in past_week_data:
            uid = value['uid']
            if uid in uids:
                continue
            uids[uid] = 1
            new_cases += int(value['confirmed'])
            new_deaths += int(value['deaths'])

        all_time_confirmed_cases, all_time_deaths = self.query_all_time_cases_and_deaths()
        past_week_new_cases = all_time_confirmed_cases - new_cases
        past_week_deaths = all_time_deaths - new_deaths

        return past_week_new_cases, past_week_deaths

    def query_past_month_cases_and_deaths(self):

        min_date, max_date = self.case_and_deaths_data_src.get_state_overview_past_month_date()
        past_month_data = self.case_and_deaths_data_src.query_state_overview_data(min_date, max_date)

        new_cases = 0
        new_deaths = 0
        uids = {}
        for value in past_month_data:
            uid = value['uid']
            if uid in uids:
                continue
            uids[uid] = 1
            new_cases += int(value['confirmed'])
            new_deaths += int(value['deaths'])

        all_time_confirmed_cases, all_time_deaths = self.query_all_time_cases_and_deaths()
        past_month_new_cases = all_time_confirmed_cases - new_cases
        past_month_deaths = all_time_deaths - new_deaths

        return past_month_new_cases, past_month_deaths

    def query_all_time_test_and_positivity(self):
        return self.test_and_vaccine_data_src.query_state_overview_all_time_test_and_positivity()

    def query_past_day_test(self):
        return self.test_and_vaccine_data_src.query_state_overview_past_day_test()

    def query_past_week_test_and_positivity(self):
        return self.test_and_vaccine_data_src.query_state_overview_past_week_test_and_positivity()

    def query_past_month_test_and_positivity(self):
        return self.test_and_vaccine_data_src.query_state_overview_past_month_test_and_positivity()

    def query_vaccine_data(self):
        return self.test_and_vaccine_data_src.query_state_overview_vaccine_data()

    def draw_hospitalizations(self):
        beds_data, icu_data = self.hospitalization_data_src.query_state_overview_hospitalizations_data()

        labels = ['Non COVID-19', 'COVID-19', 'Unoccupied']
        beds_values = list(beds_data.values())
        icu_values = list(icu_data.values())

        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

        fig.add_trace(go.Pie(labels=labels, values=beds_values, name="Beds(ICU incl.)"),
                      1, 1)

        fig.add_trace(go.Pie(labels=labels, values=icu_values, name="ICU"),
                      1, 2)

        fig.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig.update_layout(
            margin=dict(t=50, l=10, b=10, r=10),
            title=dict(
                text="Beds Occupied Last Week",
                font_size=16,
                x=0.5,
                pad=dict(t=10, l=10, b=60, r=10)
            ),
            # Add annotations in the center of the donut pies.
            annotations=[dict(text='Beds<br>(ICU incl.)', x=0.15, y=0.5, font_size=14, showarrow=False),
                         dict(text='ICU', x=0.8, y=0.5, font_size=14, showarrow=False)]
        )


        # fig.show()
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# a = StateData()
# a.draw_hospitalizations()
