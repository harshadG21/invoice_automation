from datetime import datetime

from app.extensions.database import db
from app.models.invoice import Invoice
from app.models.processing_log import ProcessingLog
from app.services.vendors_services import get_or_create_vendor
from app.services.validation_service import validate_invoice

def save_invoice(invoice_data,file_name,file_path,ocr_text,drive_file_id):

    print("\n========== EXTRACTED INVOICE DATA ==========")
    print("Invoice Number:", invoice_data.invoice_number)
    print("Invoice Date:", invoice_data.invoice_date)
    print("Vendor:", invoice_data.vendor.name)
    print("Subtotal:", invoice_data.financial.subtotal)
    print("Tax Amount:", invoice_data.financial.tax_amount)
    print("Total Amount:", invoice_data.financial.total_amount)
    print("Currency:", invoice_data.financial.currency)
    print("============================================\n")

    validation_result = validate_invoice(invoice_data)

    if not validation_result["is_valid"]:

        print("\n Invoice Validation Failed")

        for error in validation_result["errors"]:
            print(f"-{error}")

        raise ValueError(
            "Invoice Validation Failed: "
            + ";".join(validation_result["errors"])
        )

    print(" Invoice validation passed ")

    if validation_result["warnings"]:
        print("\n Invoice Warnings")

        for warning in validation_result["warnings"]:
            print(f"-{warning}")

    try:
        vendor = get_or_create_vendor(invoice_data)

        existing_file = Invoice.query.filter_by(
            drive_file_id=drive_file_id
        ).first()

        if existing_file:
            print("Duplicate Google Drive File Detected")
            print(f"Drive File Id:{drive_file_id}")
            print(f"Existing Invoice ID:{existing_file.id}")
            raise ValueError(
                "This Google Drive File has already been processed"
            )

        existing_invoice = Invoice.query.filter_by(
            invoice_number = invoice_data.invoice_number,
            vendor_id = vendor.id
        ).first()

        if existing_invoice:
            print("Duplicate Invoice Detected")
            print(f"Invoice Number: {existing_invoice.invoice_number}")
            print(f"Existing Invoice ID: {existing_invoice.id}")

            raise ValueError(
                f"Duplicate Invoice detected"
                f"{invoice_data.invoice_number}"
                f"already exists for this vendor"
            )

        invoice = Invoice(
            invoice_number=invoice_data.invoice_number or "UNKNOWN",
            vendor_id=vendor.id,
            invoice_date=invoice_data.invoice_date,
            due_date=invoice_data.due_date,
            subtotal=invoice_data.financial.subtotal,
            tax_amount=invoice_data.financial.tax_amount,
            total_amount=invoice_data.financial.total_amount,
            currency=invoice_data.financial.currency or "INR",
            file_name=file_name,
            file_path=file_path,
            drive_file_id=drive_file_id,
            ocr_data=ocr_text
        )

        db.session.add(invoice)

        db.session.flush()

        processing_log = ProcessingLog(
            invoice_id = invoice.id,
            process_type="invoice_processing",
            status="completed",
            message="Invoice processed and d successfully.",
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )

        db.session.add(processing_log)

        db.session.commit()

        return invoice

    except Exception as e:

        print("\n DATABASE ERROR:")
        print(type(e).__name__)
        print(e)

        db.session.rollback()
        raise