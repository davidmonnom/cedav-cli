import json
import os


# Need to make attention to the file location instead of user one.
CACHE_PATH = f"{os.path.dirname(__file__)}/../../.cache"


def read_json_configuration(file):
    try:
        json_configuration = open(f"{CACHE_PATH}/{file}", "r")
        return json.loads(json_configuration.read())
    except:
        return False


def write_json_configuration(file, data):
    try:
        if not os.path.exists(CACHE_PATH):
            os.makedirs(CACHE_PATH)

        json_configuration = open(f"{CACHE_PATH}/{file}", "w")
        json_configuration.write(json.dumps(data))
        json_configuration.close()

        return True
    except:
        return False
