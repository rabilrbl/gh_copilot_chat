from gh_copilot_chat import Copilot
import asyncio
import json


async def run():
    async with Copilot() as cp:
        thread_id = await cp.new_chat()
        print("-----")
        while True:
            question = input("You: ")
            if question == "exit":
                break
            print("Copilot: ", end="")
            async for line in cp.ask_stream(thread_id, question):
                response = line.replace("data: ", "")
                try:
                    response = json.loads(response)
                except json.decoder.JSONDecodeError:
                    continue
                if response["type"] == "content":
                    print(response["body"], end="")
                elif response["type"] == "complete":
                    print()
                    break
            print("-----")
        await cp.generate_title(thread_id)
    return True


asyncio.run(run())
