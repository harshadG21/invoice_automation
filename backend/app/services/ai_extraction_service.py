from google import genai
from google.genai import types

from app.config import Config
from app.schemas.invoice_schema import InvoiceData


GEMINI_API_KEY = Config.GEMINI_API_KEY

GEMINI_MODEL = Config.GEMINI_MODEL


# Create the Gemini client.
# The client is created only when the API key exists.
if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )
else:
    client = None


# ---------------------------------------------------------
# INVOICE EXTRACTION PROMPT
# ---------------------------------------------------------

INVOICE_EXTRACTION_PROMPT = """
You are an expert invoice document extraction system.

Your job is to analyze OCR text from a financial document
and extract accurate structured invoice information.

The invoice can come from ANY company, country, vendor,
industry, or invoice layout.

Do NOT rely on one fixed invoice format.

---------------------------------------------------------
DOCUMENT TYPE
---------------------------------------------------------

Determine whether the document is actually an invoice.

If it is an invoice:
document_type = "invoice"

If it is not an invoice:
document_type = "not_an_invoice"

Do not classify a document as an invoice simply because
it contains numbers, dates, prices, or company names.

---------------------------------------------------------
VENDOR
---------------------------------------------------------

The vendor is the SELLER / ISSUER of the invoice.

The vendor is NOT necessarily the company appearing under:

- BILL TO
- BILLED TO
- CUSTOMER
- CLIENT
- BUYER
- SHIP TO
- SOLD TO

Example:

ABC Digital Services

BILL TO:
Global Retail Solutions Pvt. Ltd.

Correct:
vendor_name = ABC Digital Services

Incorrect:
vendor_name = Global Retail Solutions Pvt. Ltd.

The vendor is the company that issued the invoice.

Extract:

- Vendor name
- Vendor email
- Vendor phone
- Vendor address
- GST number / GSTIN
- PAN number

Do not confuse customer, buyer, shipping, or bank
information with vendor information.

---------------------------------------------------------
INVOICE NUMBER
---------------------------------------------------------

Possible labels include:

- Invoice No
- Invoice Number
- Invoice #
- Bill No
- Bill Number
- Tax Invoice No
- Tax Invoice Number
- Reference No
- Reference Number
- Document Number

Understand the meaning rather than depending on one
exact label.

Preserve the invoice number as it appears on the document.

---------------------------------------------------------
INVOICE DATE
---------------------------------------------------------

Possible labels include:

- Invoice Date
- Bill Date
- Date
- Issue Date
- Document Date

Extract the actual invoice date.

Return it as:

YYYY-MM-DD

Never invent a date.

---------------------------------------------------------
DUE DATE
---------------------------------------------------------

Possible labels include:

- Due Date
- Payment Due
- Payment Due Date
- Due By
- Payment Deadline
- Pay Before

Return the date as:

YYYY-MM-DD

If there is no due date, return null.

---------------------------------------------------------
SUBTOTAL
---------------------------------------------------------

Possible labels include:

- Subtotal
- Taxable Amount
- Taxable Value
- Net Amount
- Net Total
- Amount Before Tax
- Taxable Base

These can represent the amount before tax.

Store the value in:

financial.subtotal

Remove currency symbols and commas.

Example:

₹48,000

becomes:

48000

---------------------------------------------------------
TAX
---------------------------------------------------------

Tax can appear as:

- Tax
- Total Tax
- GST
- VAT
- CGST
- SGST
- IGST

If CGST and SGST are both present:

tax_amount = CGST + SGST

Example:

CGST = 4320
SGST = 4320

tax_amount = 8640

If IGST is present:

tax_amount = IGST

If the invoice explicitly provides a total tax amount,
use that value.

Do not double-count taxes.

---------------------------------------------------------
TOTAL AMOUNT
---------------------------------------------------------

Possible labels include:

- Total
- Total Amount
- Grand Total
- Amount Payable
- Amount Due
- Net Payable
- Balance Due
- Final Amount

Identify the final amount that the customer is expected
to pay.

Store it as:

financial.total_amount

Remove currency symbols and commas.

---------------------------------------------------------
CURRENCY
---------------------------------------------------------

Identify the currency from:

- Currency code
- Currency symbol
- Explicit currency name

Examples:

₹ → INR

Rs / INR → INR

$ → USD when the context clearly indicates USD

€ → EUR

£ → GBP

Do not guess the currency when the evidence is ambiguous.

Return null when it cannot be confidently determined.

---------------------------------------------------------
GENERAL RULES
---------------------------------------------------------

Use the meaning and context of the entire invoice.

Do NOT simply extract:

- the first company name
- the first date
- the first large number

Understand the relationship between:

vendor
customer
invoice number
dates
subtotal
tax
total
currency

before assigning values.

Never invent information.

If information is not present or cannot be confidently
determined, return null.

---------------------------------------------------------
OCR TEXT
---------------------------------------------------------

Analyze the following OCR text:
"""


# ---------------------------------------------------------
# AI EXTRACTION FUNCTION
# ---------------------------------------------------------

def extract_invoice_with_ai(text: str) -> InvoiceData:

    # If OCR produced no text, classify the document
    # as not an invoice instead of sending empty text to Gemini.
    if not text or not text.strip():
        return InvoiceData(
            document_type="not_an_invoice"
        )

    # Make sure the Gemini client was created.
    # If it was not created, the API key is unavailable.
    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    # Combine the extraction instructions with the OCR text.
    prompt = f"""
{INVOICE_EXTRACTION_PROMPT}

{text}
"""

    try:

        # Send the OCR text to Gemini.
        # response_schema tells Gemini to return data
        # matching our InvoiceData Pydantic model.
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                # Ask Gemini to return JSON.
                response_mime_type="application/json",

                # Force the response structure to match InvoiceData.
                response_schema=InvoiceData,

                # Temperature 0 makes extraction more deterministic.
                temperature=0,
            ),
        )

        # Make sure Gemini actually returned something.
        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        # Convert Gemini's JSON response into our
        # Pydantic InvoiceData object.
        invoice_data = InvoiceData.model_validate_json(
            response.text
        )

        # Return the structured invoice data
        # to the invoice pipeline.
        return invoice_data

    except Exception as error:

        # Convert any Gemini/API/parsing error into a
        # clear application-level error.
        raise RuntimeError(
            f"Gemini invoice extraction failed: {error}"
        ) from error