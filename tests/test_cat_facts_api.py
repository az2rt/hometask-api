import pytest
import requests

from src.default import BASE_URL
from src.helper import get_random_facts


@pytest.fixture(scope="session")
def session():
    with requests.Session() as session:
        yield session


def test_get_all_facts(session):
    """
    Case 1: get list of facts about cat
    Expected: checking that response will be a list
    :param session:
    """
    response = session.get(f"{BASE_URL}/facts")
    json_data = response.json()

    # checking of json from response
    assert response.status_code == 200, "ERROR: cannot get facts"
    assert isinstance(json_data, list), "Response should be as list"
    assert len(json_data) > 0, "Response should not be empty"


@pytest.mark.parametrize("fact_id", [
    get_random_facts()["_id"],
    "invalid_id"
])
def test_get_fact_by_id(session, fact_id):
    """
    Case 2: get facts by id
    Expected: checking:
                    - received random facts and all fields correct
                    - received error, because sent wrong fact_id
    """
    response = session.get(f"{BASE_URL}/facts/{fact_id}")
    json_data = response.json()

    if fact_id == "invalid_id":
        assert response.status_code == 400, "Expected 400 ERROR for response with invalid id"
        assert json_data["message"] == ("Cast to ObjectId failed for value \"invalid_id\" (type string)"
                                        " at path \"_id\" for model \"Fact\""),\
            "Text 'Fact not found' not found in response"
    else:
        assert response.status_code == 200, f"ERROR: cannot find fact by id={fact_id}"
        assert json_data["_id"] == fact_id, "Wrong ID of facts"

def test_get_random_fact(session):
    """
    Case 3: checking random functions
    Expected: test run 10 times and everytime getting new fact (fact_id different, text different)
    """

    resp = session.get(f"{BASE_URL}/facts/random")
    current = resp.json()
    for _ in range(10):
        response = session.get(f"{BASE_URL}/facts/random")
        json_data = response.json()

        #checks structure of response
        assert response.status_code == 200, "ERROR: cannot get fact"
        assert "text" in json_data, "Random fact should consist text field"
        assert isinstance(json_data["text"], str), "Text should be string"
        assert current["_id"] != json_data["_id"], "ERROR: random fact repeated!"

        current = json_data

@pytest.mark.parametrize("data",[
    {"amount": 3, "status_code": 200, "message": ""},
    {"amount": 2**32, "status_code": 405, "message": "Limited to 500 facts at a time"},
    {"amount": -500, "status_code": 200, "message": []},
    {"amount": 0, "status_code": 200, "message": []},
    {"amount": "", "status_code": 200, "message": []},
    {"amount": " ", "status_code": 200, "message": []},
    {"amount": "invalid_id", "status_code": 200, "message": []},
])
def test_get_multiple_random_facts(session, data):
    """
    Case 4: checking of validation field 'amount'=3,4294967296,-500,0,'space',invalid_id
    Expected: according to code, amount could be from 1 to 500.
              If more - 405 and 'Limited to 500 facts at a time'.
              In other cases empty response and status_code == 200
    """
    resp = session.get(f"{BASE_URL}/facts/random", params={"amount": data["amount"]})
    response_data = resp.json()
    if data["amount"] == 3:
        assert resp.status_code == data["status_code"], "Expected 200 OK response"
        assert isinstance(response_data, list), "Response should be as list"
    elif data["amount"] == 4294967296:
        assert resp.status_code == data["status_code"], "Expected 405 response"
        assert response_data['message'] == data["message"], \
            f"Response is not as expected: {data['message']}!={response_data['message']}"
    elif data["amount"] == -500:
        assert resp.status_code == data["status_code"], "Expected 200 response"
        assert isinstance(response_data, list), "Response should be as list"
        assert response_data == data["message"], \
            f"Response is not as expected: {data['message']}!={response_data['message']}"
    else:
        assert resp.status_code == data["status_code"], "Expected 200 response"
        assert isinstance(resp.json(), list), "Response should be as list"
