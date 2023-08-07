from pydantic import BaseModel, Field
from uuid import uuid4, UUID


class Dishes(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    price: str
    submenus_id: UUID = Field(default_factory=uuid4)

    class Config:
        orm_mode = True


class Submenu(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    menus_id: UUID = Field(default_factory=uuid4)

    class Config:
        orm_mode = True


class Menu(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str

    class Config:
        orm_mode = True
