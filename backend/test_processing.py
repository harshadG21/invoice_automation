from app import create_app
from app.services.google_drive_service import list_invoice_files
from app.services.file_processing_service import process_invoice_file


app = create_app()


with app.app_context():

    files = list_invoice_files()

    print("\nFILES FOUND:")
    print("-" * 50)

    for file in files:
        print(
            file["id"],
            file["name"],
            file["mimeType"]
        )

    if files:

        first_file = files[0]

        result = process_invoice_file(
            first_file["id"],
            first_file["name"]
        )

        print("\nPROCESSING RESULT:")
        print(result)

    else:
        print("No invoice files found.")