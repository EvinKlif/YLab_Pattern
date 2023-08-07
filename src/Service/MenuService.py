from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from src.Models.models import Menu, Dishes, Submenu
from src.redis import redis
from src.Schemas.schemas import Menu as MenuSchema



class MenuService:
    def __init__(self, session: Session = Depends(get_db)):
        self.db: Session = session
        self.menu = Menu

    def create_menu(self, item: MenuSchema):
        self.menu_model = self.menu()
        self.menu_model.target_menus_id = item.id
        self.menu_model.target_menus_title = item.title
        self.menu_model.target_menus_description = item.description
        self.db.add(self.menu_model)
        self.db.commit()
        self.db.refresh(self.menu_model)
        return item

    def get_all_menu(self):
        chach = redis.keys('menu')
        if chach:
            return [redis.hgetall(i) for i in chach]
        else:
            return self.db.query(self.menu).all()

    def get_one_menu(self, menu_id: str):
        if redis.keys(menu_id):
            res = redis.hgetall(menu_id)
            return res
        else:
            self.items = self.db.query(self.menu).filter(self.menu.target_menus_id == menu_id).first()
            self.submenus_count = len(self.db.query(Submenu).all())
            self.dishes_count = len(self.db.query(Dishes).all())
            try:
                for redis_name in [str(menu_id), 'menu']:
                    redis.hmset(redis_name, {'id': str(menu_id), 'title': self.items.target_menus_title, \
                    'description': self.items.target_menus_description, 'submenus_count': self.submenus_count, \
                    'dishes_count': self.dishes_count})
            except:
                pass
            if not self.items:
                raise HTTPException(status_code=404, detail='menu not found')
            return {'id': self.items.target_menus_id, 'title': self.items.target_menus_title,\
                    "description": self.items.target_menus_description, "submenus_count":  int(self.submenus_count),\
                    'dishes_count': self.dishes_count}


    def update_menu(self, menu_id: str, item: Menu):
        self.menu_model = self.db.query(self.menu).filter(self.menu.target_menus_id == menu_id).first()
        self.menu_model.target_menus_title = item.title
        self.menu_model.target_menus_description = item.description
        self.db.add(self.menu_model)
        self.db.commit()
        self.db.refresh(self.menu_model)
        redis.delete(menu_id)
        return item

    def delete_menu(self, menu_id: str):
        self.db.query(self.menu).filter(self.menu.target_menus_id == menu_id).delete()
        self.db.commit()
        try:
            keys = redis.keys('*')
            redis.delete(*keys)
        except:
            pass
        return "Success"