from app.extensions.database import db


class Vendor(db.Model):
    __tablename__ = "vendors"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    vendor_name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=True
    )

    phone_number = db.Column(
        db.String(20),
        nullable=True
    )

    address = db.Column(
            db.Text,
            nullable=True
    )

    gst_number=db.Column(
        db.String(50),
        nullable=True
    )

    pan_number=db.Column(
        db.String(20),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )