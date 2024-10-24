import requests

from src.default import BASE_URL

def get_random_facts():
    resp = requests.get(
        f"{BASE_URL}/facts/random",
    )

    assert resp.status_code == 200
    resp_json = resp.json()
    return resp_json
