import requests
import json
import os

# GitHub'ın gizli kasasından RapidAPI şifremizi alıyoruz
RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')

url = "https://reddit34.p.rapidapi.com/getTopPostsBySubreddit"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "reddit34.p.rapidapi.com"
}

subreddits = ['TurkeyJerky', 'ShitpostTC', 'ZargoryanGalaksisi', 'KGBTR']
toplanan_postlar = []

print("Gölge Bot devrede, RapidAPI üzerinden Reddit'e sızılıyor...")

for sub in subreddits:
    print(f"Bölge taranıyor: {sub}...")
    
    # 'time' parametresi 'day' olarak ayarlandı (her gün en yeni videolar için)
    querystring = {"subreddit": sub, "time": "day"}
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            veri = response.json()
            
            # Gelen veriyi güvenli bir şekilde liste olarak yakalıyoruz
            postlar = []
            if isinstance(veri, list):
                postlar = veri
            elif isinstance(veri, dict):
                postlar = veri.get('data', veri.get('posts', veri.get('children', [])))

            for post in postlar:
                # Video olup olmadığını tespit et
                is_video = post.get('is_video') == True or post.get('isVideo') == True
                video_url = post.get('video_url') or post.get('media_url') or post.get('url', '')
                
                # Eğer gerçekten video ise listeye ekle
                if is_video or '.mp4' in str(video_url).lower():
                    post_verisi = {
                        "id": post.get('id', 'Bilinmiyor'),
                        "title": post.get('title', 'Başlıksız'),
                        "url": video_url,
                        "score": post.get('score', post.get('upvotes', 0)),
                        "subreddit": sub
                    }
                    if post_verisi["url"]: # Link boş değilse
                        toplanan_postlar.append(post_verisi)
                        
        else:
            print(f"Hata: {sub} okunamadı. Kod: {response.status_code}")
            
    except Exception as e:
        print(f"Sistemsel Hata ({sub}): {e}")

print(f"Av bitti! Toplam {len(toplanan_postlar)} harika video bulundu.")

# Json dosyamızı oluşturuyoruz
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(toplanan_postlar, f, ensure_ascii=False, indent=4)
