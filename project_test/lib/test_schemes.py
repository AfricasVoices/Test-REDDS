import json

from core_data_modules.data_models import Scheme

def _open_scheme(filename):
    with open(f"code_schemes/{filename}","r") as f:
        firebase_map = json.load(f)
        return Scheme.from_firebase_map(firebase_map)

class CodeSchemes(object):
    INTERNET = _open_scheme("yes_no_internet.json")
    WATER = _open_scheme("yes_no_water.json")
    GENDER = _open_scheme("gender.json")
    AGE = _open_scheme("age.json")
    LOCATION = _open_scheme("location.json")   
    OPERATOR = _open_scheme("operator.json")
    WS_CORRECT_DATASET = _open_scheme("ws_correct_dataset.json")
    