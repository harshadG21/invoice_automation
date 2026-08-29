from app.services.google_drive_service import list_invoice_files


files = list_invoice_files()

print("\nFILES FOUND:")
print("-" * 50)

for file in files:
    print(
        file["name"],
        "|",
        file["mimeType"],
        "|",
        file["id"]
    )