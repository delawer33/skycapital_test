import pytest
import uuid


@pytest.mark.asyncio
async def test_create_task(client):
    task_data = {
        "title": "New Task",
        "description": "Task description",
        "status": "created",
    }
    response = await client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    created_task = response.json()
    assert created_task["title"] == task_data["title"]
    assert uuid.UUID(created_task["uuid"])
    return created_task["uuid"]


@pytest.mark.asyncio
async def test_get_task(client):
    create_resp = await client.post(
        "/tasks/",
        json={
            "title": "Task for get",
            "description": "desc",
            "status": "created",
        },
    )
    task_uuid = create_resp.json()["uuid"]

    response = await client.get(f"/tasks/{task_uuid}")
    assert response.status_code == 200
    fetched_task = response.json()
    assert fetched_task["uuid"] == task_uuid


@pytest.mark.asyncio
async def test_update_task(client):
    create_resp = await client.post(
        "/tasks/",
        json={
            "title": "Task for update",
            "description": "desc",
            "status": "created",
        },
    )
    task_uuid = create_resp.json()["uuid"]

    update_data = {"title": "Updated Task", "status": "completed"}
    response = await client.patch(f"/tasks/{task_uuid}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == update_data["title"]
    assert updated_task["status"] == update_data["status"]


@pytest.mark.asyncio
async def test_delete_task(client):
    create_resp = await client.post(
        "/tasks/",
        json={
            "title": "Task for delete",
            "description": "desc",
            "status": "created",
        },
    )
    task_uuid = create_resp.json()["uuid"]

    response = await client.delete(f"/tasks/{task_uuid}")
    assert response.status_code == 204

    response = await client.get(f"/tasks/{task_uuid}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_task_missing_title(client):
    data = {"description": "No title field", "status": "pending"}
    response = await client.post("/tasks/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_task_not_found(client):
    non_exist_uuid = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/tasks/{non_exist_uuid}")
    assert response.status_code == 404
    assert "не найден" in response.text


@pytest.mark.asyncio
async def test_update_task_success(client):
    create_data = {
        "title": "Initial",
        "description": "desc",
        "status": "in_progress",
    }
    create_resp = await client.post("/tasks/", json=create_data)
    print(create_resp.json())
    task_uuid = create_resp.json()["uuid"]

    update_data = {"title": "Updated", "status": "completed"}
    update_resp = await client.patch(f"/tasks/{task_uuid}", json=update_data)
    assert update_resp.status_code == 200
    updated_task = update_resp.json()
    assert updated_task["title"] == "Updated"
    assert updated_task["status"] == "completed"


@pytest.mark.asyncio
async def test_update_task_not_found(client):
    non_exist_uuid = "00000000-0000-0000-0000-000000000000"
    update_data = {"title": "New title"}
    response = await client.patch(f"/tasks/{non_exist_uuid}", json=update_data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_success(client):
    create_data = {
        "title": "To delete",
        "description": "desc",
        "status": "in_progress",
    }
    create_resp = await client.post("/tasks/", json=create_data)
    task_uuid = create_resp.json()["uuid"]

    delete_resp = await client.delete(f"/tasks/{task_uuid}")
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/tasks/{task_uuid}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_not_found(client):
    non_exist_uuid = "00000000-0000-0000-0000-000000000000"
    response = await client.delete(f"/tasks/{non_exist_uuid}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task_invalid_data(client):
    create_resp = await client.post(
        "/tasks/", json={"title": "Test", "status": "in_progress"}
    )
    task_uuid = create_resp.json()["uuid"]

    invalid_data = {"status": 12345}
    response = await client.patch(f"/tasks/{task_uuid}", json=invalid_data)
    assert response.status_code == 422
