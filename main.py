from fastapi import FastAPI, HTTPException, Request
import uvicorn
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


class NewUser(BaseModel):
    name: str
    email: str
    password: str


users = [
    User(id=1, name="Den", email="sss@mail.ru", password="123"),
    User(id=2, name="Olga", email="fff@mail.ru", password="1234"),
    User(id=3, name="Luda", email="ffff@mail.ru", password="1234")
]


@app.get("/users", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse('table.html', {"request": request, "users": users})


@app.get("/users/{id}", response_model=User)
async def get_user(user_id: int):
    if len(users) < user_id:
        raise HTTPException(status_code=404, detail="user not found")
    return users[user_id - 1]


@app.post("/users", response_model=User)
async def new_user(user: NewUser):
    user = User(
        id=len(users) + 1,
        name=user.name,
        email=user.email,
        password=user.password
    )
    users.append(user)
    return user


@app.put('/users/{user_id}', response_model=User)
def edit_user(user_id: int, changed_user: NewUser):
    for user in users:
        if user.id == user_id:
            user.name = changed_user.name
            user.email = changed_user.email
            user.password = changed_user.password
            return user
        raise HTTPException(status_code=404, detail='User not found')


@app.delete('/users/{user_id}', response_model=str)
def delete_user(user_id: int, new_user: NewUser):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return f"User {user_id} was deleted"
        raise HTTPException(status_code=404, detail='User no found')


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
