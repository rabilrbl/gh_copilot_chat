import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()


class Copilot:
    def __init__(self, token=os.environ.get("GH_TOKEN")):
        if not token:
            raise ValueError("GH_TOKEN environment variable is not set")
        self.token = token
        self.session = None
        self.headers = {
            "Accept": "application/vnd.github.merge-info-preview+json,application/vnd.github.shadow-cat-preview+json,application/vnd.github.echo-preview+json,application/vnd.github.vixen-preview+json,application/vnd.github.antiope-preview+json,application/vnd.github.comfort-fade-preview+json,application/vnd.github.starfox-preview+json,application/vnd.github.doctor-strange-preview+json,application/json",
            "Accept-Encoding": "gzip",
            "Authorization": f"Bearer {self.token}",
            "Connection": "Keep-Alive",
            "Content-Type": "application/json; charset=UTF-8",
            "Copilot-Integration-Id": "copilot-mobile-android",
            "GraphQL-Features": "merge_queue,project_next_field_configuration,issue_types,issues_close_state,project_next_recent_connection,file_level_commenting",
            "Host": "api.githubcopilot.com",
            "User-Agent": "GitHub/1.161.0 (com.github.android; build:786; Android 13; Pixel 5)",
            "X-GitHub-Api-Version": "2023-07-07",
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def new_chat(self) -> str:
        data = {}
        async with self.session.post(
            "https://api.githubcopilot.com/github/chat/threads",
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
            f"https://api.githubcopilot.com/github/chat/threads/{thread_id}/messages",
            headers=self.headers,
            json=data,
        ) as response:
            async for line in response.content:
                yield line.decode("utf-8")

    async def generate_title(self, thread_id):
        data = {"name": "", "generate": True}
        async with self.session.patch(
            f"https://api.githubcopilot.com/github/chat/threads/{thread_id}/name",
            headers=self.headers,
            json=data,
        ) as response:
            return await response.json()
        
    async def get_all_threads(self):
        async with self.session.get(
            "https://api.githubcopilot.com/github/chat/threads",
            headers=self.headers,
        ) as response:
            return await response.json()
