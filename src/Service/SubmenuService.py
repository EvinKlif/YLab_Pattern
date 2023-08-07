from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from src.Models.models import Dishes, Submenu
from src.redis import redis
from src.Schemas.schemas import Submenu as SubmenuSchema



class SubmenuService:
    def __init__(self, session: Session = Depends(get_db)):
        self.db: Session = session
        self.submenu = Submenu

    def create_submenu(self, items: SubmenuSchema, menu_id: str):
        self.submenu_model = self.submenu()
        self.submenu_model.target_submenus_id = items.id
        self.submenu_model.target_submenus_title = items.title
        self.submenu_model.target_submenus_description = items.description
        # self.submenu_model.menus_id = menu_id
        self.db.add(self.submenu_model)
        self.db.commit()
        self.db.refresh(self.submenu_model)
        return items

    def get_all_submenu(self):
        chach = redis.keys('submenu')
        if chach:
            return [redis.hgetall(i) for i in chach]
        else:
            return self.db.query(self.submenu).all()

    def get_one_submenu(self, sub_id: str):
        if redis.keys(sub_id):
            res = redis.hgetall(sub_id)
            return res
        else:
            self.items = self.db.query(self.submenu).filter(self.submenu.target_submenus_id == sub_id).first()
            dishes_count = len(self.db.query(Dishes).all())
            try:
                for redis_name in [str(sub_id), 'submenu']:
                    redis.hmset(redis_name, {'id': str(sub_id), 'title': self.items.target_submenus_title,\
                    'description': self.items.target_submenus_description, 'dishes_count': dishes_count})
            except:
                pass
            if not self.items:
                raise HTTPException(status_code=404, detail='submenu not found')
            return {'id': self.items.target_submenus_id, 'title': self.items.target_submenus_title,\
                    "description": self.items.target_submenus_description, 'dishes_count': dishes_count}

    def update_submenu(self, sub_id: str, items: Submenu):
        self.submenu_model = self.db.query(self.submenu).filter(self.submenu.target_submenus_id == sub_id).first()
        self.submenu_model.target_submenus_title = items.title
        self.submenu_model.target_submenus_description = items.description
        self.db.add(self.submenu_model)
        self.db.commit()
        self.db.refresh(self.submenu_model)
        redis.delete(sub_id)
        return items

    def delete_submenu(self, sub_id: str):
        self.db.query(self.submenu).filter(self.submenu.target_submenus_id == sub_id).delete()
        self.db.commit()
        try:
            keys = redis.keys('*')
            redis.delete(*keys)
        except:
            pass
        return "Success"