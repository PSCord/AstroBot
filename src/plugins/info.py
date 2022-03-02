from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING

import discord
from dateutil.relativedelta import relativedelta
from discord.ext import commands

from .. import Embed


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)


class Info(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    emoji = {
        'staff': '<:staff:904388765156519967>',
        'partner': '<:partner:828359004236808204>',
        'hypesquad': '<:hypesquad:828359003955527740>',
        'bug_hunter': '<:bughunter:828359003193081867>',
        'hypesquad_bravery': '<:bravery:828359003447754762>',
        'hypesquad_brilliance': '<:brilliance:828359003281031189>',
        'hypesquad_balance': '<:balance:828359003439497227>',
        'early_supporter': '<:early:828359003775303701>',
        'bug_hunter_level_2': '<:bughunterl2:904389183311843358>',
        'verified_bot_developer': '<:dev:828359003398340628>',
        'discord_certified_moderator': '<:dcmbadge:904389152966070294>',
    }

    @commands.command(
        brief='A bunch of stats about yourself or another.',
        help='Your join position, badges, ID, time since join, and time since account creation.',
    )
    async def info(self, ctx: commands.Context, user: discord.Member = None):
        if not user:
            user = ctx.author
        pos = sum(m.joined_at < user.joined_at for m in ctx.guild.members) + 1
        desc = ''
        for flag in iter(user.public_flags):
            if flag[1]:
                desc += f'{self.emoji[flag[0]]} '
        desc += f'\n\nID `{user.id}`'
        delta = relativedelta(datetime.datetime.now(datetime.timezone.utc), user.joined_at)
        if delta.years == 0:
            desc += f'\nJoined **{delta.months}** months ago.'
        else:
            desc += f'\nJoined **{delta.years}** years and **{delta.months}** months ago.'
        delta = relativedelta(datetime.datetime.now(datetime.timezone.utc), user.created_at)
        if delta.years == 0:
            desc += f'\nCreated **{delta.months}** months ago.'
        else:
            desc += f'\nCreated **{delta.years}** years and **{delta.months}** months ago.'

        infoembed = Embed(title=f'{user.name} (Member {pos})', description=desc).set_thumbnail(
            url=str(user.avatar.url)
        )
        await ctx.send(embed=infoembed)


def setup(bot: AstroBot):
    bot.add_cog(Info(bot))
