import requests
import json
import os

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')

url = "https://reddit34.p.rapidapi.com/getTopPostsBySubreddit"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "reddit34.p.rapidapi.com"
}

# İŞTE YENİ HEDEFLERİMİZ: İnternetin en büyük küresel video/shitpost merkezleri
subreddits = ['shitposting', 'dankvideos', 'discordVideos', 'Unexpected']
toplanan_postlar = []

print("Gölge Bot devrede, küresel okyanusa açılıyoruz...")

for sub in subreddits:
    print(f"Bölge taranıyor: {sub}...")
    
    # Küresel sayfalarda her gün binlerce post atıldığı için 'day' (son 24 saat) gayet yeterli
    querystring = {"subreddit": sub, "time": "day"}
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            veri = response.json()
            
            postlar = []
            if isinstance(veri, dict) and 'data' in veri and 'posts' in veri['data']:
                postlar = veri['data']['posts']
            
            if not postlar:
                print(f"Uyarı: API {sub} sayfası için 0 post döndürdü.")
                continue

            for post in postlar:
                video_url = post.get('video_url') or post.get('media_url') or post.get('url', '')
                
                # Sadece MP4 veya Video formatındaki içerikleri alıyoruz
                if post.get('isVideo') == True or '.mp4' in str(video_url).lower():
                    post_verisi = {
                        "id": post.get('id', 'Bilinmiyor'),
                        "title": post.get('title', 'Başlıksız'),
                        "url": video_url,
                        "score": post.get('upvotes', post.get('score', 0)),
                        "subreddit": sub
                    }
                    if post_verisi["url"]: 
                        toplanan_postlar.append(post_verisi)
                        
        else:
            print(f"Hata: {sub} okunamadı. Kod: {response.status_code}")
            
    except Exception as e:
        print(f"Sistemsel Hata ({sub}): {e}")

print(f"Av bitti! Toplam {len(toplanan_postlar)} harika ithal video bulundu.")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(toplanan_postlar, f, ensure_ascii=False, indent=4)
