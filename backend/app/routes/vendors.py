from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity

from app.extensions.database import db
from app.models.vendor import Vendor
from app.models.invoice import Invoice

vendor_bp=Blueprint(
    "vendor",
    __name__,
)

@vendor_bp.route("",methods=["POST"])
@jwt_required()
def create_vendor():

    data=request.get_json()

    vendor_name=data.get("vendor_name")
    email=data.get("email")
    phone_number=data.get("phone_number")
    address=data.get("address")
    gst_number=data.get("gst_number")
    pan_number=data.get("pan_number")

    if not vendor_name or not email:
        return jsonify({
            "message":"Vendor Name and Email is Requried"
        }),400

    existing_vendor = Vendor.query.filter_by(
        email=email
    ).first()

    if existing_vendor:
        return jsonify({
            "message":"Vendor exist"
        }),409

    vendor = Vendor(
        vendor_name=vendor_name,
        email=email,
        phone_number=phone_number,
        address=address,
        gst_number=gst_number,
        pan_number=pan_number,
    )

    db.session.add(vendor)
    db.session.commit()

    return jsonify({
        "message":"Vendor Created Successfully",
        "vendor":{
           "id": vendor.id,
            "vendor_name": vendor.vendor_name,
            "email": vendor.email,
            "phone_number": vendor.phone_number,
            "address": vendor.address,
            "gst_number": vendor.gst_number,
            "pan_number": vendor.pan_number 
        }
    }),201

@vendor_bp.route("",methods=["GET"])
@jwt_required()
def get_vendors():

    vendors = Vendor.query.all()

    vendor_list=[]

    for vendor in vendors:
        vendor_list.append({
            "id":vendor.id,
            "vendor_name":vendor.vendor_name,
            "email":vendor.email,
            "phone_number":vendor.phone_number,
            "address":vendor.address,
            "gst_number":vendor.gst_number,
            "pan_number":vendor.pan_number,
        })

    return jsonify({
        "vendors":vendor_list
    }),200

@vendor_bp.route("/<int:vendor_id>",methods=["GET"])
@jwt_required()
def get_vendor(vendor_id):

    vendor= Vendor.query.get(vendor_id)

    if not vendor:
        return jsonify({
            "message": "Vendor not found"
        }),404

    return jsonify({
        "vendor":{
            "id": vendor.id,
            "vendor_name": vendor.vendor_name,
            "email": vendor.email,
            "phone_number": vendor.phone_number,
            "address": vendor.address,
            "gst_number": vendor.gst_number,
            "pan_number": vendor.pan_number
        }
    }),200

@vendor_bp.route("/<int:vendor_id>", methods=["PUT"])
@jwt_required()
def update_vendor(vendor_id):

    data = request.get_json()

    vendor = Vendor.query.get(vendor_id)

    if not vendor:
        return jsonify({
            "message": "Vendor not found"
        }), 404

    vendor_name = data.get("vendor_name")
    email = data.get("email")
    phone_number = data.get("phone_number")
    address = data.get("address")
    gst_number = data.get("gst_number")
    pan_number = data.get("pan_number")

    if not vendor_name or not email:
        return jsonify({
            "message": "Vendor name and email are required"
        }), 400

    existing_vendor = Vendor.query.filter(
        Vendor.email == email,
        Vendor.id != vendor_id
    ).first()

    if existing_vendor:
        return jsonify({
            "message": "Another vendor already uses this email"
        }), 409

    vendor.vendor_name = vendor_name
    vendor.email = email
    vendor.phone_number = phone_number
    vendor.address = address
    vendor.gst_number = gst_number
    vendor.pan_number = pan_number

    db.session.commit()

    return jsonify({
        "message": "Vendor updated successfully",
        "vendor": {
            "id": vendor.id,
            "vendor_name": vendor.vendor_name,
            "email": vendor.email,
            "phone_number": vendor.phone_number,
            "address": vendor.address,
            "gst_number": vendor.gst_number,
            "pan_number": vendor.pan_number
        }
    }), 200

@vendor_bp.route("/<int:vendor_id>", methods=["DELETE"])
@jwt_required()
def delete_vendor(vendor_id):

    vendor = Vendor.query.get(vendor_id)

    if not vendor:
        return jsonify({
            "message": "Vendor not found"
        }), 404

    db.session.delete(vendor)
    db.session.commit()

    return jsonify({
        "message": "Vendor deleted successfully"
    }), 200

@vendor_bp.route("/<int:vendor_id>/invoices", methods=["GET"])
@jwt_required()
def get_vendor_invoices(vendor_id):

    vendor = Vendor.query.get(vendor_id)

    if not vendor:
        return jsonify({
            "message":"Vendor not found"
        }),404

    invoices = Invoice.query.filter_by(
        vendor_id=vendor_id 
    ).all()

    invoice_list = []

    for invoice in invoices:
             invoice_list.append({
                 "id": invoice.id,
                 "invoice_number":invoice.invoice_number,
                 "invoice_date": (
                invoice.invoice_date.isoformat()
                if invoice.invoice_date else None
            ),
            "due_date": (
                invoice.due_date.isoformat()
                if invoice.due_date else None
            ),
            "subtotal": (
                float(invoice.subtotal)
                if invoice.subtotal is not None else None
            ),
            "tax_amount": (
                float(invoice.tax_amount)
                if invoice.tax_amount is not None else None
            ),
            "total_amount": (
                float(invoice.total_amount)
                if invoice.total_amount is not None else None
            ),
            "currency": invoice.currency,
            "payment_status": invoice.payment_status,
            "file_name": invoice.file_name,
            "created_at": (
                invoice.created_at.isoformat()
                if invoice.created_at else None
            )
        })

    return jsonify({
        "vendor":{
            "id": vendor.id,
            "vendor_name": vendor.vendor_name,
            "email": vendor.email
        },
        "invoices": invoice_list,
        "total_invoices": len(invoice_list)
    }),200