from fastapi import FastAPI
from requests import request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from todo import todo as td
import json
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://192.168.1.181:3000",
    "http://192.168.1.181:3001",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tu = td.TaskUtil()

@app.get("/")
def read_root():
    return {"To-do": "Root"}

@app.get("/users")
@app.get("/users/all")
async def get_users() -> dict:
    users = tu.GetUsersList()
    return {"data" : users}

@app.get("/tasks/all")
async def get_tasks() -> dict:
    tasks = tu.GetTaskList()
    return {"data" : tasks}

@app.get("/calendar/all")
async def get_calendar() -> dict:
    taskcalendar = tu.GetCalendarList()
    return {"data" : taskcalendar}

@app.get("/tasks/")
@app.get("/tasks/today")
async def get_tasks_today() -> dict:
    tasks = tu.GetTasksForToday()
    return {"data" : tasks}

@app.get("/tasks/all/{user_id}")
async def get_tasks_user(user_id: int) -> dict:
    tasks = tu.GetTasksForUserId(user_id)
    return {"data" : [tasks]}

@app.get("/tasks/username/{user_name}")
async def get_tasks_today_user(user_name: str) -> dict:
    tasks = tu.GetTasksForTodayUserName(user_name)
    return {"data" : [tasks]}

@app.get("/tasks/userid/{user_id}")
async def get_tasks_today_user(user_id: int) -> dict:
    tasks = tu.GetTasksForTodayUserId(user_id)
    return {"data" : tasks}

@app.get("/todo/metadata")
async def get_tasks_metadata() -> dict:
    tasks = tu.GetTasksMetadata()
    return {"data" : tasks}

@app.put("/tasks/forward/{uid}")
async def forward_task(uid: int) -> dict:
    tasks = tu.UpdateTaskForward(uid)
    return {"data" : tasks}

@app.put("/tasks/backward/{uid}")
async def backward_task(uid: int) -> dict:
    tasks = tu.UpdateTaskBackward(uid)
    return {"data" : tasks}

@app.post("/task/assign")
async def task_assign(request: dict) -> dict:
    tasks = tu.AssignTask(request)
    return {"data" : tasks}

if __name__ == '__main__' :
    uvicorn.run("main:app", port=3001, host="0.0.0.0", reload=True)
