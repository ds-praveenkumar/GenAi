#===============================================================================
#  File Name    : mail_tool.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-08-22
#  Last Updated : 2025-08-22
#  Version      : v1.0.0

#  Language     : Python
#  File name    : mail_tool.py
#  Dependencies : 
#    - Dependency 1
#    - Dependency 2

#  Inputs       : Expected inputs
#  Outputs      : Expected outputs
#  Usage        : 
#    Example usage

#  Notes        : 
#    - Notes or TODOs
#===============================================================================
import sys
sys.path.append('.')
import os.path
import base64
import os.path
import uuid

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- New Imports for HTML and OCR ---
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
import io
import re

SAVE_DIR = "emails_with_images"
os.makedirs(SAVE_DIR, exist_ok=True)

# Scopes for reading Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    # token.json stores access/refresh tokens after first run
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If no valid token, authenticate user
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server()
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def list_unread_messages():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
    messages = results.get('messages', [])
    if not messages:
        print("No unread messages.")
    else:
        print(f"Found {len(messages)} unread messages:")
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            for header in msg_data['payload']['headers']:
                if header['name'] == 'Subject':
                    print("Subject:", header['value'])
def view_unread_messages():
    """
    Retrieves and displays unread messages from the user's inbox
    without marking them as read.
    """
    service = get_gmail_service()
    if not service:
        return

    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            print("No unread messages found.")
        else:
            print(f"Found {len(messages)} unread messages:\n")
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                
                headers = msg['payload']['headers']
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
                sender = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown Sender')
                
                print(f"From: {sender}")
                print(f"Subject: {subject}")
                
                # --- START: NEW ROBUST BODY PARSING LOGIC ---
                body_text = "" # Default to an empty string
                if 'parts' in msg['payload']:
                    # It's a multipart message, find the body
                    for part in msg['payload']['parts']:
                        if part['mimeType'] == 'text/plain':
                            data = part['body']['data']
                            body_text = base64.urlsafe_b64decode(data).decode('utf-8')
                            break # Found plain text, no need to look further
                        elif part['mimeType'] == 'text/html':
                            # If no plain text, save the HTML as a fallback
                            data = part['body']['data']
                            body_text = base64.urlsafe_b64decode(data).decode('utf-8')
                            # Don't break, keep looking for a plain text version if available
                else:
                    # It's a single part message
                    if 'data' in msg['payload']['body']:
                        data = msg['payload']['body']['data']
                        body_text = base64.urlsafe_b64decode(data).decode('utf-8')

                print(f"Body: {body_text[:300]}...\n") # Increased snippet size


    except HttpError as error:
        print(f'An error occurred while processing messages: {error}')
def get_text_from_image(image_data):
    """Performs OCR on image data to extract text."""
    try:
        # Open the image from the in-memory bytes
        image = Image.open(io.BytesIO(image_data))
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Could not process image with OCR: {e}")
        return ""
    
