from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str

users = {}
next_id = 1

@app.post("/register")
def register_user(user: User):
    global next_id
    user_id = next_id
    next_id += 1
    users[user_id] = user.model_dump()
    users[user_id]["id"] = user_id
    return users[user_id]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = users.pop(user_id)
    return {"message": "User deleted", "user": deleted_user}

@app.get("/users")
def list_users():
    return list(users.values())
