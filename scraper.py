import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

subreddits = ['TurkeyJerky', 'ShitpostTC', 'ZargoryanGalaksisi', 'KGBTR']
toplanan_postlar = []

print("Avcı uyandı, ağ atılıyor...")

for sub_name in subreddits:
    url = f"https://www.reddit.com/r/{sub_name}/top.json?t=day&limit=15"
    try:
        response = requests.get(url, headers=headers)
        print(f"{sub_name} taranıyor... Cevap Kodu: {response.status_code}")
        
        if response.status_code == 200:
            veri = response.json()
            postlar = veri['data']['children']
            for post in postlar:
                post_detay = post['data']
                
                # Sadece düz yazı olanları eleyelim, geri kalan her şeyi (foto/video) alalım
                if not post_detay.get('is_self'):
                    medya_url = post_detay.get('url')
                    
                    # Eğer bu bir video ise, saf mp4 linkini alalım
                    is_video = post_detay.get('is_video', False)
                    if is_video and 'media' in post_detay and post_detay['media'] and 'reddit_video' in post_detay['media']:
                        medya_url = post_detay['media']['reddit_video']['fallback_url']
                        
                    post_verisi = {
                        "id": post_detay.get('id'),
                        "title": post_detay.get('title'),
                        "url": medya_url,
                        "score": post_detay.get('score'),
                        "subreddit": sub_name,
                        "is_video": is_video
                    }
                    toplanan_postlar.append(post_verisi)
        else:
            print(f"Uyarı: {sub_name} sayfasından veri alınamadı. (Reddit GitHub'ı engelliyor olabilir)")
            
    except Exception as e:
        print(f"Hata: {e}")

print(f"Av bitti. Toplam {len(toplanan_postlar)} içerik bulundu.")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(toplanan_postlar, f, ensure_ascii=False, indent=4)
