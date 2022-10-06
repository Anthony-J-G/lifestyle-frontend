# Builtin Modules
import json
import datetime

# 3rd-Party Modules
import pandas as pd
from werkzeug.exceptions import BadRequestKeyError


# Custom Modules
from src.components.header import NavBar
from src.constants import LEDGER_COLS, MONTHS


def year_month_is_valid(d):
    # Try to extract the month and year from the date
    y, m = None, None
    try:
        if len(d) != 7: # If the date is not 7 characters, throw an exception
            raise ValueError

        y, m = d.split('-')
        y = int(y)
        m = int(m)

        in_bounds = (0 <= m and m < 12) and (1900 <= y and y <= datetime.date.today().year)
        if not in_bounds:
            raise ValueError

        m = MONTHS[m]

    # Catch an exception if the length is incorrect or any other part of the parameters throws a ValueError
    except ValueError:
        return {"err": f"ValueError: Bad form parameter '{d}'"}, False

    return {'y': y, 'm': m}, True


# TODO: Transfer functionality from the main 'App.py' to here
def view_all_ledgers(req):

    """
    # Create Components
    nav = NavBar().render()

    # Ask client for the year to search for
    if "year" not in req.args and "month" not in request.args:
        return render_template('ledger.html', nav=nav, Years=Years, Months=[])

    # If given a year, attempt to ask client for month as well
    if "year" in request.args and "month" not in request.args:
        return render_template('ledger.html', nav=nav, Years=[], Months=MONTHS, year=request.args.get("year"))

    # Attempt to open CSV file
    if "year" in request.args and "month" in request.args:
        y = request.args.get("year")
        m = request.args.get("month")

        return redirect(url_for("show_ledger", year=y, month=m))
    """

    return 0


# TODO: Transfer functionality from the main 'App.py' to here
def render_ledger(req):
    
    nav = NavBar().render()

    y = req.args.get('year')
    m = req.args.get('month')

    csv = f"data/private/ledgers/{y}_{m}.csv" # Parse CSV file from args
    df = None
    try:
        df = pd.read_csv(csv)

    except FileNotFoundError:
        errormsg = f"File '{csv}' not found in budgets, please try again"
        return {'err': errormsg}, -1

    df.set_index("Number", drop=False, inplace=True)

    return {}, 0


# Good probably?
def make_new_ledger(req):

    # Try to access 'date' form parameter
    d = None
    try:
        d = req.form['date']
    
    # Catch an exception if any other variable is posted besides 'date'
    except BadRequestKeyError:
        return {"err": "werkzeug.exceptions.BadKeyRequestError: Missing form parameter"}, -1

    params, is_valid = year_month_is_valid(d)
    if not is_valid:
        return {"err": params["err"]}, -1
    y, m = params['y'], params['m']

    # At this point the CSV name should be formatted properly
    csv = f"data/private/ledgers/{y}_{m}.csv" # Parse CSV file from args
    df = None
    # Try to query saved CSV data
    try:
        df = pd.read_csv(csv) # If the CSV exists, redirect and render the table

        return {'y':y, 'm':m}, 1

    # Catch an exception if the file doesn't exist and make a new one to compensate
    except FileNotFoundError:
        out_df = pd.DataFrame(columns=LEDGER_COLS).set_index('Number')
        out_df.to_csv(csv)
    
    return {'y':y, 'm':m}, 0


# TODO: Super broken, needs review tomorrow
def add_transaction(req):

    return {}, 0

    params, is_valid = year_month_is_valid(d)
    if not is_valid:
        return {"err": params["err"]}, -1
    y, m = params['y'], params['m']

    csv = f"data/private/ledgers/{y}_{m}.csv" # Parse CSV file from args
    
    nm = len(df)
    dt = req.form['trdt']
    dc = req.form['desc']
    ca = req.form['cate']
    at = req.form['amnt']
    dr = req.form['dirc']

    try:
        at = float(at)*int(dr)
    except ValueError:
        return {}, -1
    
    row = pd.DataFrame([[nm, dt, dc, ca, at]], columns=LEDGER_COLS)
    df = pd.concat([df, row])
    df.set_index('Number').to_csv(csv)

    return {}, 1
