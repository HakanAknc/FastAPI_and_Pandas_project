from fastapi import (FastAPI, Query)   # FastAPI kütüphanesini import etim    # TODO Yedek proje
import pandas as pd           # FastAPI kütüphanesini import etim      -- uvicorn main:app --reload
import uuid
import func_ted as fnc


app = FastAPI()     # FastAPI tanımladım

# Dosya yolları
excel_file_path = "kisiler.xlsx"             # Excel dosyasının yolunu belirtim
csv_file_path = "persons.csv"                 # CSV dosyasının yolunu belirtim

excel_file = "kitaplar.xlsx"   
csv_file = "books.csv"   

exel_sold = "satilanlar.xlsx"
csv_sold = "bookssold.csv"


@app.get("/excel_to_csv")
async def to_csv(excel_name : str = Query(..., description='Donusturulecek excel dosya adi'), csv_name: str = Query(...)):
    result = fnc.excel_to_csv(excel_file=excel_name,
                              csv_file=csv_name)

    return result


# Veri çerçeveleri (DataFrames) oluşturma
kisiler_df = pd.read_csv(csv_file_path)
kitaplar_df = pd.read_csv(csv_file)
satilanlar_df = pd.read_csv(csv_sold)


# person_id_counter = kisiler_df["kisi_id"].max() + 1 if not kisiler_df.empty else 1
# kitap_id_counter = kitaplar_df["kitap_id"].max() + 1 if not kitaplar_df.empty else 1
# satilan_id_counter = satilanlar_df["tablo_id"].max() + 1 if not satilanlar_df.empty else 1


# Benzersiz kimlik (UUID) üretme işlemi
person_id_counter = str(uuid.uuid4()) if kisiler_df.empty else kisiler_df["kisi_id"].max() + 1
kitap_id_counter = str(uuid.uuid4()) if kitaplar_df.empty else kitaplar_df["kitap_id"].max() + 1
satilan_id_counter = str(uuid.uuid4()) if satilanlar_df.empty else satilanlar_df["tablo_id"].max() + 1


# # Sonuçları görüntüleme
# print("person_id_counter:", person_id_counter)
# print("kitap_id_counter:", kitap_id_counter)
# print("satilan_id_counter:", satilan_id_counter)



# Yeni verileri CSV'ye ekleme fonksiyonu
async def append_to_csv(dataframe, csv_path):        # verileri CSV dosyasına kaydeder.
    dataframe.to_csv(csv_path, index=False)



# 1. Tablo = Kişiler
@app.get("/kisiler/")    # "Kişiler" tablosundaki tüm kişilerin bir listesini alır.    
async def get_kisiler():
    kisiler_df = pd.read_csv(csv_file_path)   # Güncelleme
    return kisiler_df.to_dict(orient="records")


@app.get("/kisiler/{kisi_id}")       #"Kişiler" tablosundaki belirli bir kişiyi ID'sine göre alır.
async def get_kisi_by_id(kisi_id: int):
    kisiler_df = pd.read_csv(csv_file_path) # TODO
    kisi = kisiler_df[kisiler_df["kisi_id"] == kisi_id].to_dict(orient="records")
    if not kisi:
        return {"error": "Belirtilen ID'ye sahip bir kişi bulunamadı."}
    return kisi[0]       # orient parametresi ile sözlük formatında döndürüyoruz.


@app.post("/kisiler/")     # Verilen verileri (ad, soyad, tel ve bütçe) kullanarak yeni bir kişi ekliyoruz.
async def add_kisi(ad: str, soyad: str, tel: str, bütçe: float):
    if len(tel.strip()) != 10 or not tel.isdigit():
        return {"error": "Telefon numarası 10 rakamdan oluşmalıdır."}
    
    kisiler_df = pd.read_csv(csv_file_path)  # Her seferinde veriyi güncel şekilde okuyoruz

    existing_person = kisiler_df[kisiler_df["tel"] == tel]
    if not existing_person.empty:
        print(existing_person)
        return {"message": "Bu telefon numarası zaten kayıtlıdır."}

    # if kisiler_df[kisiler_df["tel"] == tel].shape[0] > 0:
    #     return {"error": "Bu tel'e sahip biri zaten kayıtlıdır. Başka tel giriniz."}

    new_person_data = pd.DataFrame({"kisi_id": [person_id_counter], "ad": [ad], "soyad": [soyad], "tel": [tel], "bütçe": [bütçe]})
    
    # Eğer "persons.csv" dosyası boş ise, yeni veriyi kullanarak veri çerçevesi oluşturuyorum.
    if pd.read_csv(csv_file_path).empty:
        updated_data_csv = new_person_data
    else:
         # Eğer "persons.csv" dosyası dolu ise, mevcut veri çerçevesini okuyor ve yeni veriyi ekleyerek güncellenmiş bir veri çerçevesi oluştur.
        existing_data_csv = pd.read_csv(csv_file_path)
        updated_data_csv = pd.concat([existing_data_csv, new_person_data], ignore_index=True)

    updated_data_csv.to_csv(csv_file_path, index=False)      # "persons.csv" dosyasına kaydet.
    return {"message": "Veriler CSV dosyanıza başarıyla kaydedildi."}



