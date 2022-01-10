import json
import requests
import os
import cgi
from urllib.request import urlopen
from random import shuffle
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    """初期画面を表示します."""
    return render_template("index.html")

@app.route("/api/recommend_article")
def api_recommend_article():
    """はてブのホットエントリーから記事を入手して、ランダムに1件返却します."""

    """
        **** ここを実装します（基礎課題） ****

        1. はてブのホットエントリーページのHTMLを取得する
        2. BeautifulSoupでHTMLを読み込む
        3. 記事一覧を取得する
        4. ランダムに1件取得する
        5. 以下の形式で返却する.
            {
                "content" : "記事のタイトル",
                "link" : "記事のURL"
            }
    """
    # 1. はてブのホットエントリーページのHTMLを取得する
    with urlopen("https://b.hatena.ne.jp/hotentry/all") as res:
        html = res.read().decode("utf-8")

    # 2. BeautifulSoupでHTMLを読み込む
    soup = BeautifulSoup(html, "html.parser")

    # 3. 記事一覧を取得する
    titles = soup.select(".js-keyboard-openable")
    shuffle(titles)
    title = titles[0]["title"]
    url = titles[0]["href"]

    # 5. 以下の形式で返却する.
    return json.dumps({
        "content" : title,
        "link" : url,
    })

@app.route("/api/dtm_sale/<info>")
def api_dtm_sale(info):
    """
        **** ここを実装します（発展課題） ****
        ・自分の好きなサイトをWebスクレイピングして情報をフロントに返却します
        ・お天気APIなども良いかも
        ・関数名は適宜変更してください
    """

    with urlopen("https://sawayakatrip.com/") as res:
        html = res.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")

    titles = soup.select(".entry-card-wrap")
    new_titles = []
    for title in titles:
        target = '%'
        idx = title["title"].find(target)
        # percent = 0
        # if title["title"][idx-2:idx].isdigit():
        #     percent = int(title["title"][idx-2:idx])
        # if percent >= 80:
        if title["title"].find(info) != -1:
            new_titles.append(title)

    shuffle(new_titles)
    title = new_titles[0]["title"]
    url = new_titles[0]["href"]

    return json.dumps({
        "content" : title,
        "link" : url,
    })

if __name__ == "__main__":
    app.run(debug=True, port=5004)
    # api_dtm_sale('ベース')
