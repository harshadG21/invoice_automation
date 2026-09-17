from datetime import date, timedelta

from app.models.invoice import Invoice
from app.services.email_service import send_email


def get_upcoming_invoices(days=3):
    """
    Find unpaid invoices that are due within the given number of days.
    """

    today = date.today()
    reminder_date = today + timedelta(days=days)

    invoices = Invoice.query.filter(
        Invoice.payment_status == "unpaid",
        Invoice.due_date >= today,
        Invoice.due_date <= reminder_date
    ).all()

    return invoices


def get_overdue_invoices():
    """
    Find invoices whose due date has passed
    and payment has not been completed.
    """

    today = date.today()

    invoices = Invoice.query.filter(
        Invoice.payment_status == "unpaid",
        Invoice.due_date < today
    ).all()

    return invoices


def send_invoice_reminder(invoice, recipient_email):
    """
    Send an upcoming invoice payment reminder.
    """

    subject = (
        f"Payment Reminder - Invoice "
        f"{invoice.invoice_number}"
    )

    body = f"""
Hello,

This is a reminder that the following invoice
is approaching its due date.

Invoice Number: {invoice.invoice_number}
Invoice Date: {invoice.invoice_date}
Due Date: {invoice.due_date}
Total Amount: {invoice.total_amount}
Currency: {invoice.currency}

Please ensure that the payment is completed
before the due date.

Regards,
Invoice Automation System
"""

    return send_email(
        invoice_id=invoice.id,
        recipient_email=recipient_email,
        subject=subject,
        body=body,
        email_type="payment_reminder"
    )


def send_overdue_email(invoice, recipient_email):
    """
    Send an overdue invoice notification.
    """

    subject = (
        f"Overdue Invoice - "
        f"{invoice.invoice_number}"
    )

    body = f"""
Hello,

The following invoice is now overdue.

Invoice Number: {invoice.invoice_number}
Invoice Date: {invoice.invoice_date}
Due Date: {invoice.due_date}
Total Amount: {invoice.total_amount}
Currency: {invoice.currency}

Our records show that the payment has not
yet been completed.

Please arrange the payment at the earliest.

Regards,
Invoice Automation System
"""

    return send_email(
        invoice_id=invoice.id,
        recipient_email=recipient_email,
        subject=subject,
        body=body,
        email_type="overdue"
    )