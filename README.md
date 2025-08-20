# Global AI Hub Python 202 Bootcamp Kütüphane Projesi

Bu proje, Python 202 Bootcamp'inde öğrenilen üç temel konuyu (OOP, Harici API Kullanımı, Kendi API'nizi FastAPI ile Yazma) birleştirerek somut bir ürün ortaya çıkarmayı amaçlamaktadır. Proje üç aşamadan oluşur ve her aşama bir önceki üzerine inşa edilir.

Amacımız, basit bir komut satırı uygulamasından başlayarak, onu harici verilerle zenginleştirmek ve son olarak bir web servisi haline getirmektir.

## Dosya Yapısı

```
Python202-Bootcamp/
├── asama1_oop_terminal.py      # Aşama 1: OOP Terminal Uygulaması
├── asama2_api_entegrasyonu.py  # Aşama 2: API Entegrasyonu
├── asama3_fastapi_web.py       # Aşama 3: FastAPI Web Servisi
├── requirements.txt            # Gerekli kütüphaneler
├── README.md                   # Bu dosya
├── screenshots/                # Ekran görüntüleri
└── testler/                    # Test dosyaları
    ├── test_asama1_oop_terminal.py
    ├── test_asama2_api_entegrasyonu.py
    └── test_asama3_fastapi_web.py
```

## Kurulum

Projeyi çalıştırmadan önce gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

## Aşama 1: OOP ile Terminalde Çalışan Kütüphane

### Amaç
Nesne Yönelimli Programlama (OOP) prensiplerini kullanarak modüler ve yönetilebilir bir konsol uygulaması oluşturmak.

### Özellikler
- **Book Sınıfı**: Her kitabı temsil eden sınıf (title, author, ISBN)
- **Library Sınıfı**: Kütüphane operasyonlarını yöneten sınıf
- **JSON Veri Saklama**: Veriler library.json dosyasında kalıcı olarak saklanır
- **Terminal Arayüzü**: Kullanıcı dostu menü sistemi
- **CRUD İşlemleri**: Kitap ekleme, silme, güncelleme, arama

### Çalıştırma
```bash
python asama1_oop_terminal.py
```

### Ekran Görüntüleri

### Ana Menü
---
![Aşama 1 Ana Menü](screenshots/asama1_menu.png)
### Kitap Ekleme
---
![Kitap Ekleme](screenshots/asama1_kitap_ekle.png)
### Kitapları Listeleme
---
![Kitapları Listeleme](screenshots/asama1_kitapları_listele.png)
### Menü Seçenekleri
1. Kitap Ekle
2. Kitap Sil
3. Kitap Güncelle
4. Kitap Ara
5. Tüm Kitapları Listele
6. Çıkış

### Test Etme
```bash
pytest testler/test_asama1_oop_terminal.py -v
```

## Aşama 2: Harici API ile Veri Zenginleştirme

### Amaç
Mevcut uygulamayı, bir harici API'ye bağlanarak daha akıllı ve kullanışlı hale getirmek. Kitap bilgilerini manuel girmek yerine, ISBN ile otomatik olarak çekmek.

### Özellikler
- **Open Library API Entegrasyonu**: ISBN ile otomatik kitap bilgisi çekme
- **httpx Kütüphanesi**: Async HTTP istekleri
- **Hata Yönetimi**: API bağlantı sorunları için güçlü hata yönetimi
- **JSON İşleme**: API cevaplarını parse etme

### Kullanılan API
- **Open Library Books API**: `https://openlibrary.org/isbn/{isbn}.json`
- Ücretsiz ve API anahtarı gerektirmez

### Çalıştırma
```bash
python asama2_api_entegrasyonu.py
```

### Ekran Görüntüleri

### API ile Kitap Ekleme
---
![API ile Kitap Ekleme](screenshots/asama2_api_kitap_ekle.png)
### Test Etme
```bash
pytest testler/test_asama2_api_entegrasyonu.py -v
```

## Aşama 3: FastAPI ile Kendi API'nizi Oluşturma

### Amaç
Kütüphane uygulamanızın mantığını bir web servisi haline getirerek, verilerinize bir web arayüzü (API) üzerinden erişim sağlamak.