@app.get("/kisiler_soyad/{soyad}")
async def get_kisiler_by_soyad(soyad: str):
    kisiler_df = pd.read_csv(csv_file_path)  # kisiler_df güncelleme
    kisiler_soyad = kisiler_df[kisiler_df["soyad"] == soyad].to_dict(orient="records")
    
    if not kisiler_soyad:
        return {"message": f"Soyadı '{soyad}' olan kişi kayıtlarda yok. Kimi arıyorsan adam akıllı öğren de gel :)"}
    
    return kisiler_soyad



# 2. Tablo = Kitaplar
@app.get("/kitaplar/")      # "Kitaplar" tablosundaki tüm kitapların bir listesini alır.
async def get_kitaplar():
    kitaplar_df = pd.read_csv(csv_file) 
    return kitaplar_df.to_dict(orient="records")


@app.get("/kitaplar/{kitap_kategori}")     # "Kitaplar" tablosundaki belirli bir kategoriye ait kitapları alır.
async def get_kitap_by_ktr(kitap_kategori: str):
    kitaplar_df = pd.read_csv(csv_file) # TODO
    kitaplar_in_kategori = kitaplar_df[kitaplar_df["kitap_kategori"] == kitap_kategori]   # Belirtilen kategoriye ait tüm kitapları alalım
    
    if kitaplar_in_kategori.empty:   # Eğer belirtilen kategoride hiç kitap yoksa hata döndürelim
        return {"error": "Belirtilen kategoride kitap bulunamadı."}
    
    sorted_kitaplar = kitaplar_in_kategori.sort_values(by="kitap_ad")  # Kitapları sıralayalım ve liste olarak döndürelim
    return sorted_kitaplar.to_dict(orient="records")



@app.post("/kitaplar/")    #  Verilen verileri (kitap_ad, kitap_kategori, kitap_ücret ve kitap_stok) kullanarak yeni bir kitap ekler.
async def kitap_kayitlari(kitap_ad: str, kitap_kategori: str, kitap_ücret: int, kitap_stok: int):
    kitaplar_df = pd.read_csv(csv_file)
    
    # Aynı "kitap_ad"a sahip kitabın zaten var olup olmadığını kontrol ediyorum
    if kitaplar_df[kitaplar_df["kitap_ad"] == kitap_ad].shape[0] > 0:
        return {"error": "Bu kitap zaten kayıtlıdır."}
    
    veri = pd.DataFrame({"kitap_id": [kitap_id_counter], "kitap_ad": [kitap_ad], "kitap_kategori": [kitap_kategori], "kitap_ücret": [kitap_ücret], "kitap_stok": [kitap_stok]})

    if kitaplar_df.empty:
        updated_veri_csv = veri
    else:
        existing_veri_csv = kitaplar_df
        updated_veri_csv = pd.concat([existing_veri_csv, veri], ignore_index=True)

    updated_veri_csv.to_csv(csv_file, index=False)
    return {"message": "Girdiğiniz kitap CSV dosyanıza başarıyla kaydedildi."}


