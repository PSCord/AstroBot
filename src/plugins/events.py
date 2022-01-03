from __future__ import annotations

import logging
import os
import time
from typing import TYPE_CHECKING

import asyncpg
from discord.ext import commands, tasks
from discord.utils import get

from .. import Embed


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)


class Events(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot
        self.event_mode = False
        self.event_role = 0

    event_embed = (
        Embed(
            title='You earned an event role in the PlayStation Discord!',
            description='Event roles are exclusive trophy roles that you can earn during time-limited events. They\'ll permanently display on your profile within the server, for everyone to see. Collect \'em all!\n\n*This is an automated message. Replies will not be monitored - use modmail to contact the mods.*',
        )
        .set_thumbnail(url='https://cdn.discordapp.com/emojis/750404031381372968.png')
        .set_footer(
            text='PlayStation',
            icon_url='https://cdn.discordapp.com/emojis/684852991081447450.png',
        )
    )


    #async def cog_before_invoke(self, ctx):
    #    async with self.bot.db.acquire() as conn:
    #        record = await conn.fetch(
    #            '''
    #            SELECT eventmode FROM options WHERE beep = 'boop'
    #            '''
    #        )
    #        self.event_mode = [x['eventmode'] for x in record][0]
    #        record = await conn.fetch(
    #            '''
    #            SELECT eventroleid FROM options WHERE beep = 'boop'
    #            '''
    #        )
    #        self.event_role = [x['eventroleid'] for x in record][0]

    main_server = 860585050838663188
    event_cooldown = {}

    def cooldown(self, id):
        if id not in self.event_cooldown:
            return False
        return self.event_cooldown[id] + 15 > time.time()

    @commands.Cog.listener()
    async def on_message(self, message):
        async with self.bot.db.acquire() as conn:
            record = await conn.fetch(
                '''
                SELECT eventmode FROM options WHERE beep = 'boop'
                '''
            )
            self.event_mode = [x['eventmode'] for x in record][0]
            record = await conn.fetch(
                '''
                SELECT eventroleid FROM options WHERE beep = 'boop'
                '''
            )
            self.event_role = [x['eventroleid'] for x in record][0]
        if message.guild.id != self.main_server:
            return
        elif self.event_mode and message.content != '!eventmode conclude':
            if not self.cooldown(message.author.id) and not message.author.bot:
                async with self.bot.db.acquire() as conn:
                    record = await conn.fetch(
                        '''
                        SELECT event FROM levels WHERE id = $1
                        ''',
                        message.author.id,
                    )
                    if record:
                        count = [x['event'] for x in record][0]
                    else: count = None
                if record and count < 15:
                    async with self.bot.db.acquire() as conn:
                        await conn.execute(
                            '''
                            UPDATE levels
                                SET event = event + 1
                            WHERE id = $1
                            ''',
                            message.author.id,
                        )
                elif count and count == 15:
                    role = get(message.guild.roles, id=self.event_role)
                    await message.author.add_roles(role, reason='15 event messages.')
                    await message.author.send(embed=self.event_embed)
                    async with self.bot.db.acquire() as conn:
                        await conn.execute(
                            '''
                            UPDATE levels
                                SET event = event + 1
                            WHERE id = $1
                            ''',
                            message.author.id,
                        )
                self.event_cooldown[message.author.id] = time.time()

    @commands.command()
    async def eventmode(self, ctx: commands.Context, *, args = None):
        if args is not None:
            set = args.split(' ')
            if set[0] == 'enable' and len(set) == 2:
                if self.event_mode:
                    await ctx.send('Event mode is already enabled.')
                else:
                    role = get(ctx.guild.roles, id=int(set[1]))
                    if not role: return await ctx.send('Please provide the right role ID.')
                    async with self.bot.db.acquire() as conn:
                        await conn.execute(
                            '''
                            ALTER TABLE levels
                            ADD event INTEGER DEFAULT 0;
                            '''
                        )
                        await conn.execute(
                            '''
                            UPDATE options
                                SET eventmode = NOT eventmode,
                                    eventroleid = $1
                            WHERE beep = 'boop';
                            ''',
                            int(set[1])
                        )
                    self.event_mode = True
                    await ctx.send('Enabled event mode')
            elif set[0] == 'conclude':
                if not self.event_mode:
                    await ctx.send('Event mode is not enabled.')
                else:
                    async with self.bot.db.acquire() as conn:
                        await conn.execute(
                            '''
                            ALTER TABLE LEVELS
                            DROP COLUMN event;
                            UPDATE options
                                SET eventmode = NOT eventmode,
                                    eventroleid = 0
                            WHERE beep = 'boop';
                            '''
                        )
                    self.event_mode = False
                    await ctx.send('Concluded event mode.')
            else:
                await ctx.send('That\'s not one of the two options.')
        else:
            await ctx.send(self.event_mode)

def setup(bot: AstroBot):
    bot.add_cog(Events(bot))
