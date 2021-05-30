from os import path
import datetime
import pickle
from app.api import API


class CachedDataSrc:
    def __init__(self):
        self.api = API()

    def is_file_out_of_date(self, file_name):
        current_date = datetime.date.today()
        date_str = current_date.strftime("%d/%m/%Y")
        my_data = {file_name: date_str}

        file_log = file_name + '_log'
        with open(file_log, 'rb') as handle:
            data = pickle.load(handle)

        file_out_of_date = True
        if my_data == data:
            file_out_of_date = False
        return file_out_of_date

    def update_file_log(self, file_name):
        current_date = datetime.date.today()
        date_str = current_date.strftime("%d/%m/%Y")
        data = {file_name: date_str}
        return data

    def get_cached_or_query_api(self, file_name, get_data_fun):
        # check if the file is stored in the caching directory
        file_name = file_name
        file_log = file_name + '_log'
        # print(f'out of date: {self.is_file_out_of_date(file_name)}')
        # print(f'path:{path.exists(file_name)}')
        # print(not path.exists(file_name) or self.is_file_out_of_date(file_name))
        if not path.exists(file_name) or self.is_file_out_of_date(file_name):
            # print("inside query.....")
            with open(file_name, 'wb') as handle:
                pickle.dump(get_data_fun(), handle, protocol=pickle.HIGHEST_PROTOCOL)
        # load data from caching file
        with open(file_name, 'rb') as handle_data:
            # print("come to herer")
            data = pickle.load(handle_data)
            with open(file_log, 'wb') as handle_file_log:
                pickle.dump(self.update_file_log(file_name), handle_file_log, protocol=pickle.HIGHEST_PROTOCOL)
        return data

    def get_cached_or_query_api_jhu_csse(self):
        file_name = './app/cached/api_jhu_csse'
        # if cached:
        #   use_cached
        # else:
        #    query
        return self.get_cached_or_query_api(file_name, self.api.query_api_jhu_csse)

    def get_cached_or_query_api_jhu_cci_testing(self):
        file_name = './app/cached/api_jhu_cci_testing'
        return self.get_cached_or_query_api(file_name, self.api.query_api_jhu_cci_testing)

    def get_cached_or_query_api_jhu_cci_vaccine_admin(self):
        file_name = './app/cached/api_jhu_cci_vaccine_admin'
        return self.get_cached_or_query_api(file_name, self.api.query_api_jhu_cci_vaccine_admin)

    def get_cached_or_query_api_jhu_cci_vaccinated(self):
        file_name = './app/cached/api_jhu_cci_vaccinated'
        return self.get_cached_or_query_api(file_name, self.api.query_api_jhu_cci_vaccinated)

    def get_cached_or_query_api_racial(self):
        file_name = './app/cached/api_racial'
        return self.get_cached_or_query_api(file_name, self.api.query_api_racial)

    def get_cached_or_query_api_hhs(self):
        file_name = './app/cached/api_hhs'
        return self.get_cached_or_query_api(file_name, self.api.query_api_hhs)

    def get_cached_or_query_api_state_population(self):
        file_name = './app/cached/api_population'
        return self.get_cached_or_query_api(file_name, self.api.query_api_state_population)

    def get_cached_or_query_api_geojson(self):
        file_name = './app/cached/api_geojson'
        return self.get_cached_or_query_api(file_name, self.api.query_api_geojson)
