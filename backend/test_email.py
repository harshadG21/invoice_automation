from app import create_app
from app.models.invoice import Invoice
from app.services.email_service import send_invoice_email


app = create_app()


with app.app_context():

    invoice = Invoice.query.first()

    if not invoice:
        print("No invoice found in database.")
    else:

        send_invoice_email(
            invoice=invoice,
            recipient_email="harshadgori0@gmail.com"
        )

        print(
            f"Invoice email sent for invoice ID: {invoice.id}"
        )