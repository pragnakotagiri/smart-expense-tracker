import os
# ✅ Use a non-GUI backend for server environments (fixes warnings with Flask)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .analytics import monthly_summary, category_summary

os.makedirs("reports", exist_ok=True)

def plot_monthly_trend(path="reports/monthly_trend.png"):
    ms = monthly_summary()
    if ms.empty:
        return None
    plt.figure()
    x = ms["year_month"].astype(str)
    y = ms["amount"]
    plt.plot(x, y, marker="o")
    plt.title("Monthly Expense Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def plot_category_pie(month=None, path="reports/category_share.png"):
    cs = category_summary(month)
    if cs.empty:
        return None
    plt.figure()
    plt.pie(cs["amount"], labels=cs["category"], autopct="%1.1f%%", startangle=90)
    plt.title(f"Category Share{f' - {month}' if month else ''}")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
