def test_criar_usuario(client):
    payload = {
        "username": "Armando",
        "email": "armando@gmail.com",
        "senha": "12345678"
    }
    response = client.post("/usuarios/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "id" in data

def test_login_usuario(client):
	payload = {
		"email": "armando@gmail.com",
		"senha": "12345678"
	}
	response = client.post("/usuarios/login/", json=payload)
	assert response.status_code == 200
	data = response.json()
	assert "access_token" in data

def test_usuario_me(client):
	payload = {
		"email": "armando@gmail.com",
		"senha": "12345678"
	}
	response = client.post("/usuarios/login/", json=payload)
	assert response.status_code == 200
	token = response.json()["access_token"]
	response_1 = client.get(
		"/usuarios/me/",
		headers={"Authorization": f"Bearer {token}"}
	)
	assert response_1.status_code == 200
	data_1 = response_1.json()
	assert data_1["email"] == "armando@gmail.com"

def test_wrong_token(client):

	token = "eyGfMg"
	response_1 = client.get(
		"/usuarios/me/",
		headers={"Authorization": f"Bearer {token}"}
	)
	assert response_1.status_code == 401

def test_login_error_senha(client):
	payload = {
		"email": "armando@gmail.com",
		"senha": "1234567"
	}
	response = client.post("/usuarios/login/", json=payload)
	assert response.status_code == 401
	data = response.json()
	assert data["detail"] == "Credenciais inválidas"

def test_login_error_email(client):
	payload = {
		"email": "parmando@gmail.com",
		"senha": "12345678"
	}
	response = client.post("/usuarios/login/", json=payload)
	assert response.status_code == 401
	data = response.json()
	assert data["detail"] == "Credenciais inválidas"

def test_wrong_delete(client):
	payload = {
		"email": "armando@gmail.com",
		"senha": "12345678"
	}
	response = client.post("/usuarios/login/", json=payload)
	assert response.status_code == 200
	token = "access_token"
	response_1 = client.delete("/usuarios/1",
		headers={"Authorization": f"Bearer {token}"}
	)
	assert response_1.status_code == 401

def test_delete_usuario(client):
	payload = {
		"email": "armando@gmail.com",
		"senha": "12345678"
	}
	response = client.post("/usuarios/login/", json=payload)
	assert response.status_code == 200
	token = response.json()["access_token"]
	response_1 = client.delete("/usuarios/1",
		headers={"Authorization": f"Bearer {token}"}
	)
	assert response_1.status_code == 204

def test_deleted_usuario(client):
	payload = {
		"email": "armando@gmail.com",
		"senha": "12345678"
	}
	response = client.post("/usuarios/login/", json=payload)
	assert response.status_code == 401