import requests
import json
import os

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')

url = "https://reddit34.p.rapidapi.com/getTopPostsBySubreddit"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "reddit34.p.rapidapi.com"
}

# Küçük harflerle yazmak API'lerde her zaman daha güvenlidir
subreddits = ['turkeyjerky', 'shitposttc', 'zargoryangalaksisi', 'kgbtr']
toplanan_postlar = []

print("Gölge Bot devrede, RapidAPI üzerinden Reddit'e sızılıyor...")

for sub in subreddits:
    print(f"Bölge taranıyor: {sub}...")
    
    # 'time' parametresini 'week' yaptık. Böylece garanti olarak en iyi videolar gelecek.
    querystring = {"subreddit": sub, "time": "week"}
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            veri = response.json()
            
            # Tam olarak senin attığın görsele göre kutuyu açıyoruz:
            postlar = []
            if isinstance(veri, dict) and 'data' in veri and 'posts' in veri['data']:
                postlar = veri['data']['posts']
            
            # Eğer API o sayfa için boş liste döndürdüyse atla
            if not postlar:
                print(f"Uyarı: API {sub} sayfası için 0 post döndürdü.")
                continue

            for post in postlar:
                # Videonun linkini yakalıyoruz
                video_url = post.get('video_url') or post.get('media_url') or post.get('url', '')
                
                # Sadece video olanları listeye alıyoruz
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

print(f"Av bitti! Toplam {len(toplanan_postlar)} harika video bulundu.")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(toplanan_postlar, f, ensure_ascii=False, indent=4)
