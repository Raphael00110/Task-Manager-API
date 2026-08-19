from typing import Optional
from fastapi import HTTPException, status
from schemas.task import *
from repositories import task_repository
from Database.redis_connection import r, TTL, invalidate_user_task_cache
from Database import redis_connection
import json


def get_task_by_id(id: int, user_id: int): 
     result = task_repository.get_task_by_id(id, user_id) # pass the id to the repository function and get the result
     if not result: # if the result is empty then raise an exception
            raise HTTPException(
                   status_code=status.HTTP_404_NOT_FOUND,
                   detail=f"Task with ID {id} not found!")
     return result


def search_task(skip: int, 
                limit: int,
                user_id: int,
                search_name: Optional[str] = None,
                task_status: Optional[str] = None,
                priority: Optional[str] = None,
                completed: Optional[bool] = None,
                sort_by: Optional[str] = None): # Add parameters for searching
          cache_key = (
                f"tasks:"
                f"user:{user_id}:"
                f"search:{search_name}:"
                f"status:{task_status}:"
                f"priority:{priority}:"
                f"completed:{completed}:"
                f"sort:{sort_by}:"
                f"skip:{skip}:"
                f"limit:{limit}"
                         ) # add this to make a redis special id per cache hit this is a default value where values will be put
          
          cache_hit = redis_connection.get_redis_connection().get(cache_key) # if there is a key inside redis with values specific to the user input then get it
          if cache_hit:
               return json.loads(cache_hit) # return it instead of searching the database

           # else no cache_hit then thats a cache miss go to the repository to fetch the data 
          result = task_repository.search_task(skip, limit, user_id, search_name, task_status, priority, completed, sort_by)
          redis_connection.get_redis_connection().set(cache_key, json.dumps(result), ex=TTL) # then store it using r.set with the default key inside it would have the result user_id ... etc
          return result # return result

def create_task(new_task: CreateTasks, user_id: int): # let new_task to the basemodel of CreateTasks Pydantic Model
            task = new_task.model_dump() # let task to the model_dump of new_task which converts the pydantic model to a dictionary
            task["user_id"] = user_id
            result =  task_repository.create_task(task) # return the result from the task_repo create_task function 
            if result: 
                    invalidate_user_task_cache(user_id)
            return result
                    

def put_task(id: int, updated_task: CreateTasks, user_id: int): # Add parameters let updated_task to the basemodel of CreateTasks
                u_task = updated_task.model_dump() # let u_task to dictionary of updated_task model
                show = task_repository.put_task(id, u_task, user_id) # pass the id and u_task dictionary to task repo put task and assign to show variable
                if not show: # if its empty then raise an exception
                      raise HTTPException(
                              status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Task with ID {id} not found!")
                
                invalidate_user_task_cache(user_id)
                return show

def deleted_task(id: int, user_id: int): 
        deleted = task_repository.deleted_task(id, user_id) # let deleted to the task_repo deleted_task function and pass id 
        if not deleted: # if its empty then raise an exception
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task with ID {id} not found!")
        invalidate_user_task_cache(user_id)
        return 






