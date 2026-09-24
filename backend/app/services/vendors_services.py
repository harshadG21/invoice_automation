from app.models.vendor import Vendor
from app.extensions.database import db
from app.services.vendor_matching_service import find_matching_vendor


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

def get_vendor_by_name(name):

    if not name:
        return None

    normalized_name = (
        name
        .strip()
        .lower()
        .replace(".", "")
        .replace(",", "")
    )

    vendors=Vendor.query.all()

    for vendor in vendors:
        if not vendor.vendor_name:
            continue

        normalized_vendor_name =(
            vendor.vendor_name
            .strip()
            .lower()
            .replace(".", "")
            .replace(",", "")
        )

        if normalized_vendor_name == normalized_name:
            return vendor 

    return None

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

   vendor = find_matching_vendor(
       invoice_data.vendor
   )

   if vendor:
       return vendor

   return create_vendor(
       invoice_data.vendor
   )
