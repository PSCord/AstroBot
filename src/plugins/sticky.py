from __future__ import annotations

import logging
import time
import asyncpg
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, List, cast, Union
from collections import defaultdict
from dataclasses import dataclass

import asyncio
from asyncio import Task

from discord import Message, utils, NotFound, Forbidden, app_commands, Interaction, TextChannel, Thread
from discord.ext import commands
from discord.ext.commands import Context

if TYPE_CHECKING:
    from .. import AstroBot

log = logging.getLogger(__name__)


@dataclass
class StickyMessage:
    """Config for a Sticky Message"""

    id: int
    channel: int
    title: str
    enabled: bool
    msg: str
    trigger_msgs: int
    trigger_minutes: int
    trigger_pending: bool = False
    last_msg_id: int | None = None
    cur_task: Task | None = None
    msg_count: int = 0
    last_trigger_unix: int = 0

    @staticmethod
    def from_db(entry):
        return StickyMessage(
            entry['id'],
            entry['channel'],
            entry['title'],
            entry['enabled'],
            entry['msg'],
            entry['trigger_msgs'],
            entry['trigger_minutes'],
        )

@app_commands.guild_only()
@app_commands.default_permissions(manage_channels=True)
class Sticky(commands.GroupCog, group_name='sticky'):
    def __init__(self, bot: AstroBot):
        self.bot = bot
        # channel id -> sticky
        self.stickies_c: dict[int, List[StickyMessage]] = defaultdict(list)
        # sticky id -> sticky
        self.stickies: dict[int, StickyMessage] = dict()

    async def cog_load(self) -> None:
        records = await self.bot.db.fetch('SELECT * FROM sticky')
        for r in records:
            s = StickyMessage.from_db(r)
            self.stickies[s.id] = s
            if not s.enabled:
                continue

            self.stickies_c[s.channel].append(s)
            s.cur_task = asyncio.create_task(self.resend_sticky(s))

    async def cog_unload(self) -> None:
        for s in self.stickies.values():
            cur_task = s.cur_task
            if cur_task is not None:
                cur_task.cancel()

    async def enable_sticky(self, sticky: StickyMessage):
        if sticky.enabled:
            return
        sticky.enabled = True

        cur_stickies = self.stickies_c[sticky.channel]
        for s in cur_stickies:
            if s.id == sticky.id:
                return

        sticky.last_msg_id = None
        sticky.last_trigger_unix = 0
        sticky.msg_count = 0

        cur_stickies.append(sticky)
        sticky.cur_task = asyncio.create_task(self.resend_sticky(sticky))

        async with self.bot.db.acquire() as conn:
            await conn.execute('UPDATE sticky SET enabled = TRUE where ID = $1', sticky.id)

    async def disable_sticky(self, sticky: StickyMessage):
        if not sticky.enabled:
            return
        sticky.enabled = False

        cur_stickies = self.stickies_c[sticky.channel]
        for s in cur_stickies:
            if s.id == sticky.id:
                cur_stickies.remove(s)
                break

        cur_task = sticky.cur_task
        if cur_task is not None:
            cur_task.cancel()

        async with self.bot.db.acquire() as conn:
            await conn.execute('UPDATE sticky SET enabled = FALSE where ID = $1', sticky.id)

    @commands.Cog.listener()
    async def on_message(self, msg: Message):
        stickies = self.stickies_c.get(msg.channel.id, [])
        for s in stickies:
            s.msg_count += 1
            msg_trigger = s.msg_count >= s.trigger_msgs

            if not msg_trigger or s.trigger_pending:
                continue

            await self.resend_sticky(s)

    async def sticky_timer(self, sticky: StickyMessage):
        diff = (round(time.time()) - sticky.last_trigger_unix) / 60
        while diff < sticky.trigger_minutes:
            diff = (round(time.time()) - sticky.last_trigger_unix) / 60
            later = datetime.now() + timedelta(minutes=sticky.trigger_minutes - diff)
            await utils.sleep_until(later)

        await self.resend_sticky(sticky)

    async def resend_sticky(self, sticky: StickyMessage):
        if sticky.trigger_pending or not sticky.enabled:
            return

        try:
            sticky.trigger_pending = True

            channel = self.bot.get_partial_messageable(sticky.channel)
            if sticky.last_msg_id is not None:
                old = channel.get_partial_message(sticky.last_msg_id)
                try:
                    await old.delete()
                except (NotFound, Forbidden):
                    log.warning("old message %s for sticky %s was manually deleted (or no perms!)", old.id, sticky.id)
            new = await channel.send(sticky.msg)

            sticky.last_trigger_unix = round(time.time())
            sticky.last_msg_id = new.id
            sticky.msg_count = 0

            old_task = sticky.cur_task
            cur_task = asyncio.current_task()
            if old_task is not None and old_task != cur_task and not old_task.cancelling():
                old_task.cancel()
            sticky.cur_task = asyncio.create_task(self.sticky_timer(sticky))
        finally:
            sticky.trigger_pending = False

    @commands.group(brief="Sticky message commands; *help sticky for more.", invoke_without_command=True)
    async def sticky(self, ctx: Context):
        await ctx.channel.send("You forgot a subcommand, silly")

    @sticky.command(brief="Enable a sticky message by it's ID")
    @commands.has_permissions(manage_channels=True)
    async def enable(self, ctx: Context, id: int):
        sticky = self.stickies.get(id)
        if sticky is None:
            await ctx.channel.send("No sticky exists with this ID.")
            return
        if sticky.enabled:
            await ctx.channel.send("This sticky is already enabled.")
            return

        await self.enable_sticky(sticky)
        await ctx.channel.send(f'Enabled sticky #{sticky.id}.')

    @sticky.command(brief="Disable a sticky message by it's ID")
    @commands.has_permissions(manage_channels=True)
    async def disable(self, ctx: Context, id: int):
        sticky = self.stickies.get(id)
        if sticky is None:
            await ctx.channel.send("No sticky exists with this ID.")
            return
        if not sticky.enabled:
            await ctx.channel.send("This sticky is already disabled.")
            return

        await self.disable_sticky(sticky)
        await ctx.channel.send(f'Disabled sticky #{sticky.id}.')

    @sticky.command(brief="List all sticky messages and their names")
    @commands.has_permissions(manage_channels=True)
    async def list(self, ctx: Context):
        if len(self.stickies) == 0:
            await ctx.send("How about creating some sticky messages first?")
            return

        res = ""  # "#id. Name - #channel - message/time triggers"
        for s in self.stickies.values():
            res += f'\n#{s.id}. {s.title} - <#{s.channel}> - **{s.trigger_msgs}** messages or **{s.trigger_minutes} minutes**'
        await ctx.send(res)

    @sticky.command(brief="See the full content for a sticky message")
    @commands.has_permissions(manage_channels=True)
    async def expand(self, ctx: Context, id: int):
        sticky = self.stickies.get(id)
        if sticky is None:
            await ctx.send("There is no sticky with this ID.")
            return

        await ctx.send(sticky.msg)

    @sticky.command(brief="Delete a sticky message.")
    @commands.has_permissions(manage_channels=True)
    async def delete(self, ctx: Context, id: int):
        sticky = self.stickies.get(id)
        if sticky is None:
            await ctx.send("There is no sticky with this ID.")
            return

        await self.disable_sticky(sticky)
        del self.stickies[id]

        async with self.bot.db.acquire() as conn:
            conn = cast(asyncpg.Connection, conn)
            await conn.execute('DELETE FROM sticky WHERE id = $1', id)

        await ctx.send(f"Sticky #{id} deleted.")

    @sticky.command(brief="Please use the slash command /sticky edit.", name='edit')
    @commands.has_permissions(manage_channels=True)
    async def _edit(self, ctx: Context):
        await ctx.send("Please use the slash command `/sticky edit`.")

    @app_commands.command(description="Edit a sticky message")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def edit(
        self,
        interaction: Interaction,
        id: int,
        message: str | None,
        name: str | None,
        channel: Union[TextChannel, Thread] | None,
        trigger_msgs: int | None,
        trigger_minutes: int | None,
    ):
        if message is None and name is None and channel is None and trigger_msgs is None and trigger_minutes is None:
            await interaction.response.send_message("What are you doing Fish...")
            return

        sticky = self.stickies.get(id)
        if sticky is None:
            await interaction.response.send_message("There is no sticky with this ID.")
            return

        await interaction.response.defer(ephemeral=False, thinking=True)
        async with self.bot.db.acquire() as conn:
            conn = cast(asyncpg.Connection, conn)
            await conn.execute(
                '''
              UPDATE sticky
              SET
              channel = $1, title = $2, msg = $3, trigger_msgs = $4, trigger_minutes = $5
              WHERE id = $6
            ''',
                channel.id if channel is not None else sticky.channel,
                name or sticky.title,
                message.replace('\\n', '\n') if message is not None else sticky.msg,
                trigger_msgs or sticky.trigger_msgs,
                trigger_minutes or sticky.trigger_minutes,
                id,
            )
        sticky.channel = channel.id if channel is not None else sticky.channel
        sticky.title = name or sticky.title
        sticky.msg = message.replace('\\n', '\n') if message is not None else sticky.msg
        sticky.trigger_msgs = trigger_msgs or sticky.trigger_msgs
        sticky.trigger_minutes = trigger_minutes or sticky.trigger_minutes

        await interaction.followup.send(f'Updated sticky #{id}. This will take effect immediately :>')
        if sticky.enabled:
            await self.disable_sticky(sticky)
            await self.enable_sticky(sticky)

    @sticky.command(brief="Please use the slash command /sticky new.", name='new')
    @commands.has_permissions(manage_channels=True)
    async def _new(self, ctx: Context):
        await ctx.send("Please use the slash command `/sticky new`.")

    @app_commands.command(description="Create a new sticky message")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def new(
        self,
        interaction: Interaction,
        name: str,
        channel: Union[TextChannel, Thread],
        trigger_msgs: int,
        trigger_minutes: int,
        message: str,
    ):
        await interaction.response.defer(ephemeral=False, thinking=True)
        content = message.replace('\\n', '\n')

        sticky: StickyMessage
        async with self.bot.db.acquire() as conn:
            conn = cast(asyncpg.Connection, conn)
            record = await conn.fetchrow(
                '''
              INSERT INTO sticky 
              (channel, title, enabled, msg, trigger_msgs, trigger_minutes)
              VALUES ($1, $2, FALSE, $3, $4, $5)
              RETURNING *
            ''',
                channel.id,
                name,
                content,
                trigger_msgs,
                trigger_minutes,
            )
            sticky = StickyMessage.from_db(record)

        self.stickies[sticky.id] = sticky
        await self.enable_sticky(sticky)
        await interaction.followup.send(
            f'Created sticky message with ID #{sticky.id} for <#{sticky.channel}> with the following content:\n{content}'
        )


async def setup(bot: AstroBot) -> None:
    await bot.add_cog(Sticky(bot))
