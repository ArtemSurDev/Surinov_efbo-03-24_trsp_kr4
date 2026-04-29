import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker
from task_11_2.main import app, db, _id_seq, _id_lock
from itertools import count
from threading import Lock

fake = Faker()

@pytest.fixture(autouse=True)
def clean_db():
    db.clear()
    global _id_seq, _id_lock
    _id_seq = count(start=1)
    _id_lock = Lock()
    yield
    db.clear()

def generate_user_data():
    return {
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=80)
    }

class TestCreateUser:
    @pytest.mark.asyncio
    async def test_create_user_success(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            user_data = generate_user_data()
            response = await client.post("/users", json=user_data)
            assert response.status_code == 201
            data = response.json()
            assert data["username"] == user_data["username"]
            assert data["age"] == user_data["age"]
            assert "id" in data
            assert data["id"] == 1

    @pytest.mark.asyncio
    async def test_create_user_invalid_data(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/users", json={"username": "test"})
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_multiple_users(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            user1 = generate_user_data()
            user2 = generate_user_data()
            r1 = await client.post("/users", json=user1)
            r2 = await client.post("/users", json=user2)
            assert r1.status_code == 201
            assert r2.status_code == 201
            assert r2.json()["id"] == r1.json()["id"] + 1

    @pytest.mark.asyncio
    async def test_create_user_boundary_age(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            user_data = {"username": fake.user_name(), "age": 1}
            response = await client.post("/users", json=user_data)
            assert response.status_code == 201
            assert response.json()["age"] == 1

            user_data = {"username": fake.user_name(), "age": 120}
            response = await client.post("/users", json=user_data)
            assert response.status_code == 201
            assert response.json()["age"] == 120


class TestGetUser:
    @pytest.mark.asyncio
    async def test_get_existing_user(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            user_data = generate_user_data()
            create_resp = await client.post("/users", json=user_data)
            user_id = create_resp.json()["id"]
            response = await client.get(f"/users/{user_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == user_data["username"]
            assert data["age"] == user_data["age"]
            assert data["id"] == user_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_user(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/users/9999")
            assert response.status_code == 404
            assert response.json()["detail"] == "User not found"

    @pytest.mark.asyncio
    async def test_get_user_zero_id(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/users/0")
            assert response.status_code == 404


class TestDeleteUser:
    @pytest.mark.asyncio
    async def test_delete_existing_user(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            user_data = generate_user_data()
            create_resp = await client.post("/users", json=user_data)
            user_id = create_resp.json()["id"]
            response = await client.delete(f"/users/{user_id}")
            assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_nonexistent_user(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete("/users/9999")
            assert response.status_code == 404
            assert response.json()["detail"] == "User not found"

    @pytest.mark.asyncio
    async def test_delete_same_user_twice(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            user_data = generate_user_data()
            create_resp = await client.post("/users", json=user_data)
            user_id = create_resp.json()["id"]
            await client.delete(f"/users/{user_id}")
            response = await client.delete(f"/users/{user_id}")
            assert response.status_code == 404
