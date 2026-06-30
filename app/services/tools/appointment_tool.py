from datetime import datetime

from app.core.logger import logger
from app.services.calendar.google_calendar_service import (
    google_calendar_service,
)


class AppointmentTool:

    async def book(
        self,
        customer_name: str,
        date: str,
        time: str,
    ):

        start = datetime.fromisoformat(
            f"{date}T{time}"
        )

        event = google_calendar_service.create_event(
            title=f"Appointment with {customer_name}",
            start=start,
        )

        logger.info(
            "appointment_booked",
            customer=customer_name,
            event_id=event["id"],
        )

        return {
                "success": True,
                "message": "Appointment booked successfully.",

                "customer_name": customer_name,

                "date": date,

                "time": time,

                "event_link": event["htmlLink"],
        }


appointment_tool = AppointmentTool()