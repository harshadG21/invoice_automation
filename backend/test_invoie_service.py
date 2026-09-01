# Imports Flask so we can create a Flask application context.
from flask import Flask

# Imports the database object.
from app.extensions.database import db

# Imports the Invoice model.
from app.models.invoice import Invoice

# Imports the function we want to test.
from app.services.invoices_services import (
    create_invoice,
    get_invoice_by_number
)


# Creates a Flask application for testing.
app = Flask(__name__)

# Uses your existing SQLite database.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///invoice.db"

# Disables SQLAlchemy modification tracking.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Connects SQLAlchemy with our test Flask application.
db.init_app(app)


# Creates an application context.
with app.app_context():

    # Sample invoice data similar to INV-1001.
    invoice_data = {
        "invoice_number": "TEST-INV-001",
        "invoice_date": "2026-08-26",
        "due_date": "2026-09-10",
        "subtotal": 25000,
        "tax_amount": 4500,
        "total_amount": 29500,
        "currency": "INR"
    }

    # Creates the invoice in the database.
    invoice = create_invoice(
        invoice_data=invoice_data,
        vendor_id=1,
        file_name="Invoice_TEST-001.pdf",
        file_path="temp/invoices/Invoice_TEST-001.pdf",
        ocr_data="Sample OCR text"
    )

    # Prints information about the newly created invoice.
    print("\n===== CREATED INVOICE =====")
    print("ID:", invoice.id)
    print("Invoice Number:", invoice.invoice_number)
    print("Vendor ID:", invoice.vendor_id)
    print("Total:", invoice.total_amount)
    print("Currency:", invoice.currency)

    # Searches for the invoice using its invoice number.
    found_invoice = get_invoice_by_number(
        "TEST-INV-001"
    )

    # Prints the result of the search.
    print("\n===== SEARCH RESULT =====")
    print("Found:", found_invoice is not None)

    # If the invoice was found, print its number.
    if found_invoice:
        print("Invoice Number:", found_invoice.invoice_number)