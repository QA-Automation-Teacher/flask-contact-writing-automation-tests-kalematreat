import csv
import time
BASE_URL = "http://localhost:5000"

def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_get_contacts(client,BASE_URL, resources):
    response = client.get(f"{BASE_URL}/{resources}")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

# 2--> Test if the response time is less than 300ms
# @pytest.mark.xfail
def test_response_time(client,BASE_URL, resources):
    start = time.time()
    client.get(f"{BASE_URL}/{resources}")
    end = time.time()
    assert end - start < 0.3

# 3--> Test if the number of posts is 100
def test_number_of_posts(client,BASE_URL, resources):
    response = client.get(f"{BASE_URL}/{resources}")
    json_data = response.get_json()
    assert len(json_data) > 0

# 4--> Test if the response is an array
def test_response_is_array(client,BASE_URL, resources):
    response = client.get(f"{BASE_URL}/{resources}")
    json_data = response.get_json()
    assert isinstance(json_data, list)