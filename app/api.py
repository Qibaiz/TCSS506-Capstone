import requests
import json
import pandas as pd
from urllib.request import urlopen
import time



API_JHU_CSSE = "https://webhooks.mongodb-stitch.com/api/client/v2.0/app/covid-19-qppza/service/REST-API/incoming_webhook/us_only?"
API_JHU_CCI_TESTING = "https://jhucoronavirus.azureedge.net/api/v1/testing/daily.json"
API_JHU_CCI_VACCINE_ADMIN = "https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/vaccine_data_us_timeline.csv"
API_JHU_CCI_VACCINATED = "https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/people_vaccinated_us_timeline.csv"
API_RACIAL = "https://covidtracking.com/data/download/washington-race-ethnicity-historical.csv"
API_HHS = "https://healthdata.gov/api/views/g62h-syeh/rows.csv"
API_POPULATION = "https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/time_series_covid19_vaccine_doses_admin_US.csv"
API_GEOJSON = "https://raw.githubusercontent.com/loganpowell/census-geojson/master/GeoJSON/20m/2019/county.json"

class API:
    def query_api_jhu_csse(self):
        # import traceback
        # traceback.print_stack()

        print(f'querying csse api... ')
        start = time.time()
        search_api_url = API_JHU_CSSE

        state = 'Washington'
        params = {'state': state,
                  'min_date': '2020-03-11T00:00:00.000Z'}
        # timeout = 5
        response = requests.get(search_api_url, params=params)
        data = response.json()
        df = pd.DataFrame(data)

        time_used = time.time() - start
        print(f'finished querying csse api, used time: {time_used}')
        pd.set_option('display.max_columns', None)

        return df

    def query_api_jhu_cci_testing(self):
        print(f'querying cci testing api...')
        start = time.time()

        with urlopen(API_JHU_CCI_TESTING) as json_file:
            data = json.load(json_file)
            df = pd.DataFrame(data)
            filt = df['state'] == 'WA'
            df = df.loc[filt]

            # df = df[['date', 'state', 'tests_combined_total', 'cases_conf_probable']]
            df['DateTime'] = df['date'].apply(
                lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
            df['tests_combined_daily'] = df['tests_combined_total'].diff(periods=1)
            df['positivity_daily'] = df['cases_conf_probable'].diff(periods=1)
            df['positivity_ratio_daily'] = df['positivity_daily'].div(df['tests_combined_daily'])
            df = df.astype({"date": str})
            df.set_index('date', inplace=True)
            pd.set_option('display.max_columns', None)

            time_used = time.time() - start
            print(f'finished querying cci testing api, used time: {time_used}')

        # print(df.info())

        # print(df.tail(10))
        return df

    def query_api_jhu_cci_vaccine_admin(self):

        print(f'querying cci vaccine admin api...')
        start = time.time()

        with urlopen(API_JHU_CCI_VACCINE_ADMIN) as csv_file:
            df = pd.read_csv(csv_file)
            filt = (df['Province_State'] == 'Washington') & (df['Vaccine_Type'] == 'All')
            df = df.loc[filt]
            df['daily_doses'] = df['Doses_admin'].diff(periods=1)
            df['seven_day_doses'] = df['Doses_admin'].diff(periods=8)
            df['seven_day_avg_daily_doses'] = df['seven_day_doses'].div(7)
            # df['DateTime'] = df['Date'].apply(lambda x: pd.to_datetime(x, format='%Y%m%d'))
            df['DateTime'] = df['Date']
            df.set_index('Date', inplace=True)
            df = df[['DateTime', 'Doses_admin', 'daily_doses', 'seven_day_doses', 'seven_day_avg_daily_doses']]

            time_used = time.time() - start
            print(f'finished querying cci vaccine admin api, used time: {time_used}')

            return df

    def query_api_jhu_cci_vaccinated(self):

        print(f'querying cci vaccinated api...')
        start = time.time()

        with urlopen(API_JHU_CCI_VACCINATED) as csv_file:
            df = pd.read_csv(csv_file)
            filt = (df['Province_State'] == 'Washington')
            df = df.loc[filt]
            df = df[['Province_State', 'Date', 'People_Fully_Vaccinated']]
            df.set_index('Date', inplace=True)

        time_used = time.time() - start
        print(f'finished querying cci vaccinated api, used time: {time_used}')

        return df

    def query_api_racial(self):

        print(f'querying racial api...')
        start = time.time()

        with urlopen(API_RACIAL) as csv_file:
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

            df = df[['State', 'Date', 'Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White', 'Cases_NHPI',
                     'Cases_LatinX', 'Cases_Ethnicity_Hispanic',
                     'Cases_Asian_per_100k', 'Cases_AIAN_per_100k', 'Cases_Black_per_100k', 'Cases_White_per_100k',
                     'Cases_NHPI_per_100k', 'Cases_LatinX_per_100k', 'Cases_Ethnicity_Hispanic_per_100k',
                     'Cases_Total',
                     'Deaths_AIAN', 'Deaths_Asian', 'Deaths_Black', 'Deaths_Ethnicity_Hispanic',
                     'Deaths_LatinX', 'Deaths_NHPI', 'Deaths_White', 'Deaths_Total',
                     'Deaths_Asian_per_100k', 'Deaths_AIAN_per_100k', 'Deaths_Black_per_100k', 'Deaths_White_per_100k',
                     'Deaths_NHPI_per_100k', 'Deaths_LatinX_per_100k', 'Deaths_Ethnicity_Hispanic_per_100k',
                     ]]

            pd.set_option('display.max_columns', None)

            time_used = time.time() - start
            print(f'finished querying racial api, used time: {time_used}')

            return df

    def query_api_hhs(self):
        # inpatient_beds_used_covid == daily covid-19 hospitalizations

        # inpatient_beds_utilization = inpatient_beds_used / inpatient_beds
        # inpatient_bed_covid_utilization = inpatient_beds_used_covid / inpatient_beds

        # adult_icu_bed_utilization = staffed_adult_icu_bed_occupancy / total_staffed_adult_icu_beds
        # adult_icu_bed_covid_utilization = covid_patient / total_staffed_adult_icu_beds

        print(f'querying hhs api...')
        start = time.time()

        with urlopen(API_HHS) as csv_file:
            df = pd.read_csv(csv_file)
            filt = df['state'] == 'WA'
            df = df.loc[filt]
            df.sort_values(by=['date'], inplace=True)

            df['accumulative_hospitalization'] = df['inpatient_beds_used_covid'].cumsum()
            df['seven_day_covid_hospitalizations'] = df['accumulative_hospitalization'].diff(periods=8)
            df['seven_day_avg_covid_hospitalizations'] = df['seven_day_covid_hospitalizations'].div(7)

            df['DateTime'] = df['date'].apply(lambda x: pd.to_datetime(x, format='%Y/%m/%d'))
            df.set_index('date', inplace=True)

            # df = df[['state', 'DateTime', 'inpatient_beds', 'inpatient_beds_used', 'inpatient_beds_used_covid',
            #          'inpatient_beds_utilization', 'inpatient_bed_covid_utilization',
            #          'adult_icu_bed_covid_utilization', 'adult_icu_bed_utilization',
            #          'seven_day_avg_covid_hospitalizations',
            #          'last_week_inpatient_beds_utilization', 'last_week_inpatient_covid_beds_utilization',
            #          'last_week_icu_utilization', 'last_week_icu_covid_utilization',
            #          'accumulative_hospitalization',
            #          ]]

            time_used = time.time() - start
            print(f'finished querying hhs api, used time: {time_used}')

            pd.set_option('display.max_columns', None)
            # print(df.tail(10))
        return df

    def query_api_state_population(self):

        print(f'querying state population api...')
        start = time.time()

        with urlopen(API_POPULATION) as csv_file:
            df = pd.read_csv(csv_file)

        time_used = time.time() - start
        print(f'finished querying state population api, used time: {time_used}')
        return df


    def query_api_geojson(self):

        print(f'querying geojson api...')
        start = time.time()

        with urlopen(API_GEOJSON) as json_file:
            data = json.load(json_file)

        # print(type(data))
        fips = {}

        for value in data['features']:
            id = value['properties']['COUNTYNS']
            if id not in fips:
                fips[id] = ''
            fips[id] = value['properties']['STATEFP'] + value['properties']['COUNTYFP']

        for value in data['features']:
            for key, fip_data in fips.items():
                if key == value['properties']['COUNTYNS']:
                    value['properties'].update({"FIPS": fip_data})

        time_used = time.time() - start
        print(f'finished querying geojson api, used time: {time_used}')

        return data


# a = API()
# a.query_api_hhs()
# a.query_api_jhu_cci_testing()
# a.query_api_jhu_csse()
# a.query_api_jhu_cci_testing()
