from calendar import month
from tkinter.tix import COLUMN
from flask import Flask, render_template, redirect, url_for, request, abort
import json
from importlib_metadata import method_cache
import pandas as pd

from scripts.header import NavBar


LEDGER_COLS = ["Number", "Date", "Description", "Category", "Amount"]


with open("data/months.json") as f:
    MONTHS = json.load(f)

with open("data/years.json") as f:
    Years = json.load(f)

app = Flask(__name__)



@app.route('/')
def index():
    nav = NavBar().render()

    return render_template('index.html', nav=nav)


@app.route('/ledgers', methods=['GET', 'POST'])
def ledgers():
    nav = NavBar().render()

    # Ask client for the year to search for
    if "year" not in request.args and "month" not in request.args:
        return render_template('ledger.html', nav=nav, Years=Years, Months=[])

    # If given a year, attempt to ask client for month as well
    if "year" in request.args and "month" not in request.args:
        return render_template('ledger.html', nav=nav, Years=[], Months=MONTHS, year=request.args.get("year"))

    # Attempt to open CSV file
    if "year" in request.args and "month" in request.args:
        y = request.args.get("year")
        m = request.args.get("month")

        return redirect(url_for("show_ledger", year=y, month=m))
        
    return render_template('ledger.html', nav=nav)


@app.route('/show_ledger', methods=['GET', 'POST'])
def show_ledger():
    nav = NavBar().render()

    y = ""
    m = ""

    if request.method == 'POST':
        y = request.form['year']
        m = request.form['month']

    if request.method == 'GET':
        y = request.args.get('year')
        m = request.args.get('month')

    csv = f"data/private/ledgers/{y}_{m}.csv" # Parse CSV file from args
    df = None
    try:
        df = pd.read_csv(csv)

    except FileNotFoundError:
        errormsg = f"File '{csv}' not found in budgets, please try again"
        return redirect(url_for('index'), 404)

        df = pd.DataFrame(columns=LEDGER_COLS)
        out_df = pd.DataFrame(columns=LEDGER_COLS).set_index('Number')
        out_df.to_csv(csv)

    if request.method == 'POST':
        print(request.form)
        nm = len(df)
        dt = request.form['trdt']
        dc = request.form['desc']
        ca = request.form['cate']
        at = request.form['amnt']
        dr = request.form['dirc']

        try:
            at = float(at)*int(dr)
        except ValueError:
            abort(404)
        
        row = pd.DataFrame([[nm, dt, dc, ca, at]], columns=LEDGER_COLS)
        df = pd.concat([df, row])
        df.set_index('Number').to_csv(csv)

        return redirect(url_for('show_ledger', year=y, month=m)) # Redirect to self to prevent form resubmission


    df.set_index("Number", drop=False, inplace=True)

    return render_template("ledger_render.html", nav=nav, Columns=df.columns, Data=df.values, year=y, month=m)


@app.route('/add_ledger', methods=['GET', 'POST'])
def add_ledger():
    nav = NavBar().render()

    return render_template('ledger_add.html', nav=nav)


@app.route('/budget', methods=['GET'])
def budget():
    if len(request.args) == 0:
        return render_template('ledger.html', Months=MONTHS)

    return redirect(url_for('index'))


@app.route('/greet<name>')
def greet(name):
    return f"Hello, {name}"



if __name__ == '__main__':
    app.debug = True
    app.run()