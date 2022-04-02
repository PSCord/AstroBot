from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from .. import get_from_environment


if TYPE_CHECKING:
    from .. import AstroBot


ROLES = {
    'She/Her': get_from_environment('SHE_HER', int),
    'He/Him': get_from_environment('HE_HIM', int),
    'They/Them': get_from_environment('THEY_THEM', int),
    'Ask for Pronoun': get_from_environment('ASK', int),
    'Any Pronoun': get_from_environment('ANY', int),
}


class Pronouns(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction) -> None:
        if interaction.type is not discord.InteractionType.application_command:
            return

        if interaction.data['name'] != 'pronouns':  # type: ignore - interaction.data typings are incorrect
            return

        guild = interaction.guild

        if guild is None:
            return
        else:
            assert isinstance(interaction.user, discord.Member)  # Pain

        data = interaction.data['options'][0]  # type: ignore - interaction.data typings are incorrect
        role = guild.get_role(ROLES[data['options'][0]['value']])  # type: ignore - interaction.data typings are incorrect

        if role is None:
            return

        if data['name'] == 'add':
            content = f'You\'ve been given the {role.name} pronoun role.'
            await interaction.user.add_roles(role, reason='Request via slash command.')
        elif data['name'] == 'remove':
            content = f'Your {role.name} pronoun role has been removed.'
            await interaction.user.remove_roles(role, reason='Request via slash command.')
        else:
            raise RuntimeError('Invalid pronoun slash command was used.')

        content += '\nAs a reminder, please message Modmail should you experience or observe any harassment.'
        await interaction.response.send_message(content, ephemeral=True)


async def setup(bot: AstroBot) -> None:
    await bot.add_cog(Pronouns(bot))
