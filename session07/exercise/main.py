"""
第7回 実習: フロントエンドとバックエンドの結合

第6回の正解をベースに、CORS設定と静的ファイル配信を追加します。
TODO コメントの部分を実装してください。

起動方法:
  python init_db.py
  python main.py
"""

import sqlite3

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- Pydantic モデル ---


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    done: bool


# --- FastAPI アプリケーション ---

app = FastAPI(title="TODO API")


# --- TODO: CORS設定を追加してください（実習4）---
# ヒント:
#   app.add_middleware(
#       CORSMiddleware,
#       allow_origins=["*"],
#       allow_credentials=True,
#       allow_methods=["*"],
#       allow_headers=["*"],
#   )


# --- データベース接続 ---

DATABASE = "todo.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# --- APIエンドポイント（第6回の正解） ---


@app.get("/todos")
def get_todos():
    """TODO一覧を取得する"""
    conn = get_db()
    cursor = conn.execute("SELECT id, title, done FROM todos ORDER BY id")
    todos = [
        {"id": row["id"], "title": row["title"], "done": bool(row["done"])}
        for row in cursor.fetchall()
    ]
    conn.close()
    return todos


@app.post("/todos")
def create_todo(todo: TodoCreate):
    """新しいTODOを追加する"""
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO todos (title, done) VALUES (?, 0)",
        (todo.title,),
    )
    conn.commit()
    todo_id = cursor.lastrowid
    conn.close()
    return {"id": todo_id, "title": todo.title, "done": False}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdate):
    """TODOの完了状態を更新する"""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    existing = cursor.fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="TODO not found")

    conn.execute(
        "UPDATE todos SET done = ? WHERE id = ?",
        (int(todo.done), todo_id),
    )
    conn.commit()
    conn.close()
    return {"id": todo_id, "title": existing["title"], "done": todo.done}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """TODOを削除する"""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    existing = cursor.fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="TODO not found")

    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return {"message": "TODO deleted", "id": todo_id}


#   --- TODO: 静的ファイル配信を追加してください（実習6）---
#   TODO(実習6): 静的ファイルを配信してください
#   ヒント:
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# 注意: app.mount() はファイルの最後に書いてください


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
