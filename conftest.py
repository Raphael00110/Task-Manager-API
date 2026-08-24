import pytest
from fastapi.testclient import TestClient
from app import app
from Database import sql_config, redis_config, connection


def clear_test_tables():
    try:
        with connection.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE users, tasks RESTART IDENTITY CASCADE;")
                conn.commit()
    except Exception as e:
        print(f"\n⚠️ Truncation failed: {e}")


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client: # this acts as a service that gets the client (app) from the main function as client for testing
         yield client # this holds the client so we can use when needed (basically pauses execution for use after use it continues if theres more code under)

@pytest.fixture(scope="session", autouse=True) # can be used whenever
def test_database(): # save the original credentials before routing to test database
    original_name = sql_config.DB_NAME
    original_host = sql_config.DB_HOST
    original_port = sql_config.DB_PORT
    original_password = sql_config.DB_PASSWORD
    original_redis_host = redis_config.HOST
    original_redis_port = redis_config.PORT


    sql_config.DB_NAME = "python_backend_test"
    sql_config.DB_HOST = "127.0.0.1"
    sql_config.DB_PORT = 5433
    sql_config.DB_PASSWORD = "postgres"
    redis_config.HOST = "127.0.0.1"
    redis_config.PORT = 6380


    print(
    "TEST DB:",
    sql_config.DB_NAME,
    sql_config.DB_HOST,
    sql_config.DB_PORT
        )
    print("✅ Started new truncated Database")
    clear_test_tables()
    
    yield

    clear_test_tables()
    print("\n🧹 Database Exiting successfully truncated.")
  
    
  
    sql_config.DB_NAME = original_name # after using change back to original credentials
    sql_config.DB_HOST = original_host
    sql_config.DB_PORT = original_port
    sql_config.DB_PASSWORD = original_password
    redis_config.HOST = original_redis_host
    redis_config.PORT = original_redis_port



@pytest.fixture(scope="session")
def test_register(): # This fixture tests the registration mechanism
    return {"username": "testuser",
            "email": "testuser@gmail.com",
            "password": "testpassword"
    }

@pytest.fixture(scope="session")
def registered_user(client): # This fixture registers a user for different tests
    user = {"username": "test2user",
            "email": "test2user@gmail.com",
            "password": "test2password"}
    response = client.post("/register",
                    json=user)
    assert response.status_code == 201
    yield user
    

@pytest.fixture(scope="session") # This fixture logs in the already registered user to get the access token to test different workings
def authenticated_client(client,registered_user):
    response = client.post("/login",
                          data={"username": registered_user["username"],
                                "password": registered_user["password"]})
    assert response.status_code == 200
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"

    yield client 

@pytest.fixture(scope="session")
def client2():
    with TestClient(app) as client2:
        yield client2

@pytest.fixture(scope="session")
def registered_user_2(client2):
    user2 = {"username": "seconduser",
             "email": "seconduser@gmail.com",
             "password": "seconduserpassword"}

    response = client2.post("/register",
                            json=user2)

    assert response.status_code == 201

    yield user2

@pytest.fixture(scope="session")
def authenticated_client_2(client2,registered_user_2):
    response = client2.post("/login",
                            data={"username": registered_user_2["username"],
                                  "password": registered_user_2["password"]})
    assert response.status_code == 200
    token = response.json()["access_token"] # convert response to json and store the access token in the token variable
    client2.headers["Authorization"] = f"Bearer {token}" # not put that token in your client's http header with the standard name Bearer <(then your token)>
    yield client2 # hold the client for use


@pytest.fixture(scope="session")
def user_tasks(authenticated_client,authenticated_client_2):
    task_user_1 =  {"title": "task_user_1",
                    "description": "user_1_test_task",
                    "completed": False,
                    "status": "todo",
                    "priority": "medium"}
    
    task_user_2 = {"title": "task_user_12",
                    "description": "user_2_test_task",
                    "completed": False,
                    "status": "todo",
                    "priority": "low"}
    
    response1 = authenticated_client.post("/task",
                            json=task_user_1)
    response2 = authenticated_client_2.post("/task",
                            json=task_user_2)

    assert response1.status_code == 201
    assert response2.status_code == 201

    task1_id = response1.json()['id']
    task2_id = response2.json()['id']
    authenticated_tasks = task1_id, task2_id
    yield authenticated_tasks



    