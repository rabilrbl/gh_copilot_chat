import aiohttp
import os
from dotenv import load_dotenv
from gh_copilot_chat import constants

load_dotenv()


class Copilot:
    def __init__(self, token=os.environ.get("GH_TOKEN")):
        if not token:
            raise ValueError("GH_TOKEN environment variable is not set")
        self.token = token
        self.session = None
        self.headers = constants.HEADERS
        self.headers.update({"Authorization": f"Bearer {self.token}"})

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def new_chat(self) -> str:
        data = {}
        print(self.headers)
        async with self.session.post(
            constants.GH_COPILOT_THREADS,
            headers=self.headers,
            json=data,
        ) as response:
            json_data = await response.json()
            return json_data["thread_id"]

    async def ask_stream(self, thread_id, content):
        data = {
            "content": content,
            "intent": "conversation",
            "references": [],
            "streaming": True,
        }
        async with self.session.post(
            f"{constants.GH_COPILOT_THREADS}/{thread_id}/messages",
            headers=self.headers,
            json=data,
        ) as response:
            async for line in response.content:
                yield line.decode("utf-8")

    async def generate_title(self, thread_id):
        data = {"name": "", "generate": True}
        async with self.session.patch(
            f"{constants.GH_COPILOT_THREADS}/{thread_id}/name",
            headers=self.headers,
            json=data,
        ) as response:
            return await response.json()

    async def get_all_threads(self):
        async with self.session.get(
            constants.GH_COPILOT_THREADS,
            headers=self.headers,
        ) as response:
            return await response.json()
