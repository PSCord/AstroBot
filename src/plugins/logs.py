from __future__ import annotations

import logging
import time
import datetime
from typing import TYPE_CHECKING

from discord.ext import commands

from .. import Embed


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)

class Logs(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    async def backup_log(self, message):
        time = datetime.datetime.utcnow().replace(microsecond=0)
        log_channel = self.bot.get_channel(927721022722031637)
        await log_channel.send(content=message.replace('[d]', time.strftime("%m/%d/%Y, %H:%M:%S")))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild.id == 860585050838663188:
            await self.backup_log(f"🗑 **{message.author}** ({message.author.id} / {message.author.mention}) deleted their message ({message.id}) at **[d]** in {message.channel.mention}> (**{message.channel.name}**, {message.channel.id}) ```{message.content}```")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.guild.id == 860585050838663188 and before.content != after.content:
            await self.backup_log(f"✏ **{before.author}** ({before.author.id} / {before.author.mention}) edited their message ({before.id}) at **[d]** in {before.channel.mention} (**{before.channel.name}**, {before.channel.id}) ```{before.content}``` to ```{after.content}```")

def setup(bot: AstroBot):
    bot.add_cog(Logs(bot))
