from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import discord
from discord.ext import commands


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)


class Test(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ...  # Received message

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def mod_only_command(self, ctx: commands.Context, message: str):
        """Echoes a message."""

        await ctx.send(message)


def setup(bot: AstroBot):
    bot.add_cog(Test(bot))
