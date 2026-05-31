import requests
import psycopg2
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()


ACCESS_TOKEN = TOKEN_DO_SEU_APP

IG_USER_ID = SEU_IG_ID

BASE_URL = "https://graph.facebook.com/v18.0"

DB_CONFIG = {
    "host": HOST_BANCO,
    "database": DATABASE_BANCO,
    "user": USER_BANCO,
    "password": SENHA_BANCO,
    "port": PORTA_BANCO
}


conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()


def analyze_sentiment(text):

    score = sia.polarity_scores(text)["compound"]

    if score >= 0.05:
        label = "positivo"
    elif score <= -0.05:
        label = "negativo"
    else:
        label = "neutro"

    return label, score



def get_profile():

    url = f"{BASE_URL}/{IG_USER_ID}"

    params = {
        "fields": "name,username,followers_count,follows_count,media_count",
        "access_token": ACCESS_TOKEN
    }

    response = requests.get(url, params=params).json()

    sql = """
    INSERT INTO perfil_instagram
    (id, username, name, followers_count, follows_count, media_count)
    VALUES (%s,%s,%s,%s,%s,%s)
    ON CONFLICT (id) DO NOTHING
    """

    cur.execute(sql, (
        IG_USER_ID,
        response.get("username"),
        response.get("name"),
        response.get("followers_count"),
        response.get("follows_count"),
        response.get("media_count")
    ))

    conn.commit()


def get_feed():

    url = f"{BASE_URL}/{IG_USER_ID}/media"

    params = {
        "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count",
        "access_token": ACCESS_TOKEN
    }

    response = requests.get(url, params=params).json()

    posts = response.get("data", [])

    for post in posts:

        sql = """
        INSERT INTO feed_instagram
        (id, ig_account_id, caption, media_type, media_url, permalink, timestamp, like_count, comments_count)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id) DO NOTHING
        """

        cur.execute(sql, (
            post["id"],
            IG_USER_ID,
            post.get("caption"),
            post.get("media_type"),
            post.get("media_url"),
            post.get("permalink"),
            post.get("timestamp"),
            post.get("like_count"),
            post.get("comments_count")
        ))

    conn.commit()

    return posts


def get_metrics(media_id):

    url = f"{BASE_URL}/{media_id}/insights"

    params = {
        "metric": "views,reach,saved,likes,comments,shares,total_interactions,ig_reels_video_view_total_time,ig_reels_avg_watch_time",
        "access_token": ACCESS_TOKEN
    }

    response = requests.get(url, params=params).json()

    metrics = {}

    for item in response.get("data", []):
        metrics[item["name"]] = item["values"][0]["value"]

    sql = """
    INSERT INTO metrica_post_instagram
    (media_id, views, reach, saved, likes, comments, shares, total_interactions,
     ig_reels_video_view_total_time, ig_reels_avg_watch_time)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cur.execute(sql, (
        media_id,
        metrics.get("views"),
        metrics.get("reach"),
        metrics.get("saved"),
        metrics.get("likes"),
        metrics.get("comments"),
        metrics.get("shares"),
        metrics.get("total_interactions"),
        metrics.get("ig_reels_video_view_total_time"),
        metrics.get("ig_reels_avg_watch_time")
    ))

    conn.commit()


def get_comments(media_id):

    url = f"{BASE_URL}/{media_id}/comments"

    params = {
        "fields": "id,text,username,timestamp",
        "access_token": ACCESS_TOKEN
    }

    response = requests.get(url, params=params).json()

    comments = response.get("data", [])

    for c in comments:

        text = c.get("text", "")

        label, score = analyze_sentiment(text)

        sql = """
        INSERT INTO comentario_instagram
        (id, media_id, username, text, timestamp, sentimento_label, sentimento_score)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id) DO NOTHING
        """

        cur.execute(sql, (
            c["id"],
            media_id,
            c.get("username"),
            text,
            c.get("timestamp"),
            label,
            score
        ))

    conn.commit()


def main():

    print("Coletando perfil...")
    get_profile()

    print("Coletando posts...")
    posts = get_feed()

    for post in posts:

        media_id = post["id"]

        print(f"Processando post {media_id}")

        try:
            get_metrics(media_id)
        except:
            print("Erro ao coletar métricas")

        try:
            get_comments(media_id)
        except:
            print("Erro ao coletar comentários")

        time.sleep(1)

    print("Coleta finalizada")

if __name__ == "__main__":
    main()