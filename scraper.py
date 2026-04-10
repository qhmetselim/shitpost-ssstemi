import requests
import json
import os

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
url = "https://tiktok-scraper7.p.rapidapi.com/feed/search"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "tiktok-scraper7.p.rapidapi.com"
}

# API'nin boş dönmemesi için kelimeleri en popüler ve garanti olanlarla değiştirdik!
keywords = ["komik", "mizah", "keşfet"]
toplanan_postlar = []

print("TikTok Türkiye Avı Başlıyor...")

for kelime in keywords:
    print(f"Aranıyor: {kelime}...")
    
    querystring = {
        "keywords": kelime,
        "region": "tr",
        "count": "15",
        "cursor": "0",
        "publish_time": "0",
        "sort_type": "0"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            veri = response.json()
            
            # Senin gönderdiğin çıktıya göre sistemi tam 'videos' klasörüne kitledik
            videolar = veri.get('videos', [])
            
            if not videolar:
                print(f"Uyarı: '{kelime}' kelimesi için sonuç bulunamadı.")
                continue
            
            for video in videolar:
                baslik = video.get('title') or video.get('desc') or "TikTok Videosu"
                video_id = str(video.get('video_id') or video.get('id') or "")
                
                # Bu API genelde 'play' veya 'wmplay' olarak verir
                video_url = video.get('play') or video.get('play_url') or video.get('wmplay') or ""
                
                # Link geçerliyse listeye ekle
                if video_url and "http" in video_url:
                    post_verisi = {
                        "id": video_id,
                        "title": baslik,
                        "url": video_url,
                        "platform": "TikTok",
                        "keyword": kelime
                    }
                    toplanan_postlar.append(post_verisi)
                    
        else:
            print(f"Hata ({kelime}): Kod {response.status_code}")
            
    except Exception as e:
        print(f"Sistemsel Hata ({kelime}): {e}")

print(f"TikTok Avı bitti! Toplam {len(toplanan_postlar)} video bulundu.")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(toplanan_postlar, f, ensure_ascii=False, indent=4)
