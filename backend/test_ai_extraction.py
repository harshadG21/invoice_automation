from app.services.ai_extraction_service import extract_invoice_with_ai
from app.services.ocr_service import extract_text_as_string


# Path to the invoice PDF
file_path = "temp/invoices/Invoice_INV-1001.pdf"


# Step 1: Run PaddleOCR
ocr_text = extract_text_as_string(file_path)

print("\n========== OCR TEXT ==========")
print(ocr_text)
print("==============================\n")


# Step 2: Send OCR text to Gemini
invoice_data = extract_invoice_with_ai(ocr_text)


# Step 3: Print the extracted data
print("\n========== GEMINI RESULT ==========")

print("Document Type:", invoice_data.document_type)
print("Invoice Number:", invoice_data.invoice_number)
print("Invoice Date:", invoice_data.invoice_date)
print("Due Date:", invoice_data.due_date)

print("\nVendor:")
print("Name:", invoice_data.vendor.name)
print("Email:", invoice_data.vendor.email)
print("GST:", invoice_data.vendor.gst_number)

print("\nFinancial:")
print("Subtotal:", invoice_data.financial.subtotal)
print("CGST:", invoice_data.financial.cgst)
print("SGST:", invoice_data.financial.sgst)
print("IGST:", invoice_data.financial.igst)
print("Tax Amount:", invoice_data.financial.tax_amount)
print("Total Amount:", invoice_data.financial.total_amount)
print("Currency:", invoice_data.financial.currency)

print("====================================\n")