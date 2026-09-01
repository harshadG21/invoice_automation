from app.services.file_processing_service import process_invoice_file

from app.services.ocr_service import extract_text_as_string

from app.services.invoice_extraction_service import (
    extract_invoice_number,
    extract_invoice_date,
    extract_due_date,
    extract_vendor_name,
    extract_vendor_email,
    extract_vendor_phone,
    extract_vendor_address,
    extract_gst_number,
    extract_pan_number,
    extract_subtotal,
    extract_total_tax,
    extract_total_amount,
    extract_currency
)

def process_invoice(file_id,file_name):

    file_info=process_invoice_file(
        file_id,
        file_name
    )

    file_path = file_info["file_path"]

    raw_text = extract_text_as_string(
        file_path
    )

    invoice_data={
        "invoice_number": extract_invoice_number(raw_text),
        "invoice_date": extract_invoice_date(raw_text),
        "due_date": extract_due_date(raw_text),

        "vendor_name": extract_vendor_name(raw_text),
        "vendor_email": extract_vendor_email(raw_text),
        "vendor_phone": extract_vendor_phone(raw_text),
        "vendor_address": extract_vendor_address(raw_text),

        "gst_number": extract_gst_number(raw_text),
        "pan_number": extract_pan_number(raw_text),

        "subtotal": extract_subtotal(raw_text),
        "tax_amount": extract_total_tax(raw_text),
        "total_amount": extract_total_amount(raw_text),
        "currency": extract_currency(raw_text)
    }

    return invoice_data