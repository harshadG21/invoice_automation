from app.services.validation_service import (
    validate_invoice_document,
    validate_invoice
)


# ---------------------------------------------------------
# TEST 1: CHECK WHETHER DOCUMENT IS AN INVOICE
# ---------------------------------------------------------

# Sample data extracted from our real invoice.
invoice_data = {

    # Invoice-specific fields.
    "invoice_number": "INV-1001",
    "invoice_date": "2026-08-26",
    "due_date": "2026-09-10",
    "vendor_name": "Tech Solutions Pvt. Ltd.",
    "vendor_email": "billing@techsolutions.com",

    # Financial fields.
    "subtotal": 25000.0,
    "tax_amount": 4500.0,
    "total_amount": 29500.0,
    "currency": "INR"
}


# Check whether the document looks like an invoice.
is_invoice = validate_invoice_document(
    invoice_data
)


print("INVOICE DOCUMENT TEST:")
print("-" * 40)
print("Is Invoice:", is_invoice)


# ---------------------------------------------------------
# TEST 2: VALIDATE THE INVOICE DATA
# ---------------------------------------------------------

# Validate all fields inside the invoice.
validation_result = validate_invoice(
    invoice_data
)


print("\nINVOICE VALIDATION TEST:")
print("-" * 40)
print("Is Valid:", validation_result["is_valid"])
print("Errors:", validation_result["errors"])


# ---------------------------------------------------------
# TEST 3: NON-INVOICE DOCUMENT
# ---------------------------------------------------------

# Simulate data extracted from a non-invoice document.
non_invoice_data = {

    "employee_name": "Rahul Sharma",
    "employee_id": "EMP-1023",
    "department": "Finance",
    "salary": 50000
}


# Check whether this document is an invoice.
is_invoice = validate_invoice_document(
    non_invoice_data
)


print("\nNON-INVOICE DOCUMENT TEST:")
print("-" * 40)
print("Is Invoice:", is_invoice)