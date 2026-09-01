# Imports the main invoice pipeline function.
from app.services.invoice_pipeline import process_invoice


# This is the Google Drive file ID of our test invoice.
file_id = "1gXdJplfkuavv07h2Joo5_E2LAF1RUG6I"

# This is the invoice file name.
file_name = "Invoice_INV-1001.pdf"


# Start the complete invoice processing pipeline.
result = process_invoice(
    file_id,
    file_name
)


# Display the final structured invoice data.
print("\nINVOICE PIPELINE RESULT")
print("=" * 50)

# Print every extracted field.
for key, value in result.items():
    print(f"{key}: {value}")