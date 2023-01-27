from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from discord import ButtonStyle, ChannelType, InteractionType
from discord.ext import commands
from discord.member import Member
from discord.ui import Button, View

from .. import get_from_environment


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)


class Mods(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    yes = Button(
        style=ButtonStyle.primary, custom_id='yes', disabled=False, emoji='<:eggg:834519001140428860>', label='Yes'
    )
    no = Button(
        style=ButtonStyle.primary, custom_id='no', disabled=False, emoji='<:egggg:834519509778956308>', label='No'
    )
    view_vote = View()
    view_vote.add_item(yes)
    view_vote.add_item(no)

    yes_disabled = Button(
        style=ButtonStyle.primary, custom_id='yes', disabled=True, emoji='<:eggg:834519001140428860>', label='Yes'
    )
    no_disabled = Button(
        style=ButtonStyle.primary, custom_id='no', disabled=True, emoji='<:egggg:834519509778956308>', label='No'
    )
    view_done = View()
    view_done.add_item(yes_disabled)
    view_done.add_item(no_disabled)

    @commands.command(brief="Make a trending thread.", help="Queue a thread to be made at admin discretion. *trending Game - Desc")
    @commands.has_permissions(ban_members=True)
    async def trending(self, ctx, *, args=None):
        forum = args.split(' - ', 1)
        if args is None or len(forum) != 2:
            await ctx.send('Please include the game name, as well as a brief description in the format \'Game - Desc\'.')
        else:
            admin = self.bot.get_channel(get_from_environment('ADMIN_CHANNEL', int))
            await admin.send(content=args, view=self.view_vote)
            await ctx.send('Sent to admins, awaiting approval.')

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.type == InteractionType.component:
            if interaction.data['custom_id'] == 'yes':
                forum = interaction.message.content.split(' - ', 1)
                trending = self.bot.get_channel(get_from_environment('TRENDING_CHANNEL', int))
                game_thread = await trending.create_thread(
                    name=forum[0],
	    	        content=f'__**{forum[0]}**__\n{forum[1]}',
                    reason='Trending thread made at mod/admin discretion',
                )
                ping = await game_thread.thread.send(content=f'<@&683768439881334826>')
                await ping.delete()
                await interaction.response.defer()
                await interaction.message.edit(
                    content=f'**Created** ~~{interaction.message.content}~~', view=self.view_done
                )
            elif interaction.data['custom_id'] == 'no':
                await interaction.response.defer()
                await interaction.message.edit(
                    content=f'**Veto\'d** ~~{interaction.message.content}~~', view=self.view_done
                )

    @commands.command(brief="Assign the artisan role.")
    @commands.has_permissions(manage_emojis=True)
    async def artisan(self, ctx: commands.Context, member: Member):
        role = ctx.guild.get_role(get_from_environment('ARTISIAN_ROLE', int))
        if role in member.roles:
            await member.remove_roles(role, reason=f"Removed artisan role as per {ctx.author.name}")
            await ctx.send(f'Removed artisan role from {member.mention}.')
        else:
            await member.add_roles(role, reason=f"Granted artisan role as per {ctx.author.name}")
            await ctx.send(f'Given {member.mention} artisan role.')


    @commands.command(brief="Assign the event winner role.")
    @commands.has_role(1011206375369605190)
    async def winner(self, ctx: commands.Context, member: Member):
        role = ctx.guild.get_role(get_from_environment('EVENT_WINNER', int))
        if role in member.roles:
            await member.remove_roles(role, reason=f"Removed event winner role as per {ctx.author.name}")
            await ctx.send(f'Removed event winner from {member.mention}.')
        else:
            await member.add_roles(role, reason=f"Granted event winner as per {ctx.author.name}")
            await ctx.send(f'Given {member.mention} event winner.')

async def setup(bot: AstroBot) -> None:
    await bot.add_cog(Mods(bot))
