import os 

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

def list_invoice_files():

    folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

    if not folder_id:
        raise ValueError(
            "GOOGLE_DRIVE_FOLDER_ID is not configured"
        )

    drive_service = get_drive_service()

    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name, mimeType, createdTime, modifiedTime)",
        orderBy="createdTime desc"
    ).execute()

    return results.get("files", [])

#to download file from Google drive to local path

def download_file(file_id,destination_path):

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
