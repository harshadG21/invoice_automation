from app.models.invoice import Invoice
from app.extensions.database import db


def get_invoice_by_number(invoice_number):

    if not invoice_number:
        return None

    return Invoice.query.filter_by(
        invoice_number=invoice_number
    ).first()


def create_invoice(
    invoice_data,
    vendor_id,
    file_name=None,
    file_path=None,
    ocr_data=None,
):

    invoice = Invoice(
        invoice_number=invoice_data.invoice_number,
        vendor_id=vendor_id,
        invoice_date=invoice_data.invoice_date,
        due_date=invoice_data.due_date,
        subtotal=invoice_data.financial.subtotal,
        tax_amount=invoice_data.financial.tax_amount,
        total_amount=invoice_data.financial.total_amount,
        currency=invoice_data.financial.currency,
        file_name=file_name,
        file_path=file_path,
        ocr_data=ocr_data,
        status="received"
    )

    db.session.add(invoice)

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return invoice