import sqlite3

DATABASE = 'wishlist.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS wishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                url TEXT,
                status TEXT DEFAULT 'хочу'
            )
        ''')
        conn.commit()

def get_all_wishes():
    with get_db() as conn:
        return conn.execute("SELECT * FROM wishes ORDER BY id DESC").fetchall()

def add_wish(name, price, url='', status='хочу'):
    with get_db() as conn:
        conn.execute("INSERT INTO wishes (name, price, url, status) VALUES (?,?,?,?)",
                     (name, float(price), url, status))
        conn.commit()

def get_wish(wish_id):
    with get_db() as conn:
        return conn.execute("SELECT * FROM wishes WHERE id=?", (wish_id,)).fetchone()

def update_wish(wish_id, name, price, url, status):
    with get_db() as conn:
        conn.execute("UPDATE wishes SET name=?, price=?, url=?, status=? WHERE id=?",
                     (name, float(price), url, status, wish_id))
        conn.commit()

def delete_wish(wish_id):
    with get_db() as conn:
        conn.execute("DELETE FROM wishes WHERE id=?", (wish_id,))
        conn.commit()

def get_total_cost():
    with get_db() as conn:
        row = conn.execute("SELECT SUM(price) as total FROM wishes WHERE status='хочу'").fetchone()
        return row['total'] or 0

def search_wishes(q):
    with get_db() as conn:
        return conn.execute("SELECT * FROM wishes WHERE name LIKE ? OR url LIKE ?",
                            (f'%{q}%', f'%{q}%')).fetchall()

def validate(name, price):
    errors = []
    if not name or not name.strip():
        errors.append("Название не может быть пустым")
    try:
        if float(price) < 0:
            errors.append("Цена не может быть отрицательной")
    except:
        errors.append("Цена должна быть числом")
    return errors
