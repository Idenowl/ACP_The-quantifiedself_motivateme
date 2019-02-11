from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaIoBaseDownload
import io

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
def findfileid_sleep(service) :
    '''
    This function search and return the ID of the Sleep file
    :param service: build service drive version 3 API
    :return: id the file (string)
    '''
    Sleepid=None
    page_token = None
    while True:
        response =service.files().list(q="name contains 'Sleep as Android Spreadsheet'").execute()
        for file in response.get('files', []):
            #print(file.get('name'),file.get('id'))
            Sleepid=file.get('id')
            page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    if Sleepid :
        return Sleepid

def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API

    #Paths declaration
    pathsleep = 'data/sleep/sleep.csv'
    pathstress = 'data/questionaires/stress.csv'
    pathemotion = 'data/questionaires/emotion.csv'

    #Id of the files
    file_id_stress = '111GQlXoY9qL8zTDr_JL9tZMaq-HhagNKrPG79WdV3jE'
    file_id_emotion = '1BoY4B4R_RFGJk7fjJHoFrlaJDDDKPP1dIHn__Ufp094'

    if findfileid_sleep(service): #If the function find the id of the file Sleep
        file_id_sleep=findfileid_sleep(service)
        print('Sleep ID :',file_id_sleep)
        #Export the file
        rq_sleep = service.files().export(fileId=file_id_sleep, mimeType='text/csv')
        fh_sleep = io.FileIO(pathsleep, 'wb')
        downloader_sleep = MediaIoBaseDownload(fh_sleep, rq_sleep)
        done = False
        while done is False:
            status_sleep, done = downloader_sleep.next_chunk()

        if not rq_sleep:
            print('Problem with export')
        else:
            print(pathsleep)

    else :
        print("Sleep file not found, check on your drive if the file exist")

    rq_stress =service.files().export(fileId=file_id_stress,mimeType='text/csv')
    rq_emotion=service.files().export(fileId=file_id_emotion,mimeType='text/csv')

    fh_stress=io.FileIO(pathstress,'wb')
    fh_emotion=io.FileIO(pathemotion, 'wb')

    downloader_stress=MediaIoBaseDownload(fh_stress, rq_stress)
    downloader_emotion = MediaIoBaseDownload(fh_emotion, rq_emotion)

    done2 = False
    done3=False

    while done2 is False:
        status_stress, done2 = downloader_stress.next_chunk()
        print
        "Download %d%%." % int(status_stress.progress() * 100)
    while done3 is False :
        status_emotion, done3 = downloader_emotion.next_chunk()
        print
        "Download %d%%." % int(status_emotion.progress() * 100)

    if not rq_stress :
        print('File stress not found')
    else :
        print(pathstress)
    if not rq_emotion :
        print('File emotion  not found')
    else :
        print(pathemotion)


if __name__ == '__main__':
    main()

    ###source https://developers.google.com/drive/api/v3/manage-downloads

