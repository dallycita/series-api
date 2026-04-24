from app.database import get_connection
import math

def get_all_series(page: int, limit: int, q: str, sort: str, order: str):
    valid_sorts = {"title", "year", "created_at", "genre"}
    if sort not in valid_sorts:
        sort = "created_at"
    order = "ASC" if order.upper() == "ASC" else "DESC"

    offset = (page - 1) * limit
    conn = get_connection()
    cur = conn.cursor()

    where = ""
    params = []
    if q:
        where = "WHERE LOWER(title) LIKE LOWER(%s)"
        params.append(f"%{q}%")

    cur.execute(f"SELECT COUNT(*) FROM series {where}", params)
    total = int(cur.fetchone()["count"])

    cur.execute(
        f"SELECT * FROM series {where} ORDER BY {sort} {order} LIMIT %s OFFSET %s",
        params + [limit, offset]
    )
    rows = cur.fetchall()
    conn.close()

    return {
        "data": rows,
        "page": page,
        "limit": limit,
        "total_count": total,
        "total_pages": math.ceil(total / limit)
    }

def get_series_by_id(series_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM series WHERE id = %s", (series_id,))
    row = cur.fetchone()
    conn.close()
    return row

def create_series(data: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO series (title, genre, status, synopsis, year, image_path)
           VALUES (%(title)s, %(genre)s, %(status)s, %(synopsis)s, %(year)s, %(image_path)s)
           RETURNING *""",
        data
    )
    row = cur.fetchone()
    conn.commit()
    conn.close()
    return row

def update_series(series_id: int, data: dict):
    fields = {k: v for k, v in data.items() if v is not None}
    if not fields:
        return get_series_by_id(series_id)  # si no hay nada que cambiar, devuelve lo actual
    set_clause = ", ".join([f"{k} = %s" for k in fields])
    values = list(fields.values()) + [series_id]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE series SET {set_clause}, updated_at = NOW() WHERE id = %s RETURNING *",
        values
    )
    row = cur.fetchone()
    conn.commit()
    conn.close()
    return row

def delete_series(series_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM series WHERE id = %s", (series_id,))
    affected = cur.rowcount
    conn.commit()
    conn.close()
    return affected

def create_rating(series_id: int, score: float, review: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO user_ratings (series_id, score, review) VALUES (%s, %s, %s) RETURNING *",
        (series_id, score, review)
    )
    row = cur.fetchone()
    conn.commit()
    conn.close()
    return row

def get_ratings(series_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_ratings WHERE series_id = %s ORDER BY rated_at DESC", (series_id,))
    rows = cur.fetchall()
    conn.close()
    return rows