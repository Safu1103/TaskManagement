from fastapi.testclient import TestClient
from src.main import api, tasks, Task


client = TestClient(api)


# Reset tasks before every test
def reset_tasks():
    tasks.clear()

    tasks.extend([
        Task(
            id=1,
            title="Study FastAPI",
            description="Learn FastAPI basics",
            status="pending",
            priority="high"
        ),
        Task(
            id=2,
            title="Write Assignment",
            description="Complete the API assignment",
            status="in_progress",
            priority="medium"
        )
    ])


# Test GET all tasks
def test_get_tasks():
    reset_tasks()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2


# Test GET one task
def test_get_single_task():
    reset_tasks()

    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Study FastAPI"


# Test POST - successful
def test_create_task():
    reset_tasks()

    response = client.post("/tasks", json={
        "id": 3,
        "title": "Learn Python",
        "description": "Practice Python programming",
        "status": "pending",
        "priority": "high"
    })

    assert response.status_code == 201
    assert response.json()["id"] == 3
    assert response.json()["title"] == "Learn Python"


# Test POST - invalid duplicate ID
def test_create_duplicate_task():
    reset_tasks()

    response = client.post("/tasks", json={
        "id": 1,
        "title": "Duplicate Task",
        "description": "This should fail",
        "status": "pending",
        "priority": "low"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Task ID already exists"


# Test POST - invalid status
def test_create_task_invalid_status():
    reset_tasks()

    response = client.post("/tasks", json={
        "id": 3,
        "title": "Invalid Task",
        "description": "This should fail",
        "status": "invalid_status",
        "priority": "high"
    })

    assert response.status_code == 422


# Test PUT - successful
def test_update_task():
    reset_tasks()

    response = client.put("/tasks/1", json={
        "id": 1,
        "title": "Study FastAPI Updated",
        "description": "Learn FastAPI and pytest",
        "status": "completed",
        "priority": "high"
    })

    assert response.status_code == 200
    assert response.json()["title"] == "Study FastAPI Updated"
    assert response.json()["status"] == "completed"


# Test PUT - invalid ID mismatch
def test_update_task_id_mismatch():
    reset_tasks()

    response = client.put("/tasks/1", json={
        "id": 5,
        "title": "Wrong ID",
        "description": "This should fail",
        "status": "pending",
        "priority": "low"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Task ID mismatch"


# Test GET - task not found
def test_get_nonexistent_task():
    reset_tasks()

    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# Test DELETE - successful
def test_delete_task():
    reset_tasks()

    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Study FastAPI"


# Test DELETE - task not found
def test_delete_nonexistent_task():
    reset_tasks()

    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"