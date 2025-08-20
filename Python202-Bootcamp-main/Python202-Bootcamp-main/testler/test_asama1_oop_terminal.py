import pytest
import os
from asama1_oop_terminal import Book, Library

TEST_FILE = "test_lib.json"

@pytest.fixture
def lib():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    lib = Library(TEST_FILE)
    yield lib
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_book():
    book = Book("Test", "Author", "123")
    assert book.title == "Test"
    assert book.to_dict()["isbn"] == "123"

def test_add_book(lib):
    book = Book("Test", "Author", "123")
    success, _ = lib.kitap_ekle(book)
    assert success == True
    assert len(lib.kitaplar) == 1

def test_duplicate_book(lib):
    book = Book("Test", "Author", "123")
    lib.kitap_ekle(book)
    success, _ = lib.kitap_ekle(book)
    assert success == False

def test_remove_book(lib):
    book = Book("Test", "Author", "123")
    lib.kitap_ekle(book)
    success, _ = lib.kitap_sil("123")
    assert success == True
    assert len(lib.kitaplar) == 0

def test_search_book(lib):
    book = Book("Python", "Author", "123")
    lib.kitap_ekle(book)
    results = lib.kitap_ara("Python")
    assert len(results) == 1