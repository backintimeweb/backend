from pydantic import BaseModel

class BasePost(BaseModel):
    year: int
    tags: str
    title: str
    desc: str


class PostIn(BasePost):
    pass

    class Config:
        orm_mode = True

class PostOut(BasePost):
    id: int

    class Config:
        orm_mode = True