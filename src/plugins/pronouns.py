from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from discord.ext import commands
from discord.utils import get
from discord import InteractionType

from .. import Embed


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)


class Pronouns(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    roles = {
        'She/Her': 927717427402379304,
        'He/Him': 927717432691408977,
        'They/Them': 927717436806021210,
        'Ask for Pronoun': 927717447442771969,
        'Any Pronoun': 927717450856943636,
    }

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.type == InteractionType.application_command and interaction.data['name'] == 'pronouns':
            data = interaction.data['options'][0]
            if data['name'] == 'add':
                role = get(interaction.guild.roles, id=self.roles[data['options'][0]['value']])
                await interaction.user.add_roles(role, reason='Request via slash command.')
                content = f"You've been given the {data['options'][0]['value']} pronoun role."
            elif data['name'] == 'remove':
                role = get(interaction.guild.roles, id=self.roles[data['options'][0]['value']])
                await interaction.user.remove_roles(role, reason='Request via slash command.')
                content = f"Your {data['options'][0]['value']} pronoun role has been removed."

            content += "\nAs a reminder, please message Modmail should you experience or observe any harassment."
            await interaction.response.send_message(content=content, ephemeral=True)


def setup(bot: AstroBot):
    bot.add_cog(Pronouns(bot))
