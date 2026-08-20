from app.extensions.database import db 

class EmailLog(db.Model):
    __tablename__= "email_logs"


    id=db.Column(
        db.Integer,
        primary_key=True
    )

    invoice_id=db.Column(
        db.Integer,
        db.ForeignKey("invoices.id")

    )

    recipient_email = db.Column(
        db.String(150),
        nullable=False
    )

    subject=db.Column(
        db.String(255),
        nullable=True
    )

    email_type=db.Column(
      db.String(50),
      nullable=True
    )

    status=db.Column(
        db.String(30),
        nullable=False,
        default="pending"
    )

    sent_at=db.Column(
        db.DateTime,
        nullable=True
    )

    error_message=db.Column(
        db.Text,
        nullable=True
    )

    created_at=db.Column(
        db.DateTime,
        server_default=db.func.now()
    )