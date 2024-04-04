import requests

# https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson


def _get_data_from_api():
    # Fetch API data from USGOV
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
    )
    data = response.json()
    return data


def get_all_alerts():
    return _get_data_from_api()
