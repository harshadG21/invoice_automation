from app.services.file_processing_service import process_invoice_file
from app.services.ocr_service import extract_text_as_string
from app.services.ai_extraction_service import extract_invoice_with_ai_with_retry
from app.services.validation_service import (
    validate_invoice,
    validate_invoice_document
)
from app.services.vendors_services import get_or_create_vendor
from app.services.invoices_services import (
    create_invoice,
    is_file_already_processed
)


def process_invoice(file_id, file_name):

    if is_file_already_processed(file_id):

        print("\n========================================")
        print("SKIPPING ALREADY PROCESSED FILE")
        print("========================================")
        print("File:", file_name)
        print("Drive File ID:", file_id)

        return {
            "status": "duplicate",
            "reason": "drive_file_already_processed",
            "message": "File has already been processed",
            "file_name": file_name,
            "drive_file_id": file_id
        }

    file_info = process_invoice_file(
        file_id,
        file_name
    )

    file_path = file_info["file_path"]

    raw_text = extract_text_as_string(
        file_path
    )

    invoice_data = extract_invoice_with_ai_with_retry(
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

    try:

        invoice = create_invoice(
            invoice_data=invoice_data,
            vendor_id=vendor.id,
            file_name=file_name,
            file_path=file_path,
            ocr_data=raw_text,
            drive_file_id=file_id
        )

    except ValueError as e:

        if "Duplicate invoice detected" in str(e):

            print("\n========================================")
            print("DUPLICATE INVOICE - SKIPPING")
            print("========================================")
            print("Invoice:", invoice_data.invoice_number)
            print("Message:", e)

            return {
                "status": "duplicate",
                "reason": "duplicate_invoice",
                "message": str(e),
                "invoice_number": invoice_data.invoice_number
            }

        raise

    return {
        "status": "success",
        "invoice_id": invoice.id,
        "vendor_id": vendor.id,
        "invoice_number": invoice.invoice_number,
        "invoice_data": invoice_data.model_dump()
    }