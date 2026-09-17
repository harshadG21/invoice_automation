from app import create_app

from app.services.google_drive_service import (
    list_incoming_invoice,
    move_file_to_processing,
    move_file_to_completed,
    move_file_to_duplicates,
    move_file_to_failed
)

from app.services.invoice_pipeline import process_invoice


# Create the Flask application.
app = create_app()


# Database queries inside the invoice pipeline need
# an active Flask application context.
with app.app_context():

    print("\n========================================")
    print("AUTOMATIC INVOICE PROCESSING")
    print("========================================")

    files = list_incoming_invoice()

    if not files:

        print("No invoices found in Incoming.")

    else:

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

                # Run the complete invoice pipeline.
                result = process_invoice(
                    file_id=file_id,
                    file_name=file_name
                )

                print("\nPipeline Result:")
                print(result)

                status = result.get("status")

                # Successfully saved to database.
                if status == "success":

                    print("\nInvoice processed successfully.")
                    print("Moving file to Completed...")

                    move_file_to_completed(file_id)

                    print("File moved to Completed.")

                # Duplicate invoice/file.
                elif status == "duplicate":

                    print("\nDuplicate invoice detected.")
                    print("Moving file to Duplicate...")

                    move_file_to_duplicates(file_id)

                    print("File moved to Duplicate.")

                # Validation failure, not an invoice,
                # or any other unsuccessful result.
                else:

                    print("\nInvoice processing failed.")
                    print("Status:", status)
                    print("Moving file to Failed...")

                    move_file_to_failed(file_id)

                    print("File moved to Failed.")

            except Exception as e:

                print("\nERROR PROCESSING FILE:")
                print(e)

                # Any unexpected error after entering
                # Processing sends the file to Failed.
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