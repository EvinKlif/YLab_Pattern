from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from src.Models.models import Dishes
from src.redis import redis
from src.Schemas.schemas import Dishes as DishSchema




class DishService:
    def __init__(self, session: Session = Depends(get_db)):
        self.db: Session = session
        self.dish = Dishes

    def create_dish(self, items: DishSchema, sud_id: str):
        self.dish_model = self.dish()
        self.dish_model.target_dishes_id = items.id
        self.dish_model.target_dishes_title = items.title
        self.dish_model.target_dishes_description = items.description
        self.dish_model.target_dishes_price = items.price
        self.dish_model.submenus_id = sud_id
        self.db.add(self.dish_model)
        self.db.commit()
        self.db.refresh(self.dish_model)
        return items

    def get_all_dish(self):
        chach = redis.keys('dish')
        if chach:
            return [redis.hgetall(i) for i in chach]
        else:
            return self.db.query(self.dish).all()

    def get_one_dish(self, dish_id: str):
        if redis.keys(dish_id):
            res = redis.hgetall(dish_id)
            return res
        else:
            self.items = self.db.query(self.dish).filter(self.dish.target_dishes_id == dish_id).first()
            try:
                for redis_name in [str(dish_id), 'dish']:
                    redis.hmset(redis_name, {'id': str(dish_id), 'title': self.items.target_dishes_title, \
                                               'description': self.items.target_dishes_description,
                                               'price': self.items.target_dishes_price})

            except:
                pass
            if not self.items:
                raise HTTPException(status_code=404, detail='dish not found')
            return {'id': self.items.target_dishes_id, 'title': self.items.target_dishes_title,\
                    "description": self.items.target_dishes_description, 'price': self.items.target_dishes_price}


    def update_dish(self, dish_id: str, items: Dishes):
        self.dish_model = self.db.query(self.dish).filter(self.dish.target_dishes_id == dish_id).first()
        self.dish_model.target_dishes_title = items.title
        self.dish_model.target_dishes_description = items.description
        self.dish_model.target_dishes_price = items.price
        self.db.add(self.dish_model)
        self.db.commit()
        self.db.refresh(self.dish_model)
        redis.delete(dish_id)
        return items

    def delete_dish(self, dish_id: str):
        self.db.query(self.dish).filter(self.dish.target_dishes_id == dish_id).delete()
        self.db.commit()
        try:
            keys = redis.keys('*')
            redis.delete(*keys)
        except:
            pass
        return "Success"