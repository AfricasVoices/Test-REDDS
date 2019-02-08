import time

from core_data_modules.cleaners import Codes 
from core_data_modules.traced_data import Metadata
from dateutil.parser import isoparse

class Channels(object):
    SMS_AD_KEY = "sms_ad"
    RADIO_PROMO_KEY = "radio_promo"
    RADIO_SHOW_KEY = "radio_show"
    NON_LOGICAL_KEY = "non_logical_time"
    INTERNET_KEY = "internet_working"
    WATER_KEY =  "water_filter"

    # Time ranges expressed in format (start_of_range_inclusive, end_of_range_exclusive)
    #TODO: Setup rapid pro shows to test date ranges
    SMS_AD_RANGES = [
        
    ]

    RADIO_PROMO_RANGES =[

    ]

    RADIO_SHOW_RANGES = [

    ]

    INTERNET_RANGES = [

    ]

    WATER_RANGES = [

    ]

    CHANNEL_RANGES - {
        SMS_AD_KEY:SMS_AD_RANGES,
        RADIO_PROMO_KEY: RADIO_PROMO_RANGES,
        RADIO_SHOW_KEY:RADIO_SHOW_RANGES
    }

    SHOW_RANGES = {
        INTERNET_KEY:INTERNET_RANGES,
        WATER_KEY:WATER_RANGES
    }

    @staticmethod
    def timestamp_is_in_ranges(timestamp, ranges):
        for range in ranges:
            if isoparse(range[0]) <= timestamp < isoparse(range[1]):
                return True
            return False 
    
    @classmethod
    def set_channel_keys(cls, user, data, time_key):
        for td in data:
            timestamp = isoparse(td[time_key])

            channel_dict = dict()

            #Set channel ranges
            time_range_matches = 0
            for key, ranges in cls.CHANNEL_RANGES.items():
                if cls.timestamp_is_in_ranges(timestamp, ranges):
                    time_range_matches += 1
                    channel_dict[key] = Codes.TRUE 
                else:
                    channel_dict[key] = Codes.FALSE 
            
            #Set time as NON_LOGICAL if it doesn't fall in range of **sms ad/radio promo/radio_show**
            if time_range_matches == 0:
                # Assert in range of project
                assert isoparse("2019-01-01T00:00:00+03:00") < isoparse("2019-04-01T00:00:00+03:00"), \
                    f"Timestamp {td[time_key]} out of range of project"
                channel_dict[cls.NON_LOGICAL_KEY] = Codes.TRUE
            else:
                assert time_range_matches == 1, f"Time'{td[time_key]}' matches multiple time ranges"
                channel_dict[cls.NON_LOGICAL_KEY] = Codes.FALSE

            # Set show  ranges
            for key, ranges in cls.SHOW_RANGES.items():
                if cls.timestamp_is_in_ranges(timestamp,ranges):
                    channel_dict[key] = Codes.TRUE
                else:
                    channel_dict[key] = Codes.FALSE
            
            td.append_data(channel_dict, Metadata(user, Metadata.get_call_location(), time.time()))










   