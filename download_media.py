# MIT License
#
# Copyright (c) 2020 Segno Lin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Media download Google Drive API for SingularityNET

Arguments folder_to_download and store_location with
OAuth2.0 credentials (credentials.json stored in working
directory) are required.
"""
import io
import os
import pickle
import sys

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=1337)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token, protocol=0)
    service = build('drive', 'v3', credentials=creds)

    location = ''
    if len(sys.argv) > 2:
        location = sys.argv[2]
        if location[-1] != '/':
            location += '/'

    # Search for desired folder in shared drive
    folder = service.files().list(
            corpora='drive',
            driveId='<Enter Shared Drive ID>',
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            q=f"name contains '{sys.argv[1]}' and mimeType='application/vnd.google-apps.folder'",
            fields='files(id, name, parents)').execute()

    total = len(folder['files'])
    if total != 1:
        print(f'{total} folders found')
        if total == 0:
            sys.exit(1)
        prompt = 'Please select the folder you want to download:\n\n'
        for i in range(total):
            prompt += f'[{i}]: {get_full_path(service, folder["files"][i])}\n'
        prompt += '\nYour choice: '
        choice = int(input(prompt))
        if 0 <= choice and choice < total:
            folder_id = folder['files'][choice]['id']
            folder_name = folder['files'][choice]['name']
        else:
            sys.exit(1)
    else:
        folder_id = folder['files'][0]['id']
        folder_name = folder['files'][0]['name']

    print(f'{folder_id} {folder_name}')
    download_folder(service, folder_id, location, folder_name)


def get_full_path(service, folder):
    if not 'parents' in folder:
        return folder['name']
    files = service.files().get(fileId=folder['parents'][0], fields='id, name, parents').execute()
    path = files['name'] + ' > ' + folder['name']
    while 'parents' in files:
        files = service.files().get(fileId=files['parents'][0], fields='id, name, parents').execute()
        path = files['name'] + ' > ' + path
    return path


def download_folder(service, folder_id, location, folder_name):
    """Recursive tree walk to download folders"""
    # Folder creation
    if not os.path.exists(location + folder_name):
        os.makedirs(location + folder_name)
    location += folder_name + '/'

    result = []
    page_token = None
    while True:
        # Get all sub-folders and files that have a common parent
        files = service.files().list(
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                q=f"'{folder_id}' in parents",
                fields='nextPageToken, files(id, name, mimeType)',
                pageToken=page_token,
                pageSize=1000).execute()
        result.extend(files['files'])
        page_token = files.get("nextPageToken")
        if not page_token:
            break

    result = sorted(result, key=lambda k: k['name'])
    # Restricting download to only Media Gallery Content
    for file in result:
        if 'Media Gallery Content' in list(file.values()):
            result = [file]

    total = len(result)
    current = 1
    # Tree walk to determine whether to download folder or file
    for item in result:
        file_id = item['id']
        filename = item['name']
        mime_type = item['mimeType']
        print(f'{file_id} {filename} {mime_type} ({current}/{total})')
        if mime_type == 'application/vnd.google-apps.folder':
            download_folder(service, file_id, location, filename)
        elif not os.path.isfile(location + filename):
            download_file(service, file_id, location, filename, mime_type)
        current += 1


def download_file(service, file_id, location, filename, mime_type):
    """Download file of given file_id"""
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(location + filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request, 1024 * 1024 * 1024)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        if status:
            print(f'\rDownload {int(status.progress() * 100)}%.', end='')
    print('')


if __name__ == '__main__':
    main()
