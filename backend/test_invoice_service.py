from app.services.ocr_service import extract_text_as_string
from app.services.invoice_extraction_service import (
    extract_invoice_number,
    extract_invoice_date,
    extract_due_date,
    extract_vendor_address,
    extract_vendor_name,
    extract_vendor_phone,
    extract_vendor_email,
    extract_gst_number,
    extract_pan_number,
    extract_subtotal,
    extract_total_tax,
    extract_total_amount,
    extract_currency
)


file_path = "temp/invoices/Invoice_INV-1001.pdf"


# Get OCR text
text = extract_text_as_string(file_path)


print("\nINVOICE NUMBER:")
print(extract_invoice_number(text))

print("\nINVOICE DATE:")
print(extract_invoice_date(text))

print("\nDUE DATE:")
print(extract_due_date(text))

print("\nVENDOR NAME:")
print(extract_vendor_name(text))
# Extracts and prints the vendor name.


print("\nVENDOR EMAIL:")
print(extract_vendor_email(text))
# Extracts and prints the vendor email.


print("\nVENDOR PHONE:")
print(extract_vendor_phone(text))
# Extracts and prints the vendor phone number.


print("\nVENDOR ADDRESS:")
print(extract_vendor_address(text))
# Extracts and prints the vendor address.


print("\nGST NUMBER:")
print(extract_gst_number(text))
# Extracts and prints the GST number.


print("\nPAN NUMBER:")
print(extract_pan_number(text))
# Extracts and prints the PAN number.

print("\nSUBTOTAL:")
print(extract_subtotal(text))
# Extracts the invoice subtotal.


print("\nTOTAL TAX:")
print(extract_total_tax(text))
# Extracts the combined CGST + SGST amount.


print("\nTOTAL AMOUNT:")
print(extract_total_amount(text))
# Extracts the final amount payable.


print("\nCURRENCY:")
print(extract_currency(text))
# Extracts the invoice currency.