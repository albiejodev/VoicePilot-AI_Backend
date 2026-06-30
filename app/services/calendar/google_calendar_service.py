from datetime import datetime, timedelta
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.core.logger import logger


SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


class GoogleCalendarService:

    def __init__(self):

        self.service = None


    def authenticate(self):

        creds = None

        if os.path.exists("token.json"):

            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES,
            )

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:

                creds.refresh(Request())

            else:

                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json",
                    SCOPES,
                )

                creds = flow.run_local_server(
                    port=0
                )

            with open(
                "token.json",
                "w",
            ) as token:

                token.write(
                    creds.to_json()
                )

        self.service = build(
            "calendar",
            "v3",
            credentials=creds,
        )

        logger.info(
            "google_calendar_authenticated"
        )


    def create_event(
        self,
        title: str,
        start: datetime,
        duration_minutes: int = 30,
    ):

        if self.service is None:

            self.authenticate()

        end = start + timedelta(
            minutes=duration_minutes
        )

        event = {

            "summary": title,

            "start": {

                "dateTime": start.isoformat(),

                "timeZone": "Asia/Kolkata",

            },

            "end": {

                "dateTime": end.isoformat(),

                "timeZone": "Asia/Kolkata",

            },

        }

        created = (
            self.service.events()
            .insert(
                calendarId="primary",
                body=event,
            )
            .execute()
        )

        logger.info(
            "calendar_event_created",
            event_id=created["id"],
        )

        return created


google_calendar_service = GoogleCalendarService()