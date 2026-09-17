from pathlib import Path

from app.services.google_drive_service import download_file


TEMP_DIR = Path("temp/invoices")


# Create the temporary invoice directory.
def ensure_temp_directory():

    TEMP_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# Check whether the invoice file format is supported.
def validate_invoice_file(file_name):

    allowed_extensions = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
    }

    extension = Path(file_name).suffix.lower()

    if extension not in allowed_extensions:

        raise ValueError(
            f"Unsupported invoice file type: {extension}"
        )

    return True


# Download an invoice and prepare it for processing.
def process_invoice_file(file_id, file_name):

    print(f"Processing invoice: {file_name}")

    # Make sure the uploaded file type is supported.
    validate_invoice_file(file_name)

    # Make sure the temporary directory exists.
    ensure_temp_directory()

    local_path = TEMP_DIR / file_name

    # Download the invoice from Google Drive.
    download_file(
        file_id,
        str(local_path)
    )

    # Verify that the file actually exists.
    if not local_path.exists():

        raise ValueError(
            f"File was not downloaded: {file_name}"
        )

    print(
        f"Invoice Downloaded Successfully: {local_path}"
    )

    return {
        "file_id": file_id,
        "file_name": file_name,
        "file_path": str(local_path),
        "status": "downloaded"
    }