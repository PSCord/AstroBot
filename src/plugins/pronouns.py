from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Literal

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
    'Any Pronouns': get_from_environment('ANY', int),
}

MAIN_GUILD = get_from_environment('MAIN_GUILD', int)


PRONOUNS = Literal['She/Her', 'He/Him', 'They/Them', 'Ask for Pronouns', 'Any Pronouns']
MODMAIL_REMINDER = 'As a reminder, please message Modmail should you experience or observe any harassment.'


class Pronouns(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    pronouns = discord.app_commands.Group(
        name='pronouns', description='Choose which pronoun roles you have in the server.'
    )

    @pronouns.command()
    async def add(self, interaction: discord.Interaction, pronoun: PRONOUNS) -> None:
        """The pronoun role you want to add."""

        if TYPE_CHECKING:
            assert isinstance(interaction.user, discord.Member)

        role_id: int = ROLES[pronoun]  # type: ignore

        await asyncio.gather(
            interaction.response.defer(ephemeral=True),
            interaction.user.add_roles(discord.Object(role_id), reason='Requested via /pronoun command'),
        )

        await interaction.followup.send(
            f'You\'ve been given the {pronoun} pronoun role.\n{MODMAIL_REMINDER}', ephemeral=True
        )

    @pronouns.command()
    async def remove(self, interaction: discord.Interaction, pronoun: PRONOUNS) -> None:
        """The pronoun role you want to remove."""

        if TYPE_CHECKING:
            assert isinstance(interaction.user, discord.Member)

        role_id: int = ROLES[pronoun]  # type: ignore

        await asyncio.gather(
            interaction.response.defer(ephemeral=True),
            interaction.user.remove_roles(discord.Object(role_id), reason='Requested via /pronoun command'),
        )

        await interaction.followup.send(
            f'Your {pronoun} pronoun role has been removed.\n{MODMAIL_REMINDER}', ephemeral=True
        )


async def setup(bot: AstroBot) -> None:
    if MAIN_GUILD is None:
        return

    await bot.add_cog(Pronouns(bot), guild=discord.Object(MAIN_GUILD))
