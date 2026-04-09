import requests
import json
import os

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
url = "https://reddit34.p.rapidapi.com/getTopPostsBySubreddit"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "reddit34.p.rapidapi.com"
}

subreddits = ['shitposting', 'dankvideos', 'discordVideos']
toplanan_postlar = []

print("Geniş Ağ devrede! Filtreler kapalı, her şey toplanıyor...")

for sub in subreddits:
    print(f"Bölge taranıyor: {sub}...")
    querystring = {"subreddit": sub, "time": "day"}
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            veri = response.json()
            
            # API veriyi nerede saklıyorsa onu bulan akıllı sistem
            postlar = []
            if isinstance(veri, list):
                postlar = veri
            elif isinstance(veri, dict):
                if 'data' in veri and isinstance(veri['data'], dict) and 'posts' in veri['data']:
                    postlar = veri['data']['posts']
                elif 'posts' in veri:
                    postlar = veri['posts']
                elif 'data' in veri and isinstance(veri['data'], list):
                    postlar = veri['data']
            
            for post in postlar:
                # VİDEO FİLTRESİ İPTAL! Ne var ne yoksa alıyoruz.
                post_verisi = {
                    "id": post.get('id', ''),
                    "title": post.get('title', 'Başlıksız'),
                    # API linki nerede gönderiyorsa onu yakala
                    "url": post.get('video_url') or post.get('media_url') or post.get('url') or post.get('permalink', ''),
                    "subreddit": sub
                }
                
                # Eğer boş bir link değilse listeye ekle
                if post_verisi["url"]:
                    toplanan_postlar.append(post_verisi)
                    
    except Exception as e:
        print(f"Sistemsel Hata ({sub}): {e}")

print(f"Av bitti! Filtresiz toplam {len(toplanan_postlar)} içerik bulundu.")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(toplanan_postlar, f, ensure_ascii=False, indent=4)
