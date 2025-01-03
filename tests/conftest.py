import pytest
import sys
import os
import json



src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)


from app import app


@pytest.fixture
def client():
    with app.app_context(): 
        app.config.update({
            "TESTING": True
        })
        yield app.test_client()

@pytest.fixture()
def BASE_URL():
    return "http://localhost:5000"

@pytest.fixture()
def ID_POST():
    return 1

@pytest.fixture()
def del_post_id():
    return 10
    #  return 54

@pytest.fixture()
def resources():
    return "contacts"

# @pytest.fixture()
# def comments_resources():
#     return "comments"