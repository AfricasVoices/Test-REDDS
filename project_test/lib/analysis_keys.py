import time
import pytz

from core_data_modules.cleaners import Codes
from core_data_modules.traced_data import Metadata
from datautil.parser import isoparse

class Analysiskeys(object):

    @staticmethod
    def get_date_time_utc(td):
        return isoparse(td["created_on"]).strftime("%Y-%m-%d %H:%M")
    
    @staticmethod
    def get_date_time_eat(td):
        return isoparse(td["created_on"]).astimezone(pytz.timezone("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def set_yes_no_matrix_keys(user, data, show_keys, coded_shows_prefix, radio_q_prefix):
        for td in data:
            matrix_d = dict()

            yes_no_key = coded_shows_prefix + "_yes_no"
            yes_no = td[yes_no_key]
            matrix_d[radio_q_prefix] = yes_no

            for key in td:
                if key.startswith(coded_shows_prefix) and key != yes_no_key:
                    yes_prefix = radio_q_prefix + "_yes"
                    no_prefix = radio_q_prefix + "_no"

                    code_yes_key = key.replace(coded_shows_prefix, yes_prefix)
                    code_no_key = key.replace(coded_shows_prefix,no_prefix)
                    show_keys.update({code_yes_key,code_no_key})

                    matrix_d[code_yes_key] = td[key] if yes_no == Codes.YES else Codes.MATRIX_0
                    matrix_d[code_no_key] = td[key] if yes_no == Codes.No else Codes.MATRIX_0

            td.append_data(matrix_d, Metadata(user, Metadata.get_call_location(), time.time()))

    @staticmethod
    def set_matrix_keys(user,data, all_matrix_keys, scheme, coded_key, matrix_prefix=""):
        for td in data:
            matrix_d = dict()

            for label in td.get(coded_key, []):
                matrix_d[f"{matrix_prefix}{scheme.get_code_with_id(label['CodeID'].string_value}"] = Codes.MATRIX_1

            for key in all_matrix_keys:
                if key not in matrix_d:
                    matrix_d[key] = Codes.MATRIX_0
            
            td.append_data(matrix_d, Metadata(user, Metadata.get_call_location(), time.time()))
    
    @staticmethod
    def set_analysis_keys(user, data, key_map):
        for td in data:
            td.append_data(
                {new_key: td[old_key] for new_key, old_key in key_map.items()},
                Metadata(user, Metadata.get_call_location(), time.time())
            )
