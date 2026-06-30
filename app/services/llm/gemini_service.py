from google import genai
from app.prompts.receptionist import RECEPTIONIST_PROMPT
from app.core.config import settings


class GeminiService:

    def __init__(self):

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)



    async def generate_response(
        self,
        history: list,
    ) -> str:

        conversation = ""

        for msg in history:

            conversation += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

        prompt = f"""
        {RECEPTIONIST_PROMPT}

        Conversation:

        {conversation}

        Remember:

        If the user wants to book an appointment AND you know:

        - customer name
        - appointment date
        - appointment time

        then respond ONLY with valid JSON.

        Otherwise answer normally.

        Assistant:
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text



    async def summarize(
    self,
    history: list,
    ):

        conversation = "\n".join(
            [
                f"{m['role']}: {m['content']}"
                for m in history
            ]
        )

        prompt = f"""
    Summarize the following conversation.

    Keep:

    - customer name
    - important preferences
    - booking details
    - phone number
    - address
    - anything useful

    Conversation:

    {conversation}
    """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text



    async def generate_confirmation(
    self,
    tool_result: dict,
    ) -> str:

            prompt = f"""
        An appointment has already been booked successfully.

        Respond to the customer naturally in one short sentence.

        Do not mention any URL.

        Booking Result:
        {tool_result["message"]}
        """

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            return response.text