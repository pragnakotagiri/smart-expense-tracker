from flask import Flask, render_template, request, redirect, url_for, flash
from expense_tracker.models import add_expense, list_expenses, delete_expense
from expense_tracker.analytics import monthly_summary, category_summary
from expense_tracker.charts import plot_monthly_trend, plot_category_pie
from flask import send_from_directory
from flask import send_file
from expense_tracker.utils import import_csv, export_csv
from dotenv import load_dotenv
import os, time

app = Flask(__name__)
load_dotenv()
print("Budget limit from env:", os.getenv("BUDGET_LIMIT"))

app.secret_key = "dev-secret-key"  # for flash messages

@app.route("/")
def home():
    rows = list_expenses(limit=50)
    return render_template("index.html", rows=rows)

@app.route("/add", methods=["GET", "POST"])
def add_page():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        description = request.form["description"]
        amount = request.form["amount"]
        method = request.form["method"]
        add_expense(date, category, description, amount, method)
        flash("Expense added successfully!")
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_page(expense_id):
    deleted = delete_expense(expense_id)
    if deleted:
        flash(f"Deleted expense #{expense_id}")
    else:
        flash("Expense not found")
    return redirect(url_for("home"))
      

@app.route("/summary")
def summary_page():
    month = request.args.get("month")  # 'YYYY-MM' or None

    ms = monthly_summary()
    cs = category_summary(month=month)

    # Charts
    path_trend = plot_monthly_trend()
    path_pie = plot_category_pie(month=month)
    cache_bust = int(time.time())

    # Budget values
    try:
        budget_limit = float(os.getenv("BUDGET_LIMIT", "0").strip())
    except Exception:
        budget_limit = 0.0

    spent = float(cs["amount"].sum()) if (cs is not None and not cs.empty) else 0.0
    over_budget = (budget_limit > 0) and (spent > budget_limit)

    return render_template(
        "summary.html",
        ms=ms,
        cs=cs,
        month=month,
        trend_path=path_trend,
        pie_path=path_pie,
        cache_bust=cache_bust,
        budget_limit=budget_limit,
        spent=spent,
        over_budget=over_budget,
    )


@app.route("/reports/<path:filename>")
def reports_files(filename):
    return send_from_directory("reports", filename)

@app.route("/export")
def export_page():
    path = "data/export_web.csv"
    n = export_csv(path)
    if n == 0:
        flash("No expenses to export.")
        return redirect(url_for("home"))
    return send_file(path, as_attachment=True)

@app.route("/import", methods=["GET", "POST"])
def import_page():
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".csv"):
            path = os.path.join("data", "upload.csv")
            file.save(path)
            n = import_csv(path)
            flash(f"Imported {n} expenses from CSV.")
            return redirect(url_for("home"))
        else:
            flash("Please upload a valid CSV file.")
            return redirect(url_for("import_page"))
    return render_template("import.html")
# (we'll add /add, /delete, /summary, /charts next steps)

if __name__ == "__main__":
    app.run(debug=True)
