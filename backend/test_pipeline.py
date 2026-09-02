from app import create_app
from app.services.google_drive_service import list_invoice_files
from app.services.invoice_pipeline import process_invoice


# Create the Flask application.
app = create_app()


# Flask-SQLAlchemy requires an application context
# whenever we use database operations such as Vendor.query or db.session.
with app.app_context():

    # Get invoice files automatically from Google Drive.
    files = list_invoice_files()

    # Stop if no invoice files were found.
    if not files:
        print("No invoice files found.")
        exit()

    # Process each invoice found in Google Drive.
    for file in files:

        print("\n========================================")
        print("PROCESSING:", file["name"])
        print("========================================")

        # Send the Google Drive file ID and filename
        # to the invoice pipeline.
        result = process_invoice(
            file_id=file["id"],
            file_name=file["name"]
        )

        print("\nRESULT:")
        print(result)
        