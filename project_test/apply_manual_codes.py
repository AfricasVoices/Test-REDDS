import time
from os import path

from core_data_modules.cleaners import Codes
from core_data_modules.cleaners.cleaning_utils import CleaningUtils
from core_data_modules.cleaners.location_tools import SomaliaLocations
from core_data_modules.data_models import Code
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataCodaV2IO

from project_test.lib.pipeline_configurations import PipelineConfiguration
from project_test.lib.test_schemes import CodeSchemes

class ApplyManualCodes(object):
    @staticmethod
    def make_location_code(scheme, clean_value):
        if clean_value == Codes.NOT_CODED:
            return scheme.get_code_with_control_code(Codes.NOT_CODED)
        else:
            return scheme.get_code_with_match_value(clean_value)

    @classmethod 
    def apply_manual_codes(cls, user, data, coda_input_dir):
        """ Merge manually coded radio show files into the cleaned dataset """
        for plan i PipelineConfiguration.TEST_SHOWS_CODING_PLANS:
            test_pipeline_messages = [td for td in data if plan.raw_field in td]
            coda_input_path = path.join(coda_input_dir, plan.coda_filename)

            f = None
            try:
                if path.exists(coda_input_path):
                    f = open(coda_input_path, 'r')
                TracedDataCodaV2IO.import_coda_2_to_traced_data_iterable_multi_coded(
                    user, test_pipeline_messages, plan.id_field, {plan.coded_field: plan.code_scheme}, f)

                if plan.binary_code_scheme is not None:
                    if f is not None:
                        f.seek(0)
                    TracedDataCodaV2IO.import_coda_2_to_traced_data_iterable(
                        user, test_pipeline_messages, plan.id_field, {plan.binary_coded_field:plan_binary_code_scheme}, f)

            finally:
                if f is not None:
                    f.close()

    # Merge manually coded survey files into cleeaned dataset
    for plan in PipelineConfiguration.SURVEY_CODING_PLANS:
        f = None
        try:
            coda_input_path = path.join(coda_input_dir, plan.coda_filename)
            if path.exists(coda_input_path):
                f = open(coda_input_path, 'r')
            TracedDataCodaV2IO.import_coda_2_to_traced_data_iterable(
                user, data, plan.id_field, {plan.coded_field: plan.code_scheme}, f)
        finally:
            if f is not None:
                f.close()
