from datetime import date

from app.models.invoice import Invoice
from app.models.vendor import Vendor
from app.models.email_log import EmailLog
from app.models.processing_log import ProcessingLog
from app.models.verifications import Verification

def get_dashboard_payload():

    today = date.today()

    total_invoices = Invoice.query.count()

    pending_invoices = Invoice.query.filter_by(
        status="received"
    ).count()

    approved_invoices = Invoice.query.filter_by(
        status="approved"
    ).count()

    rejected_invoices = Invoice.query.filter(
        Invoice.due_date.isnot(None),
        Invoice.due_date < today
    ).count()

    overdue_invoices=Invoice.query.filter(
        Invoice.due_date.isnot(None),
        Invoice.due_date < today
    ).count()

    #vendor statistics

    total_vendors=Vendor.query.count()

    #verfication statistics

    pending_verifications=Verification.query.filter_by(
        verification_status ="pending"
    ).count()

    verified_invoices =Verification.query.filter_by(
        verification_status="approved"
    ).count()

    rejected_verifications = Verification.query.filter_by(
        verification_status="rejected"
    ).count()

    #Email statistics

    total_emails = EmailLog.query.count()

    emails_sent = EmailLog.query.filter_by(
        status="sent"
    ).count()

    emails_failed = EmailLog.query.filter_by(
        status="failed"
    ).count()

    #Processing Statistics

    total_processing_logs = ProcessingLog.query.count()

    processing_failed = ProcessingLog.query.filter_by(
        status="failed"
    ).count()

    processing_completed = ProcessingLog.query.filter_by(
        status="completed"
    ).count()

    return {

        "invoices": {
            "total": total_invoices,
            "pending": pending_invoices,
            "approved": approved_invoices,
            "rejected": rejected_invoices,
            "overdue": overdue_invoices
        },

        "vendors": {
            "total": total_vendors
        },

        "verification": {
            "pending": pending_verifications,
            "approved": verified_invoices,
            "rejected": rejected_verifications
        },

        "emails": {
            "total": total_emails,
            "sent": emails_sent,
            "failed": emails_failed
        },

        "processing": {
            "total": total_processing_logs,
            "completed": processing_completed,
            "failed": processing_failed
        }
    }