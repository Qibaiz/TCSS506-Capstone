import datetime
import dateutil.parser
import requests
import pandas as pd
from app.api import API


# Cases and deaths data source
class DataFromJhuCSSE:
    def __init__(self):
        self.df_csse = API().query_api_jhu_csse()

    def process_df_csse_county_map(self):
        df = self.df_csse

        past_date = self.get_country_maps_past_day_date()
        # print(df.info())
        # print(type(past_date))
        # print(past_date)
        # print(df.tail(10))
        filt = (df['state'] == 'Washington') & (df['date'] == past_date)
        df = df.loc[filt]
        pd.set_option('display.max_columns', None)
        # print(df.tail())
        return df

    def process_df_csse_data_timeline(self):
        df = self.process_df_csse_state_overview()
        # print(df.info())

        return df

    def process_df_csse_state_overview(self):
        df = self.df_csse
        df['DateTime'] = df['date']
        # pd.to_datetime(df['DateTime'])
        df = df[df['state'] == 'Washington'].groupby('date').agg(
            accu_confirmed=pd.NamedAgg(column='confirmed', aggfunc=sum),
            acc_deaths=pd.NamedAgg(column='deaths', aggfunc=sum),
            daily_confirmed=pd.NamedAgg(column='confirmed_daily', aggfunc=sum),
            daily_deaths=pd.NamedAgg(column='deaths_daily', aggfunc=sum),
            datetime=pd.NamedAgg(column='DateTime', aggfunc='first')
        )
        df["seven_avg_daily_cases"] = df['accu_confirmed'].diff(periods=8).div(7)
        df['seven_avg_daily_deaths'] = df['acc_deaths'].diff(periods=8).div(7)

        pd.set_option('display.max_columns', None)

        # print(df.info())
        #
        # print(df.tail(10))
        return df

    def get_state_overview_data_cases_and_deaths(self):
        df = self.process_df_csse_state_overview()
        # all time
        last_date = self.get_state_overview_all_time_date()
        all_time_confirmed = df.loc[last_date, 'accu_confirmed']
        all_time_deaths = df.loc[last_date, 'acc_deaths']

        # past day
        past_date = self.get_state_overview_past_day_date()
        past_day_cases = df.loc[past_date, 'daily_confirmed']
        past_day_deaths = df.loc[past_date, 'daily_deaths']

        # past week
        past_week_date = self.get_state_overview_past_week_date()
        past_week_cases = all_time_confirmed - df.loc[past_week_date, 'accu_confirmed']
        past_week_deaths = all_time_deaths - df.loc[past_week_date, 'acc_deaths']

        # past month
        past_month_date = self.get_state_overview_past_month_date()
        past_month_cases = all_time_confirmed - df.loc[past_month_date, 'accu_confirmed']
        past_month_deaths = all_time_deaths - df.loc[past_month_date, 'acc_deaths']

        data = {
            'all_time_confirmed': f'{all_time_confirmed:,}',
            'all_time_deaths': f'{all_time_deaths:,}',
            'past_day_cases': f'{past_day_cases:,}',
            'past_day_deaths': f'{past_day_deaths:,}',
            'past_week_cases': f'{past_week_cases:,}',
            'past_week_deaths': f'{past_week_deaths:,}',
            'past_month_cases': f'{past_month_cases:,}',
            'past_month_deaths': f'{past_month_deaths:,}'
        }
        return data

    def process_date(self, date_str):
        dt = dateutil.parser.parse(date_str)
        year = dt.year
        month = dt.month
        day = dt.day
        return datetime.datetime(year, month, day)


    def process_state_overview_start_date(self, days_difference):
        today = datetime.date.today()
        target_date = today - datetime.timedelta(days=days_difference)
        # year = target_date.year
        # month = target_date.month
        # date = target_date.day
        # min_date = datetime.date(year, month, date)
        formatted_target_date = str(target_date) + 'T00:00:00.000Z'
        # formatted_max_date = str(min_date) + 'T00:00:00.000Z'
        return formatted_target_date

    def get_state_overview_all_time_date(self):
        return self.process_state_overview_start_date(1)

    def get_state_overview_past_day_date(self):
        return self.process_state_overview_start_date(1)

    def get_state_overview_past_week_date(self):
        return self.process_state_overview_start_date(8)

    def get_state_overview_past_month_date(self):
        return self.process_state_overview_start_date(31)

    def get_country_maps_past_day_date(self):
        return self.get_state_overview_past_day_date()




# a = DataFromJhuCSSE()
# a.process_df_csse_county_map()
# a.process_df_csse_county_map()
# df = a.process_county_maps_cases_and_deaths_data()
# print(df.info())

#
# df = a.convert_json_to_pd()
# with open('filename.txt', 'w') as f:
#     print(df, file=f)
# print(df.head(10))
