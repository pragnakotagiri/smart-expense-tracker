import pandas as pd
from .db import get_conn

def df_all():
    with get_conn() as c:
        return pd.read_sql_query(
            "SELECT * FROM expenses",
            c,
            parse_dates=["date", "created_at"]
        )

def monthly_summary():
    df = df_all()
    if df.empty:
        return df
    df["year_month"] = df["date"].dt.to_period("M")
    return (
        df.groupby("year_month")["amount"]
        .sum()
        .reset_index()
        .sort_values("year_month")
    )

def category_summary(month=None):
    df = df_all()
    if df.empty:
        return df
    if month:
        target = pd.Period(month, freq="M")  # 'YYYY-MM'
        df = df[df["date"].dt.to_period("M") == target]
    return (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )
