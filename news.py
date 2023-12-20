import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def aidb():
    url = "https://aiboom.net"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, features="html.parser")
    article = list(
        map(
            lambda x: {
                "date": x.find(class_="entry-date updated").text,
                "title": x.find(class_="title").text,
                "link": x.find(class_="link").get("href"),
            },
            soup.find_all(class_="post_item clearfix"),
        )
    )
    df = (
        pd.DataFrame(article)
        .sort_values("date")
        .drop_duplicates("link", keep="last")
    )
    df["date"] = pd.to_datetime(df["date"])
    df = df[
        df["date"]
        > pd.Timestamp.today(tz="JST") - pd.tseries.offsets.DateOffset(days=1)
    ]
    print(pd.Timestamp.today(tz="JST"))

    webhook_url = os.environ.get("WEBHOOK_AIDB")
    for date, link in zip(df["date"], df["link"]):
        text = date.strftime("%Y/%m/%d") + ", " + link
        res = requests.post(webhook_url, {"content": text})
        time.sleep(10)


def main():
    aidb()


if __name__ == "__main__":
    main()
