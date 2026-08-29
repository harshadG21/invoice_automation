from app.services.ocr_service import extract_text_as_string


file_path = "temp/invoices/Invoice_INV-1001.pdf"


text = extract_text_as_string(file_path)


print("\n")
print("=" * 60)
print("EXTRACTED INVOICE TEXT")
print("=" * 60)

print(text)

print("=" * 60)