### Özellikler
- **RESTful API**: Modern web standartlarına uygun API
- **Async/Await**: Performanslı asenkron işlemler
- **Pydantic Modelleri**: Veri validasyonu ve dokümantasyon
- **Otomatik Dokümantasyon**: Swagger UI ile interaktif API dokümantasyonu

### API Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/` | Ana sayfa bilgileri |
| GET | `/books` | Tüm kitapları listele |
| POST | `/books` | ISBN ile kitap ekle |
| GET | `/books/{isbn}` | Belirli kitabı getir |
| DELETE | `/books/{isbn}` | Kitap sil |
| GET | `/health` | Sistem sağlık kontrolü |

### Çalıştırma
```bash
python asama3_fastapi_web.py
```

Veya uvicorn ile:
```bash
uvicorn asama3_fastapi_web:app --reload
```

### Ekran Görüntüleri

### FastAPI Swagger Dokümantasyonu
---
![FastAPI Docs](screenshots/asama3_docs_sayfa.png)
### POST Endpoint Test
---
![POST Books](screenshots/asama3_post_kitap.png)
### GET Endpoint Test
---
![GET Books](screenshots/asama3_get_kitap.png)
### API Dokümantasyonu
Sunucu çalıştıktan sonra aşağıdaki adreslere gidebilirsiniz:
- **Interaktif Dokümantasyon**: http://localhost:8000/docs
- **Ana Sayfa**: http://localhost:8000
- **ReDoc Dokümantasyonu**: http://localhost:8000/redoc

### Test Etme
```bash
pytest testler/test_asama3_fastapi_web.py -v
```

## Test Dosyaları

Her aşama için ayrı test dosyaları hazırlanmıştır:

### Tüm Testleri Çalıştırma
```bash
pytest testler/ -v
```



### Belirli Aşama Testleri
```bash
# Aşama 1 testleri
pytest testler/test_asama1_oop_terminal.py -v

# Aşama 2 testleri  
pytest testler/test_asama2_api_entegrasyonu.py -v

# Aşama 3 testleri
pytest testler/test_asama3_fastapi_web.py -v
```

## Gereksinimler

### Python Sürümü
- Python 3.7+

### Bağımlılıklar
```
httpx==0.25.2          # API istekleri için
fastapi==0.104.1       # Web framework
uvicorn==0.24.0        # ASGI server
pydantic==2.5.0        # Veri validasyonu
pytest==7.4.3          # Test framework
pytest-asyncio==0.21.1 # Async test desteği
pytest-mock==3.12.0    # Mock desteği
```

## Kullanım Örnekleri

### Aşama 1 - Terminal Uygulaması
```bash
python asama1_oop_terminal.py
# Menüden seçim yaparak kitap işlemleri gerçekleştirin
```

### Aşama 2 - API Entegrasyonu
```bash
python asama2_api_entegrasyonu.py
# ISBN girerek otomatik kitap bilgisi çekme
```

### Aşama 3 - Web API
```bash
python asama3_fastapi_web.py
# Tarayıcıda http://localhost:8000/docs adresine gidin
```

#### API Kullanım Örnekleri

**Kitap Ekleme:**
```bash
curl -X POST "http://localhost:8000/books" \
     -H "Content-Type: application/json" \
     -d '{"isbn": "9780743273565"}'
```

**Kitapları Listeleme:**
```bash
curl "http://localhost:8000/books"
```

**Kitap Silme:**
```bash
curl -X DELETE "http://localhost:8000/books/9780743273565"
```

## Proje Özellikleri

### Teknik Özellikler
- **Nesne Yönelimli Programlama**: Temiz ve modüler kod yapısı
- **Asenkron Programlama**: Performanslı API çağrıları
- **Veri Kalıcılığı**: JSON dosya sistemi
- **Hata Yönetimi**: Güçlü exception handling
- **Test Coverage**: Kapsamlı unit testler

### Kullanılan Teknolojiler
- **Python 3.7+**
- **FastAPI**: Modern web framework
- **httpx**: Async HTTP client
- **Pydantic**: Veri validasyonu
- **pytest**: Test framework
- **JSON**: Veri saklama formatı
