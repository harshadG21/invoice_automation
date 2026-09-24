from google import genai
from google.genai import types
from openai import OpenAI

from app.config import Config
from app.schemas.invoice_schema import InvoiceData

import time


# =========================================================
# API CONFIGURATION
# =========================================================

GEMINI_API_KEY = Config.GEMINI_API_KEY
GEMINI_MODEL = Config.GEMINI_MODEL

OPENROUTER_API_KEY = Config.OPENROUTER_API_KEY
OPENROUTER_MODEL = Config.OPENROUTER_MODEL


# =========================================================
# OPENROUTER CLIENT
# =========================================================

if OPENROUTER_API_KEY:

    openrouter_client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

else:

    openrouter_client = None


# =========================================================
# GEMINI CLIENT
# =========================================================

if GEMINI_API_KEY:

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

else:

    client = None


# =========================================================
# EXTRACTION PROMPT
# =========================================================

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


6. VENDOR / BILL TO EXTRACTION

CRITICAL RULE:

The "vendor" object represents ONLY the BILL TO / BUYER /
CUSTOMER party.

The seller / issuer / company at the top of the invoice is
NOT the vendor.

The logged-in user represents the seller/distributor in our
application.

Therefore:

SELLER / FROM / ISSUED BY
        -> DO NOT put into vendor

BILL TO / CUSTOMER / BUYER
        -> PUT into vendor


BILL TO IDENTIFICATION:

Look for an explicit BILL TO section.

Examples of labels:

- BILL TO:
- BILL TO
- CUSTOMER:
- CUSTOMER NAME:
- BUYER:
- BILL TO CUSTOMER:
- CUSTOMER DETAILS:


FIELD MAPPING:

Inside the BILL TO section:

Customer Name -> vendor.name
Name -> vendor.name
Company Name -> vendor.name

Email -> vendor.email
Customer Email -> vendor.email

Phone -> vendor.phone
Phone Number -> vendor.phone
Mobile -> vendor.phone

Address -> vendor.address
Customer Address -> vendor.address

GSTIN -> vendor.gst_number
GST Number -> vendor.gst_number

PAN -> vendor.pan_number
PAN Number -> vendor.pan_number


STRICT SOURCE RULE:

Every vendor field MUST come from the BILL TO / CUSTOMER /
BUYER section.

NEVER copy a value into vendor merely because it appears
somewhere else in the invoice.

In particular:

- Seller company name MUST NOT become vendor.name.
- Seller email MUST NOT become vendor.email.
- Seller address MUST NOT become vendor.address.
- Seller phone MUST NOT become vendor.phone.
- Seller GSTIN MUST NOT become vendor.gst_number.
- Seller PAN MUST NOT become vendor.pan_number.


IMPORTANT:

If the invoice contains BOTH a seller section and a BILL TO
section, completely ignore the seller information when
extracting vendor.

Example:

FROM:
Bright Web Studio LLP
accounts@brightwebstudio.in
GSTIN: 29AAECB5678G1Z3

BILL TO:
Customer Name: Skyline Hospitality Group
Email: accounts@skylinehospitality.com
Address: Bandra West, Mumbai, Maharashtra - 400050


The ONLY valid vendor information is:

vendor.name = "Skyline Hospitality Group"

vendor.email = "accounts@skylinehospitality.com"

vendor.address = "Bandra West, Mumbai, Maharashtra - 400050"

vendor.phone = null

vendor.gst_number = null

vendor.pan_number = null


The following extraction is WRONG:

vendor.name = "Bright Web Studio LLP"

vendor.email = "accounts@brightwebstudio.in"

vendor.gst_number = "29AAECB5678G1Z3"


VERY IMPORTANT:

The seller's GSTIN appearing before the BILL TO section is
NOT the customer's GSTIN.

If a GSTIN appears in the seller section and there is no
GSTIN inside the BILL TO section:

vendor.gst_number MUST be null.


If a field is not explicitly present inside the BILL TO
section, return null.

Do not infer missing customer information.

Do not combine seller information with customer information.

Do not move information from the seller section into vendor.


BILL TO HAS PRIORITY:

When both seller and BILL TO information exist, the BILL TO
section always determines vendor.

The vendor object must represent the party receiving the
invoice / being billed, not the company issuing the invoice.


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


OUTPUT FORMAT:

Return a JSON object matching the following exact structure.

