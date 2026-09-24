from app import create_app

from app.services.google_drive_service import (
    list_incoming_invoice,
    move_file_to_processing,
    move_file_to_completed,
    move_file_to_duplicates,
    move_file_to_failed
)

from app.services.invoice_pipeline import process_invoice
from app.models.user import User


def run_invoice_auto_processing():

    app = create_app()

    with app.app_context():

        print("\n========================================")
        print("AUTOMATIC INVOICE PROCESSING")
        print("========================================")

        # Get the active application user.
        user = User.query.filter_by(
            is_active=True
        ).first()

        if not user:

            print("No active user found.")
            return

        print("Processing invoices for user:", user.email)

        files = list_incoming_invoice()

        if not files:

            print("No invoices found in Incoming.")
            return

        print(f"Found {len(files)} invoice(s).")

        for file in files:

            file_id = file["id"]
            file_name = file["name"]

            print("\n----------------------------------------")
            print("Processing:", file_name)
            print("File ID:", file_id)
            print("----------------------------------------")

            try:

                # Move the invoice from Incoming to Processing.
                print("Moving file to Processing...")

                move_file_to_processing(file_id)

                print("File moved to Processing.")

                # Run the invoice pipeline.
                result = process_invoice(
                    file_id=file_id,
                    file_name=file_name,
                    user_id=user.id
                )

                print("\nPipeline Result:")
                print(result)

                status = result.get("status")

                # Successfully processed.
                if status == "success":

                    print("\nInvoice processed successfully.")
                    print("Moving file to Completed...")

                    move_file_to_completed(file_id)

                    print("File moved to Completed.")

                # Duplicate invoice or Drive file.
                elif status == "duplicate":

                    print("\nDuplicate invoice detected.")
                    print("Moving file to Duplicate...")

                    move_file_to_duplicates(file_id)

                    print("File moved to Duplicate.")

                # Validation failure / not an invoice.
                else:

                    print("\nInvoice processing failed.")
                    print("Status:", status)
                    print("Moving file to Failed...")

                    move_file_to_failed(file_id)

                    print("File moved to Failed.")

            except Exception as e:

                print("\nERROR PROCESSING FILE:")
                print(e)

                # Unexpected error → Failed folder.
                try:

                    print("Moving file to Failed...")

                    move_file_to_failed(file_id)

                    print("File moved to Failed.")

                except Exception as move_error:

                    print("Could not move file to Failed.")
                    print(move_error)

        print("\n========================================")
        print("AUTOMATIC PROCESSING FINISHED")
        print("========================================")