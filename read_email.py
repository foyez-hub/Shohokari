import time
import base64
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request  # Added import

# If modifying these SCOPES, delete token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
from llm import generate_gemini_response 

def gmail_authenticate():
    creds = None
    # Use the token file if it exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If no valid credentials available, start login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save token for next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_latest_message_id(service):
    results = service.users().messages().list(userId='me', maxResults=1, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    return messages[0]['id'] if messages else None

def read_message(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    headers = msg['payload']['headers']
    subject = next(h['value'] for h in headers if h['name'] == 'Subject')
    from_email = next(h['value'] for h in headers if h['name'] == 'From')

    # Decode body
    body = ""
    parts = msg['payload'].get('parts')
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                body = base64.urlsafe_b64decode(data).decode()
                break
    else:
        data = msg['payload']['body']['data']
        body = base64.urlsafe_b64decode(data).decode()

    print(f"\n📩 New Email from: {from_email}")
    print(f"Subject: {subject}")
    print(f"Body: {body[:200]}...")  # First 200 characters

    return subject , body

# def main():
#     service = gmail_authenticate()
#     last_id = get_latest_message_id(service)
#     print("✅ Watching for new emails...")

#     while True:
#         time.sleep(10)  # Check every 10 seconds
#         new_id = get_latest_message_id(service)
#         if new_id != last_id:
#             read_message(service, new_id)
#             last_id = new_id

# if __name__ == '__main__':
#     main()
