from app import create_app

from app.extensions.database import db
from app.models.invoice import Invoice

from app.services.verification_service import (
    create_verification,
    get_verification_by_invoice_id
)


# Create the Flask application.
app = create_app()


# Use the Flask application context so SQLAlchemy can access the database.
with app.app_context():

    # Find the first invoice in the database.
    invoice = Invoice.query.first()

    # Stop the test if there are no invoices.
    if not invoice:
        print("No invoice found in database.")
        exit()

    print("INVOICE FOUND:")
    print("----------------------------------------")
    print("Invoice ID:", invoice.id)
    print("Invoice Number:", invoice.invoice_number)


    # Create a verification record for this invoice.
    verification = create_verification(
        invoice_id=invoice.id,
        verification_status="verified",
        remarks="Invoice passed initial verification.",
        ai_confidence=95.00
    )


    print("\nVERIFICATION CREATED:")
    print("----------------------------------------")
    print("Verification ID:", verification.id)
    print("Invoice ID:", verification.invoice_id)
    print("Status:", verification.verification_status)
    print("Remarks:", verification.remarks)
    print("AI Confidence:", verification.ai_confidence)


    # Search for the verification record using the invoice ID.
    found_verification = get_verification_by_invoice_id(
        invoice.id
    )


    print("\nVERIFICATION FOUND:")
    print("----------------------------------------")
    print("Verification ID:", found_verification.id)
    print("Status:", found_verification.verification_status)