from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from .. import Embed


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)

DEFAULT_INTERNAL_ERROR = 'Something unexpected went wrong during command execution. Please try again later.'


class Errors(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

        bot.on_error = self.on_error  # type: ignore

    def cog_unload(self):
        self.bot.on_error = commands.Bot.on_error  # type: ignore

    async def on_error(self, event: str, *args, **kwargs):
        log.exception(f'Unhandled exception in {event} handler.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        embed = None
        can_send = ctx.channel.permissions_for(ctx.me).send_messages

        if isinstance(error, commands.ConversionError):
            embed = Embed(title='Internal AstroBot Error', description=DEFAULT_INTERNAL_ERROR)
            log.exception(f'Unhandled exception in {error.converter} converter.', exc_info=error)
        elif isinstance(error, commands.CommandInvokeError):
            if not isinstance(error.original, discord.DiscordServerError):
                embed = Embed(title='Internal AstroBot Error', description=DEFAULT_INTERNAL_ERROR)

                command_name = ctx.command.qualified_name  # type: ignore
                log.exception(f'Unhandled exception in {command_name} command.', exc_info=error)
            else:
                embed = Embed(
                    title='Discord Server Error',
                    description='Discord is experiencing issues at this time. Please try again later.',
                )
        elif isinstance(error, (commands.UserInputError, commands.BadArgument)):
            embed = Embed(title='User Input Error', description=str(error))
        elif isinstance(error, commands.BotMissingPermissions):
            embed = Embed(title='Permissions Configuration Error', description=str(error))
        elif isinstance(error, commands.CommandOnCooldown):
            embed = Embed(title='Command on cooldown.', description=str(f'You are on cooldown. Try again in {int(error.retry_after)} seconds.'))

        if embed is not None and can_send:
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException:
                pass


def setup(bot: AstroBot):
    bot.add_cog(Errors(bot))
