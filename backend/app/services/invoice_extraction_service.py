import re
from datetime import datetime

from app.schemas.invoice_schema import (
    InvoiceData,
    VendorData,
    FinancialData
)


def extract_invoice_number(text):

    patterns = [
        r"(?:Invoice\s*(?:Number|No\.?|#)|Bill\s*(?:Number|No\.?)|Tax\s*Invoice\s*(?:Number|No\.?))\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9\/\-_]+)",
        r"(?:Reference\s*(?:Number|No\.?)|Document\s*(?:Number|No\.?))\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9\/\-_]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


def parse_date(date_text):

    date_formats = [
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d.%m.%Y",
        "%d-%m-%y",
        "%d/%m/%y"
    ]

    for date_format in date_formats:
        try:
            return datetime.strptime(
                date_text.strip(),
                date_format
            ).date()
        except ValueError:
            continue

    return None


def extract_invoice_date(text):

    patterns = [
        r"(?:Invoice\s*Date|Issue\s*Date|Document\s*Date|Bill\s*Date)\s*[:\-]?\s*(\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4})",
        r"(?<!Due\s)(?<!Payment\s)(?:^|\n)\s*Date\s*[:\-]?\s*(\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4})"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            parsed_date = parse_date(match.group(1))

            if parsed_date:
                return parsed_date

    return None


def extract_due_date(text):

    patterns = [
        r"(?:Due\s*Date|Payment\s*Due(?:\s*Date)?|Due\s*By|Payment\s*Deadline)\s*[:\-]?\s*(\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4})"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            parsed_date = parse_date(match.group(1))

            if parsed_date:
                return parsed_date

    return None


def extract_vendor_name(text):

    patterns = [
        r"Vendor\s*Name\s*[:\-]\s*(.+)",
        r"Supplier\s*Name\s*[:\-]\s*(.+)",
        r"Seller\s*Name\s*[:\-]\s*(.+)"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for index, line in enumerate(lines[:10]):

        upper_line = line.upper()

        if any(keyword in upper_line for keyword in [
            "BILL TO",
            "BILLED TO",
            "CUSTOMER",
            "CLIENT",
            "BUYER",
            "SHIP TO",
            "SOLD TO"
        ]):
            break

        if (
            "TAX INVOICE" not in upper_line
            and "INVOICE" not in upper_line
            and not re.search(r"GSTIN?\s*:", line, re.IGNORECASE)
            and not re.search(r"PAN\s*:", line, re.IGNORECASE)
        ):
            if not re.search(r"^[A-Z\s]+:$", line):
                return line

    return None


def extract_vendor_email(text):

    matches = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
        re.IGNORECASE
    )

    if not matches:
        return None

    return matches[0].strip()


def extract_vendor_phone(text):

    patterns = [
        r"(?:Vendor\s*)?(?:Phone|Mobile|Telephone|Contact)\s*(?:Number)?\s*[:\-]?\s*(\+?\d[\d\s\-()]{8,}\d)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return re.sub(
                r"\s+",
                " ",
                match.group(1).strip()
            )

    return None


def extract_vendor_address(text):

    patterns = [
        r"(?:Vendor\s*)?(?:Address|Registered\s*Address|Office\s*Address)\s*[:\-]\s*(.+)"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    address_parts = []

    for index, line in enumerate(lines[:10]):

        if index == 0:
            continue

        if any(keyword in line.upper() for keyword in [
            "BILL TO",
            "BILLED TO",
            "CUSTOMER",
            "CLIENT",
            "BUYER",
            "INVOICE NO",
            "INVOICE NUMBER",
            "INVOICE DATE",
            "PAYMENT DUE"
        ]):
            break

        if re.search(
            r"\b(?:ROAD|RD|STREET|ST|ROAD|LANE|LN|TOWER|FLOOR|OFFICE|MUMBAI|DELHI|BANGALORE|MAHARASHTRA|INDIA|PIN|-\s*\d{6})\b",
            line,
            re.IGNORECASE
        ):
            address_parts.append(line)

    if address_parts:
        return ", ".join(address_parts)

    return None


def extract_gst_number(text):

    patterns = [
        r"(?:GSTIN|GST\s*Number|GST\s*No\.?)\s*[:\-]?\s*([A-Z0-9]{15})"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip().upper()

    return None


def extract_pan_number(text):

    patterns = [
        r"(?:PAN|PAN\s*Number|PAN\s*No\.?)\s*[:\-]?\s*([A-Z]{5}\d{4}[A-Z])"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip().upper()

    return None


def clean_amount(amount_text):

    amount_text = re.sub(
        r"[^\d.,]",
        "",
        amount_text
    )

    amount_text = amount_text.replace(",", "")

    if not amount_text:
        return None

    return float(amount_text)


def extract_amount_after_label(text, labels):

    label_pattern = "|".join(
        re.escape(label)
        for label in labels
    )

    pattern = rf"(?:{label_pattern})\s*[:\-]?\s*[₹€£$]?\s*([\d,]+(?:\.\d{{1,2}})?)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return clean_amount(match.group(1))

    return None


def extract_subtotal(text):

    return extract_amount_after_label(
        text,
        [
            "Subtotal",
            "Taxable Amount",
            "Taxable Value",
            "Net Amount",
            "Net Total",
            "Amount Before Tax"
        ]
    )


def extract_total_tax(text):

    total_tax = extract_amount_after_label(
        text,
        [
            "Total Tax",
            "Total GST",
            "Total VAT"
        ]
    )

    if total_tax is not None:
        return total_tax

    cgst = extract_amount_after_label(
        text,
        ["CGST"]
    )

    sgst = extract_amount_after_label(
        text,
        ["SGST"]
    )

    igst = extract_amount_after_label(
        text,
        ["IGST"]
    )

    if igst is not None:
        return igst

    if cgst is not None and sgst is not None:
        return cgst + sgst

    if cgst is not None:
        return cgst

    if sgst is not None:
        return sgst

    return None


def extract_total_amount(text):

    return extract_amount_after_label(
        text,
        [
            "Total Amount",
            "Grand Total",
            "Amount Payable",
            "Amount Due",
            "Net Payable",
            "Balance Due",
            "Final Amount",
            "Total"
        ]
    )


def extract_currency(text):

    currency_match = re.search(
        r"Currency\s*[:\-]?\s*(INR|USD|EUR|GBP|AUD|CAD|SGD|AED|JPY)",
        text,
        re.IGNORECASE
    )

    if currency_match:
        return currency_match.group(1).upper()

    total_currency_match = re.search(
        r"(?:TOTAL\s*AMOUNT|GRAND\s*TOTAL|AMOUNT\s*PAYABLE)\s*\(\s*(INR|USD|EUR|GBP|AUD|CAD|SGD|AED|JPY)\s*\)",
        text,
        re.IGNORECASE
    )

    if total_currency_match:
        return total_currency_match.group(1).upper()

    if "₹" in text or re.search(r"\bINR\b|\bRs\.?\b", text, re.IGNORECASE):
        return "INR"

    if "€" in text or re.search(r"\bEUR\b", text, re.IGNORECASE):
        return "EUR"

    if "£" in text or re.search(r"\bGBP\b", text, re.IGNORECASE):
        return "GBP"

    if "$" in text or re.search(r"\bUSD\b", text, re.IGNORECASE):
        return "USD"

    return None


def extract_invoice_data(text):

    invoice_number = extract_invoice_number(text)
    invoice_date = extract_invoice_date(text)
    due_date = extract_due_date(text)

    vendor_name = extract_vendor_name(text)
    vendor_email = extract_vendor_email(text)
    vendor_phone = extract_vendor_phone(text)
    vendor_address = extract_vendor_address(text)
    gst_number = extract_gst_number(text)
    pan_number = extract_pan_number(text)

    subtotal = extract_subtotal(text)
    tax_amount = extract_total_tax(text)
    total_amount = extract_total_amount(text)
    currency = extract_currency(text)

    vendor = VendorData(
        name=vendor_name,
        email=vendor_email,
        phone=vendor_phone,
        address=vendor_address,
        gst_number=gst_number,
        pan_number=pan_number
    )

    financial = FinancialData(
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        currency=currency
    )

    return InvoiceData(
        document_type="invoice",
        invoice_number=invoice_number,
        invoice_date=invoice_date,
        due_date=due_date,
        vendor=vendor,
        financial=financial
    )