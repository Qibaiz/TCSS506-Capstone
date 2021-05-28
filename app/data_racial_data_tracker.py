from app.api import API



class DataFromRacialTracker:
    def __init__(self):
        self.api = API()
        self.df_racial_breakdown = self.api.query_api_racial()

    def get_racial_data_of_cases_and_deaths(self):
        cases_NHPI = self.df_racial_breakdown.loc[0, 'Cases_NHPI_per_100k']
        cases_Hispanic = self.df_racial_breakdown.loc[0, 'Cases_Ethnicity_Hispanic_per_100k']
        cases_Latino = self.df_racial_breakdown.loc[0, 'Cases_LatinX_per_100k']
        cases_AIAN = self.df_racial_breakdown.loc[0, 'Cases_AIAN_per_100k']
        cases_Black = self.df_racial_breakdown.loc[0, 'Cases_Black_per_100k']
        cases_Asian = self.df_racial_breakdown.loc[0, 'Cases_Asian_per_100k']
        cases_White = self.df_racial_breakdown.loc[0, 'Cases_White_per_100k']

        deaths_NHPI = self.df_racial_breakdown.loc[0, 'Deaths_NHPI_per_100k']
        deaths_Hispanic = self.df_racial_breakdown.loc[0, 'Deaths_Ethnicity_Hispanic_per_100k']
        deaths_Latino = self.df_racial_breakdown.loc[0, 'Deaths_LatinX_per_100k']
        deaths_AIAN = self.df_racial_breakdown.loc[0, 'Deaths_AIAN_per_100k']
        deaths_Black = self.df_racial_breakdown.loc[0, 'Deaths_Black_per_100k']
        deaths_Asian = self.df_racial_breakdown.loc[0, 'Deaths_Asian_per_100k']
        deathsWhite = self.df_racial_breakdown.loc[0, 'Deaths_White_per_100k']

        cases_data = [cases_White,  cases_Hispanic, cases_Latino, cases_Asian,cases_Black, cases_AIAN, cases_NHPI]
        deaths_data = [deathsWhite, deaths_Hispanic, deaths_Latino, deaths_Asian,deaths_Black,deaths_AIAN, deaths_NHPI]

        # print(type(cases_data))
        return cases_data, deaths_data



# a = DataFromRacialTracker()
# a.get_racial_data_of_cases_and_deaths()
# a.process_racial_data_of_cases_and_deaths_df()