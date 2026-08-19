from fastapi import FastAPI
from routers import tasks
from routers import user


app = FastAPI(title="Task Manager API",  
              version="1.0") #name the app home screen title Task Manager API

@app.get("/")
def welcome():
    return{"Message": "Welcome to the TaskManager API"}

app.include_router(tasks.router) #include the router code of tasks
app.include_router(user.router) #include the router code of user

 






