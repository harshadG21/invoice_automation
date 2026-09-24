from app import create_app

from app.models.invoice import Invoice
from app.services.reminder_services import (
    get_payment_state,
    send_invoice_reminder,
    send_overdue_email
)


# Create the Flask application.
app = create_app()


# Database queries require an application context.
with app.app_context():

    print("\n========================================")
    print("TESTING REMINDER SERVICE")
    print("========================================")

    # Get one unpaid invoice for testing.
    invoice = Invoice.query.filter_by(
        payment_status="unpaid"
    ).first()

    if not invoice:

        print("No unpaid invoice found.")
        print("Create or use an unpaid invoice first.")

    else:

        print("\nInvoice:")
        print(invoice.invoice_number)

        print("Vendor:",
              invoice.vendor.vendor_name
              if invoice.vendor else "No vendor")

        print("Vendor email:",
              invoice.vendor.email
              if invoice.vendor else "No vendor")

        print("User:",
              invoice.user.email
              if invoice.user else "No user")

        print("Payment state:",
              get_payment_state(invoice))

        # -------------------------------------------------
        # Send the appropriate email for testing.
        # -------------------------------------------------

        if get_payment_state(invoice) == "overdue":

            print("\nSending overdue email...")

            result = send_overdue_email(invoice)

        elif get_payment_state(invoice) == "unpaid":

            print("\nSending payment reminder...")

            result = send_invoice_reminder(invoice)

        else:

            print("\nInvoice is already paid.")
            result = None

        print("\nEmail Result:")
        print(result)

    print("\n========================================")
    print("REMINDER TEST FINISHED")
    print("========================================")

