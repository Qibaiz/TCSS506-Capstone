import datetime
import dateutil.parser
import requests
import json
import pandas as pd

# Cases and deaths data source
class DataFromJhuCSSE:
    def __init__(self):
        self.one_day_accu_confirmed = {}  # date : int
        self.one_day_daily_confirmed = {}  # date : int
        self.one_day_accu_deaths = {}  # date : int
        self.one_day_daily_deaths = {}  # date : int
        self.seven_days_avg_daily_confirmed = {}  # date : int
        self.seven_days_avg_daily_deaths = {}  # date : int

        self.process_data_timeline_all_time_data()
        self.process_data_timeline_avg_data()

    def get_one_day_accu_confirmed(self):
        return self.one_day_accu_confirmed

    def get_one_day_daily_confirmed(self):
        return self.one_day_daily_confirmed

    def get_one_day_accu_deaths(self):
        return self.one_day_accu_deaths

    def get_one_day_daily_deaths(self):
        return self.one_day_daily_deaths

    def get_seven_days_avg_daily_confirmed(self):
        return self.seven_days_avg_daily_confirmed

    def get_seven_days_avg_daily_deaths(self):
        return self.seven_days_avg_daily_deaths

    def get_data_timeline_all_time_date(self):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        year = yesterday.year
        month = yesterday.month
        date = yesterday.day
        max_date = datetime.date(year, month, date)
        formatted_min_date = '2020-03-11T00:00:00.000Z'
        formatted_max_date = str(max_date) + 'T00:00:00.000Z'
        return formatted_min_date, formatted_max_date

    def query_data_timeline_all_time_data(self):
        search_api_url = 'https://webhooks.mongodb-stitch.com/api/client/v2.0/app/covid-19-qppza/service/REST-API/incoming_webhook/us_only?'

        state = 'Washington'
        min_date, max_date = self.get_data_timeline_all_time_date()

        params = {'state': state,
                  'min_date': min_date,
                  'max_date': max_date}
        response = requests.get(search_api_url, params=params, timeout=5)
        all_time_data = response.json()
        return all_time_data

    def process_date(self, date_str):
        dt = dateutil.parser.parse(date_str)
        year = dt.year
        month = dt.month
        day = dt.day
        return datetime.datetime(year, month, day)

    def process_data_timeline_all_time_data(self):
        all_time_data = self.query_data_timeline_all_time_data()

        for value in all_time_data:
            date_str = value['date']
            date_obj = self.process_date(date_str)
            if date_obj not in self.one_day_accu_confirmed:
                self.one_day_accu_confirmed[date_obj] = 0
            self.one_day_accu_confirmed[date_obj] += int(value['confirmed'])

            if date_obj not in self.one_day_daily_confirmed:
                self.one_day_daily_confirmed[date_obj] = 0
            self.one_day_daily_confirmed[date_obj] += int(
                value['confirmed_daily'])

            if date_obj not in self.one_day_accu_deaths:
                self.one_day_accu_deaths[date_obj] = 0
            self.one_day_accu_deaths[date_obj] += int(value['deaths'])

            if date_obj not in self.one_day_daily_deaths:
                self.one_day_daily_deaths[date_obj] = 0
            self.one_day_daily_deaths[date_obj] += int(value['deaths_daily'])

    def process_data_timeline_avg_data(self):
        confirmed_date = list(self.one_day_accu_confirmed.keys())
        daily_confirmed = list(self.one_day_accu_confirmed.values())
        sum_previous_7_days_confirmed = []

        average_days = 7
        for i in range(len(daily_confirmed)):
            if (i - average_days) < 0:
                sum_previous_7_days_confirmed.append(daily_confirmed[i])
                continue
            sum_previous_7_days_confirmed.append(
                daily_confirmed[i] - daily_confirmed[i - average_days])

        for i in range(len(confirmed_date)):
            self.seven_days_avg_daily_confirmed[confirmed_date[i]] = int(
                sum_previous_7_days_confirmed[i] / average_days)

        deaths_date = list(self.one_day_accu_deaths.keys())
        daily_deaths = list(self.one_day_accu_deaths.values())
        sum_previous_7_days_deaths = []

        for i in range(len(daily_deaths)):
            if (i - average_days) < 0:
                sum_previous_7_days_deaths.append(daily_deaths[i])
                continue
            sum_previous_7_days_deaths.append(
                daily_deaths[i] - daily_deaths[i - average_days])

        for i in range(len(deaths_date)):
            self.seven_days_avg_daily_deaths[deaths_date[i]] = int(
                sum_previous_7_days_deaths[i] / average_days)

    def process_state_overview_date_period(self, days_difference):
        today = datetime.date.today()
        target_date = today - datetime.timedelta(days=days_difference)
        year = target_date.year
        month = target_date.month
        date = target_date.day
        min_date = datetime.date(year, month, date)
        formatted_min_date = str(min_date) + 'T00:00:00.000Z'
        formatted_max_date = str(min_date) + 'T00:00:00.000Z'
        return formatted_min_date, formatted_max_date

    def get_state_overview_all_time_date(self):
        return self.process_state_overview_date_period(1)

    def get_state_overview_past_day_date(self):
        return self.process_state_overview_date_period(1)

    def get_state_overview_past_week_date(self):
        return self.process_state_overview_date_period(8)

    def get_state_overview_past_month_date(self):
        return self.process_state_overview_date_period(31)

    def query_state_overview_data(self, date_from, date_to):
        search_api_url = 'https://webhooks.mongodb-stitch.com/api/client/v2.0/app/covid-19-qppza/service/REST-API/incoming_webhook/us_only?'

        state = 'Washington'

        params = {'state': state,
                  'min_date': date_from,
                  'max_date': date_to}
        response = requests.get(search_api_url, params=params, timeout=5)
        # print(f"response: {response}")

        data = response.json()
        return data

    def get_country_maps_past_day_date(self):
        return self.get_state_overview_past_day_date()

    def query_county_maps_data(self, date_from, date_to):
        search_api_url = 'https://webhooks.mongodb-stitch.com/api/client/v2.0/app/covid-19-qppza/service/REST-API/incoming_webhook/us_only?'

        state = 'Washington'

        params = {'state': state,
                  'min_date': date_from,
                  'max_date': date_to}
        response = requests.get(search_api_url, params=params, timeout=5)
        # print(f"response: {response}")
        # print(type(response))

        return response

    def process_county_maps_cases_and_deaths_data(self):
        date_from, date_to = self.get_country_maps_past_day_date()
        response = self.query_county_maps_data(date_from, date_to)
        data = response.json()
        pd.set_option('display.max_columns', None)
        df = pd.DataFrame.from_records(data)
        return df


a = DataFromJhuCSSE()
# df = a.process_county_maps_cases_and_deaths_data()
# print(df.info())

#
# df = a.convert_json_to_pd()
# with open('filename.txt', 'w') as f:
#     print(df, file=f)
# print(df.head(10))









