import os 

from app.config import Config
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES=[
   "https://www.googleapis.com/auth/drive" 
]

#connect to google drive

def get_drive_service():

    credentials_path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        ),
        "google-service-account.json"
    )

    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=SCOPES
    )

    drive_service = build(
        "drive",
        "v3",
        credentials=credentials
    )

    return drive_service

#to get list of invoices
def get_incoming_folder_id():

    folder_id=os.getenv("GOOGLE_DRIVE_INCOMING_FOLDER_ID")
    if not folder_id:
        raise ValueError(
           "GOOGLE_DRIVE_INCOMING_FOLDER_ID "
            "is not configured" 
        )

    return folder_id

def get_processing_folder_id():
    folder_id = os.getenv("GOOGLE_DRIVE_PROCESSING_FOLDER_ID")

    if not folder_id:
        raise ValueError(
            "GOOGLE_DRIVE_PROCESSING_FOLDER_ID"
            "is not configured"
        )
    
    return folder_id

def get_failed_folder_id():

    folder_id= os.getenv("GOOGLE_DRIVE_FAILED_FOLDER_ID")

    if not folder_id:
        raise ValueError(
            "GOOGLE_DRIVE_FAILED_FOLDER_ID "
            "is not configured" 
        )
    
    return folder_id

def get_completed_folder_id():
    folder_id = os.getenv("GOOGLE_DRIVE_COMPLETED_FOLDER_ID")

    if not folder_id:
        raise ValueError(
            "GOOGLE_DRIVE_COMPLETED_FOLDER_ID"
            "is not configured"
        )

    return folder_id

def get_duplicate_folder_id():
    folder_id = os.getenv("GOOGLE_DRIVE_DUPLICATE_FOLDER_ID")
    
    if not folder_id:
            raise ValueError(
                "GOOGLE_DRIVE_DUPLICATE_FOLDER_ID"
                "is not configured"
            )

    return folder_id

def list_invoice_files():

    folder_id = get_incoming_folder_id()

    drive_service = get_drive_service()

    results = drive_service.files().list(
        q=(
            f"'{folder_id}' in parents "
            "and trashed = false"
        ),
        fields=(
            "files("
            "id,"
            "name,"
            "mimeType,"
            "createdTime,"
            "modifiedTime"
            ")"
        ),
        orderBy="createdTime desc"
    ).execute()

    return results.get(
        "files",
        []
    )

#to download file from Google drive to local path
def download_file(file_id,destination_path):

    print("DEBUG download_file ID:", repr(file_id))

    drive_service=get_drive_service()

    request= drive_service.files().get_media(
        fileId=file_id
    )

    with open(destination_path,"wb") as file:
        downloader = MediaIoBaseDownload(file,request)

        done=False

        while not done:
            status,done = downloader.next_chunk()

            if status:
                print(
                    f"Download progress:"
                    f"{int(status.progress()*100)}%"
                )

    return destination_path

def move_file(file_id,destination_folder_id):

    drive_service = get_drive_service()

    file_metadata=(
        drive_service.files()
        .get(
            fileId=file_id,
            fields="parents"
        )
        .execute()
    )

    current_parents = file_metadata.get(
        "parents",
        []
    )

    drive_service.files().update(
        fileId=file_id,
        addParents=destination_folder_id,
        removeParents=",".join(
            current_parents
        ) if current_parents else None,
        fields="id, parents"
    ).execute()

    print(
        f"✅ File moved successfully: "
        f"{file_id}"
    )

    return True

def move_file_to_processing(file_id):
    processing_folder_id =get_processing_folder_id()

    return move_file(
        file_id,
        processing_folder_id
    )

def move_file_to_failed(file_id):

    failed_folder_id=get_failed_folder_id()
    return move_file(
        file_id,
        failed_folder_id
    )

def move_file_to_completed(file_id):

    completed_folder_id=get_completed_folder_id()
    return move_file(
        file_id,
        completed_folder_id
    )

def move_file_to_duplicates(file_id):

    duplicates_folder_id=get_duplicate_folder_id()
    return move_file(
        file_id,
        duplicates_folder_id
    )


def list_incoming_invoice():

    service = get_drive_service()

    incoming_folder_id= Config.GOOGLE_DRIVE_INCOMING_FOLDER_ID

    query=(
        f"'{incoming_folder_id}' in parents "
        f"and trashed = false "
        f"and mimeType = 'application/pdf'"
    )

    results = service.files().list(
        q=query,
        fields="files(id,name,mimeType,parents,createdTime,modifiedTime)",
        orderBy="createdTime"
    ).execute()

    return results.get("files",[])
