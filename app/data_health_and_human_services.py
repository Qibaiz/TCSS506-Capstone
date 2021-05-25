from urllib.request import urlopen
import json
import pandas as pd
import datetime


class DataFromHHS:

    def __init__(self):
        self.df_hospitalizations = self.process_hospitalization_df()

    def get_df_hospitalizations(self):
        return self.df_hospitalizations

    def process_hospitalization_df(self):
        # inpatient_beds_used_covid == daily covid-19 hospitalizations

        # inpatient_beds_utilization = inpatient_beds_used / inpatient_beds
        # inpatient_bed_covid_utilization = inpatient_beds_used_covid / inpatient_beds

        # adult_icu_bed_utilization = staffed_adult_icu_bed_occupancy / total_staffed_adult_icu_beds
        # adult_icu_bed_covid_utilization = covid_patient / total_staffed_adult_icu_beds

        with urlopen('https://healthdata.gov/api/views/g62h-syeh/rows.csv') as csv_file:
            df = pd.read_csv(csv_file)
            filt = df['state'] == 'WA'
            df = df.loc[filt]
            df.sort_values(by=['date'], inplace=True)

            df['accumulative_hospitalization'] = df['inpatient_beds_used_covid'].cumsum()
            df['seven_day_covid_hospitalizations'] = df['accumulative_hospitalization'].diff(periods=8)
            df['seven_day_avg_covid_hospitalizations'] = df['seven_day_covid_hospitalizations'].div(7)

            df['last_week_inpatient_beds_utilization'] = df['inpatient_beds_utilization'].cumsum().diff(periods=8).div(
                7)
            df['last_week_inpatient_covid_beds_utilization'] = df['inpatient_bed_covid_utilization'].cumsum().diff(
                periods=8).div(7)

            df['last_week_icu_utilization'] = df['adult_icu_bed_utilization'].cumsum().diff(periods=8).div(7)
            df['last_week_icu_covid_utilization'] = df['adult_icu_bed_covid_utilization'].cumsum().diff(periods=8).div(
                7)

            df['DateTime'] = df['date'].apply(lambda x: pd.to_datetime(x, format='%Y/%m/%d'))
            df.set_index('date', inplace=True)

            df = df[['state', 'DateTime', 'inpatient_beds', 'inpatient_beds_used', 'inpatient_beds_used_covid',
                     'inpatient_beds_utilization', 'inpatient_bed_covid_utilization',
                     'adult_icu_bed_covid_utilization', 'adult_icu_bed_utilization',
                     'seven_day_avg_covid_hospitalizations',
                     'last_week_inpatient_beds_utilization', 'last_week_inpatient_covid_beds_utilization',
                     'last_week_icu_utilization', 'last_week_icu_covid_utilization',
                     'accumulative_hospitalization',
                     ]]
            pd.set_option('display.max_columns', None)
        return df

    def get_hospitalizations_last_week(self):
        today = datetime.date.today()
        target_date = today - datetime.timedelta(days=8)
        formatted_date = target_date.strftime("%Y/%m/%d")
        return formatted_date

    def query_state_overview_hospitalizations_data(self):
        latest_date = self.get_hospitalizations_last_week()
        # print(type(latest_date))
        # print(self.df_hospitalizations.tail(10))
        # print(self.df_hospitalizations.info())
        beds_occupied_last_week = self.df_hospitalizations.loc[latest_date, 'last_week_inpatient_beds_utilization']
        beds_occupied_covid_last_week = self.df_hospitalizations.loc[
            latest_date, 'last_week_inpatient_covid_beds_utilization']
        icu_occupied_last_week = self.df_hospitalizations.loc[latest_date, 'last_week_icu_utilization']
        icu_occupied_covid_last_week = self.df_hospitalizations.loc[latest_date, 'last_week_icu_covid_utilization']

        beds_non_covid = beds_occupied_last_week - beds_occupied_covid_last_week
        beds_covid = beds_occupied_covid_last_week
        beds_unoccupied = 1 - beds_non_covid - beds_covid

        icu_non_covid = icu_occupied_last_week - icu_occupied_covid_last_week
        icu_covid = icu_occupied_covid_last_week
        icu_unoccupied = 1 - icu_non_covid - icu_covid

        beds_data = {
            'beds_non_covid': beds_non_covid,
            'beds_covid': beds_covid,
            'beds_unoccupied': beds_unoccupied,

        }

        icu_data = {
            'icu_non_covid': icu_non_covid,
            'icu_covid': icu_covid,
            'icu_unoccupied': icu_unoccupied
        }

        return beds_data, icu_data


a = DataFromHHS()
# b = a.query_state_overview_hospitalizations_data()
# print(b)