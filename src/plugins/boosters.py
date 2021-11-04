from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

import feedparser
from discord.ext import commands
from discord.utils import get

from .. import Embed


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)


class Boosters(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot
        self.boost_log = bot.get_channel(876496435493888100)


    colour_names = ['forest', 'porpule', 'purple', 'skyblue', 'blue', 'mint', 'black', 'pink', 'ghost']
    colour_roles = [905129271662641193, 905129293460439061, 905129304759861248, 905129309100978196, 905129310485110807, 905129313169444945, 905129315551830017, 905129318043226223, 905129320081657936]

    thank_boost = (
        Embed(
            title='Thanks for boostnig the PlayStation Discord!',
            description='You\'ve unlocked the following perks for boosting:\n<:check:684852990980522060> **A special booster role, displayed separately on the member list**\n<:check:684852990980522060> **Ability to choose your color from a unique set of roles** (`*color` command)\n<:check:684852990980522060> **Image/file attachment and link embed access in all channels**\n<:check:684852990980522060> **Access to <#684069943196909583> - an exclusive chat channel**\n\nSee <#719536356727980032> to learn more about our leveling and boosting perks system. Note that those perks are not permanent, and you will lose access if you transfer or cancel your boost - unless you earn them via our leveling system otherwise.\n\n*This is an automated message. Replies will not be monitored - use modmail to contact the mods.*',
        )
        .set_thumbnail(url='https://cdn.discordapp.com/emojis/750404031381372968.png')
        .set_footer(text='PlayStation', icon_url='https://cdn.discordapp.com/emojis/721384207213002783.png')
    )

    colour_embed = (
        Embed(
            title='Colour Roles',
            description='Enter the name of the color you\'d like to pick, e.g. `blue`, or `clear` to remove it.',
        )
        .set_image(url='https://cdn.discordapp.com/attachments/827704409730973719/830249843565527080/colors.png')
    )

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.guild.id == 860585050838663188:
            if after.premium_since and not before.premium_since:
                await after.send(embed=self.thank_boost)
                await self.boost_log.send(f'{before.mention} started boosting.')
            elif before.premium_since and not after.premium_since:
                roles = tuple(get(before.guild.roles, id=x) for x in colour_roles)
                await before.remove_roles(*roles, reason='Stopped boosting.')
                await self.boost_log.send(f'{before.mention} stopped boosting.')

    @commands.command()
    async def colour(self, ctx: commands.Context, message: str = None):
        boost_role = get(ctx.guild.roles, id=905864474538438788)
        plat = get(ctx.guild.roles, id=904116235237752832)
        if boost_role in ctx.author.roles or plat in ctx.author.roles:
            if message:
                if message == 'clear':
                        roles = tuple(get(ctx.guild.roles, id=x) for x in self.colour_roles)
                        await ctx.author.remove_roles(*roles, reason='Requested to clear colours.')
                        await ctx.send('<:check:684852990980522060> Colors updated.')
                else:
                    try:
                        num = self.colour_names.index(message)
                        role = get(ctx.guild.roles, id=self.colour_roles[num])
                        roles = tuple(get(ctx.guild.roles, id=x) for x in self.colour_roles)
                        await ctx.author.remove_roles(*roles, reason='Changing colour.')
                        await ctx.author.add_roles(role, reason='Used the *role command')
                        await ctx.send('<:check:684852990980522060> Colors updated.')
                    except ValueError:
                        await ctx.send('Please pick a valid colour.')
            else:
                await ctx.send(embed=self.colour_embed)
        else:
            await ctx.send('<:question:747469232408625314> **You don\'t meet the requirements to use this command.**\nIn order to be able to choose your color, you must have **30,000** XP points or be a booster. See <#719536356727980032> for more information.')

    @commands.command()
    async def color(self, ctx: commands.Context, message: str = None):
        await ctx.send('go away mini')

def setup(bot: AstroBot):
    bot.add_cog(Boosters(bot))
