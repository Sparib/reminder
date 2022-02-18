import time
from typing import Dict
import discord
import logging
import asyncio
import sys
import colorama
import datetime
import schedule
import aiohttp
import json
import pytz
from dotenv import dotenv_values
from utils import ColorFormatter, setup_configs
from datetime import datetime, tzinfo
from os import environ
from colorama import init, Fore

init()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
# file = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# file.setFormatter(logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)-16s : %(message)s'))
# logger.addHandler(file)
console = logging.StreamHandler(sys.stdout)
console.setFormatter(ColorFormatter('%(asctime)s | %(levelname)s | %(name)s : %(message)s'))
console.setLevel(logging.DEBUG)
logger.addHandler(console)

config, trello = setup_configs(dotenv_values())


class BotClient(discord.Client):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.seen_today_desktop = False
        self.seen_today_mobile = False
        self.send_now = True
        self.member: discord.Member = None

    async def on_ready(self):
        await self.wait_until_ready()
        logger.info("Successfully logged in to " + self.user.name)
        self.member = self.get_guild(config["GUILD_ID"]).get_member(config["USER_ID"])
        if self.member is None or self.member is None: raise Exception("ID for Sparib no worko")
        logger.info("Cached user 362355607367581716: " + self.member.name)
        # await self.get_cards()
        # await self.close()
        if self.member.dm_channel is None: await self.member.create_dm()
        logger.info(self.member.dm_channel)
        # async for message in self.get_user(362355607367581716).dm_channel.history(): await message.delete(); await asyncio.sleep(1)
        await self.schedules()

    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        logger.info(f"{after.display_name} updated | Old Status: {before.status} | New Status: {after.status}")
        logger.info(after.id)
        if after.id != self.member.id: return
        if self.seen_today_desktop and self.seen_today_mobile: return
        if int(datetime.now().hour) < 14: return
        if str(after.status).lower() != "online": return
        logger.info(f"{after.mobile_status} {after.desktop_status}")
        if not self.seen_today_mobile and after.is_on_mobile():
            # Mobile stuff
            await self.send_embed()
        elif not self.seen_today_desktop and str(after.desktop_status).lower() == "online":
            if not self.seen_today_mobile: await self.send_embed()
            else: await self.member.send("Check due")
            self.seen_today_desktop = True

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
            if list_id is None: return # TODO: Handle this
            async with session.get(trello["LIST_URL"].format(str(list_id))) as resp:
                if resp.status != 200: return
                cards = await resp.json()
                # logger.info("\n" + json.dumps(cards[0], indent=2))
                for card in cards:
                    logger.debug(card["name"])
                    # Get a datetime object by parsing the date string, then give it tzinfo of utc, then we can get the timestamp
                    date = datetime.strptime(card["due"], "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc)
                    logger.debug(int(date.timestamp()))
                    # f"<t:{int(date.timestamp())}:f>"
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
        self.seen_today_mobile = True
        self.send_now = False
        logger.info("Send")

    async def schedules(self) -> None:
        schedule.every().day.do(self.reset_day)
        schedule.every().day.at("14:00").do(self.was_online)
        # schedule.every(10).seconds.do(self.was_online)
        while True:
            schedule.run_pending()
            if self.send_now: (await self.send_embed())
            await asyncio.sleep(1)

    def reset_day(self) -> None: self.seen_today_desktop = False; self.seen_today_mobile = False; logger.info("Reset")
    def was_online(self) -> None:
        # logger.info(self.sparib)
        if str(self.member.status).lower() == "online":
            self.send_now = True
            if str(self.member.desktop_status).lower() == "online": self.seen_today_desktop = True

def main():
    intents = discord.Intents.default(); intents.typing = False; intents.presences = True; intents.members = True
    client = BotClient(intents=intents)
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(client.get_cards())
    # return
    try:
        loop.run_until_complete(client.start(config["TOKEN"]))
        # loop.run_until_complete(client.schedules())
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
