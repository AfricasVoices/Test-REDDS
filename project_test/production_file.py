from core_data_modules.traced_data.io import TracedDataCSVIO

from project_test.lib import PipelineConfiguration 

class ProductionFile(object):
    @staticmethod
    def generate(data, production_csv_output_path):
        production_keys = ["uid"]
        for plan in PipelineConfiguration.TEST_SHOWS_CODING_PLAN:
            if plan.raw_field not in production_keys:
                production_keys.append(plan.raw_field)
        for plan in PipelineConfiguration.SURVEY_CODING_PLANS:
            if plan.raw_field not in production_keys:
                production_keys.append(plan.raw_field)
                
        # Not perfoming message filtering at this stage for this test-pipeline.
        with open(production_csv_output_path, "w") as f:
            TracedDataCSVIO.export_traced_data_iterable_to_csv(data, f, headers=production_keys)
        
        return data
