from app import create_app
from app.services.google_drive_service import list_invoice_files
from app.services.invoice_pipeline import process_invoice
from app.models.user import User


# Create the Flask application.
app = create_app()


# Flask-SQLAlchemy requires an application context
# whenever we use database operations such as User.query.
with app.app_context():

    # Get the active distributor/user from the database.
    user = User.query.filter_by(is_active=True).first()

    # Stop if no active user exists.
    if not user:
        raise RuntimeError(
            "No active user found in database."
        )

    print("Processing invoices for user:", user.email)
    print("User ID:", user.id)

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

        # Send the Google Drive file ID,
        # filename, and logged-in distributor's user ID
        # to the invoice pipeline.
        result = process_invoice(
            file_id=file["id"],
            file_name=file["name"],
            user_id=user.id
        )

        print("\nRESULT:")
        print(result)
