from expense_tracker.models import add_expense, list_expenses

def test_add_and_list():
    add_expense("2025-10-04","Food","Test item",123.0,"UPI")
    rows = list_expenses(50)
    assert any(
        r[1] == "2025-10-04" and r[2] == "Food" and float(r[4]) == 123.0
        for r in rows
    )
