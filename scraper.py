import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

subreddits = ['TurkeyJerky', 'ShitpostTC', 'ZargoryanGalaksisi', 'KGBTR']
toplanan_postlar = []

for sub_name in subreddits:
    url = f"https://www.reddit.com/r/{sub_name}/top.json?t=day&limit=15"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            veri = response.json()
            postlar = veri['data']['children']
            for post in postlar:
                post_detay = post['data']
                # Sadece video içeren postları alıyoruz
                if post_detay.get('is_video'):
                    video_url = post_detay['media']['reddit_video']['fallback_url']
                    post_verisi = {
                        "id": post_detay.get('id'),
                        "title": post_detay.get('title'),
                        "url": video_url,
                        "score": post_detay.get('score'),
                        "subreddit": sub_name
                    }
                    toplanan_postlar.append(post_verisi)
    except Exception as e:
        print(f"Hata: {e}")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(toplanan_postlar, f, ensure_ascii=False, indent=4)
