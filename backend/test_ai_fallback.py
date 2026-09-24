from app.services.ai_extraction_service import (
    extract_invoice_with_ai_with_retry
)


# Sample OCR text
ocr_text = """
TAX INVOICE

Invoice Number: INV-1003
Invoice Date: 2026-09-14
Due Date: 2026-09-29

FROM:
Bright Web Studio LLP
accounts@brightwebstudio.in
GSTIN: 29AAECB5678G1Z3

BILL TO:
Customer Name: Skyline Hospitality Group
Email: accounts@skylinehospitality.com
Address: Bandra West, Mumbai, Maharashtra - 400050

Description:
Web Development Services

Subtotal: 101000

CGST 9%: 9090
SGST 9%: 9090

Total Tax: 18180
Grand Total: 119180

Currency: INR
"""

print("\n========================================")
print("       AI FALLBACK TEST")
print("========================================")


try:

    invoice_data = extract_invoice_with_ai_with_retry(
        ocr_text
    )

    print("\n========== FINAL RESULT ==========")

    print(
        "Invoice Number:",
        invoice_data.invoice_number
    )

    print("\n========== VENDOR DEBUG ==========")

    print("Vendor object:", invoice_data.vendor)

    print(
    "Vendor Name:",
    invoice_data.vendor.name
)

    print(
    "Vendor Email:",
    invoice_data.vendor.email
)

    print(
    "Vendor Address:",
    invoice_data.vendor.address
)

    print(
    "Vendor GST:",
    invoice_data.vendor.gst_number
)

    print(
    "Vendor PAN:",
    invoice_data.vendor.pan_number
)

    print("==================================")

    print(
        "Subtotal:",
        invoice_data.financial.subtotal
    )

    print(
        "CGST:",
        invoice_data.financial.cgst
    )

    print(
        "SGST:",
        invoice_data.financial.sgst
    )

    print(
        "Tax Amount:",
        invoice_data.financial.tax_amount
    )

    print(
        "Total Amount:",
        invoice_data.financial.total_amount
    )

    print("=================================")

except Exception as error:

    print("\nAI extraction failed:")
    print(error)
