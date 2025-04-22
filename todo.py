from fastapi import APIRouter , Path
from model.model import Todo


todo_router = APIRouter()

todo_list = [{"id": 1, "title": "Buy milk"}, {"id": 2, "title": "Learn FastAPI"}]


@todo_router.post("/post_todo")
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {"message": "todo added success"}


@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return {"todos": todo_list}


@todo_router.get("/todo/{todo_id}")