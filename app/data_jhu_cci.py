import datetime
from app.api import API
from app.cached_data_src import CachedDataSrc


class DataFromJhuCCI:

    def __init__(self):
        # self.api = API()
        self.cached_data_src = CachedDataSrc()
        self.df_testing = self.cached_data_src.get_cached_or_query_api_jhu_cci_testing()
        self.df_vaccine_administered = self.cached_data_src.get_cached_or_query_api_jhu_cci_vaccine_admin()
        self.df_vaccinated = self.cached_data_src.get_cached_or_query_api_jhu_cci_vaccinated()
        self.df_population = self.cached_data_src.get_cached_or_query_api_state_population()

    def get_df_testing(self):
        return self.df_testing

    def get_df_vaccine_administered(self):
        return self.df_vaccine_administered

    def get_df_vaccinated(self):
        return self.df_vaccinated


    def get_state_overview_test_and_positivity(self):
        # all time
        last_date = self.get_state_overview_all_time_date()
        # print(type(last_date))
        # print(last_date)

        all_time_tested = self.df_testing.loc[last_date, 'tests_combined_total']
        all_time_positivity_cases = self.df_testing.loc[last_date, 'cases_conf_probable']
        all_time_testing_positivity = '{:.2%}'.format(all_time_positivity_cases / all_time_tested)

        # past day
        past_date = self.get_state_overview_past_day_date()
        past_day_tested = self.df_testing.loc[past_date, 'tests_combined_daily']

        # past week
        past_week_date = self.get_state_overview_past_week_date()
        past_week_tested = all_time_tested - self.df_testing.loc[past_week_date, 'tests_combined_total']
        past_week_positivity_cases = all_time_positivity_cases - self.df_testing.loc[
            past_week_date, 'cases_conf_probable']
        past_week_testing_positivity = '{:.2%}'.format(past_week_positivity_cases / past_week_tested)

        # past month
        past_month_date = self.get_state_overview_past_month_date()
        past_month_tested = all_time_tested - self.df_testing.loc[past_month_date, 'tests_combined_total']
        past_month_positivity_cases = all_time_positivity_cases - self.df_testing.loc[past_month_date, 'cases_conf_probable']
        past_month_testing_positivity = '{:.2%}'.format(past_month_positivity_cases / past_month_tested)

        data = {
            'all_time_tested': f'{all_time_tested:,.0f}',
            'all_time_testing_positivity': all_time_testing_positivity,
            'past_day_tested': f'{past_day_tested:,.0f}',
            'past_week_tested': f'{past_week_tested :,.0f}',
            'past_week_testing_positivity': past_week_testing_positivity,
            'past_month_tested': f'{past_month_tested :,.0f}',
            'past_month_testing_positivity': past_month_testing_positivity,

        }
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

    def get_state_population(self):
        self.df_population.set_index('Province_State', inplace=True)
        # print(df.index)
        population = self.df_population.loc['Washington', 'Population']
        # print(population)
        return population

    def get_vaccines_administered_past_date(self):
        today = datetime.date.today()
        target_date = today - datetime.timedelta(days=1)
        formatted_date = target_date.strftime("%Y-%m-%d")
        return formatted_date

    def get_state_overview_vaccine_data(self):
        latest_date = self.get_vaccines_administered_past_date()
        # print(f"vaccine date:{type(latest_date)}")
        dose_administered = self.df_vaccine_administered.loc[latest_date, 'Doses_admin']

        fully_vaccinated_cases = self.df_vaccinated.loc[latest_date, 'People_Fully_Vaccinated']
        population = self.get_state_population()
        vaccinated_ratio = '{:.2%}'.format(fully_vaccinated_cases / population)

        data = {
            'dose_administered': f'{dose_administered:,.0f}',
            'fully_vaccinated_cases': f'{fully_vaccinated_cases:,.0f}',
            'vaccinated_ratio': vaccinated_ratio
        }

        return data


# a = DataFromJhuCCI()
# a.get_state_overview_test_and_positivity()
# a.get_state_overview_vaccine_data()