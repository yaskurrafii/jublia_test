import db.models as model
from .db import database


def create_email(data):
    email = model.Email(
        subject=data["subject"], content=data["content"], send_time=data["send-time"]
    )

    database.session.add(email)
    database.session.commit()

    recipent = model.Recipent(email_id=email.id, recipent=data["recipient"])

    database.session.add(recipent)
    database.session.commit()
    return True


def get_all_item(name_item):
    model_db = getattr(model, name_item.title())
    data = model_db.query.all()

    result = []
    for item in data:
        email_data = {
            "id": item.id,
            "subject": item.subject,
            "content": item.content,
            "send_time": item.send_time,
            "recipients": [
                {"recipient_email": recipient.recipent}
                for recipient in item.recipients
            ],
        }
        result.append(email_data)
    return result
