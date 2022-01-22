from __future__ import print_function
from os import device_encoding
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import base64
import email
import logging
from bs4 import BeautifulSoup
import json

def build_service(credential,id):
    """
    Builds a gmail service
    Args:
        credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                    request.
        id: users discord Id.
    Returns:
        A gamil service which helps us in retriving info from gmail.
    """
    creds=Credentials.from_authorized_user_info(info=credential)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # file = open('user_info.json','w+')
        # user_id = json.loads(file.read())
        # user_id[f"{id}"]['token']=creds.to_json()
        # file.seek(0)
        # file.write(json.dumps(user_id))
        # file.close()
        # print(user_id[f"{id}"]['token'])
    # else:
    #     raise Exception("User did not authorize this app from their gmail ID.")
    return build(serviceName='gmail', version='v1', credentials=creds)

def get_profile(credential,discord_id):
    """Send a request to the UserInfo API to retrieve the user's information.
    Args:
        credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                    request.
    Returns:
        User information as a dict.
    """
    service = build_service(credential,discord_id)
    user_info=None
    try:
        user_info = service.users().getProfile(userId='me').execute()
        unread = service.users().labels().get(userId='me',id='UNREAD').execute()
        msg=f"""Email Address: {user_info['emailAddress']}
        Message Total: {user_info['messagesTotal']}
        Unread Messages Total: {unread['messagesTotal']}
        Threads Total: {user_info['threadsTotal']}
        History Id: {user_info['historyId']}"""
    except Exception as error:
        logging.error('An error occurred: %s', error)
    return msg

def get_emails(credential,discord_id,maxresult=1):
    """Send a request to the UserInfo API to retrieve the user's information.
    Args:
        credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                    request.
        discord_id: users discord Id.
        maxresult: maximum number of result a user want to retrieve.
    Returns:
        A dictionary with emails basic info.(NOT THE CONTENT OF EMAILS)
    """
    service = build_service(credential,discord_id)
    result = service.users().messages().list(maxResults=maxresult,userId='me',labelIds=['INBOX']).execute()
    return result['messages']

def get_message(Id,credential,discord_id):
    try:
        service = build_service(credential,discord_id)
        msg_str = service.users().messages().get(userId='me',id=Id).execute()
        payld = msg_str['payload'] # get payload of the message 
        headr = payld['headers'] # get header of the payload
        try:
		
            # Fetching message body
            mssg_parts = payld['parts'] # fetching the message parts
            part_one  = mssg_parts[0] # fetching first element of the part 
            part_body = part_one['body'] # fetching body of the message
            part_data = part_body['data'] # fetching data from the body
            clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
            clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
            clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
            soup = BeautifulSoup(clean_two , "lxml" )
            mssg_body = soup.body()
            # mssg_body is a readible form of message body
            # depending on the end user's requirements, it can be further cleaned 
            # using regex, beautiful soup, or any other method
            # temp_dict['Message_body'] = mssg_body
            if len(str(mssg_body))>2000:return msg_str['snippet']
            else:return mssg_body
        except :
            print("Except")
            return msg_str['snippet']
    except Exception as error:
        print('An error occured: %s'%error)

#Labels:
# CHAT
# SENT
# INBOX
# IMPORTANT
# TRASH
# DRAFT
# SPAM
# CATEGORY_FORUMS
# CATEGORY_UPDATES
# CATEGORY_PERSONAL
# CATEGORY_PROMOTIONS
# CATEGORY_SOCIAL
# STARRED
# UNREAD
# Personal
# Receipts
# Work