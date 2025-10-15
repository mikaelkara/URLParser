1. **Yazılım Dili**
    1. Python 3.10 veya daha yüksek bir sürüm kullanılmalıdır.
2. **Depo ve Dal Seçimi**
    1. GitHub ana deposunda çalışılması gerekmektedir.
    2. Ek dal (branch) oluşturulmamalıdır.
    3. Tüm yenilikler, güncellemeler ve düzenlemeler yalnızca ana depoda gerçekleştirilmelidir.
3. **Teknik Gereksinimler ve Kısıtlamalar**
    1. Kullanılacak kütüphane: Playwright
    2. Kullanılacak ortam: Google Colab
    3. Her URL için maksimum bekleme süresi 10 saniye olarak ayarlanmalıdır.
    4. Aynı URL'nin birden fazla kez taranmasını önlemek için bir kontrol mekanizması eklenmelidir.
4. **Görev Tanımı**
    1. URL Tespit Etme
        1. Belirtilen web sayfasındaki tüm URL'leri Python kullanılarak tespit et.
        2. Alt URL'leri Python kullanılarak tespit et.
    2. Tespit edilen URL'leri uygun bir veri yapısında (liste, dictionary vb.) sakla.
    3. URL Yapısını Görselleştirme
        1. Tespit edilen URL'leri yapılandırılmış bir biçimde gösteren bir dosya oluştur.
        2. Dosya formatı: sitemap, dizin listesi veya ağaç yapısı olabilir.
        3. Örnek:
            
            ```markdown
            https://example.com/
            ├── https://example.com/about
            │   ├── https://example.com/about/team
            │   └── https://example.com/about/contact
            ├── https://example.com/products
            │   ├── https://example.com/products/electronics
            │   │   ├── https://example.com/products/electronics/phones
            │   │   └── https://example.com/products/electronics/laptops
            │   └── https://example.com/products/clothing
            ├── https://example.com/blog
            │   ├── https://example.com/blog/2024
            │   └── https://example.com/blog/2025
            └── https://example.com/support
                ├── https://example.com/support/faq
                └── https://example.com/support/contact
            ```
            
    4. Veri Kaydetme
        1. Elde edilen verileri bir dosyaya kaydet.
        2. Desteklenen formatlar: JSON, CSV, TXT
        3. URL'leri tam formatında yaz (örnek: ana adres https://example.com/about ise, alt adres https://example.com/about/team şeklinde eksiksiz olarak belirt).
    5. Hata Yönetimi ve Loglama
        1. Hata yönetimi mekanizması entegre et.
        2. Loglama mekanizması entegre et.
5. **Beklenen Çıktılar ve Kriterler**
    1. Her bir farklı eylem için ayrı ve bağımsız Python fonksiyonu oluştur.
    2. Her bir farklı işlem için ayrı ve bağımsız Python fonksiyonu oluştur.
    3. Her bir farklı adım için ayrı ve bağımsız Python fonksiyonu oluştur.
    4. Her bir farklı özellik için ayrı ve bağımsız Python fonksiyonu oluştur.
6. **Performans ve Optimizasyon**
    1. Tarama Hızı Optimizasyonu
        1. Çoklu iş parçacığı (threading) kullanarak tarama hızını optimize et.
        2. Alternatif: Asenkron programlama (asyncio) kullanarak tarama hızını optimize et.
    2. Büyük web siteleri için derinlik sınırı belirle (maksimum 5 seviye).
    3. Tarama Engelleri Kontrolü
        1. Robots.txt dosyasını kontrol et.
        2. Rate limiting kontrolü yap.
        3. CAPTCHA kontrolü yap.
        4. IP yasaklama kontrolü yap.
        5. Bot Tespitini Önleme Teknikleri
            1. Kullanıcı aracısı (User-Agent) rotasyonu uygula.
            2. Rastgele gecikme süreleri (random delays) uygula.
            3. Oturum yönetimi uygula.
            4. IP rotasyonu uygula.
7. **Kod Yapısı ve Organizasyon**
    1. Tüm fonksiyonları modüler yapıda oluştur (her fonksiyon tek bir sorumluluğa sahip olmalı).
    2. Kod Dokümantasyonu
        1. Kod içerisinde açıklayıcı yorumlar (docstring) ekle.
        2. Yorumlar Türkçe dilinde olmalı.
    3. Değişken ve fonksiyon isimlendirmelerini anlamlı ve tutarlı yap.
