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

from app.services.validation_service import validate_invoice,validate_invoice_document
from app.services.vendors_services import get_or_create_vendor
from app.services.invoices_services import create_invoice

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

    is_invoice = validate_invoice_document(
        invoice_data
    )

    if not is_invoice:
        return {
            "status": "not_an_invoice",
            "message": "The uploaded document does not appear to be an invoice.",
            "invoice_data": invoice_data
        }

    validation_result = validate_invoice(
        invoice_data
    )

    if not validation_result["is_valid"]:
        return{
            "status":"validation_failed",
            "errors":validation_result["errors"],
            "invoice_data" : invoice_data
        }

    vendor = get_or_create_vendor(
        invoice_data
    )

    invoice = create_invoice(
         invoice_data=invoice_data,
        vendor_id=vendor.id,
        file_name=file_name,
        file_path=file_path,
        ocr_data=raw_text
    )

    return {
        "status": "success",
        "invoice_id": invoice.id,
        "vendor_id": vendor.id,
        "invoice_number": invoice.invoice_number,
        "invoice_data": invoice_data
    }