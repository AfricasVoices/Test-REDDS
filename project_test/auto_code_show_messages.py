import random
import time
from os import path

from core_data_modules.cleaners import swahili, Codes 
from core_data_modules.cleaners.cleaning_utils import CleaningUtils 
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataCSVIO, TracedDataCodaV2IO
from core_data_modules.util import IOUtils
from dateutil.parser import isoparse

from project_test.lib import ICRTools, Channels
from project_test.lib import MessageFilters
from project_test.lib.pipeline_configurations import PipelineConfiguration

class AutoCodeShowMessages(object):
    TEST_KEYS = []
    for plan in PipelineConfiguration.TEST_SHOWS_CODING_PLANS:
        TEST_KEYS.append(plan.raw_field)

    SENT_ON_KEY = "sent_on"
    NOISE_KEY = "noise"
    PROJECT_START_DATE = isoparse("2019-01-01T00:00:00+03:00")
    PROJECT_END_DATE = isoparse("2019-04-01T00:00:00+03:00")
    ICR_MESSAGES_COUNT = 1 # Since we have few test messages
    ICR_SEED = 0

    @classmethod
    def auto_code_show_messages(cls, user, data, icr_output_dir, coda_output_dir):
        # Filter out test messages sent by AVF.
        if not PipelineConfiguration.DEV_MODE:
            data = MessageFilters.filter_test_messages(data)

        # Filter for runs which don't contain a response to any week's question 
        data = MessageFilters.filter_empty_messages(data, cls.TEST_KEYS)

        # Filter out runs sent outside the project start and end dates
        data = MessageFilters.filter_time_range(data, cls.SENT_ON_KEY, cls.PROJECT_START_DATE, cls.PROJECT_END_DATE)
        
        # Label missing data
        for td in data:
            missing_dict = dict()
            for plan in PipelineConfiguration.TEST_SHOWS_CODING_PLANS:
                if plan.raw_field not in td:
                    na_label = CleaningUtils.make_label_from_cleaner_code(
                        plan.code_scheme, plan.code_scheme.get_code_with_control_code(Codes.TRUE_MISSING),
                        Metadata.get_call_location()
                    )
                    missing_dict[plan.coded_field] = [na_label.to_dict()]

                if plan.binary_code_scheme is not None:
                    na_label = CleaningUtils.make_label_from_cleaner_code(
                        plan.binary_code_scheme, plan.binary_code_scheme.get_code_with_control_code(Codes.TRUE_MISSING),
                        Metadata.get_call_location()
                    )
                    missing_dict[plan.binary_coded_field] = na_label.to_dict()
            
            td.append_data(missing_dict, Metadata(user, Metadata.get_call_location(), time.time()))
    
        # Label each message with channel keys
        Channels.set_channel_keys(user, data, cls.SENT_ON_KEY)

        # Output messagges for Coda
        IOUtils.ensure_dirs_exist(coda_output_dir)
        for plan in PipelineConfiguration.TEST_SHOWS_CODING_PLANS:
            TracedDataCodaV2IO.compute_message_ids(user, data, plan.raw_field, plan.id_field)

            output_path = path.join(coda_output_dir, plan.coda_filename)
            with open(output_path, "w") as f:
                TracedDataCodaV2IO.export_traced_data_iterable_to_coda_2(
                    data, plan.raw_field, cls.SENT_ON_KEY, plan.id_field, {}, f
                )
        print("Coda message files successfully exported")

        # Output messages for ICR
        IOUtils.ensure_dirs_exist(icr_output_dir)
        for plan in PipelineConfiguration.TEST_SHOWS_CODING_PLANS:
            test_pipeline_messages = []
            na_messages = []
            for td in data:
                if plan.coded_field not in td:
                    test_pipeline_messages.append(td)
                    
                else:
                    assert len(td[plan.coded_field]) == 1
                    assert td[plan.coded_field][0]["CodeID"] == \
                            plan.code_scheme.get_code_with_control_code(Codes.TRUE_MISSING).code_id

            
            icr_messages = ICRTools.generate_sample_for_icr(
                test_pipeline_messages, cls.ICR_MESSAGES_COUNT, random.Random(cls.ICR_SEED))
            
            icr_output_path = path.join(icr_output_dir, plan.icr_filename)
            with open(icr_output_path, "w") as f:
                TracedDataCSVIO.export_traced_data_iterable_to_csv(
                    icr_messages, f, headers=[plan.run_id_field, plan.raw_field]
                )
        print("ICR files successfully exported")

        return data
