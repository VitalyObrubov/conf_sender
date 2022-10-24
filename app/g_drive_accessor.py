import os
import io
import qrcode
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import Resource, build
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.globals import MyApp

class GoogleDrive:
    service: Resource
    credentials: service_account.Credentials
    def __init__(self, app: "MyApp"):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = app.config.google.cred_file
        self.credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    def init(self):
        self.service = build('drive', 'v3', credentials = self.credentials)

    def download_conf_file(self, file: str, app: "MyApp"):
        self.init()
        results = self.service.files().list(
            pageSize=5, 
            fields="nextPageToken, files(id, name)",
            q=f"'{app.config.google.configs_folder}' in parents and name = '{file}.conf'").execute()
        if results:
            file_id = results["files"][0]["id"]
            request = self.service.files().get_media(fileId=file_id)
            filename = os.path.join("temp", results["files"][0]["name"])
            fh = io.FileIO(filename, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            f = open(filename,'r').read()
            img = qrcode.make(f)
            img.save(os.path.join("temp",file+".png"))

    def clear_temp(self):
        res = ""
        for filename in os.listdir("temp"):
            file_path = os.path.join("temp", filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                res += f'Не удалено {file_path}. По причине: {e} \n'
                print(res)
        return res        

    