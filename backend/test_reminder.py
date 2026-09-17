from app import create_app

from app.services.reminder_services import (
    get_upcoming_invoices,
    get_overdue_invoices
)


app = create_app()


with app.app_context():

    print("\n--- UPCOMING INVOICES ---")

    upcoming_invoices = get_upcoming_invoices(days=3)

    if not upcoming_invoices:
        print("No invoices due within the next 3 days.")

    else:
        for invoice in upcoming_invoices:
            print(
                f"Invoice ID: {invoice.id} | "
                f"Invoice Number: {invoice.invoice_number} | "
                f"Due Date: {invoice.due_date} | "
                f"Amount: {invoice.total_amount}"
            )


    print("\n--- OVERDUE INVOICES ---")

    overdue_invoices = get_overdue_invoices()

    if not overdue_invoices:
        print("No overdue invoices.")

    else:
        for invoice in overdue_invoices:
            print(
                f"Invoice ID: {invoice.id} | "
                f"Invoice Number: {invoice.invoice_number} | "
                f"Due Date: {invoice.due_date} | "
                f"Amount: {invoice.total_amount}"
            )