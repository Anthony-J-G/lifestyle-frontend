import re
from flask import Flask, render_template, redirect, url_for, request, abort
import json
import pandas as pd

from src import ledger
from src.components.header import NavBar



app = Flask(__name__)



"""
    Root Route
"""
@app.route('/')
def index():
    nav = NavBar().render()

    return render_template('index.html', nav=nav)


"""
    Ledger Routes
"""
@app.route('/ledgers', methods=['GET'])
def ledgers():

    # Create Header Components
    header = {
        "nav" : NavBar().render()
    }

    # Run Route Functionality
    case = ledger.view_all_ledgers(req=request)

    if case == -1: # Default Case
        return render_template('ledger.html', header=header)

    if case == 1:
        return render_template('ledger.html', header=header, Years=[2022], Months=[])

    if case == 2:
        return render_template('ledger.html', header=header)

    # Ask client for the year to search for
    if "year" not in request.args and "month" not in request.args:
        return render_template('ledger.html', header=header, Years=[2022], Months=[])

    # If given a year, attempt to ask client for month as well
    if "year" in request.args and "month" not in request.args:
        return render_template('ledger.html', header=header, Years=[], Months=[2022], year=request.args.get("year"))

    # Attempt to open CSV file
    if "year" in request.args and "month" in request.args:
        y = request.args.get("year")
        m = request.args.get("month")

        return redirect(url_for("show_ledger", year=y, month=m))

    
    return render_template('ledger.html', header=header)


@app.route('/ledgers/show_ledger', methods=['GET'])
def show_ledger(): 
    # Create Header Components
    header = {
        "nav" : NavBar().render()
    }

    params, case = ledger.render_ledger(req=request)

    if case == -1:
        return redirect(url_for('ledgers', err=params['err']), 404)

    return render_template(
        "ledger_render.html",
        header=header,
        Columns=params['cols'],
        Data=params['data'],
        year=params['y'],
        month=params['m']
    )


@app.route('/ledgers/add_ledger', methods=['POST'])
def add_ledger():

    params, case = ledger.make_new_ledger(req=request)

    if case == -1: # Error Case
        return redirect(
            url_for('ledgers')
        )

    if case == 1:
        return redirect(
            url_for('show_ledger', year=params['y'], month=params['m'])
        )

    # Default Case
    return redirect(
        url_for('ledgers')
    )


@app.route('/ledgers/add_transaction', methods=['POST'])
def add_transaction_to_ledger():
    
    params, case = ledger.add_transaction(req=request)

    if case == -1: # Error Case
        abort(404)

    # Default Case
    return redirect(
        url_for('ledgers')
    )
    


"""
    Budgeting Routes
"""
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