from fastapi.testclient import TestClient
from unittest.mock import patch
from asama3_fastapi_web import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["version"] == "1.0.0"

def test_get_books_empty(tmp_path):
    file = tmp_path / "lib.json"
    with patch('asama3_fastapi_web.library_api.dosya_adi', str(file)):
        response = client.get("/books")
        assert response.status_code == 200
        assert response.json()["toplam"] == 0

def test_add_book(tmp_path):
    file = tmp_path / "lib.json"
    with patch('asama3_fastapi_web.library_api.dosya_adi', str(file)):
        with patch('asama3_fastapi_web.library_api.isbn_ile_kitap_bilgisi_al') as mock:
            mock.return_value = {"title": "Test", "author": "Author", "isbn": "123"}
            response = client.post("/books", json={"isbn": "123"})
            assert response.status_code == 200

def test_add_duplicate(tmp_path):
    file = tmp_path / "lib.json"
    with patch('asama3_fastapi_web.library_api.dosya_adi', str(file)):
        with patch('asama3_fastapi_web.library_api.isbn_ile_kitap_bilgisi_al') as mock:
            mock.return_value = {"title": "Test", "author": "Author", "isbn": "123"}
            client.post("/books", json={"isbn": "123"})
            response = client.post("/books", json={"isbn": "123"})
            assert response.status_code == 400

def test_get_book(tmp_path):
    file = tmp_path / "lib.json"
    with patch('asama3_fastapi_web.library_api.dosya_adi', str(file)):
        with patch('asama3_fastapi_web.library_api.isbn_ile_kitap_bilgisi_al') as mock:
            mock.return_value = {"title": "Test", "author": "Author", "isbn": "123"}
            client.post("/books", json={"isbn": "123"})
            response = client.get("/books/123")
            assert response.status_code == 200

def test_delete_book(tmp_path):
    file = tmp_path / "lib.json"
    with patch('asama3_fastapi_web.library_api.dosya_adi', str(file)):
        with patch('asama3_fastapi_web.library_api.isbn_ile_kitap_bilgisi_al') as mock:
            mock.return_value = {"title": "Test", "author": "Author", "isbn": "123"}
            client.post("/books", json={"isbn": "123"})
            response = client.delete("/books/123")
            assert response.status_code == 200

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"