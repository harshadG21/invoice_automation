from app.models.vendor import Vendor

def normalize(value):

    if not value:
        return None

    return (
        value
        .strip()
        .lower()
        .replace(".","")
        .replace(",","")
    )

def find_matching_vendor(vendor_data):

    vendor_name = normalize(vendor_data.name)
    vendor_email=normalize(vendor_data.email)
    vendor_gst = normalize(vendor_data.gst_number)

    if vendor_email:
        vendor = Vendor.query.filter_by(
            email=vendor_data.email
        ).first()

        if vendor:
            print("\n========================================")
            print("VENDOR MATCHED BY EMAIL")
            print("========================================")
            print("Invoice Vendor:", vendor_data.name)
            print("Database Vendor:", vendor.vendor_name)
            print("Email:", vendor_data.email)
            print("========================================")

            return vendor

    if vendor_gst:

         vendor=Vendor.query.filter_by(
              gst_number=vendor_data.gst_number
         ).first()

         if vendor:
            database_name = normalize(vendor.vendor_name)

            if database_name == vendor_name:

                print("\n=================================")
                print("VENDOR MATCHED BY GST + NAME")
                print("===================================")
                print("Invoice Vendor:", vendor_data.name)
                print("Database Vendor:", vendor.vendor_name)
                print("GST:", vendor_data.gst_number)
                print("=====================================")
                return vendor 

            print("\n=============================")
            print("VENDOR IDENTITY CNFLICT")
            print("================================")
            print("Invoice Vendor:", vendor_data.name)
            print("Existing Vendor:", vendor.vendor_name)
            print("GST:", vendor_data.gst_number)
            print("========================================")

            return None

    if vendor_name:
            vendor = Vendor.query.filter(
                 Vendor.vendor_name.isnot(None)
            ).all()

            vendor = next((v for v in vendor if normalize(v.vendor_name)==vendor_name),None)

            if vendor:
                print("\n========================================")
                print("VENDOR MATCHED BY NAME")
                print("========================================")
                print("Invoice Vendor:", vendor_data.name)
                print("Database Vendor:", vendor.vendor_name)
                print("========================================")
                return vendor

    print("\n========================================")
    print("NEW VENDOR")
    print("========================================")
    print("Vendor:", vendor_data.name)
    print("Email:", vendor_data.email)
    print("GST:", vendor_data.gst_number)
    print("========================================")

    return None

    

