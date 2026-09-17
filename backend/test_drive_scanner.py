from app.services.google_drive_service import list_incoming_invoice


files = list_incoming_invoice()

print("\n========== INCOMING INVOICES ==========")

if not files:
    print("No invoice PDFs found.")

else:
    for file in files:
        print("----------------------------------------")
        print("File ID:", file["id"])
        print("File Name:", file["name"])
        print("MIME Type:", file["mimeType"])
        print("Parents:", file.get("parents"))
        print("Created:", file.get("createdTime"))
        print("Modified:", file.get("modifiedTime"))

print("========================================\n")