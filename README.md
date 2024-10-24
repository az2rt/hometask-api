# hometask-api

installation:
Clone repository, then run commands in terminal:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```

# API Tests for Cat Facts

This repository contains test cases for the Cat Facts API. The tests are written using `pytest` and `requests`.

## Test Cases

| Case # | Test Case Description | Input                                                                                                                                                                                                                              | Expected Result |
|--------|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| 1      | Get list of facts about cats. Checking if the response is a list and not empty. | API call: `/facts`                                                                                                                                                                                                                 | - Status Code: `200` <br> - Response should be a list <br> - List should not be empty |
| 2      | Get fact by `fact_id`. Checking valid and invalid IDs. | - Valid `fact_id`: Random valid fact ID <br> - Invalid `fact_id`: `"invalid_id"`                                                                                                                                                   | - For valid `fact_id`: <br> Status Code: `200`, valid fact details <br> - For invalid `fact_id`: <br> Status Code: `400`, error message `"Fact not found"` |
| 3      | Get random facts. Test runs 10 times to check that new facts are returned each time. | API call: `/facts/random` (10 times)                                                                                                                                                                                               | - Status Code: `200` <br> - `text` field present <br> - Fact ID and text should be different in each response |
| 4      | Check multiple random facts with different amounts. Validation of 'amount' parameter. | - `amount = 3`: Valid <br> - `amount = 4294967296`: Too large <br> - `amount = -500`: Negative <br> - `amount = 0`: Zero <br> - `amount = " "/""`: empty/empty string, invalid input <br> - `amount = "invalid_id"`: Invalid input | - `amount = 3`: <br> Status Code: `200`, response is a list <br> - `amount = 4294967296`: <br> Status Code: `405`, message `"Limited to 500 facts at a time"` <br> - `amount = -500`: <br> Status Code: `200`, empty list <br> - `amount = 0`: <br> Status Code: `200`, empty list <br> - `amount = "invalid_id"`: <br> Status Code: `200`, empty list |

### Description
Case #1 - positive case; <br>
Case #2 - positive/negative positive case, checking validation of field; <br>
Case #3 - positive case, checking of random function; <br>
Case #4 - validation test of parameter `amount`, used Boundary Value Analysis and Equivalence Partitioning to find meaningful values to test a given field <br>

## Running Tests

To run the tests, you can use the following command:

```bash
pytest -v
```

