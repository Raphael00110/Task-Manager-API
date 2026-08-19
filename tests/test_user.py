from fastapi.testclient import TestClient 
from app import app
from unittest.mock import patch
from services import task_service

# home testing
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

# user testing
def test_register_user(client,test_register):
    response = client.post("/register",
                           json=test_register)
    assert response.status_code == 201

def test_already_registered_user(client,registered_user):
    response = client.post("/register",
                           json=registered_user)
    assert response.status_code == 409



def test_register_invalid_user(client):
    response = client.post("/register",
                           json={"username": "anotheruser",
                                 "email": "this-is-not-an-email",
                                 "password": "anothertest"})
    assert response.status_code == 422

# Authenticated CRUD checks
def test_me(authenticated_client):
    response = authenticated_client.get("/me")
    assert response.status_code == 200
def test_create_task(authenticated_client):
    response = authenticated_client.post("/task",
                                         json= {
  "id": 1,
  "title": "test",
  "description": "test_description",
  "completed": False,
  "status": "todo",
  "priority": "medium"
}
)
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == "test"
    assert data["status"] == "todo"



def test_search_tasks(authenticated_client):
    response = authenticated_client.get("/tasks",
                                        params={"search_name": "test",
                                                "task_status": "todo",
                                                "priority": "medium"})
    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0
    assert "test" in data[0]["title"]
    assert data[0]["status"] == "todo"
  

def test_update_task(authenticated_client):

    task = authenticated_client.post("/task",
                                       json= {
                                         "title": "update_test",
                                         "description": "test_description",
                                         "completed": False,
                                         "status": "todo",
                                         "priority": "low"
                                       })
    task = task.json()['id']

    response = authenticated_client.put(f"/task/{task}",

                                        json= {
                                          "title": "updated_test",
                                          "description": "updated_test_description",
                                          "completed": False,
                                          "status": "todo",
                                          "priority": "medium"
                                        })
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "updated_test"

def test_delete_task(authenticated_client):
     task = authenticated_client.post("/task",
                                           json= {
                                             "title": "update_test",
                                             "description": "test_description",
                                             "completed": False,
                                             "status": "todo",
                                             "priority": "low"
                                           })
     task = task.json()['id']
    
     response = authenticated_client.delete(f"/task/{task}")
     assert response.status_code == 204
     deleted_response = authenticated_client.get(f"/tasks/{task}")
     assert deleted_response.status_code == 404

def test_me_without_auth(): 

    unauth_client = TestClient(app)

    response = unauth_client.get("/me")
    assert response.status_code == 401


# 2 User Conflict Checks

def test_task_conflict_get(authenticated_client,authenticated_client_2, user_tasks):

    task_user_1, task_user_2 = user_tasks

    # request task of client 2 to client 1

    response_user_1 = authenticated_client.get(f"/tasks/{task_user_2}")

    assert response_user_1.status_code == 404

    # request task of client 1 to client 2

    response_user_2 = authenticated_client_2.get(f"/tasks/{task_user_1}")

    assert response_user_2.status_code == 404

def test_task_conflict_put(authenticated_client,authenticated_client_2,user_tasks):
    task_user_1, task_user_2 = user_tasks
    response_user_1 = authenticated_client.put(
        f"/task/{task_user_2}",
        json={
            "title": "conflict_test",
            "description": "updated_description",
            "completed": False,
            "status": "todo",
            "priority": "medium"
        }
    )
    print(response_user_1.json())
    assert response_user_1.status_code == 404
            
    response_user_2 = authenticated_client_2.put(
        f"/task/{task_user_1}",
        json={
            "title": "conflict_test_2",
            "description": "updated_description_2",
            "completed": False,
            "status": "todo",
            "priority": "medium"
        }
    )
    assert response_user_2.status_code == 404

def test_task_conflict_delete(authenticated_client,authenticated_client_2,user_tasks):
    task_user_1, task_user_2 = user_tasks

    response_user_1 = authenticated_client.delete(f"/task/{task_user_2}")
    assert response_user_1.status_code == 404
    response_user_2 = authenticated_client_2.delete(f"/task/{task_user_1}")
    assert response_user_2.status_code == 404



# Redis Testing
def test_task_cache_hit(authenticated_client):
    with patch("services.task_service.task_repository.search_task") as mock_search: # if ur calling this location heres the fake result u need to use
         mock_search.return_value = [{
                "id": 999,
                "title": "cached_task",
                "status": "todo",
                "priority": "medium",
                "completed": False,}]
         first = authenticated_client.get("/tasks") # this will go to router -> service -> repository -> result = mock value
         second = authenticated_client.get("/tasks") # mock value will not get called because of cache hit

         assert first.status_code == 200
         assert second.status_code == 200
         assert mock_search.call_count == 1 

         post = authenticated_client.post("/task", json={
            "title": "cach_test",
            "description": "cache description",
            "completed": False,
            "status": "todo",
            "priority": "high"})

         third = authenticated_client.get("/tasks") 
         assert third.status_code == 200
         assert mock_search.call_count == 2  


    




    


