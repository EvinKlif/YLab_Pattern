import uuid

from starlette.testclient import TestClient

from main import app

client = TestClient(app)

url = 'http://localhost:8000'

menu_id = uuid.uuid4()
submenu_id = uuid.uuid4()

menu = {
    'id': str(menu_id),
    "title": "My menu 1",
    "description": "My menu description 1",
}
submenu = {
    'id': str(submenu_id),
    "title": "My submenu 1",
    "description": "My submenu description 1"
    }

updated_submenu = {
    'id': str(submenu_id),
    "title": "My updated submenu 1",
    "description": "My updated submenu description 1",
}


def test_create_menu():
    response = client.post(f"{url}/api/v1/menus", json=menu)
    assert response.status_code == 201, " Wrong status code"
    response = response.json()
    assert response["id"] == str(menu_id), "Wrong id"
    assert response["title"] == menu["title"], "Wrong title"
    assert response["description"] == menu["description"], "Wrong description"


def test_get_empty_submemenus():
    response = client.get(f"{url}/api/v1/menus/{submenu_id}/submenus")
    assert response.status_code == 200, " Wrong status code"
    assert response.json() == []


def test_create_submenu():
    response = client.post(f"{url}/api/v1/menus/{submenu_id}/submenus", json=submenu)
    assert response.status_code == 201, " Wrong status code"
    response = response.json()
    assert response["id"] == str(submenu_id), "Wrong id"
    assert response["title"] == submenu["title"], "Wrong title"
    assert response["description"] == submenu["description"], "Wrong description"


def test_get_submenus():
    response = client.get(f"{url}/api/v1/menus/{submenu_id}/submenus")
    assert response.status_code == 200, " Wrong status code"
    response = response.json()
    assert response != [], "Menu list not empty"


def test_get_one_submenu():
    response = client.get(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200, " Wrong status code"
    response = response.json()
    assert response["id"] == str(submenu_id), "Wrong id"
    assert response["title"] == submenu["title"], "Wrong title"
    assert response["description"] == submenu["description"], "Wrong description"


def test_update_submenu():
    response = client.patch(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}", json=updated_submenu)
    assert response.status_code == 200, " Wrong status code"
    response = response.json()
    assert response["id"] == str(submenu_id), "Wrong id"
    assert response["title"] == updated_submenu["title"], "Wrong title"
    assert (response["description"] == updated_submenu["description"]), "Wrong description"


def test_get_updated_submenu():
    response = client.get(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200, " Wrong status code"
    response = response.json()
    assert response["id"] == str(submenu_id), "Wrong id"
    assert response["title"] == updated_submenu["title"], "Wrong title"
    assert (response["description"] == updated_submenu["description"]), "Wrong description"


def test_delete_submenu():
    response = client.delete(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200, " Wrong status code"


def test_get_deleted_submemenus():
    response = client.get(f"{url}/api/v1/menus/{submenu_id}/submenus")
    assert response.status_code == 200, " Wrong status code"
    assert response.json() == []


def test_get_deleted_submenu():
    response = client.get(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 404, " Wrong status code"
    response = response.json()
    assert response["detail"] == "submenu not found", "Item not delete"


def test_deleted_menu():
    response = client.delete(f"{url}/api/v1/menus/{menu_id}")
    assert response.status_code == 200, " Wrong status code"


def test_get_empty_menus():
    response = client.get(f"{url}/api/v1/menus")
    assert response.status_code == 200, " Wrong status code"
    assert response.json() == [], "Menu list not empty"