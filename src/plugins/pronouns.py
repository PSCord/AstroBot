from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from discord import InteractionType
from discord.ext import commands
from discord.utils import get

from .. import Embed, get_from_environment


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)


class Pronouns(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    roles = {
        'She/Her': get_from_environment('SHE_HER', int),
        'He/Him': get_from_environment('HE_HIM', int),
        'They/Them': get_from_environment('THEM_THEM', int),
        'Ask for Pronoun': get_from_environment('ASK', int),
        'Any Pronoun': get_from_environment('ANY', int),
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
