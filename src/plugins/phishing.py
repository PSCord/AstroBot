from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import TYPE_CHECKING, AsyncGenerator, NamedTuple, Set

import aiohttp
import discord
from discord.ext import commands


if TYPE_CHECKING:
    from ..bot import AstroBot


log = logging.getLogger(__name__)


class YachtError(Exception):
    ...


class FeedResult(NamedTuple):
    domain: str
    addition: bool


class Phishing(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

        self.domains: Set[str] = set()
        self.updater: asyncio.Task = asyncio.create_task(self.fetch_domains())

    def cog_unload(self) -> None:
        self.updater.cancel()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.handle_message(message)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent) -> None:
        content = payload.data.get('content')

        if content is None:
            return

        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)  # type: ignore
        try:
            message = payload.cached_message or await channel.fetch_message(payload.message_id)
        except discord.HTTPException:
            return

        await self.handle_message(message)

    async def handle_message(self, message: discord.Message) -> None:
        if not isinstance(message.author, discord.Member):
            return

        if message.author.bot or message.author.guild_permissions.administrator:
            return

        is_phish = False

        for domain in re.findall(r'https?://([^\s/]{3,})', message.content, re.I):
            # Add leading full stop to not match longer domains:
            # `discord.com` matching on eg. `bobs-cool-discord.com`
            identifier = '.' + domain

            for known_domain in self.domains:
                # Use .endswith to ensure subdomains are handled
                # And the full TLD is taken into account as well
                # `discord.co` does not end with `discord.com`
                # `discord.com` does not end with `discord.co`
                # However
                # `printer.discord.com` ends with `discord.com`!
                if identifier.endswith('.' + known_domain):
                    is_phish = True

        if is_phish:
            await message.author.ban(reason='Posted a phishing link', delete_message_days=1)

    async def fetch_domains(self) -> None:
        while not self.bot.is_closed():
            try:
                self.domains = await self._fetch_all_domains()
            except YachtError:
                await asyncio.sleep(60)
                continue

            try:
                async for result in self._listen_for_domains():
                    if result.addition:
                        self.domains.add(result.domain)
                    else:
                        self.domains.discard(result.domain)
            except YachtError:
                pass

    async def _fetch_all_domains(self) -> Set[str]:
        session: aiohttp.ClientSession = self.bot.session  # type: ignore

        headers = {
            'X-Identity': session.headers['User-Agent'],
        }

        async with session.get('https://phish.sinking.yachts/v2/all', headers=headers) as resp:
            if not resp.ok:
                raise YachtError

            data = await resp.json()

        return set(data)

    async def _listen_for_domains(self) -> AsyncGenerator[FeedResult, None]:
        session: aiohttp.ClientSession = self.bot.session  # type: ignore

        headers = {
            'X-Identity': session.headers['User-Agent'],
        }

        async with session.ws_connect('wss://phish.sinking.yachts/feed', headers=headers) as ws:
            while not ws.closed:
                message = await ws.receive()
                log.debug(f'Received {message!r}.')

                if message.type in (aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType.BINARY):
                    data = json.loads(message.data)

                    for domain in data['domains']:
                        yield FeedResult(domain, addition=data['type'] == 'add')
                elif message.type is aiohttp.WSMsgType.ERROR:
                    log.exception(f'Feed returned an error: {message!r}.')
                #  elif message.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSED):

        raise YachtError


async def setup(bot: AstroBot) -> None:
    await bot.add_cog(Phishing(bot))
