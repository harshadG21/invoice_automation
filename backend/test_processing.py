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

        for file in files:

            print("\n" + "=" * 60)
            print(f"PROCESSING INVOICE: {file['name']}")
            print("=" * 60)

            try:

                result = process_invoice_file(
                    file["id"],
                    file["name"]
                )

                print("\nPROCESSING RESULT:")
                print(result)

            except Exception as e:

                print("\nPROCESSING FAILED:")
                print(type(e).__name__)
                print(e)

                print(
                    f"\nSkipping {file['name']} "
                    "and continuing with the next invoice..."
                )

    else:
        print("No invoice files found.")