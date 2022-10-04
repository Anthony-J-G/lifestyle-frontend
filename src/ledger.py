from src.components.header import NavBar


def ledger_interface():

    """
    # Create Components
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
    """


def edit_ledger():
    pass


def render_ledger():
    pass


def make_new_ledger():
    pass