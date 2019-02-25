import json

from core_data_modules.data_models import Scheme

def _open_scheme(filename):
    with open(f"code_schemes/{filename}", "r") as f:
        firebase_map = json.load(f)
        return Scheme.from_firebase_map(firebase_map)

class CodeSchemes(object):

    INTERNET = _open_scheme("internet_working.json")
    INTERNET_YES_NO = _open_scheme("yes_no_internet.json")
    WATER = _open_scheme("water_filter_working.json")
    WATER_YES_NO = _open_scheme("yes_no_water.json")
    WASTE = _open_scheme("waste_disposal_improvement.json")
    WASTE_YES_NO = _open_scheme("yes_no_waste.json")

    GENDER = _open_scheme("gender.json")
    AGE = _open_scheme("age.json")
    LOCATION = _open_scheme("location.json")   
    WS_CORRECT_DATASET = _open_scheme("ws_correct_dataset.json")
