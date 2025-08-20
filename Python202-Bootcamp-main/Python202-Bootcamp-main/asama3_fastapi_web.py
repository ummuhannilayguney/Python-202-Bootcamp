import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import uvicorn


class BookRequest(BaseModel):
    isbn: str

class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str


app = FastAPI(
    title="Kütüphane API",
    description="Global AI Hub Python 202 Bootcamp Projesi - Aşama 3",
    version="1.0.0"
)

class LibraryAPI:
    
    def __init__(self, dosya_adi="library.json"):
        self.dosya_adi = dosya_adi
    
    def verileri_yukle(self):
        if os.path.exists(self.dosya_adi):
            try:
                with open(self.dosya_adi, 'r', encoding='utf-8') as dosya:
                    return json.load(dosya)
            except:
                return []
        return []
    
    def verileri_kaydet(self, kitaplar):
        try:
            with open(self.dosya_adi, 'w', encoding='utf-8') as dosya:
                json.dump(kitaplar, dosya, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    async def isbn_ile_kitap_bilgisi_al(self, isbn):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
                response = await client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    book_key = f"ISBN:{isbn}"
                    
                    if book_key in data:
                        book_info = data[book_key]
                        title = book_info.get('title', 'Bilinmeyen Başlık')
                        
                        author = "Bilinmeyen Yazar"
                        if 'authors' in book_info and book_info['authors']:
                            author = book_info['authors'][0].get('name', 'Bilinmeyen Yazar')
                        
                        return {"title": title, "author": author, "isbn": isbn}
                    else:
                        return None
                else:
                    return None
        except:
            return None


library_api = LibraryAPI()

@app.get("/")
async def ana_sayfa():
    return {
        "message": "Kütüphane API'sine Hoş Geldiniz!",
        "version": "1.0.0",
        "endpoints": [
            "GET /books - Tüm kitapları listele",
            "POST /books - ISBN ile kitap ekle",
            "GET /books/{isbn} - Belirli kitabı getir",
            "DELETE /books/{isbn} - Kitap sil"
        ]
    }

@app.get("/books")
async def kitaplari_listele():
    kitaplar = library_api.verileri_yukle()
    return {"kitaplar": kitaplar, "toplam": len(kitaplar)}

@app.post("/books")
async def kitap_ekle(book_request: BookRequest):
    isbn = book_request.isbn
    kitaplar = library_api.verileri_yukle()
    

    for kitap in kitaplar:
        if kitap['isbn'] == isbn:
            raise HTTPException(status_code=400, detail="Bu ISBN zaten mevcut!")
    

    kitap_bilgisi = await library_api.isbn_ile_kitap_bilgisi_al(isbn)
    
    if kitap_bilgisi:
        kitaplar.append(kitap_bilgisi)
        if library_api.verileri_kaydet(kitaplar):
            return {"message": "Kitap başarıyla eklendi!", "kitap": kitap_bilgisi}
        else:
            raise HTTPException(status_code=500, detail="Kaydetme hatası!")
    else:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı!")

@app.get("/books/{isbn}")
async def kitap_getir(isbn: str):
    kitaplar = library_api.verileri_yukle()
    
    for kitap in kitaplar:
        if kitap['isbn'] == isbn:
            return kitap
    
    raise HTTPException(status_code=404, detail="Kitap bulunamadı!")

@app.delete("/books/{isbn}")
async def kitap_sil(isbn: str):
    kitaplar = library_api.verileri_yukle()
    
    for i, kitap in enumerate(kitaplar):
        if kitap['isbn'] == isbn:
            silinen_kitap = kitaplar.pop(i)
            if library_api.verileri_kaydet(kitaplar):
                return {"message": "Kitap silindi!", "silinen_kitap": silinen_kitap}
            else:
                raise HTTPException(status_code=500, detail="Kaydetme hatası!")
    
    raise HTTPException(status_code=404, detail="Kitap bulunamadı!")

@app.get("/health")
async def saglik_kontrolu():
    return {"status": "OK", "message": "API çalışıyor"}

if __name__ == "__main__":
    print("FastAPI sunucusu başlatılıyor...")
    print("API Dokümantasyonu: http://localhost:8000/docs")
    print("Ana Sayfa: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