def view_unread_messages():
    """
    Retrieves, parses (HTML and images), and displays unread messages.
    """
    service = get_gmail_service()
    if not service:
        return

    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            print("No unread messages found.")
            return

        print(f"Found {len(messages)} unread messages:\n" + "="*30)

        for message in messages:
            # Use format='full' to get all parts, including attachments
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            
            headers = msg['payload']['headers']
            subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), 'No Subject')
            sender = next((header['value'] for header in headers if header['name'].lower() == 'from'), 'Unknown Sender')
            
            print(f"From: {sender}")
            print(f"Subject: {subject}\n")
            
            # --- Advanced Body and Attachment Parsing Logic ---
            plain_text_body = ""
            html_body = ""
            image_texts = []
            
            parts = [msg['payload']] # Start with the main payload
            while parts:
                part = parts.pop(0)
                mime_type = part.get('mimeType', '')
                
                # 1. Handle Text and HTML parts
                if mime_type == 'text/plain' and 'data' in part['body']:
                    data = part['body']['data']
                    plain_text_body += base64.urlsafe_b64decode(data).decode('utf-8', 'ignore')
                
                elif mime_type == 'text/html' and 'data' in part['body']:
                    data = part['body']['data']
                    html_content = base64.urlsafe_b64decode(data).decode('utf-8', 'ignore')
                    # Use BeautifulSoup to convert HTML to clean text
                    soup = BeautifulSoup(html_content, "html.parser")
                    html_body += soup.get_text(separator='\n', strip=True)

                # 2. Handle Image Attachments
                elif mime_type.startswith('image/') and 'attachmentId' in part['body']:
                    attachment_id = part['body']['attachmentId']
                    attachment = service.users().messages().attachments().get(
                        userId='me', messageId=message['id'], id=attachment_id
                    ).execute()
                    image_data = base64.urlsafe_b64decode(attachment['data'])
                    ocr_text = get_text_from_image(image_data)
                    if ocr_text.strip():
                        image_texts.append(ocr_text)

                # 3. Handle multipart content (dig deeper)
                if 'parts' in part:
                    parts.extend(part['parts'])
            
            # --- Display the extracted content ---
            print("--- Message Body ---")
            if plain_text_body:
                print(plain_text_body)
            elif html_body:
                print(html_body)
            else:
                print("[No readable text body found]")

            if image_texts:
                print("\n--- Text Extracted from Images (OCR) ---")
                for i, text in enumerate(image_texts, 1):
                    print(f"[Image {i} Text]:\n{text}")
            
            print("="*30 + "\n")

    except HttpError as error:
        print(f'An error occurred while processing messages: {error}')
        
        
def remove_links(text):
    """Uses a regular expression to remove URLs from a string."""
    if not isinstance(text, str):
        return ""
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def view_unread_messages_final():
    """
    Retrieves, parses (HTML and images), cleans, and displays unread messages.
    """
    service = get_gmail_service()
    if not service:
        return

    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            print("No unread messages found.")
            return

        print(f"Found {len(messages)} unread messages:\n" + "="*30)

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            
            headers = msg['payload']['headers']
            subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), 'No Subject')
            sender = next((header['value'] for header in headers if header['name'].lower() == 'from'), 'Unknown Sender')
            
            print(f"From: {sender}")
            print(f"Subject: {subject}\n")
            
            plain_text_body = ""
            html_body = ""
            image_texts = []
            
            parts = [msg['payload']]
            while parts:
                part = parts.pop(0)
                mime_type = part.get('mimeType', '')
                
                if mime_type == 'text/plain' and 'data' in part['body']:
                    data = part['body']['data']
                    decoded_text = base64.urlsafe_b64decode(data).decode('utf-8', 'ignore')
                    # <-- MODIFIED: Apply link removal -->
                    plain_text_body += remove_links(decoded_text)
                
                elif mime_type == 'text/html' and 'data' in part['body']:
                    data = part['body']['data']
                    html_content = base64.urlsafe_b64decode(data).decode('utf-8', 'ignore')
                    soup = BeautifulSoup(html_content, "html.parser")
                    # <-- MODIFIED: Apply link removal -->
                    html_body += remove_links(soup.get_text(separator='\n', strip=True))

                elif mime_type.startswith('image/') and 'attachmentId' in part['body']:
                    attachment_id = part['body']['attachmentId']
                    attachment = service.users().messages().attachments().get(
                        userId='me', messageId=message['id'], id=attachment_id
                    ).execute()
                    image_data = base64.urlsafe_b64decode(attachment['data'])
                    ocr_text = get_text_from_image(image_data)
                    # <-- MODIFIED: Apply link removal -->
                    cleaned_ocr_text = remove_links(ocr_text)
                    if cleaned_ocr_text.strip():
                        image_texts.append(cleaned_ocr_text)

                if 'parts' in part:
                    parts.extend(part['parts'])
            
            print("--- Message Body (links removed) ---")
            if plain_text_body:
                print(plain_text_body)
            elif html_body:
                print(html_body)
            else:
                print("[No readable text body found]")

            if image_texts:
                print("\n--- Text Extracted from Images (OCR, links removed) ---")
                for i, text in enumerate(image_texts, 1):
                    print(f"[Image {i} Text]:\n{text}")
            
            print("="*30 + "\n")

    except HttpError as error:
        print(f'An error occurred while processing messages: {error}')
        
