from app import create_app
from app.extensions.database import db
from app.models.vendor import Vendor
from app.models.invoice import Invoice
from app.models.processing_log import ProcessingLog


app = create_app()

with app.app_context():

    print("\n========== VENDORS ==========")

    vendors = Vendor.query.all()

    for vendor in vendors:
        print(
            f"ID: {vendor.id} | "
            f"Name: {vendor.vendor_name} | "
            f"Email: {vendor.email} | "
            f"GST: {vendor.gst_number}"
        )


    print("\n========== INVOICES ==========")

    invoices = Invoice.query.all()

    for invoice in invoices:
        print(
            f"ID: {invoice.id} | "
            f"Invoice No: {invoice.invoice_number} | "
            f"Vendor ID: {invoice.vendor_id} | "
            f"Total: {invoice.total_amount}"
        )


    print("\n========== PROCESSING LOGS ==========")

    logs = ProcessingLog.query.all()

    for log in logs:
        print(
            f"ID: {log.id} | "
            f"Invoice ID: {log.invoice_id} | "
            f"Type: {log.process_type} | "
            f"Status: {log.status}"
        )