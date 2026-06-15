import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "public" / "songs.sqlite"


SONGS = [
    {
        "slug": "night-train-keikaku",
        "title": "Night Train Keikaku",
        "artist": "Placeholder Signal",
        "youtube_id": "UENxZiDpPFA",
        "uploaded_at": "2026-06-14T21:20:00-07:00",
        "japanese_lyrics": [
            ["夜の線路を歩いて", "赤い月だけ見ていた", "言葉はノイズになって"],
            ["君の名前をしまって", "明日の影をほどいた", "計画通りと笑った"],
        ],
        "english_lyrics": [
            ["I walked along the night rails", "Watching only the red moon", "Words dissolved into noise"],
            ["I folded your name away", "Unwound tomorrow's shadow", "And laughed: all according to plan"],
        ],
    },
    {
        "slug": "static-bloom",
        "title": "Static Bloom",
        "artist": "CRT Heartbreak",
        "youtube_id": "UENxZiDpPFA",
        "uploaded_at": "2026-05-28T18:45:00-07:00",
        "japanese_lyrics": [
            ["砂嵐の花が咲く", "画面の奥で呼んでる"],
            ["壊れた星を拾って", "胸のポケットに隠す"],
        ],
        "english_lyrics": [
            ["A static flower opens", "Calling from behind the screen"],
            ["I pick up a broken star", "And hide it in my chest pocket"],
        ],
    },
    {
        "slug": "zero-set",
        "title": "Zero Set",
        "artist": "Euclid.exe",
        "youtube_id": "UENxZiDpPFA",
        "uploaded_at": "2026-04-03T09:10:00-07:00",
        "japanese_lyrics": [
            ["空集合の海で", "証明だけが光る"],
            ["終わりのない余白に", "小さな夢を写す"],
        ],
        "english_lyrics": [
            ["In the sea of the empty set", "Only the proof gives off light"],
            ["On an endless margin", "I project a small dream"],
        ],
    },
]


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("drop table if exists songs")
        connection.execute(
            """
            create table songs (
              slug text primary key,
              title text not null,
              artist text not null,
              youtube_id text not null,
              uploaded_at text not null,
              japanese_lyrics text not null,
              english_lyrics text not null
            )
            """
        )
        connection.executemany(
            """
            insert into songs (
              slug, title, artist, youtube_id, uploaded_at, japanese_lyrics, english_lyrics
            ) values (
              :slug, :title, :artist, :youtube_id, :uploaded_at, :japanese_lyrics, :english_lyrics
            )
            """,
            [
                {
                    **song,
                    "japanese_lyrics": json.dumps(song["japanese_lyrics"], ensure_ascii=False),
                    "english_lyrics": json.dumps(song["english_lyrics"], ensure_ascii=False),
                }
                for song in SONGS
            ],
        )


if __name__ == "__main__":
    main()
