import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

Calendarid = "(enter your calendar id here)"
OriginalName = "(Original name of event you want to change)"
FinalName = "(Final name of the event)"
EventDateTime = '(Enter the datetime of the event you want to change)'


def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials2.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build('calendar', 'v3', credentials = creds)

        now = dt.datetime.now().isoformat() + 'Z'

        #timeMin = Minimum time you want to consider from. MaxResults = maximum number of results. orderBy = criteria to order by

        event_result = service.events().list(calendarId = Calendarid, timeMin = None, maxResults = None, singleEvents = True, orderBy = "startTime").execute()
        events = event_result.get('items', [])

        if not events:
            print('No upcoming events found!')
            return
        
        for event in events:
            if event['summary'] == OriginalName and event['start'].get('dateTime') == EventDateTime:
                event['summary'] = FinalName
                updatedevent = service.events().update(calendarId = Calendarid, eventId = event['id'], body = event).execute()

    except HttpError as error:
        print('An error occuredd', error)

if __name__ == "__main__":
    main()