@app.get("/kitap_al/")        # Stok ve bütçe kontrolü
async def kitap_al(kisi_id: int, kitap_id: int):
    kitaplar_df = pd.read_csv(csv_file)         # TODO
    kisiler_df = pd.read_csv(csv_file_path)     # TODO
    satilanlar_df = pd.read_csv(csv_sold) 
    
    kullanici = kisiler_df[kisiler_df["kisi_id"] == kisi_id]

    if kullanici.empty:
        return {"message": "Kullanıcı bulunamadı."}

    kitap = kitaplar_df[kitaplar_df["kitap_id"] == kitap_id]

    if kitap.empty:
        return {"message": "Kitap bulunamadı."}

    bakiye = kullanici["bütçe"].values[0]
    kitap_ücreti = kitap["kitap_ücret"].values[0]

    if bakiye >= kitap_ücreti:
        stok_sayisi = kitap["kitap_stok"].values[0]

        if stok_sayisi > 0:
            # Kullanıcının bu kitabı zaten satın alıp almadığını kontrol edin
            existing_sale = satilanlar_df[(satilanlar_df["kullanici_id"] == kisi_id) & (satilanlar_df["satilan_kitap_id"] == kitap_id)]
            if not existing_sale.empty:
                return {"message": f"{kisi_id} ID'li kullanıcı, {kitap_id} ID'li kitabı daha önce zaten aldınız."}

            tablo_id = satilan_id_counter   # benzersiz ID

            new_sale = pd.DataFrame({"tablo_id": [tablo_id], "satilan_kitap_id": [kitap_id], "kullanici_id": [kisi_id]})
            updated_sales_csv = pd.concat([satilanlar_df, new_sale], ignore_index=True)

            updated_sales_csv.to_csv(csv_sold, index=False)

            # Bakiye güncelleme
            kalan_bakiye = bakiye - kitap_ücreti
            kisiler_df.loc[kisiler_df["kisi_id"] == kisi_id, "bütçe"] = kalan_bakiye
            kisiler_df.to_csv(csv_file_path, index=False)

            # Stok güncelleme
            kitaplar_df.loc[kitaplar_df["kitap_id"] == kitap_id, "kitap_stok"] = stok_sayisi - 1
            kitaplar_df.to_csv(csv_file, index=False)

            return {"message": f"{kisi_id} ID'li kullanıcı, {kitap_id} ID'li kitabı aldınız. Bakiyenizde {kalan_bakiye:.2f} TL kaldı. Hayırlı olsun!"}
        else:
            return {"message": f"{kitap_id} ID'li kitap stokta kalmamıştır. Başka bir kitap seçiniz."}
    else:
        return {"message": "Bütçeniz yetersiz. Kitabı alamazsınız."}
    


# 3. Tablo = Satılan Kitaplar
@app.get("/satilan_kitaplar/")        # "Satılan Kitaplar" tablosundaki tüm satılan kitapların bir listesini alır.
async def get_satilan_kitaplar():
    satilanlar_df = pd.read_csv(csv_sold) # TODO
    return satilanlar_df.to_dict(orient="records")


@app.get("/stok_kontrol/{kitap_ad}")      # Verilen kitap adına (kitap_ad) göre "Kitaplar" tablosundaki stok durumunu kontrol eder.
async def check_stok(kitap_ad: str):
    kitaplar_df = pd.read_csv(csv_file) # TODO
    kitap_stok = kitaplar_df[kitaplar_df["kitap_ad"] == kitap_ad]["kitap_stok"]
    if kitap_stok.empty:
        return {"error": "Bu kitap mevcut değil."}
    else:
        return {"kitap_ad": kitap_ad, "kitap_stok": int(kitap_stok)}
    


@app.get("/satilan_kitaplar/{tablo_id}")
async def get_satilan_kitap_by_id(tablo_id: int):
    satilanlar_df = pd.read_csv(csv_sold) # TODO
    satilan_kitap = satilanlar_df[satilanlar_df["tablo_id"] == tablo_id]

    if satilan_kitap.empty:
        return {"message": "Belirtilen tablo_id bulunamadı."}

    kitap_id = satilan_kitap["satilan_kitap_id"].values[0]
    kullanici_id = satilan_kitap["kullanici_id"].values[0]

    kitap_df = pd.read_csv("books.csv")
    kitap = kitap_df[kitap_df["kitap_id"] == kitap_id]

    kisiler_df = pd.read_csv("persons.csv")
    kullanici = kisiler_df[kisiler_df["kisi_id"] == kullanici_id]

    if kitap.empty or kullanici.empty:
        return {"message": "İlgili kitap veya kullanıcı bulunamadı. Git kimi aramak istiyorsan adam akılı öğren öyle gel yürüüüü :)"}

    kitap_ad = kitap["kitap_ad"].values[0]
    ad = kullanici["ad"].values[0] 
    soyad = kullanici["soyad"].values[0] 
    tel = kullanici["tel"].values[0] 

    result = f"Ad: {ad}, Soyad: {soyad}, Tel: {tel}, Kitab adı: {kitap_ad}"
    return {"satilan_kitap_bilgileri": result}



@app.get("/kitap_satilan/{kitap_id}")
async def get_kitap_satilan(kitap_id: int):
    try:
        books_df = pd.read_csv(csv_file)
        sold_df = pd.read_csv(csv_sold)
        
        kitap = books_df[books_df["kitap_id"] == kitap_id]

        if kitap.empty:
            return {"message": "Belirtilen kitap_id bulunamadı."}

        kitap_ad = kitap["kitap_ad"].values[0]

        satilan_kitaplar = sold_df[sold_df["satilan_kitap_id"] == kitap_id]
        toplam_satilan = len(satilan_kitaplar)

        return {
            "kitap_ad": kitap_ad,
            "toplam_satilan": toplam_satilan
        }
    except Exception as error:
        return {"message": str(error)}
