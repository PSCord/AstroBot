from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from discord.ext import commands
import discord 

from .. import get_from_environment


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)


class Welcome(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    cooldown = 0

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild == get_from_environment('MAIN_GUILD', int):
            general = self.bot.get_channel(get_from_environment('WELCOME_CHANNEL', int))
            if (time.time() - self.cooldown) < 90:
                return
            else:
                await general.send(
                    content=f'Welcome to the **unofficial** PS Discord, {member.mention}! Check <#719536356727980032> to get started.',
                    delete_after=90,
                )
                self.cooldown = time.time()


def setup(bot: AstroBot):
    bot.add_cog(Welcome(bot))
