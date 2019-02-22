import time

from core_data_modules.cleaners import Codes 
from core_data_modules.traced_data import Metadata
from dateutil.parser import isoparse

class Channels(object):
    #TODO: Setup rapid pro shows to test Ad,promos,shows & date ranges then update the list below.
    NON_LOGICAL_KEY = "non_logical_time"
    INTERNET_KEY = "internet_working"
    WATER_KEY =  "water_filter"
    WASTE_KEY = "waste_disposal"

    # Time ranges expressed in format (start_of_range_inclusive, end_of_range_exclusive)
    INTERNET_RANGES = [("2019-01-01T00:00:00+03:00","2019-04-01T00:00:00+03:00")]
    WATER_RANGES = [("2019-01-01T00:00:00+03:00","2019-04-01T00:00:00+03:00")]
    WASTE_RANGES = [("2019-01-01T00:00:00+03:00","2019-04-01T00:00:00+03:00")]
 
    SHOW_RANGES = {
        INTERNET_KEY:INTERNET_RANGES,
        WATER_KEY:WATER_RANGES,
        WASTE_KEY:WASTE_RANGES
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
            
            # Set time as NON_LOGICAL if it doesn't fall in range of ** radio_show**
            time_range_matches = 0
            if time_range_matches == 0:
                # Assert in range of project
                assert isoparse("2019-01-01T00:00:00+03:00") <= timestamp < isoparse("2019-04-01T00:00:00+03:00"), \
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
