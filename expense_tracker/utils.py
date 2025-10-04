import csv
from .models import add_expense
from .db import get_conn

def import_csv(path):
    count = 0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            add_expense(
                row["date"],
                row["category"],
                row.get("description",""),
                float(row["amount"]),
                row.get("method","UPI")
            )
            count += 1
    return count

def export_csv(path):
    with get_conn() as c:
        cur = c.execute("SELECT date,category,description,amount,method FROM expenses ORDER BY date")
        rows = cur.fetchall()
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date","category","description","amount","method"])
        w.writerows(rows)
    return len(rows)