def process_and_display_messages(service, messages):
    """
    Takes a list of message objects, fetches their full content, parses,
    cleans, and displays them.
    """
    if not messages:
        print("No matching unread messages found.")
        return

    print(f"Found {len(messages)} matching unread messages:\n" + "="*30)
    processed_mails = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        
        headers = msg['payload']['headers']
        subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), 'No Subject')
        sender = next((header['value'] for header in headers if header['name'].lower() == 'from'), 'Unknown Sender')
        
        print(f"From: {sender}")
        print(f"Subject: {subject}\n")
        
        plain_text_body = ""
        html_body = ""
        image_texts = []
        
        parts = [msg['payload']]
        while parts:
            part = parts.pop(0)
            mime_type = part.get('mimeType', '')
            
            if mime_type == 'text/plain' and 'data' in part['body']:
                data = part['body']['data']
                decoded_text = base64.urlsafe_b64decode(data).decode('utf-8', 'ignore')
                plain_text_body += remove_links(decoded_text)
            
            elif mime_type == 'text/html' and 'data' in part['body']:
                data = part['body']['data']
                html_content = base64.urlsafe_b64decode(data).decode('utf-8', 'ignore')
                soup = BeautifulSoup(html_content, "html.parser")
                html_body += remove_links(soup.get_text(separator='\n', strip=True))

            elif mime_type.startswith('image/') and 'attachmentId' in part['body']:
                attachment_id = part['body']['attachmentId']
                attachment = service.users().messages().attachments().get(
                    userId='me', messageId=message['id'], id=attachment_id
                ).execute()
                image_data = base64.urlsafe_b64decode(attachment['data'])
                ocr_text = get_text_from_image(image_data)
                cleaned_ocr_text = remove_links(ocr_text)
                if cleaned_ocr_text.strip():
                    image_texts.append(cleaned_ocr_text)

            if 'parts' in part:
                parts.extend(part['parts'])
        
        print("--- Message Body (links removed) ---")
        if plain_text_body:
            print(plain_text_body)
            processed_mails.append(plain_text_body)
        elif html_body:
            print(html_body)
            processed_mails.append(plain_text_body)
        else:
            print("[No readable text body found]")

        if image_texts:
            print("\n--- Text Extracted from Images (OCR, links removed) ---")
            for i, text in enumerate(image_texts, 1):
                print(f"[Image {i} Text]:\n{text}")
                processed_mails.append(text)
        
        print("="*30 + "\n")
    return processed_mails

def view_unread_messages_from_sender( sender_email):
    """Retrieves unread messages from a specific sender and processes them."""
    service = get_gmail_service()
    try:
        # The query 'q' is updated to filter by sender
        query = f"is:unread from:{sender_email}"
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q=query).execute()
        messages = results.get('messages', [])
        process_and_display_messages(service, messages)
    except HttpError as error:
        print(f'An error occurred: {error}')

def view_unread_messages_from_sender(sender_name: str):
    """
    Retrieves unread messages from a sender (partial match) and:
    - Extracts HTML and images.
    - Saves them locally.
    - Marks the messages as read.
    """
    service = get_gmail_service()
    try:
        query = f'is:unread from:"{sender_name}"'
        response = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            q=query
        ).execute()

        messages = response.get("messages", [])
        if not messages:
            print(f"No unread messages found from '{sender_name}'.")
            return
        print(f"Found {len(messages)} unread message(s) from '{sender_name}'.")
        mails = process_and_display_messages(service, messages)
        if mails:
            return { f"mail {i+1}: {mail}" for i,mail in enumerate(mails) }
        else:
            return "no mails found"
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == '__main__':
    # list_unread_messages()
    # view_unread_messages()
    # view_unread_messages()
    # view_unread_messages_final()
    mails = view_unread_messages_from_sender("Neo ")
    print( mails )