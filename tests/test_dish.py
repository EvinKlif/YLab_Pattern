import uuid

from starlette.testclient import TestClient

from main import app

client = TestClient(app)

url = 'http://localhost:8000'

menu_id = uuid.uuid4()
submenu_id = uuid.uuid4()
dish_id = uuid.uuid4()

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

dish = {
    'id': str(dish_id),
    "title": "My dish 1",
    "description": "My dish description 1",
    "price": str(12.50),
}

updated_dish = {
    'id': str(dish_id),
    "title": "My updated dish 1",
    "description": "My updated dish description 1",
    "price": str(14.50),
}


def test_create_menu():
    response = client.post(f"{url}/api/v1/menus", json=menu)
    assert response.status_code == 201, " Wrong status code"
    response = response.json()
    assert response["id"] == str(menu_id), "Wrong id"
    assert response["title"] == menu["title"], "Wrong title"
    assert response["description"] == menu["description"], "Wrong description"


def test_create_submenu():
    response = client.post(f"{url}/api/v1/menus/{submenu_id}/submenus", json=submenu)
    assert response.status_code == 201, " Wrong status code"
    response = response.json()
    assert response["id"] == str(submenu_id), "Wrong id"
    assert response["title"] == submenu["title"], "Wrong title"
    assert response["description"] == submenu["description"], "Wrong description"


def test_get_empty_dishes():
    response = client.get(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200, " Wrong status code"
    assert response.json() == []


def test_create_dish():
    response = client.post(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish)
    assert response.status_code == 201, " Wrong status code"
    response = response.json()
    assert response["id"] == str(dish_id), "Wrong id"
    assert response["title"] == dish["title"], "Wrong title"
    assert response["description"] == dish["description"], "Wrong description"
    assert response["price"] == dish["price"], "Wrong price"


def test_get_new_dishes():
    response = client.get(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200, " Wrong status code"
    assert response.json() != []


def test_get_new_dish():
    response = client.get(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200, " Wrong status code"
    response = response.json()
    assert response["id"] == str(dish_id), "Wrong id"
    assert response["title"] == dish["title"], "Wrong title"
    assert response["description"] == dish["description"], "Wrong description"
    assert response["price"] == dish["price"], "Wrong price"


def test_update_dish():
    response = client.patch(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=updated_dish)
    assert response.status_code == 200, " Wrong status code"
    response = response.json()
    assert response["id"] == str(dish_id)
    assert response["title"] == updated_dish["title"], "Wrong title"
    assert response["description"] == updated_dish["description"], "Wrong description"
    assert response["price"] == updated_dish["price"], "Wrong price"


def test_get_updated_dish():
    response = client.get(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200, " Wrong status code"
    response = response.json()
    assert response["id"] == str(dish_id)
    assert response["title"] == updated_dish["title"], "Wrong title"
    assert response["description"] == updated_dish["description"], "Wrong description"
    assert response["price"] == updated_dish["price"], "Wrong price"


def test_delete_dish():
    response = client.delete(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200, " Wrong status code"


def test_get_deleted_dishes():
    response = client.get(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200, " Wrong status code"
    assert response.json() == []


def test_get_deleted_dish():
    response = client.get(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 404, " Wrong status code"
    response = response.json()
    assert response["detail"] == "dish not found", "Item not delete"


def test_delete_submenu():
    response = client.delete(f"{url}/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200, " Wrong status code"


def test_get_deleted_submemenus():
    response = client.get(f"{url}/api/v1/menus/{submenu_id}/submenus")
    assert response.status_code == 200, " Wrong status code"
    assert response.json() == []


def test_deleted_menu():
    response = client.delete(f"{url}/api/v1/menus/{menu_id}")
    assert response.status_code == 200, " Wrong status code"


def test_get_empty_menus():
    response = client.get(f"{url}/api/v1/menus")
    assert response.status_code == 200, " Wrong status code"
    assert response.json() == [], "Menu list not empty"