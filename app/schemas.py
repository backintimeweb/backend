from pydantic import BaseModel

class BasePost(BaseModel):
    tags: str
    title: str
    desc: str


class PostIn(BasePost):
    ...

class PostOut(BasePost):
    id: int

    class Config:
        orm_mode = True