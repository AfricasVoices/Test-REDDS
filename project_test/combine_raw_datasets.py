from core_data_modules.traced_data import TracedData 

class CombineRawDatasets(object):
    @staticmethod
    def combine_raw_datasets(user, shows_datasets, survey_datasets):
        data = []

        for show_dataset in shows_datasets:
            data.extend(show_dataset)

        for survey in survey_datasets:
            TracedData.update_iterable(user, "avf_phone_id", data, survey, "survey_responses")
        
        return data
