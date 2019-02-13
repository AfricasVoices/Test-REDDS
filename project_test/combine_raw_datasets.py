from core_data_modules.traced_data import TracedData 

class CombineRawDatasets(objects):
    @staticmethod
    def combine_raw_datasets(user, shows_datasets, survey_datasets):
        data = []

        for show_dataset in shows_datasets:
            data.extend(show_dataset)

        for surveys_datasets in survey_datasets:
            TracedData.update_iterable(user, "avf_phone_id", data, survey_dataset, "survey_responses")
        
        return data
        