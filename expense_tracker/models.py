from .db import get_conn
# top of file
from datetime import datetime, UTC


def add_expense(date, category, description, amount, method):
    with get_conn() as c:
        c.execute(
            "INSERT INTO expenses(date,category,description,amount,method,created_at) VALUES(?,?,?,?,?,?)",
            (date, category, description, float(amount), method, datetime.now(UTC).isoformat()
)
        )

def list_expenses(limit=50):
    with get_conn() as c:
        cur = c.execute(
            "SELECT id,date,category,description,amount,method FROM expenses ORDER BY date DESC, id DESC LIMIT ?",
            (limit,)
        )
        return cur.fetchall()

def delete_expense(expense_id: int):
    with get_conn() as c:
        cur = c.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        # commit is handled by the context manager, but this is harmless:
        # c.commit()
        return cur.rowcount  # number of rows deleted (0 if not found)
