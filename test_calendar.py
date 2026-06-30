import asyncio

from app.services.tools.appointment_tool import (
    appointment_tool,
)


async def main():

    result = await appointment_tool.book(
        customer_name="Albin",
        date="2026-07-01",
        time="16:00:00",
    )

    print(result)


asyncio.run(main())