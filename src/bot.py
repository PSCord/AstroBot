import asyncio
import logging
import os
from typing import Optional

import asyncpg
import discord
from discord.ext import commands


log = logging.getLogger(__name__)


EXTENSIONS = {
    'jishaku',
    'src.plugins.autochannels',
    'src.plugins.errors',
    'src.plugins.welcome',
    'src.plugins.levels',
}


class AstroBot(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions.none()

        intents = discord.Intents(
            guilds=True,
            members=True,
            guild_messages=True,
        )

        super().__init__(
            allowed_mentions=allowed_mentions,
            case_insensitive=True,
            command_prefix='!',
            intents=intents,
            max_messages=None,
        )

        self.db: Optional[asyncpg.Pool] = None

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

        for name in EXTENSIONS:
            self.load_extension(name)

        await super().start(*args, **kwargs)
