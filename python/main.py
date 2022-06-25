from io import StringIO
from typing import Dict
import discord
import logging
import asyncio
import sys
import datetime
import schedule
import aiohttp
import pytz
import os
from dotenv import dotenv_values
from utils import ColorFormatter, setup_configs
from datetime import datetime
from colorama import init

init()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
console = logging.StreamHandler(sys.stdout)
console.setFormatter(ColorFormatter('%(asctime)s | %(levelname)s | %(name)s : %(message)s'))
console.setLevel(logging.DEBUG)
logger.addHandler(console)

if 'ENV_FILE' in os.environ:
    config, trello = setup_configs(dotenv_values(stream=StringIO(os.environ['ENV_FILE'])))
else:
    config, trello = setup_configs(dotenv_values())


class BotClient(discord.Client):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.seen_today = False
        self.member: discord.Member = None

    async def on_ready(self):
        await self.wait_until_ready()
        logger.info("Successfully logged in to " + self.user.name)
        self.member = self.get_guild(int(config["GUILD_ID"])).get_member(int(config["USER_ID"]))
        
        if self.member is None or self.member is None: raise Exception("ID for Sparib no worko")
        logger.info("Cached user 362355607367581716: " + self.member.name)

        if self.member.dm_channel is None: await self.member.create_dm()
        logger.info(self.member.dm_channel)
        
        await self.schedules()

    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:        
        if after.id != self.member.id or self.seen_today or int(datetime.now().hour) < 14 or str(after.status).lower() != "online": return

        await self.member.send("Check due")
        self.seen_today = True

    async def get_cards(self) -> Dict[str, str]:
        dict: Dict = {}
        async with aiohttp.ClientSession(headers={"Accept": "application/json"}) as session:
            list_id = None
            async with session.get(trello["BOARD_URL"]) as resp:
                if resp.status != 200: return
                lists = await resp.json()
                for list in lists:
                    if str(list["name"]).lower() == str(trello["LIST"]).lower():
                        list_id = list["id"]
                        break
            if list_id is None: self.send_error("No list ID returned for given list name"); return
            async with session.get(trello["LIST_URL"].format(str(list_id))) as resp:
                if resp.status != 200: return
                cards = await resp.json()
                
                for card in cards:
                    logger.debug(card["name"])
                    # Get a datetime object by parsing the date string, then give it tzinfo of utc, then we can get the timestamp
                    date = datetime.strptime(card["due"], "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc)
                    logger.debug(int(date.timestamp()))
                    
                    if len(card["labels"]) == 0:
                        dict[card["name"]] = f"Due <t:{int(date.timestamp())}:t>"
                    else:
                        dict[f"{card['name']} | In {card['labels'][0]['name']}"] = f"Due <t:{int(date.timestamp())}:t>"                        
        return dict

    async def send_embed(self) -> None:
        embed = discord.Embed(
            title="Due Today",
            color=0xff8000
        )
        cards = (await self.get_cards())
        for name in cards: embed.add_field(name=name, value=cards[name], inline=False)
        await self.member.send(embed=embed)
        logger.info("Send")

    async def send_error(self, message) -> None:
        embed = discord.Embed(
            title="Error",
            color=0xff0000,
            description=message
        )
        await self.member.send(embed=embed)
        logger.error(message)

    async def schedules(self) -> None:
        reset_done = False
        send_done = False
        while True:
            time = datetime.now()
            
            if time.hour == 0 and not reset_done: self.reset_day(); reset_done = True
            elif time.hour == 14 and not send_done: await self.send_embed(); send_done = True
            
            if time.hour != 0: reset_done = False
            if time.hour != 14: send_done = False

            await asyncio.sleep(60)

    def reset_day(self) -> None: self.seen_today_desktop = False; self.seen_today_mobile = False; logger.info("Reset")

def main():
    intents = discord.Intents.default(); intents.typing = False; intents.presences = True; intents.members = True
    client = BotClient(intents=intents)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.start(config["TOKEN"]))C
    except KeyboardInterrupt:
        loop.run_until_complete(client.close())
        # pass
    finally:
        loop.close()
        logging.info("CLOSING")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