{
    "document_type": "invoice",
    "invoice_number": "INV-1003",
    "invoice_date": "2026-09-14",
    "due_date": "2026-09-29",

    "vendor": {
        "name": "Skyline Hospitality Group",
        "email": "accounts@skylinehospitality.com",
        "phone": null,
        "address": "Bandra West, Mumbai, Maharashtra - 400050",
        "gst_number": null,
        "pan_number": null
    },

    "financial": {
        "subtotal": 101000,
        "cgst": 9090,
        "sgst": 9090,
        "igst": null,
        "tax_amount": 18180,
        "total_amount": 119180,
        "currency": "INR"
    }
}


IMPORTANT OUTPUT RULES:

1. "vendor" MUST always be a JSON object.
2. "financial" MUST always be a JSON object.
3. Never return vendor as a plain string.
4. Never return financial as a plain string.
5. Use the exact field names shown above.
6. Use null when a value is not available.
7. Do not invent missing information.
8. Dates must use YYYY-MM-DD.
9. Return ONLY valid JSON.
10. Do not include markdown code fences.
11. The JSON must match the InvoiceData schema.

OCR TEXT:
"""


# =========================================================
# GEMINI EXTRACTION
# =========================================================

def extract_invoice_with_ai(text: str) -> InvoiceData:
    """
    Extract invoice information using Gemini.

    This function is used as the Gemini fallback.
    """

    # -----------------------------------------------------
    # Check OCR text
    # -----------------------------------------------------

    if not text or not text.strip():

        return InvoiceData(
            document_type="not_an_invoice"
        )


    # -----------------------------------------------------
    # Check Gemini API configuration
    # -----------------------------------------------------

    if client is None:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )


    # -----------------------------------------------------
    # Build prompt
    # -----------------------------------------------------

    prompt = f"""
{INVOICE_EXTRACTION_PROMPT}

{text}
"""


    try:

        # -------------------------------------------------
        # Send request to Gemini
        # -------------------------------------------------

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=InvoiceData,
                temperature=0,
            ),
        )


        # -------------------------------------------------
        # Check Gemini response
        # -------------------------------------------------

        if not response.text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )


        # -------------------------------------------------
        # Convert JSON into Pydantic model
        # -------------------------------------------------

        invoice_data = InvoiceData.model_validate_json(
            response.text
        )


        # -------------------------------------------------
        # Debug output
        # -------------------------------------------------

        print(
            "\n========== GEMINI VALUES =========="
        )

        print(
            "Invoice Number:",
            invoice_data.invoice_number
        )

        print(
            "Vendor/Bill To:",
            invoice_data.vendor.name
        )

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

        print(
            "==================================\n"
        )


        return invoice_data


    except Exception as error:

        raise RuntimeError(
            f"Gemini invoice extraction failed: {error}"
        ) from error


# =========================================================
# OPENROUTER / LLAMA EXTRACTION
# =========================================================

def extract_invoice_with_llama(
    text: str
) -> InvoiceData:
    """
    Extract invoice information using
    OpenRouter / Llama.
    """

    # -----------------------------------------------------
    # Check OCR text
    # -----------------------------------------------------

    if not text or not text.strip():

        return InvoiceData(
            document_type="not_an_invoice"
        )


    # -----------------------------------------------------
    # Check OpenRouter configuration
    # -----------------------------------------------------

    if openrouter_client is None:

        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured."
        )


    # -----------------------------------------------------
    # Build prompt
    # -----------------------------------------------------

    prompt = f"""
{INVOICE_EXTRACTION_PROMPT}

