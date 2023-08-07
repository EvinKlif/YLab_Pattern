import uuid

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

url = 'http://localhost:8000'

menu_id = uuid.uuid4()

menu = {
    'id': str(menu_id),
    "title": "My menu 1",
    "description": "My menu description 1",
}
updated_menu = {
    'id': str(menu_id),
    "title": "My updated menu 1",
    "description": "My updated menu description 1",
}

def test_get_empty_menus():
    response = client.get(f"{url}/api/v1/menus")
    print(response)
    assert response.status_code == 200, " Wrong status code"
    assert response.json() == [], "Menu list not empty"


def test_create_menu():
    response = client.post(f"{url}/api/v1/menus", json=menu)
    assert response.status_code == 201, " Wrong status code"
    response = response.json()
    assert response["id"] == str(menu_id), "Wrong id"
    assert response["title"] == menu["title"], "Wrong title"
    assert response["description"] == menu["description"], "Wrong description"

def test_get_menus():
    response = client.get(f"{url}/api/v1/menus")
    assert response.status_code == 200, " Wrong status code"
    response = response.json()
    assert response != [], "Menu list not empty"


def test_get_one_menu():
    response = client.get(f"{url}/api/v1/menus")
    assert response.status_code == 200, " Wrong status code"
    response = response.json()[0]
    assert response["target_menus_id"] == str(menu_id), "Wrong id"
    assert response["target_menus_title"] == menu["title"], "Wrong title"
    assert response["target_menus_description"] == menu["description"], "Wrong description"

def test_update_menu():
    response = client.patch(f'{url}/api/v1/menus/{menu_id}', json=updated_menu)
    assert response.status_code == 200, " Wrong status code"
    response = response.json()
    assert response["id"] == str(menu_id), "Wrong id"
    assert response["title"] == updated_menu["title"], "Wrong title"
    assert response["description"] == updated_menu["description"], "Wrong description"

def test_get_update_one_menu():
    response = client.get(f'{url}/api/v1/menus/{menu_id}')
    assert response.status_code == 200, " Wrong status code"
    response = response.json()
    assert response["id"] == str(menu_id), "Wrong id"
    assert response["title"] == updated_menu["title"], "Wrong title"
    assert response["description"] == updated_menu["description"], "Wrong description"


def test_deleted_menu():
    response = client.delete(f"{url}/api/v1/menus/{menu_id}")
    assert response.status_code == 200, " Wrong status code"


def test_get_deleted_menus():
    response = client.get(f"{url}/api/v1/menus/")
    assert response.status_code == 200, " Wrong status code"
    assert response.json() == []


def test_get_deleted_menu():
    response = client.get(f"{url}/api/v1/menus/{menu_id}")
    assert response.status_code == 404, " Wrong status code"
    response = response.json()
    assert response["detail"] == "menu not found", "Menu not delete"