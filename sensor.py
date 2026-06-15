import os
import time
import json
import random
import ssl
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion # Yeni sürüm için eklendi

# --- 1. DEĞİŞTİRİLECEK KISIM: AWS ENDPOINT ---
AWS_ENDPOINT = "acmtpuzwx915x-ats.iot.us-east-1.amazonaws.com"

# Cihaz ve Konu (Topic) Ayarları
CLIENT_ID = "AkilliCopKutusu_01"
TOPIC = "sehir/copkutusu/veri"

# --- 2. DEĞİŞTİRİLECEK KISIM: SERTİFİKA İSİMLERİ ---
PATH_TO_ROOT_CA = "AmazonRootCA1.pem"
PATH_TO_CERT = "41b64223ccf0957afd8dd1a54fe46c2d640e96ea041516c8baf7e45a12a7830c-certificate.pem.crt" # Kendi indirdiğin crt dosyasının tam adı
PATH_TO_KEY = "41b64223ccf0957afd8dd1a54fe46c2d640e96ea041516c8baf7e45a12a7830c-private.pem.key "      # Kendi indirdiğin key dosyasının tam adı

# Dosyaların tam yolunu otomatik bulma (Klasör hatasını engeller)
Mevcut_Klasor = os.path.dirname(os.path.abspath(__file__))
root_ca_path = os.path.join(Mevcut_Klasor, PATH_TO_ROOT_CA)
cert_path = os.path.join(Mevcut_Klasor, PATH_TO_CERT)
key_path = os.path.join(Mevcut_Klasor, PATH_TO_KEY)

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("✅ AWS IoT Core'a başarıyla bağlanıldı!")
    else:
        print(f"❌ Bağlantı hatası! Kod: {rc}")

# Yeni V2 API standardıyla MQTT İstemcisini oluştur (Uyarıyı çözer)
client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
client.on_connect = on_connect

# TLS/SSL Güvenlik ayarları (ALPN ile 443 portu üzerinden güvenlik duvarını aşıyoruz)
client.tls_set(ca_certs=root_ca_path,
               certfile=cert_path,
               keyfile=key_path,
               tls_version=ssl.PROTOCOL_TLSv1_2,
               alpn_protocols=["x-amzn-mqtt-ca"]) # <-- GİZLİ SİLAH: ALPN EKLENDİ

# AWS'ye bağlan (Port 8883 yerine standart 443 kullanıyoruz)
print("⏳ AWS'ye bağlanılıyor (Port 443 ALPN Bypass), lütfen bekleyin...")
client.connect(AWS_ENDPOINT, 443, 60) # <-- PORT 443 OLARAK DEĞİŞTİ
client.loop_start()

print("🚀 Sensör simülasyonu başlatıldı. Veriler gönderiliyor (Durdurmak için Ctrl+C)...")

mevcut_doluluk = 0 # Çöp kutusu boş başlıyor
try:
    while True:
        # 1 ile 10 arasında rastgele bir çöp kutusu ID'si oluştur
        kutu_no = random.randint(1, 10)
        aktif_cihaz = f"AkilliCopKutusu_{kutu_no:02d}"
        
        # O anki çöp kutusu için rastgele doluluk oranı
        doluluk = random.randint(10, 100)
        
        mesaj = {
            "cihaz_id": aktif_cihaz,
            "doluluk_orani": doluluk,
            "zaman_damgasi": int(time.time()),
            "durum": "Kritik (BOŞALTILMALI)" if doluluk > 85 else "Normal"
        }
        
        client.publish(TOPIC, json.dumps(mesaj), qos=1)
        print(f"📡 Veri Gönderildi: {mesaj}")
        
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\n🛑 Simülasyon durduruldu.")
    client.loop_stop()
    client.disconnect()