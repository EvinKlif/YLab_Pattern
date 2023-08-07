from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from src.Service.SubmenuService import SubmenuService

from src.Schemas.schemas import Submenu

router = APIRouter(tags=['Submenu'])


# # Get all submenu


@router.get('/api/v1/menus/{menu_id}/submenus', status_code=HTTP_200_OK)
def get_all_menu(submenu: SubmenuService = Depends()):
    return submenu.get_all_submenu()

# Create submenu


@router.post('/api/v1/menus/{menu_id}/submenus', status_code=HTTP_201_CREATED)
def create_submenu(items: Submenu, menu_id: str, submenu: SubmenuService = Depends()):
    return submenu.create_submenu(items, menu_id)


# Get one submenu

@router.get('/api/v1/menus/{menu_id}/submenus/{sub_id}')
def get_one_submenu(sub_id: str, submenu: SubmenuService = Depends()):
    return submenu.get_one_submenu(sub_id)


# Update submenu


@router.patch('/api/v1/menus/{menu_id}/submenus/{sub_id}')
def update_submenu(sub_id: str, item: Submenu, submenu: SubmenuService = Depends()):
    return submenu.update_submenu(sub_id, item)


# Remove submenu

@router.delete('/api/v1/menus/{menu_id}/submenus/{sub_id}')
def delete_submenu(sub_id: str, submenu: SubmenuService = Depends()):
    return submenu.delete_submenu(sub_id)