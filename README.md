# 🚀 Django Mini-Blog & IGN Web Scraper

Bu proje, Django'nun temellerini öğrenmek amacıyla başlatılmış bir mini-blog uygulamasıdır. Proje, zamanla Django'nun gelişmiş özelliklerini (Kullanıcı Yönetimi, `ForeignKey` ilişkileri) ve harici kütüphaneleri (`Selenium`, `BeautifulSoup`) kullanarak IGN gibi modern web sitelerinden otomatik oyun incelemeleri çeken bir web scraper'a (veri kazıyıcı) dönüşmüştür.

## ✨ Temel Özellikler

* 📰 **Otomatik Veri Kazıma:** IGN'in oyun incelemeleri sayfasından (`/reviews/games`) "sonsuz kaydırma" (infinite scroll) özelliğini taklit ederek (`Selenium`) veri çeken özel bir yönetim komutu.
* 🔐 **Tam Kullanıcı Yönetimi:** Django'nun `auth` sistemi ile tam kullanıcı (Kayıt Ol, Giriş Yap, Çıkış Yap) ve yetkilendirme (sadece yazarın düzenleyebilmesi/silebilmesini sağlayan) entegrasyonu.
* 🔗 **İlişkisel Veritabanı:** Yazıların (`Post`) ve Kullanıcıların (`User`) `ForeignKey` ile birbirine bağlanması. Her yazının bir "sahibi" (yazarı) vardır.
* 📝 **Tam CRUD Fonksiyonelliği:** Kullanıcıların kendi blog yazılarını oluşturması, okuması, güncellemesi ve silmesi (Create, Read, Update, Delete).
* 🗄️ **PostgreSQL Entegrasyonu:** Geliştirme ortamında SQLite yerine güçlü PostgreSQL veritabanı kullanılmıştır.

---

## 🛠️ Kullanılan Teknolojiler

* **Backend:** Django
* **Veritabanı:** PostgreSQL
* **Web Scraping (Veri Kazıma):**
    * Selenium (JavaScript-yoğun sitelerle başa çıkmak için)
    * BeautifulSoup4 (HTML parçalama için)
* **Veritabanı Bağlayıcısı:** psycopg2-binary
* **Python Kütüphaneleri:** requests
