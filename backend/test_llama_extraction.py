from app.services.ai_extraction_service import extract_invoice_with_llama


# Sample OCR text
ocr_text = """
TAX INVOICE

Invoice Number: INV-1003
Invoice Date: 2026-09-14
Due Date: 2026-09-29

Bright Web Studio LLP
accounts@brightwebstudio.in
GSTIN: 29AAECB5678G1Z3

Description:
Web Development Services

Subtotal: 101000

CGST 9%: 9090
SGST 9%: 9090

Total Tax: 18180

Grand Total: 119180

Currency: INR
"""


print("\n========== LLAMA EXTRACTION TEST ==========")

try:

    invoice_data = extract_invoice_with_llama(
        ocr_text
    )

    print("\nLlama extraction successful!")

    print("Invoice Number:", invoice_data.invoice_number)
    print("Invoice Date:", invoice_data.invoice_date)
    print("Vendor:", invoice_data.vendor.name)

    print("\nFinancial:")
    print("Subtotal:", invoice_data.financial.subtotal)
    print("CGST:", invoice_data.financial.cgst)
    print("SGST:", invoice_data.financial.sgst)
    print("IGST:", invoice_data.financial.igst)
    print("Tax Amount:", invoice_data.financial.tax_amount)
    print("Total Amount:", invoice_data.financial.total_amount)

except Exception as error:

    print("\nLlama extraction failed:")
    print(error)