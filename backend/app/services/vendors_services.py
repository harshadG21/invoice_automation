from app.models.vendor import Vendor
from app.extensions.database import db


def get_vendor_by_gst(gst_number):

    if not gst_number:
        return None

    return Vendor.query.filter_by(
        gst_number=gst_number
    ).first()


def get_vendor_by_email(email):

    if not email:
        return None

    return Vendor.query.filter_by(
        email=email
    ).first()


def create_vendor(vendor_data):

    vendor = Vendor(
        vendor_name=vendor_data.name,
        email=vendor_data.email,
        phone_number=vendor_data.phone,
        address=vendor_data.address,
        gst_number=vendor_data.gst_number,
        pan_number=vendor_data.pan_number
    )

    db.session.add(vendor)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return vendor


def get_or_create_vendor(invoice_data):

    vendor_data = invoice_data.vendor

    vendor = get_vendor_by_gst(
        vendor_data.gst_number
    )

    if vendor:
        return vendor

    vendor = get_vendor_by_email(
        vendor_data.email
    )

    if vendor:
        return vendor

    return create_vendor(vendor_data)

def get_vendor_by_email(email):

    # Don't query the database when email is missing.
    if not email:
        return None

    return Vendor.query.filter_by(
        email=email
    ).first()

def get_vendor_by_gst(gst_number):

    if not gst_number:
        return None

    return Vendor.query.filter_by(
        gst_number=gst_number
    ).first()