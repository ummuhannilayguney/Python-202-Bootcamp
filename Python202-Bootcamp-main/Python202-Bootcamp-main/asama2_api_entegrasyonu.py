import json
import os
import httpx
import asyncio

class Book:
    
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn
        }
    
    def __str__(self):
        return f"Kitap: {self.title} - Yazar: {self.author} - ISBN: {self.isbn}"

class Library:
    
    def __init__(self, dosya_adi="library.json"):
        self.dosya_adi = dosya_adi
        self.kitaplar = self.verileri_yukle()
    
    def verileri_yukle(self):
        if os.path.exists(self.dosya_adi):
            try:
                with open(self.dosya_adi, 'r', encoding='utf-8') as dosya:
                    return json.load(dosya)
            except:
                return []
        return []
    
    def verileri_kaydet(self):
        try:
            with open(self.dosya_adi, 'w', encoding='utf-8') as dosya:
                json.dump(self.kitaplar, dosya, ensure_ascii=False, indent=2)
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
                        
                        return True, Book(title, author, isbn)
                    else:
                        return False, "Kitap bulunamadı!"
                else:
                    return False, "Kitap bulunamadı!"
        
        except httpx.TimeoutException:
            return False, "Bağlantı zaman aşımı!"
        except httpx.ConnectError:
            return False, "API'ye bağlanılamadı!"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    async def isbn_ile_kitap_ekle(self, isbn):

        for kitap in self.kitaplar:
            if kitap['isbn'] == isbn:
                return False, "Bu ISBN zaten mevcut!"
        

        basarili, sonuc = await self.isbn_ile_kitap_bilgisi_al(isbn)
        
        if basarili:
            self.kitaplar.append(sonuc.to_dict())
            if self.verileri_kaydet():
                return True, f"Kitap eklendi: {sonuc.title}"
            else:
                return False, "Kaydetme hatası!"
        else:
            return False, sonuc
    
    def kitap_sil(self, isbn):
        for i, kitap in enumerate(self.kitaplar):
            if kitap['isbn'] == isbn:
                del self.kitaplar[i]
                if self.verileri_kaydet():
                    return True, "Kitap silindi!"
                else:
                    return False, "Kaydetme hatası!"
        return False, "Kitap bulunamadı!"
    
    def kitaplari_listele(self):
        return self.kitaplar

def menu_goster():
    print("\n" + "="*50)
    print("     KÜTÜPHANE YÖNETİM SİSTEMİ - API ENTEGRASYONLU")
    print("="*50)
    print("1. ISBN ile Kitap Ekle (API)")
    print("2. Kitap Sil")
    print("3. Kitapları Listele")
    print("4. Çıkış")
    print("="*50)

async def main():
    kutuphane = Library()
    
    while True:
        menu_goster()
        
        try:
            secim = input("Seçiminizi yapın (1-4): ").strip()
            
            if secim == "1":

                print("\n--- ISBN ile Kitap Ekleme ---")
                isbn = input("ISBN giriniz: ").strip()
                
                if isbn:
                    print("API'den kitap bilgileri alınıyor...")
                    basarili, mesaj = await kutuphane.isbn_ile_kitap_ekle(isbn)
                    print(f"\n{mesaj}")
                else:
                    print("\nISBN giriniz!")
            
            elif secim == "2":

                print("\n--- Kitap Silme ---")
                kitaplar = kutuphane.kitaplari_listele()
                if kitaplar:
                    print("Mevcut kitaplar:")
                    for i, kitap in enumerate(kitaplar, 1):
                        print(f"{i}. {kitap['title']} - {kitap['author']} - {kitap['isbn']}")
                    
                    isbn = input("\nSilinecek kitabın ISBN'i: ").strip()
                    if isbn:
                        basarili, mesaj = kutuphane.kitap_sil(isbn)
                        print(f"\n{mesaj}")
                    else:
                        print("\nISBN giriniz!")
                else:
                    print("\nKütüphanede kitap yok!")
            
            elif secim == "3":

                print("\n--- Kitap Listesi ---")
                kitaplar = kutuphane.kitaplari_listele()
                if kitaplar:
                    print(f"Toplam {len(kitaplar)} kitap:")
                    for i, kitap in enumerate(kitaplar, 1):
                        print(f"{i}. {kitap['title']} - {kitap['author']} - {kitap['isbn']}")
                else:
                    print("Kütüphanede hiç kitap yok!")
            
            elif secim == "4":
                print("\nProgram sonlandırılıyor...")
                break
            
            else:
                print("\nGeçersiz seçim! Lütfen 1-4 arasında bir sayı giriniz.")
        
        except KeyboardInterrupt:
            print("\n\nProgram kullanıcı tarafından sonlandırıldı.")
            break
        except Exception as e:
            print(f"\nBir hata oluştu: {e}")

if __name__ == "__main__":
    asyncio.run(main())
