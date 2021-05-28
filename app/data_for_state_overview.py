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

    def get_cases_and_deaths(self):
        return self.case_and_deaths_data_src.get_state_overview_data_cases_and_deaths()

    def get_test_and_positivity(self):
        return self.test_and_vaccine_data_src.get_state_overview_test_and_positivity()

    def query_vaccine_data(self):
        return self.test_and_vaccine_data_src.get_state_overview_vaccine_data()

    def draw_hospitalizations(self):
        beds_data, icu_data = self.hospitalization_data_src.query_state_overview_hospitalizations_data()

        labels = ['Non COVID-19', 'COVID-19', 'Unoccupied']
        beds_values = list(beds_data.values())
        icu_values = list(icu_data.values())
        colors = ['#9FE2BF', '#EE82EE', '#87CEEB']

        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

        fig.add_trace(go.Pie(labels=labels, values=beds_values, name="Beds(ICU incl.)"),
                      1, 1)

        fig.add_trace(go.Pie(labels=labels, values=icu_values, name="ICU"),
                      1, 2)

        fig.update_traces(hole=.4, hoverinfo="label+percent+name", marker=dict(colors=colors))
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
