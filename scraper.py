import requests
import json
import os

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
url = "https://tiktok-api23.p.rapidapi.com/api/post/trending"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "tiktok-api23.p.rapidapi.com"
}

# 16 yerine biraz daha bol alalım ki kaydıracak çok videomuz olsun
querystring = {"count": "30"}

toplanan_postlar = []

print("TikTok 'Trending' radarı açıldı! Ana akım sömürülüyor...")

try:
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        veri = response.json()
        
        # Farklı API'lerin kutu yapılarına karşı geniş ağımız
        videolar = []
        if isinstance(veri, list):
            videolar = veri
        elif isinstance(veri, dict):
            videolar = veri.get('data', veri.get('itemList', veri.get('videos', [])))
            
        if not videolar:
            print("Uyarı: API başarılı oldu ama video listesi boş döndü. (Servis anlık yavaş olabilir)")
            
        for video in videolar:
            baslik = video.get('title') or video.get('desc') or "Trend Video"
            video_id = str(video.get('id') or video.get('video_id') or "")
            
            # Linki yakalamak için tüm ihtimalleri tarıyoruz
            video_url = ""
            
            # İhtimal 1: Link 'video' adında ayrı bir klasördeyse
            if 'video' in video and isinstance(video['video'], dict):
                vid = video['video']
                video_url = vid.get('playAddr') or vid.get('downloadAddr') or ""
                # Bazen liste olarak gelir
                if isinstance(video_url, list) and len(video_url) > 0:
                    video_url = video_url[0]
            
            # İhtimal 2: Link direkt ana dizindeyse
            if not video_url:
                video_url = video.get('playUrl') or video.get('play_url') or video.get('play') or video.get('video_url') or ""
                
            # Eğer geçerli bir link bulduysak ve http ile başlıyorsa listeye ekle
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

print(f"Av bitti! Toplam {len(toplanan_postlar)} trend video yakalandı.")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(toplanan_postlar, f, ensure_ascii=False, indent=4)
