from app.models.invoice import Invoice
from app.extensions.database import db

#serches the invoices table using the invoice number
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

        invoice_number = invoice_data.get("invoice_number") ,#store invoice number
        vendor_id = vendor_id,
        invoice_date = invoice_data.get("invoice_date"),
        due_date=invoice_data.get("due_date"),
        subtotal=invoice_data.get("subtotal"),
        tax_amount = invoice_data.get("tax_amount"),
        total_amount =  invoice_data.get("total_amount"),
        currency =  invoice_data.get("currency"),
        file_name = file_name,
        file_path = file_path,
        ocr_data=ocr_data,
        status = "received"        
    )

    db.session.add(invoice)

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return invoice
