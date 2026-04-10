import requests
import json
import os

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
url = "https://tiktok-api23.p.rapidapi.com/api/post/trending"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "tiktok-api23.p.rapidapi.com"
}

# Vanaları açıyoruz: Tek seferde 100 video!
querystring = {"count": "100"}

toplanan_postlar = []

print("TikTok 'Trending' radarı açıldı! Hedef: 100 Video...")

try:
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        veri = response.json()
        
        # API'nin yapısına göre videoları bulma
        videolar = []
        if isinstance(veri, list):
            videolar = veri
        elif isinstance(veri, dict):
            videolar = veri.get('data', veri.get('itemList', veri.get('videos', [])))
            
        if not videolar:
            print("Uyarı: API başarılı oldu ama video listesi boş döndü.")
            
        for video in videolar:
            baslik = video.get('title') or video.get('desc') or "Trend Video"
            video_id = str(video.get('id') or video.get('video_id') or "")
            
            # Video linkini yakalama (Tüm ihtimalleri tarıyoruz)
            video_url = ""
            if 'video' in video and isinstance(video['video'], dict):
                vid = video['video']
                video_url = vid.get('playAddr') or vid.get('downloadAddr') or ""
                if isinstance(video_url, list) and len(video_url) > 0:
                    video_url = video_url[0]
            
            if not video_url:
                video_url = video.get('playUrl') or video.get('play_url') or video.get('play') or video.get('video_url') or ""
                
            # Eğer geçerli bir link bulduysak listeye ekle
            if video_url and isinstance(video_url, str) and "http" in video_url:
                post_verisi = {
                    "id": video_id,
                    "title": baslik,
                    "url": video_url,
                    "platform": "TikTok",
                    "keyword": "trending"
                }
                toplanan_postlar.append(post_verisi)
                
    else:
        print(f"Hata: API reddetti. Kod: {response.status_code}")
        
except Exception as e:
    print(f"Sistemsel Hata: {e}")

print(f"Yeni çekilen saf video sayısı: {len(toplanan_postlar)}")


# --- VERİTABANI GÜNCELLEME KISMI (Eskileri silmeden üstüne ekleme) ---

# 1. Eski dosyayı oku (varsa)
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        eski_postlar = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    eski_postlar = []

# 2. Yeni ve eski videoları birleştir
tum_postlar = eski_postlar + toplanan_postlar

# 3. Aynı videonun iki kez eklenmesini (kopyaları) engelle
# id değerine göre filtreleyerek benzersiz olanları tutuyoruz
benzersiz_postlar = {post['id']: post for post in tum_postlar}.values()
nihai_liste = list(benzersiz_postlar)

print(f"Veritabanı başarıyla güncellendi! Havuzda toplam {len(nihai_liste)} eşsiz video var.")

# 4. Hepsini geri kaydet
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(nihai_liste, f, ensure_ascii=False, indent=4)
