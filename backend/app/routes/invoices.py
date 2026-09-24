from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime

from app.extensions.database import db
from app.models.invoice import Invoice
from app.models.vendor import Vendor
from app.services.reminder_services import get_payment_state

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
    payment_status = data.get("status", "received")
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
        payemnt_status=payment_status,
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
            "payment_status": invoice.payment_status,
            "payment_state":get_payment_state(invoice),
            "ocr_data": invoice.ocr_data
        }
    }),201

#Get Invoice
@invoice_bp.route("",methods=["GET"])
@jwt_required()
def get_invoices():

    payment_state_filter = request.args.get("payment_state")

    invoices=Invoice.query.all()

    invoice_list=[]

    for invoice in invoices:

        payment_state = get_payment_state(invoice)
        if payment_state_filter:
            if payment_state_filter not in ["paid", "unpaid", "overdue"]:
                return jsonify({
                   "message": (
                        "payment_state must be "
                        "'paid', 'unpaid', or 'overdue'" 
                   )
                }),400
            
            if payment_state != payment_state_filter:
                continue

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
            "payment_status":invoice.payment_status,
            "payment_state": payment_state,
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

@invoice_bp.route("/payment-summary", methods=["GET"])
@jwt_required()
def get_payment_summary():

    invoices = Invoice.query.all()

    paid_count=0
    unpaid_count = 0
    overdue_count = 0

    total_amount =0
    paid_amount =0
    unpaid_amount = 0
    overdue_amount = 0

    for invoice in invoices:

        payment_state = get_payment_state(invoice)

        amount=(
            float(invoice.total_amount)
            if invoice.total_amount is not None
            else 0
        )

        total_amount += amount

        if payment_state == "paid":

            paid_count +=1
            paid_amount += amount

        elif payment_state == "overdue":

            overdue_count +=1
            overdue_amount += amount

        else:

            unpaid_count +=1
            unpaid_amount += amount

    return jsonify({
        "total_invoices": len(invoices),

        "paid": paid_count,
        "unpaid": unpaid_count,
        "overdue": overdue_count,

        "total_amount": total_amount,
        "paid_amount": paid_amount,
        "unpaid_amount": unpaid_amount,
        "overdue_amount": overdue_amount
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
    payemnt_status = data.get("payement_status")
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
    invoice.payment_status= payemnt_status
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
            "payment_status": invoice.payment_status,
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

@invoice_bp.route("/<int:invoice_id>/payment-status", methods=["PUT"])
@jwt_required()
def update_payment_status(invoice_id):

    data = request.get_json() or {}

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({
            "message": "Invoice not found"
        }), 404

    payment_status = data.get("payment_status")

    # Only allow valid payment statuses
    if payment_status not in ["unpaid", "paid"]:
        return jsonify({
            "message": "payment_status must be either 'unpaid' or 'paid'"
        }), 400

    invoice.payment_status = payment_status

    db.session.commit()

    return jsonify({
        "message": "Payment status updated successfully",
        "invoice": {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "payment_status": invoice.payment_status
        }
    }), 200

