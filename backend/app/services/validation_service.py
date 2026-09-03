import re
from datetime import date

from app.schemas.invoice_schema import InvoiceData


def validate_invoice_document(invoice_data):

    if isinstance(invoice_data, InvoiceData):
        return invoice_data.document_type == "invoice"

    return False


def validate_required_fields(invoice_data):

    missing_fields = []

    if invoice_data.invoice_number is None:
        missing_fields.append("invoice_number")

    if invoice_data.invoice_date is None:
        missing_fields.append("invoice_date")

    if invoice_data.vendor.name is None:
        missing_fields.append("vendor.name")

    if invoice_data.financial.total_amount is None:
        missing_fields.append("financial.total_amount")

    return missing_fields


def validate_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return bool(re.match(pattern, email))


def validate_gst_number(gst_number):

    pattern = r"^\d{2}[A-Z]{5}\d{4}[A-Z]\d[Z][A-Z0-9]$"

    return bool(
        re.match(
            pattern,
            gst_number.upper()
        )
    )


def validate_pan_number(pan_number):

    pattern = r"^[A-Z]{5}\d{4}[A-Z]$"

    return bool(
        re.match(
            pattern,
            pan_number.upper()
        )
    )


def validate_amounts(invoice_data):

    subtotal = invoice_data.financial.subtotal
    tax_amount = invoice_data.financial.tax_amount
    total_amount = invoice_data.financial.total_amount

    if total_amount is None:
        return True

    if subtotal is None or tax_amount is None:
        return True

    expected_total = subtotal + tax_amount

    return round(expected_total, 2) == round(total_amount, 2)


def validate_dates(invoice_data):

    errors = []

    invoice_date = invoice_data.invoice_date
    due_date = invoice_data.due_date

    if invoice_date and invoice_date > date.today():
        errors.append("Invoice date is in the future")

    if invoice_date and due_date:
        if due_date < invoice_date:
            errors.append("Due date is before invoice date")

    return errors


def validate_invoice(invoice_data):

    errors = []
    warnings = []

    missing_fields = validate_required_fields(
        invoice_data
    )

    for field in missing_fields:
        errors.append(
            f"Missing required field: {field}"
        )

    vendor = invoice_data.vendor
    financial = invoice_data.financial

    if vendor.email:

        if not validate_email(vendor.email):
            errors.append(
                "Invalid vendor email"
            )

    if vendor.gst_number:

        if not validate_gst_number(
            vendor.gst_number
        ):
            errors.append(
                "Invalid GST number"
            )

    if vendor.pan_number:

        if not validate_pan_number(
            vendor.pan_number
        ):
            errors.append(
                "Invalid PAN number"
            )

    if financial.subtotal is not None:
        if financial.subtotal < 0:
            errors.append(
                "Subtotal cannot be negative"
            )

    if financial.tax_amount is not None:
        if financial.tax_amount < 0:
            errors.append(
                "Tax amount cannot be negative"
            )

    if financial.total_amount is not None:
        if financial.total_amount < 0:
            errors.append(
                "Total amount cannot be negative"
            )

    if not validate_amounts(invoice_data):

        errors.append(
            "Subtotal + tax does not equal total amount"
        )

    errors.extend(
        validate_dates(invoice_data)
    )

    if invoice_data.due_date is None:
        warnings.append(
            "Due date is missing"
        )

    if vendor.email is None:
        warnings.append(
            "Vendor email is missing"
        )

    if vendor.phone is None:
        warnings.append(
            "Vendor phone is missing"
        )

    if vendor.address is None:
        warnings.append(
            "Vendor address is missing"
        )

    if vendor.gst_number is None:
        warnings.append(
            "Vendor GST number is missing"
        )

    if vendor.pan_number is None:
        warnings.append(
            "Vendor PAN number is missing"
        )

    if financial.subtotal is None:
        warnings.append(
            "Subtotal is missing"
        )

    if financial.tax_amount is None:
        warnings.append(
            "Tax amount is missing"
        )

    if financial.currency is None:
        warnings.append(
            "Currency is missing"
        )

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }