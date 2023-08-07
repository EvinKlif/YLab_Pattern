from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from src.Service.MenuService import MenuService


from src.Schemas.schemas import Menu

router = APIRouter(tags=['Menu'])

# Get all menu


@router.get('/api/v1/menus', status_code=HTTP_200_OK)
def get_all_menu(menu: MenuService = Depends()):
    return menu.get_all_menu()


# Get one menu

@router.get('/api/v1/menus/{menu_id}')
def get_all_menu(menu_id: str, menu: MenuService = Depends()):
    return menu.get_one_menu(menu_id)


# Create menu

@router.post('/api/v1/menus', status_code=HTTP_201_CREATED)
def create_menu(items: Menu, menu: MenuService = Depends()):
    return menu.create_menu(items)


# Update menu

@router.patch('/api/v1/menus/{menu_id}')
def update_menu(menu_id: str, items: Menu, menu: MenuService = Depends()):
    return menu.update_menu(menu_id, items)

# # Remove menu


@router.delete('/api/v1/menus/{menu_id}')
def delete_menu(menu_id: str, menu: MenuService = Depends()):
    return menu.delete_menu(menu_id)