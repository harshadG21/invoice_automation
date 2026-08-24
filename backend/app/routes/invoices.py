from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime

from app.extensions.database import db
from app.models.invoice import Invoice
from app.models.vendor import Vendor

invoice_bp = Blueprint(
    "invoice",
    __name__
)

#Create Invoice
@invoice_bp.route("",methods=['POST'])
@jwt_required()
def create_invoice():

    data = request.get_json()

    invoice_number=data.get("invoice_number")
    vendor_id=data.get("vendor_id")
    invoice_date=data.get("invoice_date")
    due_date=data.get("due_date")
    subtotal=data.get("subtotal")
    tax_amount = data.get("tax_amount")
    total_amount = data.get("total_amount")
    currency = data.get("currency", "INR")
    file_name = data.get("file_name")
    file_path = data.get("file_path")
    status = data.get("status", "received")
    ocr_data = data.get("ocr_data")

    if not invoice_number:
        return jsonify({
            "message":"Invoice number is required"
        }),400

    if vendor_id:
        vendor= Vendor.query.get(vendor_id)

        if not vendor:
            return jsonify({
                "message":"Vendor not found"
            }),404
                
    existing_invoice=Invoice.query.filter_by(
        invoice_number=invoice_number
    ).first()

    if existing_invoice:
        return jsonify({
            "message":"Invoice with this number already exists"
        }),409

    try:

        parsed_invoice_date=(
            datetime.strptime(invoice_date,"%Y-%m-%d").date()
            if invoice_date
            else None
        )

        parsed_due_date = (
            datetime.strptime(due_date,"%Y-%m-%d").date()  
            if due_date
            else None
         )

    except ValueError:

        return jsonify({
            "message":"Date must be in YYYY-MM-DD Format"
        }),400

    invoice=Invoice(
       invoice_number=invoice_number,
        vendor_id=vendor_id,
        invoice_date=parsed_invoice_date,
        due_date=parsed_due_date,
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        currency=currency,
        file_name=file_name,
        file_path=file_path,
        status=status,
        ocr_data=ocr_data 
    )

    db.session.add(invoice)
    db.session.commit()

    return jsonify({
        "message":"Invoice created successfully",
        "invoice":{
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "vendor_id": invoice.vendor_id,
            "invoice_date": invoice.invoice_date.isoformat()
                if invoice.invoice_date else None,
            "due_date": invoice.due_date.isoformat()
                if invoice.due_date else None,
            "subtotal": float(invoice.subtotal)
                if invoice.subtotal is not None else None,
            "tax_amount": float(invoice.tax_amount)
                if invoice.tax_amount is not None else None,
            "total_amount": float(invoice.total_amount)
                if invoice.total_amount is not None else None,
            "currency": invoice.currency,
            "file_name": invoice.file_name,
            "file_path": invoice.file_path,
            "status": invoice.status,
            "ocr_data": invoice.ocr_data
        }
    }),201

#Get Invoice
@invoice_bp.route("",methods=["GET"])
@jwt_required()
def get_invoices():

    invoices=Invoice.query.all()

    invoice_list=[]

    for invoice in invoices:
        invoice_list.append({
            "id":invoice.id,
            "invoice_number":invoice.invoice_number,
            "vendor_id": invoice.vendor_id,
            "invoice_date":(
                invoice.invoice_date.isoformat()
                if invoice.invoice_date else None
            ),
            "due_date":(
                invoice.due_date.isoformat()
                if invoice.due_date else None
            ),
            "subtotal":(
                float(invoice.subtotal)  #you can run into JSON serialization problems because standard JSON doesn't have a native Decimal type.
                if invoice.subtotal is not None else None
            ),
            "total_amount":(
                float(invoice.total_amount)
                if invoice.total_amount is not None else None
            ),
            "currency":invoice.currency,
            "fle_name":invoice.file_name,
            "file_path":invoice.file_path,
            "status":invoice.status,
            "ocr_data": invoice.ocr_data,
            "created_at":(
                invoice.created_at.isoformat()
                if invoice.created_at else None
            ),
            "updated_at":(
                invoice.updated_at.isoformat()
                if invoice.updated_at else None
            )
        })

    return jsonify({
        "invoices":invoice_list
    }),200

