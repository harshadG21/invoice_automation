import re 

def validate_invoice_document(invoice_data):

    invoice_indicators=[
       "invoice_number",
        "invoice_date",
        "vendor_name",
        "subtotal",
        "total_amount", 
    ]

    found_indicators = 0

    for field in invoice_indicators:

        value = invoice_data.get(field)

        if value is not None and value != "":
            found_indicators += 1

    if found_indicators >= 3:
        return True

    return False 

# Validate that all mandatory invoice fields are present.
def validate_required_fields(invoice_data):

    required_fields=[
       "invoice_number",
        "invoice_date",
        "due_date",
        "vendor_name",
        "vendor_email",
        "subtotal",
        "tax_amount",
        "total_amount",
        "currency", 
    ]

    missing_fields=[]

    for field in required_fields:
        value = invoice_data.get(field)

        if value is None or value == "":
            missing_fields.append(field)

    return missing_fields



def validate_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern,email))

def validate_gst_number(gst_number):

    pattern = r"^\d{2}[A-Z]{5}\d{4}[A-Z]\d[Z][A-Z0-9]$"
    return bool(re.match(pattern,gst_number))

def validate_pan_number(pan_number):

    pattern = r"^[A-Z]{5}\d{4}[A-Z]$"
    return bool(re.match(pattern,pan_number))

def validate_amounts(invoice_data):

    subtotal = invoice_data.get("subtotal")
    tax_amount = invoice_data.get("tax_amount")
    total_amount = invoice_data.get("total_amount")

    if subtotal is None or tax_amount is None or total_amount is None:
        return False

    expected_total = subtotal + tax_amount

    return round(expected_total,2)==round(total_amount,2)

def validate_invoice(invoice_data):

    errors = []
    missing_field=validate_required_fields(invoice_data)

    for field in missing_field:
        errors.append(f"Missing required field: {field}")

    if invoice_data.get("vendor_email"):
        if not validate_email(invoice_data["vendor_email"]):
            errors.append("Invalid vendor email")

    if invoice_data.get("gst_number"):
        if not validate_gst_number(invoice_data["gst_number"]):
            errors.append("Invalid GST number")

    if invoice_data.get("pan_number"):
        if not validate_pan_number(invoice_data["pan_number"]):
            errors.append("Invalid PAN number")

    if not validate_amounts(invoice_data):
        errors.append("Subtotal + tax does not equal total amount")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }