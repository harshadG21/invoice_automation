from app.services.google_drive_service import (
    list_incoming_invoice,
    move_file_to_processing,
    move_file_to_duplicates
)

print("\n========================================")
print("DRIVE MOVE TEST")
print("========================================")

files = list_incoming_invoice()

if not files:
    print("No invoice files found in Incoming.")
else:
    # Use only the first file for this test.
    file = files[0]

    file_id = file["id"]
    file_name = file["name"]

    print("File selected:")
    print("Name:", file_name)
    print("ID:", file_id)

    print("\nMoving file to Processing...")

    move_file_to_processing(file_id)

    print("File is now in Processing.")

    print("\nMoving file to Duplicate...")

    move_file_to_duplicates(file_id)

    print("File is now in Duplicate.")

print("\n========================================")
print("TEST FINISHED")
print("========================================")