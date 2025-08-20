import json
import os

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
    
    def kitap_ekle(self, book):

        for kitap in self.kitaplar:
            if kitap['isbn'] == book.isbn:
                return False, "Bu ISBN zaten mevcut!"
        
        self.kitaplar.append(book.to_dict())
        if self.verileri_kaydet():
            return True, "Kitap başarıyla eklendi!"
        else:
            return False, "Kaydetme hatası!"
    
    def kitap_sil(self, isbn):
        for i, kitap in enumerate(self.kitaplar):
            if kitap['isbn'] == isbn:
                del self.kitaplar[i]
                if self.verileri_kaydet():
                    return True, "Kitap başarıyla silindi!"
                else:
                    return False, "Kaydetme hatası!"
        return False, "Kitap bulunamadı!"
    
    def kitap_guncelle(self, isbn, yeni_title=None, yeni_author=None):
        for kitap in self.kitaplar:
            if kitap['isbn'] == isbn:
                if yeni_title:
                    kitap['title'] = yeni_title
                if yeni_author:
                    kitap['author'] = yeni_author
                if self.verileri_kaydet():
                    return True, "Kitap başarıyla güncellendi!"
                else:
                    return False, "Kaydetme hatası!"
        return False, "Kitap bulunamadı!"
    
    def kitap_ara(self, arama_terimi):
        bulunanlar = []
        for kitap in self.kitaplar:
            if (arama_terimi.lower() in kitap['title'].lower() or 
                arama_terimi.lower() in kitap['author'].lower() or 
                arama_terimi in kitap['isbn']):
                bulunanlar.append(kitap)
        return bulunanlar
    
    def tum_kitaplari_listele(self):
        return self.kitaplar

def menu_goster():
    print("\n" + "="*50)
    print("           KÜTÜPHANE YÖNETİM SİSTEMİ")
    print("="*50)
    print("1. Kitap Ekle")
    print("2. Kitap Sil")
    print("3. Kitap Güncelle")
    print("4. Kitap Ara")
    print("5. Tüm Kitapları Listele")
    print("6. Çıkış")
    print("="*50)

def main():
    kutuphane = Library()
    
    while True:
        menu_goster()
        
        try:
            secim = input("Seçiminizi yapın (1-6): ").strip()
            
            if secim == "1":

                print("\n--- Kitap Ekleme ---")
                title = input("Kitap başlığı: ").strip()
                author = input("Yazar adı: ").strip()
                isbn = input("ISBN: ").strip()
                
                if title and author and isbn:
                    book = Book(title, author, isbn)
                    basarili, mesaj = kutuphane.kitap_ekle(book)
                    print(f"\n{mesaj}")
                else:
                    print("\nTüm alanları doldurun!")
            
            elif secim == "2":

                print("\n--- Kitap Silme ---")
                isbn = input("Silinecek kitabın ISBN'i: ").strip()
                if isbn:
                    basarili, mesaj = kutuphane.kitap_sil(isbn)
                    print(f"\n{mesaj}")
                else:
                    print("\nISBN giriniz!")
            
            elif secim == "3":

                print("\n--- Kitap Güncelleme ---")
                isbn = input("Güncellenecek kitabın ISBN'i: ").strip()
                if isbn:
                    yeni_title = input("Yeni başlık (boş bırakabilirsiniz): ").strip()
                    yeni_author = input("Yeni yazar (boş bırakabilirsiniz): ").strip()
                    
                    if yeni_title or yeni_author:
                        basarili, mesaj = kutuphane.kitap_guncelle(isbn, yeni_title, yeni_author)
                        print(f"\n{mesaj}")
                    else:
                        print("\nEn az bir alan güncellenmelidir!")
                else:
                    print("\nISBN giriniz!")
            
            elif secim == "4":

                print("\n--- Kitap Arama ---")
                arama = input("Arama terimi (başlık, yazar veya ISBN): ").strip()
                if arama:
                    bulunanlar = kutuphane.kitap_ara(arama)
                    if bulunanlar:
                        print(f"\n{len(bulunanlar)} kitap bulundu:")
                        for i, kitap in enumerate(bulunanlar, 1):
                            print(f"{i}. {kitap['title']} - {kitap['author']} - {kitap['isbn']}")
                    else:
                        print("\nKitap bulunamadı!")
                else:
                    print("\nArama terimi giriniz!")
            
            elif secim == "5":

                print("\n--- Tüm Kitaplar ---")
                kitaplar = kutuphane.tum_kitaplari_listele()
                if kitaplar:
                    print(f"\nToplam {len(kitaplar)} kitap:")
                    for i, kitap in enumerate(kitaplar, 1):
                        print(f"{i}. {kitap['title']} - {kitap['author']} - {kitap['isbn']}")
                else:
                    print("\nKütüphanede hiç kitap yok!")
            
            elif secim == "6":
                print("\nProgram sonlandırılıyor...")
                break
            
            else:
                print("\nGeçersiz seçim! Lütfen 1-6 arasında bir sayı giriniz.")
        
        except KeyboardInterrupt:
            print("\n\nProgram kullanıcı tarafından sonlandırıldı.")
            break
        except Exception as e:
            print(f"\nBir hata oluştu: {e}")

if __name__ == "__main__":
    main()
