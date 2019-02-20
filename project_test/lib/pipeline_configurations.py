from core_data_modules.cleaners import swahili, Codes

from project_test.lib.test_schemes import CodeSchemes

class CodingPlan(object):
    def __init__ (self, raw_field, coded_field, coda_filename, cleaner=None, code_scheme=None, time_field=None,
                    run_id_field=None, icr_filename=None, analysis_file_key=None, id_field=None,
                    binary_code_scheme=None, binary_coded_field=None, binary_analysis_file_key=None):
        self.raw_field = raw_field
        self.coded_field = coded_field
        self.coda_filename = coda_filename
        self.icr_filename = icr_filename
        self.cleaner = cleaner
        self.code_scheme = code_scheme
        self.time_field = time_field
        self.run_id_field = run_id_field
        self.analysis_file_key = analysis_file_key
        self.binary_code_scheme = binary_code_scheme
        self.binary_coded_field = binary_coded_field
        self.binary_analysis_file_key = binary_analysis_file_key


        if id_field is None:
            id_field = "{}_id".format(self.raw_field)
        self.id_field = id_field

class PipelineConfiguration(object):
   
    DEV_MODE = True # Set to True when testing the pipeline - False removes data for AVF test contacts.

    TEST_SHOWS_CODING_PLAN = [
       CodingPlan(raw_field="internet_working_raw",
                time_field="sent_on",
                coded_field="internet_working_coded",
                coda_filename="internet_working.json",
                icr_filename="internet_working.csv",
                run_id_field="internet_working_id",
                cleaner=None,
                analysis_file_key="internet_working_",
                code_scheme=CodeSchemes.INTERNET,
                binary_code_scheme=CodeSchemes.INTERNET_YES_NO,
                binary_coded_field="internet_working_coded",
                binary_analysis_file_key="internet_working_yes_no"),

        CodingPlan(raw_field="water_filter_raw",
                time_field="sent_on",
                coded_field="water_filter_coded",
                coda_filename="water_filter.json",
                icr_filename="water_filter_icr.csv",
                run_id_field="water_filter_id",
                cleaner=None,
                analysis_file_key="water_filter_",
                code_scheme=CodeSchemes.WATER,
                binary_code_scheme=CodeSchemes.WATER_YES_NO,
                binary_coded_field="water_filter_coded",
                binary_analysis_file_key="water_filter_yes_no"),

        CodingPlan(raw_field="waste_disposal_raw",
                time_field="sent_on",
                coda_filename="waste_disposal_improvement.json",
                icr_filename="waste_disposal_icr.csv",
                run_id_field="waste_disposal_improvement.json",
                cleaner=None,
                coded_field="waste_disposal_coded",
                analysis_file_key="waste_disposal_",
                code_scheme=CodeSchemes.WASTE,
                binary_coded_field="waste_disposal_yes_no_coded",
                binary_analysis_file_key="waste_disposal_yes_no",
                binary_code_scheme=CodeSchemes.WASTE_YES_NO),
    ]
    
    @staticmethod
    def clean_age_within_range(text):
        age = swahili.DemographicCleaner.clean_age(text)
        if type(age) == int and 10 <= age < 100:
            return str(age)
        else:
            return Codes.Not_Coded

    SURVEY_CODING_PLANS = [
        CodingPlan(raw_field="age_raw",
                coded_field="age_coded",
                time_field="age_time",
                coda_filename="age.json",
                analysis_file_key="age",
                cleaner=lambda text: PipelineConfiguration.test_clean_age(text),
                code_scheme=CodeSchemes.AGE),

        CodingPlan(raw_field="gender_raw",
                coded_field="gender_coded",
                time_field="gender_time",
                coda_filename="gender.json",
                run_id_field="gender_id",
                analysis_file_key="gender",
                cleaner=swahili.DemographicCleaner.clean_gender,
                code_scheme=CodeSchemes.GENDER),

        CodingPlan(raw_field="client_region_raw",
                coded_field="client_region_coded",
                time_field="client_region_time",
                coda_filename="location.json",
                run_id_field="client_region_id",
                analysis_file_key="client_region_",
                cleaner=None,
                code_scheme=CodeSchemes.LOCATION)
    ]
