from fastapi import FastAPI

from src.Routers import MenuRouter, SubmenuRouter, DishRouter

app = FastAPI()

app.include_router(MenuRouter.router)

app.include_router(SubmenuRouter.router)

app.include_router(DishRouter.router)
