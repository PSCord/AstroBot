import asyncio
import logging
import os
from typing import Optional

import aiohttp
import asyncpg
import discord
from discord.ext import commands


log = logging.getLogger(__name__)


EXTENSIONS = {
    'jishaku',
    'src.plugins.autochannels',
    'src.plugins.boosters',
    'src.plugins.errors',
    'src.plugins.events',
    'src.plugins.info',
    'src.plugins.levels',
    'src.plugins.logs',
    'src.plugins.mods',
    'src.plugins.phishing',
    'src.plugins.pronouns',
    'src.plugins.welcome',
}


class AstroBot(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions.none()

        intents = discord.Intents(
            guilds=True,
            members=True,
            guild_messages=True,
            bans=True,
        )

        super().__init__(
            allowed_mentions=allowed_mentions,
            case_insensitive=True,
            command_prefix='!',
            intents=intents,
        )

        self.db: Optional[asyncpg.Pool] = None
        self.session: Optional[aiohttp.ClientSession] = None

    def run(self):
        super().run(os.environ['BOT_TOKEN'])

    async def start(self, *args, **kwargs):
        for attempt in range(5):
            try:
                self.db = await asyncpg.create_pool(os.environ['PSQL_DSN'])
            except ConnectionRefusedError as e:
                if attempt == 5:
                    raise e

                seconds = (attempt + 1) ** 2

                log.info(f'Failed to connected to database, retrying in {seconds} second(s).')
                await asyncio.sleep(seconds)
            else:
                break

        self.session = aiohttp.ClientSession(headers={'User-Agent': 'Astrobot/1.0 (+https://discord.gg/ps)'})

        for name in EXTENSIONS:
            self.load_extension(name)

        await super().start(*args, **kwargs)
