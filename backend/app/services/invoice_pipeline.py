from app.services.file_processing_service import process_invoice_file
from app.services.ocr_service import extract_text_as_string
from app.services.invoice_extraction_service import extract_invoice_data
from app.services.ai_extraction_service import extract_invoice_with_ai
from app.services.validation_service import (
    validate_invoice,
    validate_invoice_document
)
from app.services.vendors_services import get_or_create_vendor
from app.services.invoices_services import create_invoice


def process_invoice(file_id, file_name):

    file_info = process_invoice_file(
        file_id,
        file_name
    )

    file_path = file_info["file_path"]

    raw_text = extract_text_as_string(
        file_path
    )

    regex_data = extract_invoice_data(
        raw_text
    )

    if not validate_invoice_document(
        regex_data
    ):
        return {
            "status": "not_an_invoice",
            "message": "The uploaded document does not appear to be an invoice."
        }

    validation_result = validate_invoice(
        regex_data
    )

    if validation_result["is_valid"]:

        invoice_data = regex_data

    else:

        invoice_data = extract_invoice_with_ai(
            raw_text
        )

        if not validate_invoice_document(
            invoice_data
        ):
            return {
                "status": "not_an_invoice",
                "message": "Gemini determined that the document is not an invoice."
            }

        validation_result = validate_invoice(
            invoice_data
        )

        if not validation_result["is_valid"]:
            return {
                "status": "validation_failed",
                "errors": validation_result["errors"],
                "warnings": validation_result["warnings"],
                "invoice_data": invoice_data.model_dump()
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
        "invoice_data": invoice_data.model_dump()
    }