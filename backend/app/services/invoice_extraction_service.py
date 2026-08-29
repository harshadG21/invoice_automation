"""
Raw OCR text
     ↓
Extract fields
     ↓
Validate fields
     ↓
Create/update Invoice
     ↓
Database
"""

import re 
from datetime import datetime

#extract invoice number
def extract_invoice_numbers(text):

    pattern= r"Invoice Number:\s*([A-Za-z0-9\-]+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return None


# to extract date
def extract_invoice_date(text):

    pattern= r"Invoice Date:\s*(\d{2}-\d{2}-\d{4})"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return datetime.strptime(
            match.group(1),
            "%d-%m-%Y"
        ).date()

#to extract Due Date

def extract_due_date(text):

    pattern = r"Due Date:\s(\d{2}-\d{2}-\d{4})"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return datetime.strptime(
                    match.group(1),
                    "%d-%m-%Y"
                ).date()

    return None


def extract_vendor_name(text):
    pattern = r"Vendor Name:\s*(.+)"
    match = re.search(pattern,text,re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def extract_vendor_email(text):

    pattern = r"Email:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})"
    # Searches for a standard email address after "Email:".

    matches=re.findall(pattern,text,re.IGNORECASE) # findall because incase 2 emails

    if len(matches) >= 2:
        return matches[1].strip() #returns second mail as second mail is vendors
    return None

def extract_vendor_phone(text):

    pattern=r"Phone:\s*([+\d][\d\s\-]{8,})" # supports value like +91 xxxxxxxxx
    matches = re.search(
        pattern,
        text,
        re.IGNORECASE
    )
    if matches:
        return matches.group(1).strip()
    return None

def extract_vendor_address(text):

    pattern = r"Address:\s*(.+)" #searches ater address

    matches = re.findall(
        pattern,
        text,
        re.IGNORECASE
    ) # finds both customer and vendor address

    if len(matches) >= 2:
        return matches[1].strip() # return vendor's address
    return None

def extract_gst_number(text):

    pattern = r"GST Number:\s*([A-Z0-9]{15})" #searches for 15-character GST number
    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )
    if match:
        return match.group(1).strip().upper() # upper() ensures it is stored in uppercase.
    return None

def extract_pan_number(text):

    pattern = r"PAN Number:\s*([A-Z]{5}\d{4}[A-Z])" # Searches for the standard 10-character PAN format.
    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )
    if match:
        return match.group(1).strip().upper() # Returns the PAN number in uppercase.
    return None

def clean_amount(amount_text):

    amount_text = re.sub(r"[^\d.,]","", amount_text) #remove currancy symbols 
    amount_text = amount_text.replace(",","") # remove thousand sepaerators
    return float(amount_text) 

def extract_subtotal(text):

    pattern = r"(?:Subtotal)[\s\n]*[₹€$]?\s*([\d,]+(?:\.\d{1,2})?)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return clean_amount(match.group(1))
    return None

def extract_total_tax(text):

    pattern = r"(?:Total Tax)[\s\n]*[₹€$]?\s*([\d,]+(?:\.\d{1,2})?)"
    match = re.search(pattern,text,re.IGNORECASE)
    if match:
        return clean_amount(match.group(1))
    return None

def extract_total_amount(text):

    pattern = r"OTAL AMOUNT\s*\(INR\)[\s\n]*₹?\s*([\d,]+(?:\.\d{1,2})?)"
    match = re.search(pattern,text,re.IGNORECASE) 
    if match:
        return clean_amount(match.group(1))
    return None

def extract_currency(text):
    pattern = r"TOTAL AMOUNT\s*\((INR|USD|EUR|GBP)\)" #currency explicitly written beside TOTAL AMOUNT
    match = re.search(pattern,text,re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return "INR"    
