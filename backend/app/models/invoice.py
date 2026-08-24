from app.extensions.database import db


class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    invoice_number = db.Column(
        db.String(100),
        nullable=False
    )

    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey("vendors.id"),
        nullable=True
    )

    invoice_date = db.Column(
        db.Date,
        nullable=True
    )

    due_date = db.Column(
            db.Date,
            nullable=True
    )

    subtotal=db.Column(
        db.Numeric(12,2),
        nullable=True
    )

    tax_amount=db.Column(
        db.Numeric(12,2),
        nullable=True
    )

    total_amount=db.Column(
            db.Numeric(12,2),
            nullable=True
        )

    currency=db.Column(
            db.String(255),
            nullable=True,
            default="INR"
    )

    file_name = db.Column(
        db.String(255),
        nullable=True
    )

    file_path = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="received"
    )

    ocr_data = db.Column(
        db.Text,
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