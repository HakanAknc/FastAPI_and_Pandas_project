# FastAPI_and_Pandas_project

# Verileri Yönetmek İçin FastAPI Web Uygulaması

Bu, CSV dosyalarında saklanan verileri yönetmek ve etkileşimde bulunmak için kullanılan bir FastAPI web uygulamasıdır. Excel dosyalarını CSV'ye dönüştürme, insanlarla ilgili verileri ("Kişiler" tablosu) alıp eklemek ve muhtemelen kitapla ilgili verileri işlemek gibi çeşitli işlemleri yapmanıza olanak tanır.

## Özellikler

- **Excel'den CSV'ye Dönüştürme**: Excel dosyalarını CSV formatına dönüştürme.

- **Kişi Verilerini Yönetme**: İsim, soyad, telefon numarası ve bütçe gibi bireylerle ilgili verileri eklemek, almak ve güncellemek.

- **Kitap Verileri Yönetimi** (isteğe bağlı): Uygulamanın kitapla ilgili verileri de işleyebildiği görünmektedir.

# Uç Noktalar (Endpoints)
/excel_to_csv: Excel dosyalarını CSV'ye dönüştürme.

/kisiler/: "Kişiler" tablosuyla ilgili verileri yönetme.

GET: Tüm kişilerin listesini alın.
GET /kisiler/{kisi_id}: ID'ye göre belirli bir kişiyi alın.
POST: Ad, soyad, telefon numarası ve bütçe ile yeni bir kişi ekleyin.
/kitaplar/ (isteğe bağlı): Kitapla ilgili verileri yönetme.

(Var ise geçerli uç noktalarını burada listeleyin)
/satilanlar/ (isteğe bağlı): Satılan ürün verilerini yönetme.

(Var ise geçerli uç noktalarını burada listeleyin)
# Veri Depolama
Kişi verileri persons.csv dosyasında saklanır.
Kitap verileri (varsa) books.csv dosyasında saklanır.
Satılan ürün verileri (varsa) bookssold.csv dosyasında saklanır.
Katkıda Bulunma
Katkılarınızı bekliyoruz! Bu projeye katkıda bulunmak istiyorsanız, lütfen aşağıdaki adımları izleyin:

# Depoyu çatallayın (forklayın).
Özellik veya hata düzeltmesi için yeni bir dal (branch) oluşturun: git checkout -b ozellik-adi.
Değişikliklerinizi yapın: git commit -m 'Yeni bir özellik ekle'.
Değişikliklerinizi kendi çatalınıza (fork) gönderin: git push origin ozellik-adi.
Ana depoya bir çekme isteği (pull request) gönderin.
