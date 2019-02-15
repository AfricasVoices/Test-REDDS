import time
from os import path

from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataCoda2IO
from dateutil.parser import isoparse

from project_test.lib.test_schemes import CodeSchemes

class TranslateRapidProKeys(object):
    RAPID_PRO_KEY_MAP = [
        # List of (new_key, old_key)
        ("uid", "avf_phone_id"),

        ("internet_working_raw", "Response_2 (Value) - internet_working_poll" ),
        ("internet_working_run_id", "Response_2 (Run ID) - internet_working_poll"),
        ("sent_on", "Response_2 (Time) - internet_working_poll"),

        ("water_filter_raw", "Filter_Working (Value) - water_filter_poll"),
        ("water_filter_run_id", "Filter_Working (Run ID) - water_filter_poll"),
        ("sent_on", "Filter_Working (Time) - water_filter_poll"),
        
        ("age_raw", "Age (Value) - demogs"),
        ("age_time", "Age (Time) - demogs"),

        ("gender_raw", "Gender_Test (Value) - demogs"),
        ("gender_time", "Gender_Test (Time) - demogs"),

        ("client_region_raw", "Response_4 (Value) - demogs")
        ("client_region_time", "Response_4 (Time) - demogs")
        
        ]

    @classmethod
    def translate_rapid_pro_keys(cls, user, data, coda_input_dir):
        """
        Uses the cls.RAPID_PRO_KEY_MAP to rename the keys exported by Textit to keys which are easier to work
        with in the pipeline.
        """
        for td in data:
            mapped_dict = dict()

            for new_key,old_key in cls.RAPID_PRO_KEY_MAP:
                if old_key in td:
                    mapped_dict[new_key] = td[old_key]
            
            td.append_data(mapped_dict,Metadata(user, Metadata.get_call_location(), time.time()))
        
        return data
        