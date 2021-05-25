from urllib.request import urlopen
import json
import pandas as pd
import datetime


class DataFromJhuCCI:

    def __init__(self):
        self.data = self.process_testing_json_file()  # only Washington data
        self.df_testing = self.process_testing_df()
        self.df_vaccine_administered = self.process_vaccine_administered_df()
        self.df_vaccinated = self.process_vaccinated_df()

    def get_df_testing(self):
        return self.df_testing

    def get_df_vaccine_administered(self):
        return self.df_vaccine_administered

    def get_df_vaccinated(self):
        return self.df_vaccinated

    def get_vaccines_administered_past_date(self):
        today = datetime.date.today()
        target_date = today - datetime.timedelta(days=1)
        formatted_date = target_date.strftime("%Y-%m-%d")
        return formatted_date

    def process_vaccine_administered_df(self):
        with urlopen(
                'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/vaccine_data_us_timeline.csv') as csv_file:
            df = pd.read_csv(csv_file)
            filt = (df['Province_State'] == 'Washington') & (df['Vaccine_Type'] == 'All')
            df = df.loc[filt]
            df['daily_doses'] = df['Doses_admin'].diff(periods=1)
            df['seven_day_doses'] = df['Doses_admin'].diff(periods=8)
            df['seven_day_avg_daily_doses'] = df['seven_day_doses'].div(7)
            # df['DateTime'] = df['Date'].apply(lambda x: pd.to_datetime(x, format='%Y%m%d'))
            df['DateTime'] = df['Date']
            df.set_index('Date', inplace=True)
            df = df[['DateTime','Doses_admin', 'daily_doses', 'seven_day_doses', 'seven_day_avg_daily_doses']]

        return df

    def process_vaccinated_df(self):
        with urlopen(
                'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/people_vaccinated_us_timeline.csv') as csv_file:
            df = pd.read_csv(csv_file)
            filt = (df['Province_State'] == 'Washington')
            df = df.loc[filt]
            df = df[['Province_State', 'Date', 'People_Fully_Vaccinated']]
            df.set_index('Date', inplace=True)
        return df

    def process_testing_df(self):
        df = pd.DataFrame(self.data)
        df = df.loc[df['state'] == 'WA']
        df = df[['date', 'state', 'tests_combined_total', 'cases_conf_probable']]
        df['DateTime'] = df['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
        df['tests_combined_daily'] = df['tests_combined_total'].diff(periods=1)
        df['positivity_daily'] = df['cases_conf_probable'].diff(periods=1)
        df['positivity_ratio_daily'] = df['positivity_daily'].div(df['tests_combined_daily'])
        return df

    def process_testing_json_file(self):
        with urlopen(
                'https://jhucoronavirus.azureedge.net/api/v1/testing/daily.json'
        ) as json_file:
            data = json.load(json_file)
        return data

    def process_state_overview_date_period(self, days_difference):
        today = datetime.date.today()
        target_date = today - datetime.timedelta(days=days_difference)
        formatted_date = target_date.strftime("%Y%m%d")
        return formatted_date

    def get_state_overview_all_time_date(self):
        return self.process_state_overview_date_period(1)

    def get_state_overview_past_day_date(self):
        return self.process_state_overview_date_period(1)

    def get_state_overview_past_week_date(self):
        return self.process_state_overview_date_period(8)

    def get_state_overview_past_month_date(self):
        return self.process_state_overview_date_period(31)

    def query_state_overview_all_time_test_and_positivity(self):
        date = self.get_state_overview_all_time_date()
        test_cases = 0
        testing_positivity = 0
        for value in self.data:
            if value['date'] == int(date) and value['state'] == 'WA':
                test_cases = value['tests_combined_total']
                positivity_cases = value['cases_conf_probable']
                testing_positivity = '{:.2%}'.format(positivity_cases / test_cases)  # str
        data = {
            'test': test_cases,  # int
            'positivity': testing_positivity  # str
        }

        return data

    def query_state_overview_past_day_test(self):
        past_date = self.get_state_overview_past_day_date()
        the_day_before_past_day = self.process_state_overview_date_period(2)
        test_cases_from = 0
        test_cases_end = 0
        for value in self.data:
            if value['date'] == int(the_day_before_past_day) and value['state'] == 'WA':
                test_cases_from = value['tests_combined_total']

            if value['date'] == int(past_date) and value['state'] == 'WA':
                test_cases_end = value['tests_combined_total']
        test_result = test_cases_end - test_cases_from

        return test_result

    def query_state_overview_past_week_test_and_positivity(self):
        date_end = self.get_state_overview_past_day_date()
        date_from = self.get_state_overview_past_week_date()
        test_cases_from = 0
        test_cases_end = 0
        positivity_cases_from = 0
        positivity_cases_end = 0

        for value in self.data:
            if value['date'] == int(date_from) and value['state'] == 'WA':
                test_cases_from = value['tests_combined_total']
                positivity_cases_from = value['cases_conf_probable']

            if value['date'] == int(date_end) and value['state'] == 'WA':
                test_cases_end = value['tests_combined_total']
                positivity_cases_end = value['cases_conf_probable']

        test_result = test_cases_end - test_cases_from
        positivity_cases_result = positivity_cases_end - positivity_cases_from
        positivity_ratio = '{:.2%}'.format(positivity_cases_result / test_result)

        data = {
            'test': test_result,
            'positivity': positivity_ratio
        }
        return data

    def query_state_overview_past_month_test_and_positivity(self):
        date_end = self.get_state_overview_past_day_date()
        date_from = self.get_state_overview_past_month_date()
        test_cases_from = 0
        test_cases_end = 0
        positivity_cases_from = 0
        positivity_cases_end = 0

        for value in self.data:
            if value['date'] == int(date_from) and value['state'] == 'WA':
                test_cases_from = value['tests_combined_total']
                positivity_cases_from = value['cases_conf_probable']

            if value['date'] == int(date_end) and value['state'] == 'WA':
                test_cases_end = value['tests_combined_total']
                positivity_cases_end = value['cases_conf_probable']

        test_result = test_cases_end - test_cases_from
        positivity_cases_result = positivity_cases_end - positivity_cases_from
        positivity_ratio = '{:.2%}'.format(positivity_cases_result / test_result)

        data = {
            'test': test_result,
            'positivity': positivity_ratio
        }
        return data

    def get_state_population(self):

        with urlopen(
                'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/time_series_covid19_vaccine_doses_admin_US.csv') as csv_file:
            df = pd.read_csv(csv_file)
            df.set_index('Province_State', inplace=True)
            # print(df.index)
            population = df.loc['Washington', 'Population']
            # print(population)
            return population

    def query_state_overview_vaccine_data(self):
        latest_date = self.get_vaccines_administered_past_date()
        dose_administered = self.df_vaccine_administered.loc[latest_date, 'Doses_admin']

        fully_vaccinated_cases = self.df_vaccinated.loc[latest_date, 'People_Fully_Vaccinated']
        population = self.get_state_population()
        vaccinated_ratio = '{:.2%}'.format(fully_vaccinated_cases / population)

        data = {
            'dose_administered': dose_administered,
            'fully_vaccinated_cases': fully_vaccinated_cases,
            'vaccinated_ratio': vaccinated_ratio
        }

        return data


a = DataFromJhuCCI()

