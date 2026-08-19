from fastapi import APIRouter, status, Query, Depends
from typing import Optional, List
from schemas.task import *
from Database.connection import *
import services.task_service as task_service 
from services.user_service import get_current_user_id




router = APIRouter() # as this is not the main app we have to route to the main file connection

# get task by id
@router.get("/tasks/{id}", response_model=ViewTasks)
def view_task(id: int,user_id: int = Depends(get_current_user_id)):

      return task_service.get_task_by_id(id, user_id)

# get task by any attribute
@router.get("/tasks", response_model= List[ViewTasks]) # get tasks with different attributes response should be viewtasks basemode but a list of it because the response can be multiple tasks
def view_tasks(search_name: Optional[str] = None,
                task_status: Optional[str] = None,
                priority: Optional[str] = None,
                completed: Optional[bool] = None,
                sort_by: Optional[str] = None,
                skip: int = Query(0, ge=0),
                limit: int = Query(10, ge=1, le=100),
                user_id: int = Depends(get_current_user_id)):
      
      return task_service.search_task(
          skip=skip,
          limit=limit,
          user_id=user_id,
          search_name=search_name,
          task_status=task_status,
          priority=priority,
          completed=completed,
          sort_by=sort_by
      )

# create a new task              
@router.post("/task", response_model=ViewTasks, status_code=status.HTTP_201_CREATED) # to add a task  we use code 201 for sucessfull creation and response is viewtask base model
def post_task(new_task: CreateTasks,
              user_id: int = Depends(get_current_user_id)): # let new_task to the basemodel of CreateTasks
      
      return task_service.create_task(new_task, user_id)

 # update a task by id            
@router.put("/task/{id}", response_model=ViewTasks) # to update task we also use viewtasks response model
def update_task(id: int, updated_task: CreateTasks, user_id = Depends(get_current_user_id)): # updated_task should has base createtasks and we have to provide the task ID
          
          return task_service.put_task(id, updated_task, user_id)

# delete task by id
@router.delete("/task/{id}", status_code=status.HTTP_204_NO_CONTENT) # to delete task we use status code 204 for sucess
def delete_task(id: int, user_id = Depends(get_current_user_id)): # we pass id we want to delete and loop through the index and item of task fake database list and if we find we delete the task using its index
      return task_service.deleted_task(id, user_id)
