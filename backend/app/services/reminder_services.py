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

def send_invoice_reminder(invoice):
    """
    Send an upcoming payment reminder to both
    the vendor and the user.
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

    email_logs = []

    # Send reminder to the vendor.
    if invoice.vendor and invoice.vendor.email:

        vendor_email_log = send_email(
            invoice_id=invoice.id,
            recipient_email=invoice.vendor.email,
            subject=subject,
            body=body,
            email_type="payment_reminder"
        )

        email_logs.append(vendor_email_log)

    # Send reminder to the user.
    if invoice.user and invoice.user.email:

        user_email_log = send_email(
            invoice_id=invoice.id,
            recipient_email=invoice.user.email,
            subject=subject,
            body=body,
            email_type="payment_reminder"
        )

        email_logs.append(user_email_log)

    return email_logs


def send_overdue_email(invoice):
    """
    Send an overdue notification to both
    the vendor and the user.
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

    email_logs = []

    # Send overdue notification to the vendor.
    if invoice.vendor and invoice.vendor.email:

        vendor_email_log = send_email(
            invoice_id=invoice.id,
            recipient_email=invoice.vendor.email,
            subject=subject,
            body=body,
            email_type="overdue"
        )

        email_logs.append(vendor_email_log)

    # Send overdue notification to the user.
    if invoice.user and invoice.user.email:

        user_email_log = send_email(
            invoice_id=invoice.id,
            recipient_email=invoice.user.email,
            subject=subject,
            body=body,
            email_type="overdue"
        )

        email_logs.append(user_email_log)

    return email_logs

def get_payment_state(invoice):

    #if the invoice has already been paid,don't consider it overdue
    if invoice.payment_status=="paid":
        return "paid"
    
    #if there is no due date,we cannot determine wheter the invoice is overdue
    if not invoice.due_date:
        return "unpaid"

    if invoice.due_date < date.today():
        return "overdue"

    return "unpaid"