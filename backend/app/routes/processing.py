from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required

from app.extensions.database import db
from app.models.processing_log import ProcessingLog
from app.models.invoice import Invoice


processing_log_bp=Blueprint(
    "processing_log",
    __name__
)

#get all the processing logs

@processing_log_bp.route("",methods=["GET"])
@jwt_required()
def get_processing_logs():

    logs=ProcessingLog.query.order_by(
        ProcessingLog.created_at.desc()
    ).all()

    log_list=[]

    for log in logs:

        log_list.append({
            "id": log.id,
            "invoice_id": log.invoice_id,
            "process_type": log.process_type,
            "status": log.status,
            "message": log.message,
            "started_at": (
                log.started_at.isoformat()
                if log.started_at
                else None
            ),
            "completed_at": (
                log.completed_at.isoformat()
                if log.completed_at
                else None
            ),
            "created_at": (
                log.created_at.isoformat()
                if log.created_at
                else None
            )
        })

    return jsonify({
        "processing_logs":log_list
    }),200

#get processing log for one invoice

@processing_log_bp.route("/<int:invoice_id>",methods=["GET"])
@jwt_required()
def get_invoice_processing_log(invoice_id):

    invoice=Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({
            "message": "Invoice Not Found"
        }),404

    logs=ProcessingLog.query.filter_by(
        invoice_id=invoice_id
    ).order_by(
        ProcessingLog.created_at.desc()
    ).all()

    log_list = []

    for log in logs:

        log_list.append({
           "id": log.id,
            "invoice_id": log.invoice_id,
            "process_type": log.process_type,
            "status": log.status,
            "message": log.message,
            "started_at": (
                log.started_at.isoformat()
                if log.started_at
                else None
            ),
            "completed_at": (
                log.completed_at.isoformat()
                if log.completed_at
                else None
            ),
            "created_at": (
                log.created_at.isoformat()
                if log.created_at
                else None
            ) 
        })

    return jsonify({
        "invoice_id":invoice_id,
        "processing_logs":log_list
    }),200