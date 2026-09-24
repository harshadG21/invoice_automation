from app.models.invoice import Invoice
from app.extensions.database import db
from datetime import datetime
from app.models.processing_log import ProcessingLog


def get_invoice_by_number(invoice_number):

    if not invoice_number:
        return None

    return Invoice.query.filter_by(
        invoice_number=invoice_number
    ).first()

def is_file_already_processed(drive_file_id):

    if not drive_file_id:
        return False
    
    existing_invoice = Invoice.query.filter_by(
        drive_file_id=drive_file_id
    ).first()

    return existing_invoice is not None


def create_invoice(
    invoice_data,
    vendor_id,
    user_id,
    file_name=None,
    file_path=None,
    ocr_data=None,
    drive_file_id=None,
):

    existing_invoice = Invoice.query.filter_by(
        invoice_number =invoice_data.invoice_number,
        vendor_id=vendor_id
    ).first()

    if existing_invoice:

        raise ValueError(
            f"Duplicate invoice detected: "
            f"{invoice_data.invoice_number} "
            f"already exists for this vendor." 
        )

    invoice = Invoice(
        invoice_number=invoice_data.invoice_number,
        vendor_id=vendor_id,
        user_id=user_id,
        invoice_date=invoice_data.invoice_date,
        due_date=invoice_data.due_date,
        subtotal=invoice_data.financial.subtotal,
        tax_amount=invoice_data.financial.tax_amount,
        total_amount=invoice_data.financial.total_amount,
        currency=invoice_data.financial.currency,
        file_name=file_name,
        file_path=file_path,
        drive_file_id=drive_file_id,
        ocr_data=ocr_data,
        payment_status="unpaid"
    )

    db.session.add(invoice)

    try:
        db.session.flush()

        processing_log = ProcessingLog(
            invoice_id=invoice.id,
            process_type="invoice_processing",
            status="completed",
            message="Invoice processed and saved successfully.",
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )

        db.session.add(processing_log)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return invoice