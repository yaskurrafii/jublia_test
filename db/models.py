from sqlalchemy import ForeignKey, String, Integer, Column, PrimaryKeyConstraint, Text
from sqlalchemy.orm import relationship
from .db import database


class Email(database.Model):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    subject = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    send_time = Column(Text, nullable=False)

    recipients = relationship("Recipent", back_populates="email")


class Recipent(database.Model):
    __tablename__ = "recipent"

    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    recipent = Column(String(30), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("email_id", "recipent", name="pk_recipent"),)

    email = relationship("Email", back_populates="recipients")
