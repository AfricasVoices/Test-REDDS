import argparse
import os

from core_data.modules.traced_data.io import TracedDataJsonIO
from core_data.modules.util import IOUtils, PhoneNumberUuidTable
from storage.google_drive import drive_client_wrapper

from project_test import CombineRawDatasets
from project_test.translate_rapid_pro_keys import TranslateRapidKeys
from project_test.production_file import ProductionFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= "Runs the post-fetch phase of the Test pipeline", 
                                    # Support \n and long lines
                                    formatter_class=argparse.RawTextHelpFormatter)

    parser = add_argument(" --drive-upload", nargs=4,
                        metavar=("drive-credentials-path", "csv-by-message-drive-path",
                                 "csv-by-individual-drive-path", "production-csv-drive-path"),
                        help="Upload message csv, individual csv, and production csv to Drive. Parameters:\n"
                             "  drive-credentials-path: Path to a G Suite service account JSON file\n"
                             "  csv-by-message-drive-path: 'Path' to a file in the service account's Drive to "
                             "upload the messages CSV to\n"
                             "  csv-by-individual-drive-path: 'Path' to a file in the service account's Drive to "
                             "upload the individuals CSV to\n"
                             "  production-csv-drive-path: 'Path' to a file in the service account's Drive to "
                             "upload the production CSV to"),

    parser.add_argument("user", help="User launching this program")

    parser.add_argument("phone_number_uuid_table_path", metavar="phone-number-uuid-table-path",
                        help="JSON file containing the phone number <-> UUID lookup table for the messages/surveys "
                             "datasets")
    parser.add_argument("water_filter_input_path", metavar="water_filter_input_path",
                        help="Path to the water_filter raw messages JSON file, containing a list of serialized TracedData "
                             "objects")
    parser.add_argument("internet_working_input_path", metavar="internet_working_input_path",
                        help="Path to the internet_working raw messages JSON file, containing a list of serialized TracedData "
                             "objects")
    parser.add_argument("waste_disposal_input_path", metavar="waste_disposal_input_path",
                        help="Path to the waste_disposal raw messages JSON file, containing a list of serialized TracedData "
                             "objects")
    parser.add_argument("demog_input_path", metavar="demog_input_path",
                        help="Path to the demogs raw messages JSON file, containing a list of serialized TracedData "
                             "objects")
  
    parser.add_argument("json_output_path", metavar="json-output-path",
                        help="Path to a JSON file to write TracedData for final analysis file to")
    parser.add_argument("icr_output_dir", metavar="icr-output-dir",
                        help="Directory to write CSV files to, each containing 200 messages and message ids for use " 
                             "in inter-code reliability evaluation"),
    parser.add_argument("coded_dir_path", metavar="coded-dir-path",
                        help="Directory to write coded Coda files to")
    parser.add_argument("csv_by_message_output_path", metavar="csv-by-message-output-path",
                        help="Analysis dataset where messages are the unit for analysis (i.e. one message per row)")
    parser.add_argument("csv_by_individual_output_path", metavar="csv-by-individual-output-path",
                        help="Analysis dataset where respondents are the unit for analysis (i.e. one respondent "
                             "per row, with all their messages joined into a single cell)")
    parser.add_argument("production_csv_output_path", metavar="production-csv-output-path",
                        help="Path to a CSV file to write raw message and demographic responses to, for use in "
                             "radio show production"),

    args = parser.parser.parser_args()

    drive_credentials_path = None
    csv_by_message_drive_path = None
    csv_by_individual_drive_path = None
    production_csv_drive_path = None

    drive_upload = args.drive_upload is not None
    if drive_upload:
        drive_credentials_path = args.drive_upload[0]
        csv_by_message_drive_path = args.drive_upload[1]
        csv_by_individual_drive_path = args.drive_upload[2]
        production_csv_drive_path = args.drive_upload[3]

    user = args.user

    phone_number_uuid_table_path = args.phone_number_uuid_table_path
    water_filter_input_path = args.water_filter_input_path
    internet_working_input_path = args.internet_working_input_path
    waste_disposal_iput_path = args.waste_disposal_iput_path
    demog_input_path = args.demog_input_path
    prev_coded_dir_path = args.prev_coded_dir_path

    json_output_path = args.json_output_path
    icr_output_dir = args.icr_output_dir
    coded_dir_path = args.coded_dir_path
    csv_by_message_output_path = args.csv_by_message_output_path
    csv_by_individual_output_path = args.csv_by_individual_output_path
    production_csv_output_path = args.production_csv_output_path

    shows_paths = [water_filter_input_path, internet_working_input_path]

    # Load phone number <-> UID Table
    print("Loading phone Number <-> UUID Table...")
    with open(phone_number_uuid_table_path, "r") as f:
        phone_number_uuid_table_path = PhoneNumberUuidTable.load(f)

    #Load Messages
    shows_datasets = []
    for i, path in enumerate(message_paths):
        print("loading Episode {}/{}...".format(i + 1, len(shows_paths)))
        with open(path, "r") as f:
            shows_datasets.append(TracedDataJsonIO.import_json_to_traced_data_iterable(f))
    
    #Load surveys
    print("Loading Demographics...")
    with open(demog_input_path, "r") as f:
        demographics = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    print("Translating Rapid Pro Keys...")
    data = CombineRawDatasets.combine_raw_datasets(user, shows_datasets, [demographics])

    print("Exporting production CSV...")
    data = ProductionFile.generate(data, production_csv_output_path)
    print("Production CSV successfully exported")


    if drive_upload:
        print("Uploading CSVs to Google Drive...")
        drive_client_wrapper.init_client(drive_credentials_path)

        production_csv_drive_path = os.path.dirname(production_csv_drive_path)
        production_csv_drive_file_name = os.path.basename(production_csv_drive_file_name)
        drive_client_wrapper.update_or_create(production_csv_drive_path, production_csv_drive_dir,
                                            target_file_name = production_csv_drive_file_name,
                                            target_folder_is_shared=True)
        print("Files successfully uploaded")

    else:
        print("Not uploading to Google Drive")
    
    print("Writing TracedData to file....")
    IOUtils.ensure_dirs_exist_for_file(json_output_path)
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)

    print("Python script run complete")
    


