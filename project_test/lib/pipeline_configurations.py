from core_data_modules.cleaners import swahili, Codes

from project_redss.lib.redss_schemes import CodeSchemes

class CodingPlan(object):
    def __init__ (self, raw_field, coded_field, coda_filename, cleaner=None, code_scheme=None, time_field=None,
                    run_id_field=None, icr_filename=None, analysis_file_key=None, id_field=None):
        self.raw_field = raw_field
        self.coded_field = coded_field
        self.coda.coda_filename = coda_filename
        self.icr_filename = icr_filename
        self.cleaner = cleaner
        self.code_scheme = code_scheme
        self.time_field = time_field
        self.run_id_field = time_field
        self.analysis_file_key = analysis_file_key

        if id_field is None:
            id_field = "{}_id".format(self.raw_field)
        self.run_id_field = id_field

class PipelineConfiguration(object):
    
    DEV_MODE = False

    TEST_SHOWS_CODING_PLAN = [
        CodingPlan(raw_field="internet_working_raw",
        coded_field="internet_working_coded",
        time_field="sent_on",
        coda_filename="internet_working.json"
        icr_filename="internet_working.csv",
        run_id_field="internet_working_id",
        analysis_file_key="internet_working_",
        cleaner=None,
        code_scheme=CodeSchemes.INTERNET),

        CodingPlan(raw_field="water_filter_raw",
        coded_field="water_filter_coded",
        time_field="sent_on",
        coda_filename="water_filter.json"
        icr_filename="water_filter_icr.csv",
        run_id_field="water_filter_id",
        analysis_file_key="water_filter_",
        cleaner=None,
        code_scheme=CodeSchemes.WATER),
    ]
    
    @staticmethod
    def test_clean_age(text):
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
        code_scheme=CodeScheme.AGE),
    ]

    SURVEY_CODING_PLANS.extend([
        CodingPlan(raw_field="gender_raw",
        coded_field="gender_coded",
        time_field="gender_time",
        coda_filename="gender.json"
        run_id_field="gender_id",
        analysis_file_key="gender",
        cleaner=swahili.DemographicCleaner.clean_gender,
        code_scheme=CodeSchemes.WATER)
    ])
        
    LOCATION_CODING_PLANS = [
        CodingPlan(raw_field="client_region_raw",
        coded_field="client_region_coded",
        time_field="client_region_time",
        coda_filename="location.json"
        run_id_field="client_region_id",
        analysis_file_key="client_region_",
        cleaner=None,
        code_scheme=CodeSchemes.LOCATION),
    ]

    SURVEY_CODING_PLANS.extend(LOCATION_CODING_PLANS)