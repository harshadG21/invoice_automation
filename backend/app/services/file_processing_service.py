import os 
from pathlib import Path

from app.services.google_drive_service import download_file

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

    return{
        "file_id":file_id,
        "file_name":file_name,
        "file_path":str(local_path),
        "status":"downlaoded"
    }