from urllib.request import urlopen
import pandas as pd



class DataFromRacialTracker:
    def __init__(self):
        self.df_racial_breakdown = self.process_racial_data_of_cases_and_deaths_df()


    def process_racial_data_of_cases_and_deaths_df(self):
        with urlopen(
                'https://covidtracking.com/data/download/washington-race-ethnicity-historical.csv') as csv_file:
            df = pd.read_csv(csv_file)


            df['Cases_Asian_per_100k'] = df['Cases_Asian'].div(df['Cases_Total']) * 100000
            df['Cases_AIAN_per_100k'] = df['Cases_AIAN'].div(df['Cases_Total']) * 100000
            df['Cases_Black_per_100k'] = df['Cases_Black'].div(df['Cases_Total']) * 100000
            df['Cases_White_per_100k'] = df['Cases_White'].div(df['Cases_Total']) * 100000
            df['Cases_NHPI_per_100k'] = df['Cases_NHPI'].div(df['Cases_Total']) * 100000
            df['Cases_LatinX_per_100k'] = df['Cases_LatinX'].div(df['Cases_Total']) * 100000
            df['Cases_Ethnicity_Hispanic_per_100k'] = df['Cases_Ethnicity_Hispanic'].div(df['Cases_Total']) * 100000

            df['Deaths_Asian_per_100k'] = df['Deaths_Asian'].div(df['Deaths_Total']) * 100000
            df['Deaths_AIAN_per_100k'] = df['Deaths_AIAN'].div(df['Deaths_Total']) * 100000
            df['Deaths_Black_per_100k'] = df['Deaths_Black'].div(df['Deaths_Total']) * 100000
            df['Deaths_White_per_100k'] = df['Deaths_White'].div(df['Deaths_Total']) * 100000
            df['Deaths_NHPI_per_100k'] = df['Deaths_NHPI'].div(df['Deaths_Total']) * 100000
            df['Deaths_LatinX_per_100k'] = df['Deaths_LatinX'].div(df['Deaths_Total']) * 100000
            df['Deaths_Ethnicity_Hispanic_per_100k'] = df['Deaths_Ethnicity_Hispanic'].div(df['Deaths_Total']) * 100000

            df = df[['State','Date', 'Cases_Asian','Cases_AIAN', 'Cases_Black','Cases_White', 'Cases_NHPI',
                    'Cases_LatinX','Cases_Ethnicity_Hispanic',
                     'Cases_Asian_per_100k', 'Cases_AIAN_per_100k','Cases_Black_per_100k','Cases_White_per_100k',
                     'Cases_NHPI_per_100k','Cases_LatinX_per_100k','Cases_Ethnicity_Hispanic_per_100k',
                     'Cases_Total',
                     'Deaths_AIAN', 'Deaths_Asian', 'Deaths_Black','Deaths_Ethnicity_Hispanic',
                     'Deaths_LatinX','Deaths_NHPI','Deaths_White','Deaths_Total',
                     'Deaths_Asian_per_100k','Deaths_AIAN_per_100k','Deaths_Black_per_100k','Deaths_White_per_100k',
                     'Deaths_NHPI_per_100k','Deaths_LatinX_per_100k','Deaths_Ethnicity_Hispanic_per_100k',
                     ]]

            pd.set_option('display.max_columns', None)

            # print(df.head(10))
            return df

            # print(df.info())

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



a = DataFromRacialTracker()
a.get_racial_data_of_cases_and_deaths()
# a.process_racial_data_of_cases_and_deaths_df()