@invoice_bp.route("/<int:invoice_id>",methods=["GET"])
@jwt_required()
def get_invoice(invoice_id):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({
            "message":"Invoice not Found"
        }),404

    return jsonify({
        "invoice":{
            "id":invoice.id,
            "invoice_number":invoice.invoice_number,
            "vendor_id": invoice.vendor_id,
            "invoice_date":(
                invoice.invoice_date.isoformat()
                if invoice.invoice_date else None
            ),
            "due_date":(
                invoice.due_date.isoformat()
                if invoice.due_date else None
            ),
            "subtotal":(
                float(invoice.subtotal)
                if invoice.subtotal is not None else None
            ),
            "tax_amount":(
                float(invoice.tax_amount)
                if invoice.tax_amount is not None else None
            ),
            "total_amount":(
                float(invoice.total_amount)
                if invoice.total_amount is not None else None
            ),
            "currency":invoice.currency,
            "file_name":invoice.file_name,
            "status": invoice.status,
            "ocr_data": invoice.ocr_data,
            "created_at": (
                invoice.created_at.isoformat()
                if invoice.created_at else None
            ),
            "updated_at": (
                invoice.updated_at.isoformat()
                if invoice.updated_at else None
            )
        }
    }),200

@invoice_bp.route("/<int:invoice_id>",methods=["PUT"])
@jwt_required()
def update_invoice(invoice_id):

    data = request.get_json()

    invoice=Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({
            "message":"Invoice not found"
        }),404

    invoice_number = data.get("invoice_number")
    vendor_id = data.get("vendor_id")
    invoice_date=data.get("invoice_date")
    due_date = data.get("due_date")
    subtotal=data.get("subtotal")
    tax_amount=data.get("tax_amount")
    total_amount = data.get("total_amount")
    currency = data.get("currency")
    file_name = data.get("file_name")
    file_path = data.get("file_path")
    status = data.get("status")
    ocr_data = data.get("ocr_data")

    if not invoice_number:
        return jsonify({
            "message":"Invoice number is required"
        }),400

    #check vendor 
    if vendor_id is not None:

        vendor=Vendor.query.get(vendor_id)

        if not vendor:
            return jsonify({
                "message":"Vendor not Found"
            }),404

        
    #check duplicates

    existing_invoice=Invoice.query.filter(
        Invoice.invoice_number == invoice_number,
        invoice.id != invoice_id
    ).first()


    if existing_invoice:
        return jsonify({
        "message": "Another invoice with this number alreasy exists"
    }),409

    try:

        parsed_invoice_date = (
            datetime.strptime(
                invoice_date,
                "%Y-%m-%d"
            ).date()
            if invoice_date
            else None
        )

        parsed_due_date = (
            datetime.strptime(
                due_date,
                "%Y-%m-%d"
            ).date()
            if due_date
            else None
        )

    except ValueError:

        return jsonify({
            "message": "Date must be in YYYY-MM-DD Format"
        }),400

    invoice.invoice_number=invoice_number
    invoice.vendor_id = vendor_id
    invoice.invoice_date = parsed_invoice_date
    invoice.due_date = parsed_due_date
    invoice.subtotal = subtotal
    invoice.tax_amount = tax_amount
    invoice.total_amount = total_amount
    invoice.currency = currency
    invoice.file_name = file_name
    invoice.file_path = file_path
    invoice.status = status
    invoice.ocr_data = ocr_data

    db.session.commit()

    return jsonify({
        "message":"Invoice updated Successfully",
        "invoice":{
            "id" : invoice.id,
                        "invoice_number": invoice.invoice_number,
            "vendor_id": invoice.vendor_id,
            "invoice_date": (
                invoice.invoice_date.isoformat()
                if invoice.invoice_date
                else None
            ),
            "due_date": (
                invoice.due_date.isoformat()
                if invoice.due_date
                else None
            ),
            "subtotal": (
                float(invoice.subtotal)
                if invoice.subtotal is not None
                else None
            ),
            "tax_amount": (
                float(invoice.tax_amount)
                if invoice.tax_amount is not None
                else None
            ),
            "total_amount": (
                float(invoice.total_amount)
                if invoice.total_amount is not None
                else None
            ),
            "currency": invoice.currency,
            "file_name": invoice.file_name,
            "file_path": invoice.file_path,
            "status": invoice.status,
            "ocr_data": invoice.ocr_data
        }
    }),200


#delete invoice

@invoice_bp.route("<int:invoice_id>",methods=["DELETE"])
@jwt_required()
def delete_invoice(invoice_id):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({
            "message":"Invoice not Found"
        }),404

    db.session.delete(invoice)
    db.session.commit()

    return jsonify({
        "message":"Invoice deleted Successfully"
    }),200
    