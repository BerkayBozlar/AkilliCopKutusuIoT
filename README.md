# Akıllı Şehir Kontrol Merkezi: IoT Tabanlı Çöp Kutusu Takip Sistemi

Bu proje, Akıllı Şehir (Smart City) konsepti kapsamında sokaklarda bulunan çöp kutularının doluluk oranlarını ve durumlarını anlık olarak takip edebilen, merkezi ve bulut tabanlı bir IoT (Nesnelerin İnterneti) altyapısıdır. Uç cihazlardan (Edge Devices) gelen telemetri verilerinin buluta taşınması ve gerçek zamanlı bir kontrol panelinde görselleştirilmesi hedeflenmiştir.

## Proje Amacı
Sistem, Python ile geliştirilen ve 10 farklı çöp kutusunu eşzamanlı simüle eden bir sensör ağına sahiptir. Üretilen doluluk verileri, kurumsal güvenlik duvarlarını (Firewall) aşabilmek adına ALPN protokolü kullanılarak standart web portu (Port 443) üzerinden **AWS IoT Core** servisine aktarılır. Buluta ulaşan veriler Amazon DynamoDB NoSQL veri tabanında depolanır ve doluluk oranı %85'i aştığı anda asenkron web panelinde "Kritik (BOŞALTILMALI)" şeklinde kırmızı alarm üretir.

## Kullanılan Teknolojiler
Bu sistem, IoT sensörlerinden son kullanıcı arayüzüne kadar uçtan uca güvenli bir bulut veri hattı (Data Pipeline) sunar:
* **Backend:** Python & Flask (Web Sunucusu ve API)
* **IoT & İletişim:** AWS IoT Core, Paho-MQTT (X.509 Kriptografik Sertifikalar, mTLS)
* **Bulut Veri Tabanı:** Amazon DynamoDB (Zaman damgalı NoSQL telemetri depolama)
* **Frontend:** HTML5, CSS3, JavaScript (AJAX ile sayfa yenilenmeden asenkron veri akışı)
* **AWS SDK:** Boto3 (Python ile AWS servisleri arası yetkilendirilmiş erişim)

## Kurulum ve Çalıştırma

**1. Depoyu Klonlayın:**
```bash
git clone [https://github.com/BerkayBozlar/AkilliCopKutusuIoT.git](https://github.com/BerkayBozlar/AkilliCopKutusuIoT.git)
cd AkilliCopKutusuIoT
```

**2. Gerekli Kütüphaneleri Yükleyin:**
```bash
pip install paho-mqtt boto3 flask python-dotenv
```

**3. AWS IoT Sertifikalarını Ekleyin:**
AWS IoT Core üzerinden oluşturduğunuz cihaza ait sertifika dosyalarını (`AmazonRootCA1.pem`, `...-certificate.pem.crt`, `...-private.pem.key`) proje dizinine taşıyın. **(Güvenlik Notu: Bu dosyaları asla GitHub'a yüklemeyin.)** `sensor.py` içerisindeki `AWS_ENDPOINT` ve sertifika yollarını kendi dosyalarınıza göre güncelleyin.

**4. Çevre Değişkenlerini Ayarlayın:**
Proje dizininde bir `.env` dosyası oluşturarak AWS IAM kimlik bilgilerinizi girin:
```env
AWS_ACCESS_KEY_ID=kendi_access_keyini_gir
AWS_SECRET_ACCESS_KEY=kendi_secret_keyini_gir
AWS_REGION=us-east-1
```

**5. Sensör Simülasyonunu ve Sunucuyu Başlatın:**
Proje iki ayaklı çalışmaktadır. İki ayrı terminal penceresi açın.

İlk terminalde IoT cihaz filosunu simüle etmek ve veri üretmek için:
```bash
python sensor.py
```

İkinci terminalde web yönetim panelini ayağa kaldırmak için:
```bash
python app.py
```

Tarayıcınızda `http://127.0.0.1:5000` adresine giderek asenkron veri akan Akıllı Şehir kontrol panelini canlı olarak izleyebilirsiniz.
