from app.data_jhu_csse import DataFromJhuCSSE


class FavoriteData:
    def __init__(self):
        self.case_and_deaths_data_src = DataFromJhuCSSE()

    def get_cases_and_deaths(self):
        df = self.case_and_deaths_data_src.process_df_csse_favorites()
        counties = sorted(df['county'].tolist())
        return counties

    def get_one_county_data(self, county):
        df = self.case_and_deaths_data_src.process_df_csse_favorites()

        # print(df.info())
        # print(df.tail(10))
        total_cases = df.loc[county, 'confirmed']
        total_deaths = df.loc[county, 'deaths']
        past_day_cases = df.loc[county, 'confirmed_daily']
        past_day_deaths = df.loc[county, 'deaths_daily']

        data = {
            'total_cases': total_cases,
            'total_deaths':total_deaths,
            'past_day_cases': past_day_cases,
            'past_day_deaths':past_day_deaths,
        }

        return data

# a = FavoriteData()
# b = a.get_one_county_data('Yakima')
# print(b)