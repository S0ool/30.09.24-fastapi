from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from posts.rep import UserRepository, PostRepository

app = FastAPI()



# Pydantic схемы
class UserCreate(BaseModel):
    name: str
    email: str


class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int




# Маршруты для пользователей
@app.post("/users/", response_model=UserCreate)
async def create_user(user: UserCreate):
    try:
        return await UserRepository.create(user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")


@app.get("/users/")
async def get_users():
    return await UserRepository.get_all(join_related=['posts'])


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return await UserRepository.get_by_id(user_id, join_related=['posts'])


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserCreate):
    return await UserRepository.update(user_id, user.dict())


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return await UserRepository.delete(user_id)


# Маршруты для постов
@app.post("/posts/", response_model=PostCreate)
async def create_post(post: PostCreate):
    return await PostRepository.create(post)


@app.get("/posts/")
async def get_posts():
    return await PostRepository.get_all()


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    return await PostRepository.get_by_id(post_id)


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: PostCreate):
    return await PostRepository.update(post_id, post.dict())


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    return await PostRepository.delete(post_id)




