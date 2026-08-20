from app.extensions.database import db


class Verification(db.Model):
    __tablename__ = "verification"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    invoice_id = db.Column(
        db.Integer,
        db.ForeignKey("invoices.id"),
        nullable=False
    )

    verified_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    verification_status = db.Column(
        db.String(50),
        nullable=False,
        default="pending"
    )

    remarks = db.Column(
        db.Text,
        nullable=True
    )

    ai_confidence = db.Column(
        db.Numeric(5, 2),
        nullable=True
    )

    verified_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )