from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from src.Service.DishService import DishService


from src.Schemas.schemas import Dishes

router = APIRouter(tags=['Dish'])


# # Get all dishes

@router.get('/api/v1/menus/{menu_id}/submenus/{sub_id}/dishes')
def get_all_dishes(dish: DishService = Depends()):
    return dish.get_all_dish()


# Create dishes


@router.post('/api/v1/menus/{menu_id}/submenus/{sub_id}/dishes', status_code=HTTP_201_CREATED)
def create_dishes(items: Dishes, sub_id: str, dish: DishService = Depends()):
    return dish.create_dish(items, sub_id)


# # Get one dishes

@router.get('/api/v1/menus/{menu_id}/submenus/{sub_id}/dishes/{dish_id}',status_code=HTTP_200_OK)
def get_one_dishes(dish_id: str, dish: DishService = Depends()):
    return dish.get_one_dish(dish_id)


# Update dishes


@router.patch('/api/v1/menus/{menu_id}/submenus/{sub_id}/dishes/{dish_id}')
def update_dishes(dish_id: str, item: Dishes, dish: DishService = Depends()):
    return dish.update_dish(dish_id, item)


#  Delete dishes

@router.delete('/api/v1/menus/{menu_id}/submenus/{sub_id}/dishes/{dish_id}')
def delete_dishes(dish_id: str, dish: DishService = Depends()):
    return dish.delete_dish(dish_id)
