from app import create_app

from app.services.vendors_services import (
    create_vendor,
    get_vendor_by_gst,
    get_vendor_by_email,
)

app = create_app()

with app.app_context():

    vendor_data = {
    "vendor_name": "Tech Solutions Pvt. Ltd.",
    "vendor_email": "billing@techsolutions.com",
    "vendor_phone": "+91 9876543210",
    "vendor_address": "Andheri East, Mumbai, Maharashtra - 400069",
    "gst_number": "27AABCT1234F1Z5",
    "pan_number": "AABCT1234F",
}


    # Create the vendor in the database.
    vendor = create_vendor(vendor_data)


# Display the vendor that was created.
    print("VENDOR CREATED:")
    print("-" * 40)
    print("ID:", vendor.id)
    print("Name:", vendor.vendor_name)
    print("Email:", vendor.email)
    print("GST:", vendor.gst_number)
    print("PAN:", vendor.pan_number)


# Search for the same vendor using its GST number.
    found_by_gst = get_vendor_by_gst(
    "27AABCT1234F1Z5"
    )


# Display the GST search result.
    print("\nVENDOR FOUND BY GST:")
    print("-" * 40)
    print("ID:", found_by_gst.id)
    print("Name:", found_by_gst.vendor_name)


# Search for the same vendor using its email.
    found_by_email = get_vendor_by_email(
    "billing@techsolutions.com"
     )


# Display the email search result.
    print("\nVENDOR FOUND BY EMAIL:")
    print("-" * 40)
    print("ID:", found_by_email.id)
    print("Name:", found_by_email.vendor_name)