import datetime
from app.cached_data_src import CachedDataSrc

class DataFromHHS:

    def __init__(self):
        # self.api = API()
        self.cached_data_src = CachedDataSrc()
        self.df_hospitalizations = self.cached_data_src.get_cached_or_query_api_hhs()

    def get_df_hospitalizations(self):
        return self.df_hospitalizations

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
        beds_occupied_last_week = self.df_hospitalizations.loc[latest_date, 'inpatient_beds_utilization']
        beds_occupied_covid_last_week = self.df_hospitalizations.loc[
            latest_date, 'inpatient_bed_covid_utilization']
        icu_occupied_last_week = self.df_hospitalizations.loc[latest_date, 'adult_icu_bed_utilization']
        icu_occupied_covid_last_week = self.df_hospitalizations.loc[latest_date, 'adult_icu_bed_covid_utilization']

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


# a = DataFromHHS()
# b = a.query_state_overview_hospitalizations_data()
# print(b)