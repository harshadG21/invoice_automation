from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime

from app.extensions.database import db
from app.models.verifications import Verification
from app.models.invoice import Invoice

verification_bp=Blueprint(
    "verification",
    __name__
)

# Get verfied

@verification_bp.route("/<int:invoice_id>",methods=['GET'])
@jwt_required()
def fet_verification(invoice_id):

    invoice=Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({
            "message":"Invoice not Found"
        }),404

    verification=Verification.query.filter_by(
        invoice_id=invoice_id
    ).first()

    if not verification:
        return jsonify({
            "message":"Verification Record Not Found"
        }),404

    return jsonify({
        "verificatio":{
           "id": verification.id,
            "invoice_id": verification.invoice_id,
            "verified_by": verification.verified_by,
            "verification_status": verification.verification_status,
            "remarks": verification.remarks,
            "ai_confidence": (
                float(verification.ai_confidence)
                if verification.ai_confidence is not None
                else None
            ),
            "verified_at": (
                verification.verified_at.isoformat()
                if verification.verified_at
                else None
            ),
            "created_at": (
                verification.created_at.isoformat()
                if verification.created_at
                else None
            ) 
        }
    }),200


#update verification

@verification_bp.route("/<int:invoice_id>", methods=["PUT"])
@jwt_required()
def update_verification(invoice_id):

    data = request.get_json()

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({
            "message": "Invoice not found"
        }), 404

    verification = Verification.query.filter_by(
        invoice_id=invoice_id
    ).first()

    if not verification:
        verification = Verification(
            invoice_id=invoice_id
        )

        db.session.add(verification)

    verification_status = data.get("verification_status")
    remarks = data.get("remarks")
    ai_confidence = data.get("ai_confidence")

    allowed_statuses = [
        "pending",
        "approved",
        "rejected"
    ]

    if verification_status:

        if verification_status not in allowed_statuses:
            return jsonify({
                "message": "Invalid verification status"
            }), 400

        verification.verification_status = verification_status

    if remarks is not None:
        verification.remarks = remarks

    if ai_confidence is not None:
        verification.ai_confidence = ai_confidence

    # Get logged-in user
    user_id = get_jwt_identity()

    if verification_status in ["approved", "rejected"]:

        verification.verified_by = user_id
        verification.verified_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        "message": "Verification updated successfully",
        "verification": {
            "id": verification.id,
            "invoice_id": verification.invoice_id,
            "verified_by": verification.verified_by,
            "verification_status": verification.verification_status,
            "remarks": verification.remarks,
            "ai_confidence": (
                float(verification.ai_confidence)
                if verification.ai_confidence is not None
                else None
            ),
            "verified_at": (
                verification.verified_at.isoformat()
                if verification.verified_at
                else None
            )
        }
    }), 200