from app.services.google_drive_service import get_drive_service

FILE_ID = "14ARRw4-OcaYxztxgq6ZqNeubrZOp5AUG"

INCOMING_FOLDER_ID = "1YZyp4wiYFogqKULaIri73J4LIQmmcQU8"

PROCESSING_FOLDER_ID = "1XXPQHHXeq6lmJFy5qM0jTz--ShOiR9tF"

service = get_drive_service()

print("\n========== MOVING INVOICE ==========")
print("File ID:", FILE_ID)
print("From:", INCOMING_FOLDER_ID)
print("To:", PROCESSING_FOLDER_ID)

result = service.files().update(
    fileId=FILE_ID,
    addParents=PROCESSING_FOLDER_ID,
    removeParents=INCOMING_FOLDER_ID,
    supportsAllDrives=True,
    fields="id,name,parents"
).execute()

print("\n========== MOVE SUCCESS ==========")
print("ID:", result.get("id"))
print("Name:", result.get("name"))
print("Parents:", result.get("parents"))
print("==================================\n")