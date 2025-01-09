from fastapi import HTTPException, APIRouter
from typing import List, Optional
# In-memory storage
todos = []
router = APIRouter(prefix="/simple", tags=["simple"])

@router.get("/")
def read_root():
    return {"message": "Welcome to our API!"}

@router.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

@router.get("/calculator/")
def calculate(a: int, b: int, operation: str):
    if operation == "add":
        return {"result": a + b}
    elif operation == "multiply":
        return {"result": a * b}
    else:
        raise HTTPException(status_code=400, detail="Operation not supported")

# Simple CRUD for todos (using list as storage)
@router.post("/todos/")
def create_todo(title: str, completed: bool = False):
    todo = {"id": len(todos) + 1, "title": title, "completed": completed}
    todos.append(todo)
    return todo

@router.get("/todos/")
def get_todos(skip: int = 0, limit: int = 10):
    return todos[skip : skip + limit]

@router.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, title: str = None, completed: bool = None):
    for todo in todos:
        if todo["id"] == todo_id:
            if title is not None:
                todo["title"] = title
            if completed is not None:
                todo["completed"] = completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            return todos.pop(index)
    raise HTTPException(status_code=404, detail="Todo not found")

# Query parameters example
@router.get("/search/")
def search_items(q: str, category: Optional[str] = None):
    return {
        "search_term": q,
        "category": category,
        "message": f"Searching for {q} in category {category if category else 'all'}"
    }
