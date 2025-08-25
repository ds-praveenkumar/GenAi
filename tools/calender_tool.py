
import datetime
import pytz
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_datetime_with_tz(year, month, day, hour, minute, tz_name="Asia/Kolkata"):
    tz = pytz.timezone(tz_name)
    return tz.localize(datetime.datetime(year, month, day, hour, minute))

def get_calendar_service():
    creds = None
    if os.path.exists('calendar_token.json'):
        creds = Credentials.from_authorized_user_file('calendar_token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('calendar_token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def event_exists(service, summary, start_time, end_time):
    """
    Check if an event with the same summary exists in the given time range.
    """
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    for event in events:
        if event.get('summary', '').lower() == summary.lower():
            return True
    return False

def add_calendar_event(summary, start_time, end_time, description="", location=""):
    """
    Add a new event only if it doesn't already exist in the specified time range.
    """
    service = get_calendar_service()

    if event_exists(service, summary, start_time, end_time):
        print(f"Event '{summary}' already exists between {start_time} and {end_time}.")
        return None

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',  # Change as needed
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {created_event.get('htmlLink')}")
    return created_event

if __name__ == "__main__":
    start = get_datetime_with_tz(2025, 8, 24, 10, 0)
    end = get_datetime_with_tz(2025, 8, 24, 11, 0)
    add_calendar_event(
        summary="Team Meeting",
        start_time=start,
        end_time=end,
        description="Discuss project updates",
        location="Google Meet"
    )