{text}
"""


    try:

        # -------------------------------------------------
        # Send request to OpenRouter
        # -------------------------------------------------

        response = openrouter_client.chat.completions.create(

            model=OPENROUTER_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0,

            response_format={
                "type": "json_object"
            }
        )


        # -------------------------------------------------
        # Check response choices
        # -------------------------------------------------

        if not response.choices:

            raise RuntimeError(
                "OpenRouter returned an empty response."
            )


        # -------------------------------------------------
        # Get model response
        # -------------------------------------------------

        response_text = (
            response.choices[0]
            .message
            .content
        )


        if not response_text:

            raise RuntimeError(
                "OpenRouter returned empty content."
            )


        # -------------------------------------------------
        # Validate JSON with Pydantic
        # -------------------------------------------------

        invoice_data = InvoiceData.model_validate_json(
            response_text
        )


        # -------------------------------------------------
        # Debug output
        # -------------------------------------------------

        print(
            "\n========== OPENROUTER / LLAMA VALUES =========="
        )

        print(
            "Invoice Number:",
            invoice_data.invoice_number
        )

        print(
            "Vendor/Bill To:",
            invoice_data.vendor.name
        )

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

        print(
            "==============================================\n"
        )


        return invoice_data


    except Exception as error:

        raise RuntimeError(
            f"OpenRouter invoice extraction failed: {error}"
        ) from error


# =========================================================
# PRIMARY + FALLBACK EXTRACTION
# =========================================================

def extract_invoice_with_ai_with_retry(
    raw_text,
    max_retries=3
):
    """
    AI invoice extraction flow.

    Priority:

    1. OpenRouter / Llama
    2. Retry OpenRouter
    3. Gemini fallback
    4. Retry Gemini
    5. Raise final error

    OpenRouter is the PRIMARY model.
    Gemini is the FALLBACK model.
    """

    # =====================================================
    # STEP 0: CHECK OCR TEXT
    # =====================================================

    if not raw_text or not raw_text.strip():

        return InvoiceData(
            document_type="not_an_invoice"
        )


    # =====================================================
    # STEP 1: OPENROUTER / LLAMA
    # =====================================================

    if openrouter_client is not None:

        for attempt in range(
            1,
            max_retries + 1
        ):

            try:

                print(
                    "\n========================================"
                )

                print(
                    f"OPENROUTER / LLAMA "
                    f"(attempt {attempt}/{max_retries})"
                )

                print(
                    "========================================"
                )


                invoice_data = extract_invoice_with_llama(
                    raw_text
                )


                print(
                    "\nOpenRouter extraction successful."
                )


                return invoice_data


            except Exception as error:

                print(
                    f"\nOpenRouter extraction failed "
                    f"(attempt {attempt}/{max_retries})"
                )

                print(
                    f"Error: {error}"
                )


                # -----------------------------------------
                # Final OpenRouter attempt
                # -----------------------------------------

                if attempt == max_retries:

                    print(
                        "\n========================================"
                    )

                    print(
                        "OPENROUTER FAILED AFTER ALL RETRIES"
                    )

                    print(
                        "Switching to Gemini fallback..."
                    )

                    print(
                        "========================================"
                    )

                    break


                # -----------------------------------------
                # Wait before retry
                # -----------------------------------------

                wait_time = attempt * 5

                print(
                    f"Retrying OpenRouter in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)

    else:

        print(
            "\nOpenRouter is not configured."
        )

        print(
            "Skipping OpenRouter and using Gemini..."
        )


    # =====================================================
    # STEP 2: GEMINI FALLBACK
    # =====================================================

    if client is not None:

        for attempt in range(
            1,
            max_retries + 1
        ):

            try:

                print(
                    "\n========================================"
                )

                print(
                    f"GEMINI FALLBACK "
                    f"(attempt {attempt}/{max_retries})"
                )

                print(
                    "========================================"
                )


                invoice_data = extract_invoice_with_ai(
                    raw_text
                )


                print(
                    "\nGemini extraction successful."
                )


                return invoice_data


            except Exception as error:

                print(
                    f"\nGemini extraction failed "
                    f"(attempt {attempt}/{max_retries})"
                )

                print(
                    f"Error: {error}"
                )


                # -----------------------------------------
                # Final Gemini attempt
                # -----------------------------------------

                if attempt == max_retries:

                    print(
                        "\n========================================"
                    )

                    print(
                        "GEMINI FAILED AFTER ALL RETRIES"
                    )

                    print(
                        "ALL AI EXTRACTION ATTEMPTS FAILED"
                    )

                    print(
                        "========================================"
                    )

                    raise RuntimeError(
                        "Both OpenRouter and Gemini "
                        "invoice extraction failed."
                    ) from error


                # -----------------------------------------
                # Wait before retry
                # -----------------------------------------

                wait_time = attempt * 5

                print(
                    f"Retrying Gemini in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)

    else:

        # =================================================
        # BOTH API KEYS ARE MISSING
        # =================================================

        raise RuntimeError(
            "Both OPENROUTER_API_KEY and "
            "GEMINI_API_KEY are not configured."
        )

