import requests
import pandas as pd
from datetime import datetime
import time
from typing import List


def call_api(size: int = 1, ssl=True) -> List[dict]:
    url = "https://random-data-api.com/api/v2/users?size={}".format(size)
    response = requests.get(url, verify=ssl)
    response_list = response.json()
    if len(response_list) == 1:
        response_list = [response_list]
    return response_list


def call_api_single(size: int = 1000, ssl=True, wait=0) -> List[dict]:
    url = "https://random-data-api.com/api/v2/users"
    response_list = []
    for i in range(0, size):
        response = requests.get(url, verify=ssl)
        time.sleep(wait)
        response_list.append(response)
    return response_list


def flatten_df(response_list: List[dict]) -> pd.DataFrame:
    today = datetime.today().strftime("%Y-%m-%d")
    df_flat = pd.json_normalize(response_list)
    df_flat["pull_datetime"] = today
    return df_flat
