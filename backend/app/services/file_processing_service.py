import os
from pathlib import Path

from app.services.google_drive_service import download_file
from app.services.ocr_service import extract_text_as_string
from app.services.invoice_extraction_service import extract_invoice_data
from app.services.invoice_database_service import save_invoice


TEMP_DIR=Path("temp/invoices")

#create the temporary invoice directory 
def ensure_temp_directory():

    TEMP_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

#check whether the invoice file format is supported
def validate_invoice_file(file_name):

    allowed_extensions ={
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
    }

    extension = Path(file_name).suffix.lower()

    if extension not in allowed_extensions:
        raise ValueError(
            f"Unsupported invoice file type:{extension}"
        )

    return True

#download an invoice and prepare for ocr processsing

def process_invoice_file(file_id,file_name):

    print(f"Processing invoice:{file_name}")

    validate_invoice_file(file_name)

    ensure_temp_directory()

    local_path = TEMP_DIR/file_name

    download_file(file_id,str(local_path))

    if not local_path.exists():
        raise ValueError(
            f"File was not downloaded:{file_name}"
        )

    print(
        f"Invoice Downloaded Successfullly"
        f"{local_path}"
    )

    print("Starting OCR..")

    extracted_text = extract_text_as_string(
        str(local_path)
    )

    if not extracted_text.strip():
        raise ValueError(
            f"No text could be extracted from invoice: {file_name}"
        )

    print("OCR completed successfully")

    print("Extracting Invoice_data...")

    invoice_data = extract_invoice_data(
        extracted_text
    )

    print("Invoice data extraction completed")

    print("Saving invoice to database")

    invoice = save_invoice(
        invoice_data=invoice_data,
        file_name=file_name,
        file_path = str(local_path),
        ocr_text=extracted_text
    )

    print(
        f"Invoice saved successfully."
        f"Invoice ID:{invoice.id}"
    )

    return{
        "file_id":file_id,
        "file_name":file_name,
        "file_path":str(local_path),
        "status":"downlaoded"
    }