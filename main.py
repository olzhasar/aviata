import os

from flask import Flask, render_template, request

from aviata.tasks import check_all_flights, update_all_flights
from aviata.utils import get_flights_from_cache

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(PROJECT_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)


@app.route("/")
def index():
    date = request.args.get("date", "")
    flights = get_flights_from_cache(date=date)
    return render_template("index.html", flights=flights)


@app.route("/update")
def update():
    update_all_flights.delay()
    return render_template(
        "message.html",
        message="Update started. You can monitor progress in celery logs",
    )


@app.route("/check")
def check():
    check_all_flights.delay()
    return render_template(
        "message.html",
        message="Check started. You can monitor progress in celery logs",
    )


if __name__ == "__main__":
    app.run()
