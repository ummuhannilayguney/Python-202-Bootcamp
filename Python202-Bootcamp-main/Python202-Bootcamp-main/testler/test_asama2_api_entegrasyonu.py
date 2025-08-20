import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from asama2_api_entegrasyonu import Book, Library

@pytest.mark.asyncio
async def test_api_success(tmp_path):
    file = tmp_path / "lib.json"
    lib = Library(str(file))
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_context = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_context
        
        book_resp = MagicMock()
        book_resp.status_code = 200
        book_resp.json.return_value = {"title": "Test Book", "authors": [{"key": "/auth/123"}]}
        
        auth_resp = MagicMock()
        auth_resp.status_code = 200
        auth_resp.json.return_value = {"name": "Test Author"}
        
        mock_context.get.side_effect = [book_resp, auth_resp]
        
        success, result = await lib.isbn_ile_kitap_bilgisi_al("123")
        assert success == True
        assert result.title == "Test Book"

@pytest.mark.asyncio
async def test_add_book_success(tmp_path):
    file = tmp_path / "lib.json"
    lib = Library(str(file))
    
    with patch.object(lib, 'isbn_ile_kitap_bilgisi_al') as mock_api:
        mock_api.return_value = (True, Book("Test", "Author", "123"))
        success, _ = await lib.isbn_ile_kitap_ekle("123")
        assert success == True
        assert len(lib.kitaplar) == 1

@pytest.mark.asyncio
async def test_add_duplicate(tmp_path):
    file = tmp_path / "lib.json"
    lib = Library(str(file))
    lib.kitaplar = [{"title": "Test", "author": "Author", "isbn": "123"}]
    
    success, _ = await lib.isbn_ile_kitap_ekle("123")
    assert success == False

def test_remove_book(tmp_path):
    file = tmp_path / "lib.json"
    lib = Library(str(file))
    lib.kitaplar = [{"title": "Test", "author": "Author", "isbn": "123"}]
    
    success, _ = lib.kitap_sil("123")
    assert success == True
    assert len(lib.kitaplar) == 0