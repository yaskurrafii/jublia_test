from flask import Flask, render_template, request, jsonify
from db.db import db_init
from db.func import create_email, get_all_item
from worker.config import Config
from celery.result import AsyncResult
from celery import Celery
from celery.schedules import crontab
from datetime import datetime
import smtplib, ssl, uuid

app = Flask(__name__)
app.config.from_object(Config)

celery = Celery(
    app.name,
    broker=app.config["CELERY_BROKER_URL"],
    backend=app.config["CELERY_RESULT_BACKEND"],
)
# celery.conf.update(app.config)


@celery.task
def send_mail(receiver, subject, body):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "myasykurrafii2@gmail.com"  # Enter your address
    receiver_email = receiver  # Enter receiver address
    password = "jbyqzytxqryuqhfu"
    message = f"""\
    Subject: {subject}

    {body}"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def before_execution():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db_init(app)


@app.route("/")
def main_route():
    return render_template("index.html")


@app.post("/send_email")
def send_email():
    days = {
        "Sunday": 0,
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7,
    }
    """
    Function to save Email and save to DB
    """
    data = request.form
    given_day = datetime.strptime(data["send-time"], "%Y-%m-%dT%H:%M")
    idx = uuid.uuid4()
    print(given_day.strftime("%A"))
    celery.conf.beat_schedule = {
        **celery.conf.beat_schedule,
        idx: {
            "task": "main.send_mail",
            "schedule": crontab(
                day_of_week=days.get(given_day.strftime("%A")),
                month_of_year=given_day.month,
                minute=given_day.minute,
                hour=given_day.hour,
            ),
        },
    }

    if not data:
        return jsonify({"error": "Wrong Input"}), 400

    create_email(data)

    return render_template("index.html")


@app.get("/get-email")
def get_email():
    data = get_all_item("email")
    task_result = AsyncResult("b3277dc0-6592-4b57-a3c4-5447af6b7ab1")
    print(task_result.result)
    return jsonify(data), 200


if __name__ == "__main__":
    before_execution()
    app.run(debug=True)
