from app import create_app

from app.models.invoice import Invoice

from app.services.reminder_services import (
    send_invoice_reminder,
    send_overdue_email
)


app = create_app()


with app.app_context():

    invoice = Invoice.query.first()

    if not invoice:
        print("No invoice found in database.")
        exit()

    print(
        f"Testing reminder for Invoice: "
        f"{invoice.invoice_number}"
    )

    recipient_email = "harshadgori0@gmail.com"

    print("\n--- TESTING UPCOMING REMINDER ---")

    try:

        result = send_invoice_reminder(
            invoice,
            recipient_email
        )

        print(
            f"Reminder email sent successfully."
        )

        print(
            f"Email Log ID: {result.id}"
        )

    except Exception as error:

        print(
            f"Reminder email failed: {error}"
        )


    print("\n--- TESTING OVERDUE EMAIL ---")

    try:

        result = send_overdue_email(
            invoice,
            recipient_email
        )

        print(
            f"Overdue email sent successfully."
        )

        print(
            f"Email Log ID: {result.id}"
        )

    except Exception as error:

        print(
            f"Overdue email failed: {error}"
        )