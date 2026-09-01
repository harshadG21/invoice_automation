from app import create_app
from app.services.invoice_pipeline import process_invoice

# Create the Flask application
app = create_app()

# Application context is required because the pipeline uses SQLAlchemy
with app.app_context():

    # Google Drive file ID
    file_id = "1gXdJplfkuavv07h2Joo5_E2LAF1RUG6I"

    # Invoice file name
    file_name = "Invoice_INV-1001.pdf"

    # Run the complete invoice processing pipeline
    result = process_invoice(file_id, file_name)

    # Print the pipeline result
    print("\nINVOICE PIPELINE RESULT")
    print("=" * 50)

    # Print every result returned by the pipeline
    for key, value in result.items():
        print(f"{key}: {value}")