import json

from app.services.tools.tool_registry import TOOLS


class ToolExecutor:

    async def execute(
        self,
        response: str,
    ):

        try:

            data = json.loads(response)

        except Exception:

            return None

        tool = data.get("tool")

        if tool not in TOOLS:

            return None

        return await TOOLS[tool](

            customer_name=data["customer_name"],

            date=data["date"],

            time=data["time"],

        )


tool_executor = ToolExecutor()