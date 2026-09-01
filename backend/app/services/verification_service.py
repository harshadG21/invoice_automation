from datetime import datetime 

from app.models.verifications import Verification
from app.extensions.database import db

def create_verification(
     invoice_id,
    verification_status="pending",
    remarks=None,
    ai_confidence=None,
    verified_by=None   
):
    verification = Verification(
        invoice_id = invoice_id,
        verified_by=verified_by,
        verification_status=verification_status,
        remarks=remarks,
        ai_confidence=ai_confidence,
        verified_at=(
            datetime.utcnow()
            if verification_status != "pending"
            else None
        )
    )

    db.session.add(verification)

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return verification

def get_verification_by_invoice_id(invoice_id):

    if not invoice_id:
        return None

    return Verification.query.filter_by(
        invoice_id = invoice_id
    ).first()