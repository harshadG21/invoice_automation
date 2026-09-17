import smtplib
from email.message import EmailMessage
from pathlib import Path
from datetime import datetime

from flask import current_app

from app.extensions.database import db
from app.models.email_log import EmailLog


def send_email(
    invoice_id,
    recipient_email,
    subject,
    body,
    email_type="invoice"
):
    """
    Send a normal email and record the result in email_logs.
    """

    email_log = EmailLog(
        invoice_id=invoice_id,
        recipient_email=recipient_email,
        subject=subject,
        email_type=email_type,
        status="pending"
    )

    db.session.add(email_log)

    try:

        smtp_server = current_app.config["MAIL_SERVER"]
        smtp_port = current_app.config["MAIL_PORT"]
        sender_email = current_app.config["MAIL_USERNAME"]
        sender_password = current_app.config["MAIL_PASSWORD"]

        message = EmailMessage()

        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP(
            smtp_server,
            smtp_port
        ) as server:

            server.starttls()

            server.login(
                sender_email,
                sender_password
            )

            server.send_message(message)

        email_log.status = "sent"
        email_log.sent_at = datetime.utcnow()

        db.session.commit()

        return email_log

    except Exception as error:

        email_log.status = "failed"
        email_log.error_message = str(error)

        db.session.commit()

        raise


def send_email_with_attachment(
    invoice_id,
    recipient_email,
    subject,
    body,
    attachment_path,
    email_type="invoice"
):
    """
    Send an email with an attachment
    and record the result in email_logs.
    """

    email_log = EmailLog(
        invoice_id=invoice_id,
        recipient_email=recipient_email,
        subject=subject,
        email_type=email_type,
        status="pending"
    )

    db.session.add(email_log)

    try:

        mail_server = current_app.config["MAIL_SERVER"]
        mail_port = current_app.config["MAIL_PORT"]
        mail_username = current_app.config["MAIL_USERNAME"]
        mail_password = current_app.config["MAIL_PASSWORD"]

        # Create email
        message = EmailMessage()

        message["From"] = mail_username
        message["To"] = recipient_email
        message["Subject"] = subject

        message.set_content(body)

        # Check attachment
        attachment = Path(attachment_path)

        if not attachment.exists():
            raise FileNotFoundError(
                f"Attachment file not found: {attachment_path}"
            )

        # Read attachment
        with open(
            attachment,
            "rb"
        ) as file:

            file_data = file.read()

        # Add attachment
        message.add_attachment(
            file_data,
            maintype="application",
            subtype="pdf",
            filename=attachment.name
        )

        # Send email
        with smtplib.SMTP(
            mail_server,
            mail_port
        ) as server:

            server.starttls()

            server.login(
                mail_username,
                mail_password
            )

            server.send_message(message)

        email_log.status = "sent"
        email_log.sent_at = datetime.utcnow()

        db.session.commit()

        print(
            f"Email with attachment sent successfully "
            f"to {recipient_email}"
        )

        return email_log

    except Exception as error:

        email_log.status = "failed"
        email_log.error_message = str(error)

        db.session.commit()

        print(
            f"Email sending failed: {error}"
        )

        raise


def send_invoice_email(
    invoice,
    recipient_email
):
    """
    Send an invoice email with the invoice PDF attached.
    """

    subject = (
        f"Invoice {invoice.invoice_number} Processed"
    )

    body = f"""
Hello,

Your invoice has been successfully processed.

Invoice Number: {invoice.invoice_number}
Invoice Date: {invoice.invoice_date}
Due Date: {invoice.due_date}
Subtotal: {invoice.subtotal}
Tax Amount: {invoice.tax_amount}
Total Amount: {invoice.total_amount}
Currency: {invoice.currency}

The invoice has been successfully recorded in our system.

Please find the invoice PDF attached to this email.

Regards,
Invoice Automation System
"""

    attachment_path = Path(
        invoice.file_path
    )

    if not attachment_path.exists():
        raise FileNotFoundError(
            f"Invoice file not found: {invoice.file_path}"
        )

    # IMPORTANT:
    # Use send_email_with_attachment()
    return send_email_with_attachment(
        invoice_id=invoice.id,
        recipient_email=recipient_email,
        subject=subject,
        body=body,
        attachment_path=str(attachment_path),
        email_type="invoice"
    )