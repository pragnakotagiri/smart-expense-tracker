import click
from tabulate import tabulate
from .models import add_expense, list_expenses, delete_expense
from .analytics import monthly_summary, category_summary
from .charts import plot_monthly_trend, plot_category_pie
from .utils import import_csv, export_csv

@click.group()
def cli():
    """Smart Expense Tracker CLI"""

@cli.command()
@click.option("--date", prompt=True, help="YYYY-MM-DD")
@click.option("--category", prompt=True, type=click.Choice(["Food","Rent","Travel","Bills","Shopping","Other"]))
@click.option("--description", prompt=True, default="")
@click.option("--amount", prompt=True, type=float)
@click.option("--method", prompt=True, default="UPI")
def add(date, category, description, amount, method):
    add_expense(date, category, description, amount, method)
    click.echo("✅ Added.")

@cli.command(name="list")
@click.option("--limit", default=20)
def _list(limit):
    rows = list_expenses(limit)
    click.echo(tabulate(rows, headers=["id","date","category","desc","amount","method"]))

@cli.command()
@click.argument("expense_id", type=int)
def delete(expense_id):
    n = delete_expense(expense_id)
    click.echo("🗑️ Deleted." if n else "Not found.")

@cli.command()
def summary():
    ms = monthly_summary()
    cs = category_summary()
    if ms.empty:
        click.echo("No data yet.")
        return
    click.echo("== Monthly ==")
    click.echo(tabulate(ms, headers=ms.columns))
    click.echo("\n== Category (All-Time) ==")
    click.echo(tabulate(cs, headers=cs.columns))

@cli.command()
@click.option("--month", help="YYYY-MM (optional, e.g., 2025-10)")
def charts(month):
    p1 = plot_monthly_trend()
    p2 = plot_category_pie(month=month)
    click.echo(f"Saved: {p1 or 'no data'}, {p2 or 'no data'}")

@cli.command()
@click.argument("csv_path")
def importcsv(csv_path):
    n = import_csv(csv_path)
    click.echo(f"📥 Imported {n} rows.")

@cli.command()
@click.argument("csv_path")
def exportcsv(csv_path):
    n = export_csv(csv_path)
    click.echo(f"📤 Exported {n} rows.")

def main():
    cli()
