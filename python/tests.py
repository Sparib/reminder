from typing import Dict

import dotenv
import aiohttp, asyncio, json as jsons, requests
from datetime import datetime
from utils import setup_configs
from dotenv import dotenv_values
from functools import wraps
from colorama import init, Fore, Style

from asyncio.proactor_events import _ProactorBasePipeTransport
    

if __name__ == "__main__":
    print(datetime.now().weekday())
    exit(0)

# def silence_event_loop_closed(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         try:
#             return func(self, *args, **kwargs)
#         except RuntimeError as e:
#             if str(e) != 'Event loop is closed':
#                 raise
#     return wrapper

# _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)

# config = dotenv_values()
# trello: Dict[str, str | None] = {}

# key = config["TRELLO_KEY"]
# token = config["TRELLO_TOKEN"]

# headers = {
#    "Accept": "application/json"
# }

# url = f"https://api.trello.com/1/boards/6028350b5f8b510ca5d62651/lists?key={key}&token={token}"
# list_url = f"https://api.trello.com/1/lists/{{}}/cards?key={key}&token={token}"

# async def main():
#     async with aiohttp.ClientSession(headers=headers) as session:
#         list_id = None
#         async with session.get(trello["BOARD_URL"]) as resp:
#             if resp.status != 200: return
#             lists = await resp.json()
#             # print(json)
#             for list in lists:
#                 if str(list["name"]).lower() == "do it now":
#                     list_id = list["id"]
#                     break
#             # print(list_id)
#         # json = None
#         # print(list_url.format(list_id))
#         async with session.get(trello["LIST_URL"].format(list_id)) as resp:
#             # print(resp.status)
#             if resp.status != 200: return
#             cards = await resp.json()
#             # print(jsons.dumps(cards, indent=2))
#             for card in cards:
#                 print(card["name"])

# def env_test():
#     config = dotenv_values()
#     new_config = config.copy()
#     for key in config:
#         if not key.startswith("TRELLO_"): continue
#         print(f"{key}: {config[key]}")
#         trello[key.replace("TRELLO_", "")] = config[key]
#         new_config.pop(key)
#     config = new_config
#     for key in config: print(f"{key}: {config[key]}")
#     for key in trello: print(f"{key}: {trello[key]}")
