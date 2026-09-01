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

        vendor_name = vendor_data.get("vendor_name"),
        email= vendor_data.get("vendor_email"),
        phone_number=vendor_data.get("vendor_phone"),
        address=vendor_data.get("vendor_address"),
        gst_number=vendor_data.get("gst_number"),
        pan_number=vendor_data.get("pan_number"),
    )

    db.session.add(vendor)

    try:
     db.session.commit()
    except Exception:
     db.session.rollback()
     raise
    return vendor

def get_or_create_vendor(vendor_data):

   vendor = get_vendor_by_gst(
      vendor_data.get("gst_number")
   )

   if vendor:
      return vendor

   vendor = get_vendor_by_email(
      vendor_data.fet("vendor_email")
   )

   if vendor:
      return vendor

   return create_vendor(vendor_data)

"""
Does GST 27AABCT1234F1Z5 exist?
        ↓
       NO
        ↓
Create vendor
        ↓
Vendor ID = 1

"""