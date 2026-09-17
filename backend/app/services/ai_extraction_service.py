from google import genai
from google.genai import types

from app.config import Config
from app.schemas.invoice_schema import InvoiceData
import time 


GEMINI_API_KEY = Config.GEMINI_API_KEY
GEMINI_MODEL = Config.GEMINI_MODEL


# ---------------------------------------------------------
# GEMINI CLIENT
# ---------------------------------------------------------

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )
else:
    client = None


# ---------------------------------------------------------
# EXTRACTION PROMPT
# ---------------------------------------------------------

INVOICE_EXTRACTION_PROMPT = """
You are an expert invoice extraction system.

Extract structured information from the OCR text below.

IMPORTANT FINANCIAL RULES:

1. SUBTOTAL

financial.subtotal must be the amount BEFORE tax.

Examples:

Subtotal ₹25,000 -> 25000
Taxable Amount ₹48,000 -> 48000

Never use CGST, SGST, IGST, VAT, Total Tax,
Grand Total, or Total Amount as subtotal.


2. TAX COMPONENTS

Extract individual tax components separately.

If the invoice contains:

CGST (9%) = 9090
SGST (9%) = 9090

then return:

cgst = 9090
sgst = 9090
igst = null
tax_amount = 18180

If only CGST exists:

cgst = its actual amount
sgst = null
igst = null

If only SGST exists:

sgst = its actual amount
cgst = null
igst = null

If IGST exists:

igst = its actual amount

Do NOT confuse the subtotal with a tax component.

Do NOT infer a tax component when it is not explicitly present.


3. TOTAL TAX

financial.tax_amount must contain the TOTAL of ALL taxes.

For example:

CGST = 2250
SGST = 2250

then:

tax_amount = 4500

NOT 2250.

If the invoice explicitly contains:

Total Tax = 4500

then:

tax_amount = 4500.

When individual tax components are available:

cgst + sgst + igst = tax_amount

where applicable.


4. TOTAL AMOUNT

financial.total_amount must contain the FINAL invoice
amount payable by the customer.

If the invoice contains:

Subtotal = 25000
CGST = 2250
SGST = 2250
Total Tax = 4500
TOTAL AMOUNT = 29500

then:

subtotal = 25000
cgst = 2250
sgst = 2250
igst = null
tax_amount = 4500
total_amount = 29500

NEVER use CGST as total_amount.

NEVER use SGST as total_amount.

NEVER use Total Tax as total_amount.

The final total is the amount labelled:

- Total Amount
- TOTAL AMOUNT
- Grand Total
- Amount Payable
- Amount Due
- Final Amount

Prefer the explicitly printed final total.


5. FINANCIAL CONSISTENCY

When all values are available:

subtotal + tax_amount = total_amount

For example:

25000 + 4500 = 29500

Use this relationship to understand the invoice.

Do not invent numbers.


6. VENDOR

The vendor is the company that ISSUED the invoice.

Do not use the BILL TO customer as the vendor.


7. DATES

Return dates as YYYY-MM-DD.

Never invent dates.


8. CURRENCY

Identify the currency from the invoice.

₹ / Rs / INR -> INR
$ -> USD when clearly applicable
€ -> EUR
£ -> GBP

Return null if unclear.


9. DOCUMENT TYPE

If this is an invoice:

document_type = "invoice"

Otherwise:

document_type = "not_an_invoice"


Return only structured data matching the provided schema.

OCR TEXT:
"""


# ---------------------------------------------------------
# AI EXTRACTION
# ---------------------------------------------------------

def extract_invoice_with_ai(text: str) -> InvoiceData:

    # If OCR produced no text, the document cannot be extracted.
    if not text or not text.strip():
        return InvoiceData(
            document_type="not_an_invoice"
        )

    # Make sure Gemini API key is configured.
    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    # Build the Gemini prompt using the OCR text.
    prompt = f"""
{INVOICE_EXTRACTION_PROMPT}

{text}
"""

    try:

        # Send OCR text to Gemini and request structured JSON.
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=InvoiceData,
                temperature=0,
            ),
        )

        # Make sure Gemini actually returned something.
        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        # Convert Gemini JSON into our Pydantic InvoiceData model.
        invoice_data = InvoiceData.model_validate_json(
            response.text
        )

        # Print extracted financial values for debugging.
        print("\n========== AI FINANCIAL VALUES ==========")

        print(
            "Subtotal:",
            invoice_data.financial.subtotal
        )

        print(
            "CGST:",
            invoice_data.financial.cgst
        )

        print(
            "SGST:",
            invoice_data.financial.sgst
        )

        print(
            "IGST:",
            invoice_data.financial.igst
        )

        print(
            "Tax Amount:",
            invoice_data.financial.tax_amount
        )

        print(
            "Total Amount:",
            invoice_data.financial.total_amount
        )

        print("=========================================\n")

        return invoice_data

    except Exception as error:

        raise RuntimeError(
            f"Gemini invoice extraction failed: {error}"
        ) from error

def extract_invoice_with_ai_with_retry(
        raw_text,
        max_retries=3
):
    for attempt in range(1,max_retries+1):

        try:

            return extract_invoice_with_ai(raw_text)

        except Exception as e:

            print(
                f"\nGemini extraction failed "
                f"(attempt {attempt}/{max_retries})"
            )

            print(f"Error: {e}")

            if attempt == max_retries:
                print(
                    "\nGemini extraction failed after"
                    f"{max_retries} attempts"
                )
                raise

            wait_time = attempt * 5

            print(
               f"Retrying Gemini in "
               f"{wait_time} seconds..."  
            )

            time.sleep(wait_time)