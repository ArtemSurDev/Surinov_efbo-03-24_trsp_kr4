from fastapi.testclient import TestClient
from task_11_1.main import app

client = TestClient(app)

class TestUserRegistration:
    def test_register_user_success(self):
        response = client.post("/register", json={
            "username": "john_doe",
            "email": "john@example.com"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "john_doe"
        assert data["email"] == "john@example.com"
        assert "id" in data

    def test_register_multiple_users(self):
        response1 = client.post("/register", json={
            "username": "user1",
            "email": "user1@example.com"
        })
        response2 = client.post("/register", json={
            "username": "user2",
            "email": "user2@example.com"
        })
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response2.json()["id"] == response1.json()["id"] + 1

    def test_register_user_invalid_data(self):
        response = client.post("/register", json={
            "username": 123,
            "email": "not-email"
        })
        assert response.status_code == 422


class TestGetUser:
    def test_get_existing_user(self):
        response = client.post("/register", json={
            "username": "jane_doe",
            "email": "jane@example.com"
        })
        user_id = response.json()["id"]
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["username"] == "jane_doe"

    def test_get_nonexistent_user(self):
        response = client.get("/users/9999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


class TestDeleteUser:
    def test_delete_existing_user(self):
        response = client.post("/register", json={
            "username": "to_delete",
            "email": "delete@example.com"
        })
        user_id = response.json()["id"]
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted"

    def test_delete_nonexistent_user(self):
        response = client.delete("/users/9999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_delete_user_then_get(self):
        response = client.post("/register", json={
            "username": "temp_user",
            "email": "temp@example.com"
        })
        user_id = response.json()["id"]
        client.delete(f"/users/{user_id}")
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 404


class TestListUsers:
    def test_list_users_empty(self):
        import task_11_1.main as main_module
        main_module.users.clear()
        response = client.get("/users")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_users_with_data(self):
        client.post("/register", json={
            "username": "list_user1",
            "email": "list1@example.com"
        })
        client.post("/register", json={
            "username": "list_user2",
            "email": "list2@example.com"
        })
        response = client.get("/users")
        assert response.status_code == 200
        assert len(response.json()) >= 2
