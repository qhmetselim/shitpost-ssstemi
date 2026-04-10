import requests
import json
import os

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
url = "https://tiktok-scraper7.p.rapidapi.com/feed/search"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "tiktok-scraper7.p.rapidapi.com"
}

# Türkiye TikTok'unda viral olan shitpost anahtar kelimeleri
keywords = ["shitpost türkiye", "shitposttc", "komik montaj"]
toplanan_postlar = []

print("Rota yeniden hesaplandı: TikTok Türkiye'nin karanlık sularına iniliyor...")

for kelime in keywords:
    print(f"Aranıyor: {kelime}...")
    
    # Senin bulduğun parametreleri Türkiye'ye (tr) uyarladık
    querystring = {
        "keywords": kelime,
        "region": "tr", # Türkiye videoları
        "count": "15",
        "cursor": "0",
        "publish_time": "0",
        "sort_type": "0"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            veri = response.json()
            
            # API'nin yapısına göre videoları bulma (Geniş ağ taktiği)
            videolar = []
            if isinstance(veri, dict):
                if 'data' in veri and isinstance(veri['data'], dict) and 'videos' in veri['data']:
                    videolar = veri['data']['videos']
                elif 'data' in veri and isinstance(veri['data'], list):
                    videolar = veri['data']
                elif 'aweme_list' in veri:
                    videolar = veri['aweme_list']
                elif 'itemList' in veri:
                    videolar = veri['itemList']
            
            for video in videolar:
                # Başlık
                baslik = video.get('title') or video.get('desc') or "TikTok Videosu"
                video_id = str(video.get('video_id') or video.get('aweme_id') or video.get('id') or "")
                
                # VİDEO LİNKİNİ YAKALAMA (Farklı TikTok API'lerinin ortak değişken isimleri)
                video_url = ""
                if 'play' in video and isinstance(video['play'], str):
                    video_url = video['play']
                elif 'play_url' in video and isinstance(video['play_url'], str):
                    video_url = video['play_url']
                elif 'playAddr' in video and isinstance(video['playAddr'], str):
                    video_url = video['playAddr']
                # Eğer link 'video' klasörünün içindeyse:
                elif 'video' in video and isinstance(video['video'], dict):
                    vid_obj = video['video']
                    if 'play_addr' in vid_obj and 'url_list' in vid_obj['play_addr']:
                        video_url = vid_obj['play_addr']['url_list'][0]
                    elif 'download_addr' in vid_obj and 'url_list' in vid_obj['download_addr']:
                        video_url = vid_obj['download_addr']['url_list'][0]
                
                # Eğer filigransız bulamazsa filigranlı (wmplay) alsın
                if not video_url and 'wmplay' in video:
                    video_url = video['wmplay']

                # Eğer geçerli bir link bulduysak listeye ekle
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
            print(f"Hata ({kelime}): API reddetti, Kod: {response.status_code}")
            
    except Exception as e:
        print(f"Sistemsel Hata ({kelime}): {e}")

print(f"TikTok Avı bitti! Toplam {len(toplanan_postlar)} video bulundu.")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(toplanan_postlar, f, ensure_ascii=False, indent=4)
