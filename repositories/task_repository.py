from typing import Optional
from Database.connection import get_connection
from psycopg.rows import dict_row # Added this soo fastapi can communicate properly with SQL in the Dict Format



def get_task_by_id(id: int, user_id: int):
     with get_connection() as connection: # initiate connection and cursor pass the query and execute cursor then return
          with connection.cursor(row_factory=dict_row) as cursor:
               query = ("""SELECT id,title,status FROM tasks WHERE id = %s AND user_id = %s;""")
               cursor.execute(query, (id, user_id))
               return cursor.fetchone()

def search_task(skip: int, 
                limit: int,
                user_id: int,
                search_name: Optional[str] = None,
                task_status: Optional[str] = None,
                priority: Optional[str] = None,
                completed: Optional[bool] = None,
                sort_by: Optional[str] = None): # add parameters for searching
    
     base_query = ("SELECT id,title,status FROM TASKS WHERE user_id = %(user_id)s") # add a base query to add on top of WHERE 1=1 is used so WHERE is always True and we dont need to add it
     query_parms = {"user_id": user_id, "limit": limit, "skip": skip} # making lists of parameters to append on
     if search_name: # if search name has something 
          base_query += " AND title LIKE %(search_name)s"  # add to base AND title...
          query_parms["search_name"] = f"%{search_name}%" # append to query parameters list with %search_name% as a wild card so the title can be anyways 
     if task_status: # same goes for the rest
          base_query += " AND status = %(task_status)s" 
          query_parms["task_status"] = task_status
     if priority:
          base_query += " AND priority = %(priority)s"
          query_parms["priority"] = priority
     if completed is not None:
          base_query += " AND completed = %(completed)s::text::boolean"
          query_parms["completed"] = completed
          

     if sort_by == "id":
          base_query += " ORDER BY id" 
     elif sort_by == "title":
               base_query += " ORDER BY title"
     else:
            base_query += " ORDER BY id DESC"


     base_query += " LIMIT %(limit)s OFFSET %(skip)s" # added pagination inside SQL so we dony have to do it through RestAPI 
     with get_connection() as connection: # initiate connection and cursor then execute the base_query and query parms inside it and return results
               with connection.cursor(row_factory=dict_row) as cursor:
                         cursor.execute(base_query, query_parms)
                         results = cursor.fetchall()
                         return results

def create_task(task: dict): # let task be a dictionary as we did convert the pydantic model to a dictionary in the service layer
        query = ("""INSERT INTO tasks (title,description,completed,status,priority,user_id)
                    VALUES(%(title)s, %(description)s, %(completed)s, %(status)s, %(priority)s, %(user_id)s)
                    RETURNING id, title, status;""")  #query with s at the end of every title on SQL to prevent sql injections it tells the database driver to treat it as a string behind the scenes only
        with get_connection() as connection: # initiate connection and execute and result the created task
            with connection.cursor(row_factory=dict_row) as cursor: 
                    cursor.execute(query,task)
                    created_task = cursor.fetchone()
                    connection.commit()
                    return created_task


def put_task(id: int, u_task: dict, user_id: int): # let u_task be a dictionary as we did convert the pydantic model to a dictionary in the service layer
                u_task ["id"] = id # added id to the dictionary 
                u_task["user_id"] = user_id
      
                query = (""" UPDATE tasks
                              SET title = %(title)s, 
                              description = %(description)s,
                              completed = %(completed)s, 
                              status = %(status)s,
                              priority =  %(priority)s
                             WHERE id = %(id)s
                             AND user_id = %(user_id)s
                             RETURNING id, title, status; """)
      
                with get_connection() as connection: # initiate connection let cursor return in RealDictCursor format and execute then return
                      with connection.cursor(row_factory=dict_row) as cursor:
                            cursor.execute(query, u_task)
                            updated_task = cursor.fetchone()
                            connection.commit()
                            return updated_task
                            

def deleted_task(id: int, user_id: int):  # pass in query to delete then initiate connection and cursor then execute and return 
        query = ("""DELETE FROM tasks
        WHERE id = %s AND user_id = %s
        RETURNING id;""") 
        parm = [id , user_id]
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query,parm)
                result = cursor.fetchone()
                connection.commit()
                return result

