"""
データベース初期化スクリプト
todosテーブルを作成し、サンプルデータを投入する

使い方:
  python init_db.py
"""

import os
import sqlite3

DATABASE = "todo.db"


def init_db():
    """データベースを初期化する"""

    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"既存の {DATABASE} を削除しました。")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # todosテーブルを作成
    cursor.execute("""
        CREATE TABLE todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    print("todosテーブルを作成しました。")

    # サンプルデータを投入
    sample_todos = [
        ("買い物に行く", 0),
        ("レポートを書く", 0),
        ("部屋の掃除", 1),
    ]

    cursor.executemany(
        "INSERT INTO todos (title, done) VALUES (?, ?)",
        sample_todos,
    )
    print(f"{len(sample_todos)}件のサンプルデータを投入しました。")

    conn.commit()

    # 確認表示
    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()
    print(f"\n{'ID':<4} {'タイトル':<20} {'完了':<4}")
    print("-" * 30)
    for row in rows:
        done_str = "済" if row[2] else "未"
        print(f"{row[0]:<4} {row[1]:<20} {done_str:<4}")

    conn.close()
    print(f"\n{DATABASE} の初期化が完了しました。")


if __name__ == "__main__":
    init_db()