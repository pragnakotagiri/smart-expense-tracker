\# Smart Expense Tracker (Python)



A command-line tool to track, analyze, and visualize personal expenses.



\## Tech

\- Python 3.13, SQLite

\- pandas (analytics), matplotlib (charts)

\- click (CLI), pytest (tests)



\## Quickstart

```bash

\# create env

python -m venv .venv

.\\.venv\\Scripts\\activate

pip install -r requirements.txt



\# add expense

python main.py add --date 2025-10-01 --category Food --description "Lunch" --amount 180 --method UPI



\# list / summary

python main.py list

python main.py summary



\# charts

python main.py charts --month 2025-10   # saves PNGs in /reports



\# csv

python main.py exportcsv data\\backup.csv

python main.py importcsv data\\sample\_expenses.csv



\# test

pytest -q



