from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from datetime import date

from app.models.invoice import Invoice


reminder_bp = Blueprint(
    "reminder",
    __name__,
)

# GET INVOICES REQUIRING REMINDER

@reminder_bp.route("", methods=["GET"])
@jwt_required()
def get_reminders():

    today = date.today()

    invoices = Invoice.query.filter(
        Invoice.due_date.isnot(None),
        Invoice.due_date <= today
    ).all()

    reminder_list = []

    for invoice in invoices:

        if invoice.due_date < today:
            reminder_type = "overdue"
        else:
            reminder_type = "due_today"

        reminder_list.append({
            "invoice_id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "due_date": invoice.due_date.isoformat(),
            "reminder_type": reminder_type,
            "status": invoice.status
        })

    return jsonify({
        "reminders": reminder_list
    }), 200