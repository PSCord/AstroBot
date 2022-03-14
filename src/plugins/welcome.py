from __future__ import annotations

import time
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from .. import get_from_environment


if TYPE_CHECKING:
    from .. import AstroBot


class Welcome(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot
        self.last_welcome = 0

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        guild_id = get_from_environment('MAIN_GUILD', int)
        channel_id = get_from_environment('WELCOME_CHANNEL', int)

        if member.guild.id != guild_id or channel_id is None:
            return

        now = time.perf_counter()
        channel: discord.TextChannel = self.bot.get_channel(channel_id)  # type: ignore

        if (now - self.last_welcome) < 90:
            return

        self.last_welcome = now

        content = (
            f'Welcome to the **unofficial** PS Discord, {member.mention}! '
            f'Check <#719536356727980032> to get started.'
        )

        try:
            await channel.send(content, allowed_mentions=discord.AllowedMentions(users=[member]), delete_after=90)
        except discord.HTTPException:
            pass


async def setup(bot: AstroBot) -> None:
    await bot.add_cog(Welcome(bot))
