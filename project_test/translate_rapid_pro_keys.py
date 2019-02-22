import time
from os import path

from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataCodaV2IO

from dateutil.parser import isoparse

from project_test.lib.test_schemes import CodeSchemes

class TranslateRapidProKeys(object):
    RAPID_PRO_KEY_MAP = [
        # List of (new_key, old_key)
        ("uid", "avf_phone_id"),

        ("internet_working_raw", "Internet_Working (Value) - internet_working_poll" ),
        ("internet_working_run_id", "Internet_Working (Run ID) - internet_working_poll"),
        ("sent_on", "Internet_Working (Time) - internet_working_poll"),

        ("water_filter_raw", "Filter_Working (Value) - water_filter_poll"),
        ("water_filter_run_id", "Filter_Working (Run ID) - water_filter_poll"),
        ("sent_on", "Filter_Working (Time) - water_filter_poll"),

        ("waste_disposal_raw", "Waste_Disposal_Satisfaction (Value) - waste_disposal_satisfaction"),
        ("waste_disposal_run_id", "Waste_Disposal_Satisfaction (Run ID) - waste_disposal_satisfaction"),
        ("sent_on", "Waste_Disposal_Satisfaction (Time) - waste_disposal_satisfaction"),

        ("age_raw", "Age (Value) - demogs"),
        ("age_time", "Age (Time) - demogs"),

        ("gender_raw", "Gender_Test (Value) - demogs"),
        ("gender_time", "Gender_Test (Time) - demogs"),

        ("client_region_raw", "Response_4 (Value) - demogs"),
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
