from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from discord import ButtonStyle, ChannelType, InteractionType
from discord.ext import commands
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

    @commands.command(brief="Make a trending thread", help="Queue a thread to be made at admin discretion.")
    @commands.has_permissions(ban_members=True)
    async def trending(self, ctx, *, args=None):
        if args is None:
            await ctx.send('Please include the game name.')
        else:
            admin = self.bot.get_channel(get_from_environment('ADMIN_CHANNEL', int))
            await admin.send(content=args, view=self.view_vote)
            await ctx.send('Sent to admins, awaiting approval.')

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.type == InteractionType.component:
            if interaction.data['custom_id'] == 'yes':
                trending = self.bot.get_channel(get_from_environment('TRENDING_CHANNEL', int))
                await trending.create_thread(
                    name=interaction.message.content,
                    type=ChannelType.public_thread,
                    reason='Trending thread made at mod/admin discretion',
                )
                await interaction.edit_original_message(
                    content=f'**Created** ~~{interaction.message.content}~~', view=self.view_done
                )
            elif interaction.data['custom_id'] == 'no':
                await interaction.edit_original_message(
                    content=f'**Veto\'d** ~~{interaction.message.content}~~', view=self.view_done
                )


def setup(bot: AstroBot):
    bot.add_cog(Mods(bot))
