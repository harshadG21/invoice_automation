from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.models.email_log import EmailLog
from app.models.invoice import Invoice


email_log_bp = Blueprint(
    "email_log",
    __name__,
)


# GET ALL EMAIL LOGS

@email_log_bp.route("", methods=["GET"])
@jwt_required()
def get_email_logs():

    logs = EmailLog.query.order_by(
        EmailLog.created_at.desc()
    ).all()

    log_list = []

    for log in logs:

        log_list.append({
            "id": log.id,
            "invoice_id": log.invoice_id,
            "recipient_email": log.recipient_email,
            "subject": log.subject,
            "email_type": log.email_type,
            "status": log.status,
            "sent_at": (
                log.sent_at.isoformat()
                if log.sent_at
                else None
            ),
            "error_message": log.error_message,
            "created_at": (
                log.created_at.isoformat()
                if log.created_at
                else None
            )
        })

    return jsonify({
        "email_logs": log_list
    }), 200



# get invoice email_logs

@email_log_bp.route("/<int:invoice_id>", methods=["GET"])
@jwt_required()
def get_invoice_email_logs(invoice_id):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({
            "message": "Invoice not found"
        }), 404

    logs = EmailLog.query.filter_by(
        invoice_id=invoice_id
    ).order_by(
        EmailLog.created_at.desc()
    ).all()

    log_list = []

    for log in logs:

        log_list.append({
            "id": log.id,
            "invoice_id": log.invoice_id,
            "recipient_email": log.recipient_email,
            "subject": log.subject,
            "email_type": log.email_type,
            "status": log.status,
            "sent_at": (
                log.sent_at.isoformat()
                if log.sent_at
                else None
            ),
            "error_message": log.error_message,
            "created_at": (
                log.created_at.isoformat()
                if log.created_at
                else None
            )
        })

    return jsonify({
        "invoice_id": invoice_id,
        "email_logs": log_list
    }), 200