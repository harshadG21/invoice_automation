from datetime import datetime

from app.extensions.database import db
from app.models.invoice import Invoice
from app.models.processing_log import ProcessingLog
from app.services.vendors_services import get_or_create_vendor

def save_invoice(invoice_data,file_name,file_path,ocr_text):

    try:
        vendor = get_or_create_vendor(invoice_data)

        invoice = Invoice(
            invoice_number=invoice_data.invoice_number or "UNKNOWN",
            vendor_id=vendor.id,
            invoice_date=invoice_data.invoice_date,
            due_date=invoice_data.due_date,
            subtotal=invoice_data.financial.subtotal,
            tax_amount=invoice_data.financial.tax_amount,
            total_amount=invoice_data.financial.total_amount,
            currency=invoice_data.financial.currency or "INR",
            file_name=file_name,
            file_path=file_path,
            status="processed",
            ocr_data=ocr_text
        )

        db.session.add(invoice)

        db.session.flush()

        processing_log = ProcessingLog(
            invoice_id = invoice.id,
            process_type="invoice_processing",
            status="completed",
            message="Invoice processed and saved successfully.",
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )

        db.session.add(processing_log)

        db.session.commit()

        return invoice

    except Exception as e:

        print("\n❌ DATABASE ERROR:")
        print(type(e).__name__)
        print(e)

        db.session.rollback()
        raise