from __future__ import annotations

import logging
import math
import os
import time
from typing import TYPE_CHECKING

import asyncpg
import discord
from discord.ext import commands, tasks
from discord.utils import get

from .. import Embed, get_list, get_from_environment


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)


class Levels(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    double = False

    # async def cog_before_invoke(self, ctx):
    #   async with self.bot.db.acquire() as conn:
    #        record = await conn.fetch(
    #            '''
    #            SELECT doublexp FROM options WHERE beep = 'boop'
    #            '''
    #        )
    #        self.double = [x['doublexp'] for x in record][0]

    levelup = [
        (
            Embed(
                title='You leveled up to Bronze 1 in **PlayStation**!',
                description='''You now have access to **talk in voice channels**, and **post links to any website**!
You're currently at **250** <:point:756582101339471933>. Check your progress any time by using \`*xp\` in #bot-commands.

Your next level is <:b2:763397325208551484> **Bronze 2** at **750** <:point:756582101339471933>.''',
                colour=0xA26161,
            )
            .set_thumbnail(url='https://cdn.discordapp.com/emojis/763397324994248714.png')
            .add_field(
                name='Your Progress',
                value='''<:b1:763397324994248714><:c:684852990980522060> **Bronze 1** - **Talk in voice channels and post all kinds of links**
<:b2:763397325208551484><:clear:904125930467913789> **Bronze 2** - Participate in double XP events
<:b3:763397329096278056><:clear:904125930467913789> **Bronze 3** - Stream in voice channels
<:s1:763397329079894016><:clear:904125930467913789> **Silver 1** - File attachments and link embeds
<:s2:763397329499455508><:clear:904125930467913789> **Silver 2** - Jumbo command (!jumbo)
<:s3:763397329541136397><:clear:904125930467913789> **Silver 3** - (Work in progress, stay tuned!)
<:g1:763397329100734494><:clear:904125930467913789> **Gold 1** - Access the lounge, a special chat channel
<:g2:763397329067442256><:clear:904125930467913789> **Gold 2** - Ability to post in the FAQs channel
<:g3:763397329130094652><:clear:904125930467913789> **Gold 3** - Priority application for project teams
<:p:763397329788862524><:clear:904125930467913789> **Platinum** - Hoisted role, Choose your own color (\*color)''',
                inline=False,
            )
            .set_footer(
                text='This is an automatic message. Replies will not be seen, use Modmail to contact the mods.',
                icon_url='https://cdn.discordapp.com/emojis/684852991081447450.png',
            )
        ),
        (
            Embed(
                title='You leveled up to Bronze 2 in **PlayStation**!',
                description='''You now have access to **double XP events**, earn double the points during special events!
You're currently at **750** <:point:756582101339471933>. Check your progress any time by using \`*xp\` in #bot-commands.

Your next level is <:b2:763397329096278056> **Bronze 3** at **1,250** <:point:756582101339471933>.''',
                colour=0xC78585,
            )
            .set_thumbnail(url='https://cdn.discordapp.com/emojis/763397325208551484.png')
            .add_field(
                name='Your Progress',
                value='''<:b1:763397324994248714><:c:684852990980522060> **Bronze 1** - **Talk in voice channels and post all kinds of links**
<:b2:763397325208551484><:c:684852990980522060> **Bronze 2** - **Participate in double XP events**
<:b3:763397329096278056><:clear:904125930467913789> **Bronze 3** - Stream in voice channels
<:s1:763397329079894016><:clear:904125930467913789> **Silver 1** - File attachments and link embeds
<:s2:763397329499455508><:clear:904125930467913789> **Silver 2** - Jumbo command (!jumbo)
<:s3:763397329541136397><:clear:904125930467913789> **Silver 3** - (Work in progress, stay tuned!)
<:g1:763397329100734494><:clear:904125930467913789> **Gold 1** - Access the lounge, a special chat channel
<:g2:763397329067442256><:clear:904125930467913789> **Gold 2** - Ability to post in the FAQs channel
<:g3:763397329130094652><:clear:904125930467913789> **Gold 3** - Priority application for project teams
<:p:763397329788862524><:clear:904125930467913789> **Platinum** - Hoisted role, Choose your own color (\*color)''',
                inline=False,
            )
            .set_footer(
                text='This is an automatic message. Replies will not be seen, use Modmail to contact the mods.',
                icon_url='https://cdn.discordapp.com/emojis/684852991081447450.png',
            )
        ),
        (
            Embed(
                title='You leveled up to Bronze 3 in **PlayStation**!',
                description='''You now have access to **stream in voice channels**!
You're currently at **1,250** <:point:756582101339471933>. Check your progress any time by using \`*xp\` in #bot-commands.

Your next level is <:b2:763397329079894016> **Silver 1** at **2,500** <:point:756582101339471933>.''',
                colour=0xC29F8C,
            )
            .set_thumbnail(url='https://cdn.discordapp.com/emojis/763397329096278056.png')
            .add_field(
                name='Your Progress',
                value='''<:b1:763397324994248714><:c:684852990980522060> **Bronze 1** - **Talk in voice channels and post all kinds of links**
<:b2:763397325208551484><:c:684852990980522060> **Bronze 2** - **Participate in double XP events**
<:b3:763397329096278056><:c:684852990980522060> **Bronze 3** - **Stream in voice channels**
<:s1:763397329079894016><:clear:904125930467913789> **Silver 1** - File attachments and link embeds
<:s2:763397329499455508><:clear:904125930467913789> **Silver 2** - Jumbo command (!jumbo)
<:s3:763397329541136397><:clear:904125930467913789> **Silver 3** - (Work in progress, stay tuned!)
<:g1:763397329100734494><:clear:904125930467913789> **Gold 1** - Access the lounge, a special chat channel
<:g2:763397329067442256><:clear:904125930467913789> **Gold 2** - Ability to post in the FAQs channel
<:g3:763397329130094652><:clear:904125930467913789> **Gold 3** - Priority application for project teams
<:p:763397329788862524><:clear:904125930467913789> **Platinum** - Hoisted role, Choose your own color (\*color)''',
                inline=False,
            )
            .set_footer(
                text='This is an automatic message. Replies will not be seen, use Modmail to contact the mods.',
                icon_url='https://cdn.discordapp.com/emojis/684852991081447450.png',
            )
        ),
        (
            Embed(
                title='You leveled up to Silver 1 in **PlayStation**!',
                description='''You now have access to **attach files and embed links**! Finally, all the images and reaction gifs are yours.
You're currently at **2,500** <:point:756582101339471933>. Check your progress any time by using \`*xp\` in #bot-commands.

Your next level is <:b2:763397329499455508> **Silver 2** at **5,000** <:point:756582101339471933>.''',
                colour=0x4C769A,
            )
            .set_thumbnail(url='https://cdn.discordapp.com/emojis/763397329079894016.png')
            .add_field(
                name='Your Progress',
                value='''<:b1:763397324994248714><:c:684852990980522060> **Bronze 1** - **Talk in voice channels and post all kinds of links**
<:b2:763397325208551484><:c:684852990980522060> **Bronze 2** - Participate in double XP events
<:b3:763397329096278056><:c:684852990980522060> **Bronze 3** - Stream in voice channels
<:s1:763397329079894016><:c:684852990980522060> **Silver 1** - **File attachments and link embeds**
<:s2:763397329499455508><:clear:904125930467913789> **Silver 2** - Jumbo command (!jumbo)
<:s3:763397329541136397><:clear:904125930467913789> **Silver 3** - (Work in progress, stay tuned!)
<:g1:763397329100734494><:clear:904125930467913789> **Gold 1** - Access the lounge, a special chat channel
<:g2:763397329067442256><:clear:904125930467913789> **Gold 2** - Ability to post in the FAQs channel
<:g3:763397329130094652><:clear:904125930467913789> **Gold 3** - Priority application for project teams
<:p:763397329788862524><:clear:904125930467913789> **Platinum** - Hoisted role, Choose your own color (\*color)''',
                inline=False,
            )
            .set_footer(
                text='This is an automatic message. Replies will not be seen, use Modmail to contact the mods.',
                icon_url='https://cdn.discordapp.com/emojis/684852991081447450.png',
            )
        ),
        (
            Embed(
                title='You leveled up to Silver 2 in **PlayStation**!',
                description='''You now have access to **Jumbo command (!jumbo)**, post large versions of emoji like they're stickers!
You're currently at **5,000** <:point:756582101339471933>. Check your progress any time by using \`*xp\` in #bot-commands.

Your next level is <:b2:763397329541136397> **Silver 3** at **7,500** <:point:756582101339471933>.''',
                colour=0x798DA8,
            )
            .set_thumbnail(url='https://cdn.discordapp.com/emojis/763397329499455508.png')
            .add_field(
                name='Your Progress',
                value='''<:b1:763397324994248714><:c:684852990980522060> **Bronze 1** - **Talk in voice channels and post all kinds of links**
<:b2:763397325208551484><:c:684852990980522060> **Bronze 2** - Participate in double XP events
<:b3:763397329096278056><:c:684852990980522060> **Bronze 3** - Stream in voice channels
<:s1:763397329079894016><:c:684852990980522060> **Silver 1** - File attachments and link embeds
<:s2:763397329499455508><:c:684852990980522060> **Silver 2** - **Jumbo command (!jumbo)**
<:s3:763397329541136397><:clear:904125930467913789> **Silver 3** - (Work in progress, stay tuned!)
<:g1:763397329100734494><:clear:904125930467913789> **Gold 1** - Access the lounge, a special chat channel
<:g2:763397329067442256><:clear:904125930467913789> **Gold 2** - Ability to post in the FAQs channel
<:g3:763397329130094652><:clear:904125930467913789> **Gold 3** - Priority application for project teams
<:p:763397329788862524><:clear:904125930467913789> **Platinum** - Hoisted role, Choose your own color (\*color)''',
                inline=False,
            )
            .set_footer(
                text='This is an automatic message. Replies will not be seen, use Modmail to contact the mods.',
                icon_url='https://cdn.discordapp.com/emojis/684852991081447450.png',
            )
        ),
        (
            Embed(
                title='You leveled up to Silver 3 in **PlayStation**!',
                description='''You're currently at **7,500** <:point:756582101339471933>. Check your progress any time by using \`*xp\` in #bot-commands.

Your next level is <:b2:763397329100734494> **Gold 1** at **10,000** <:point:756582101339471933>.''',
                colour=0xB0B7CA,
            )
            .set_thumbnail(url='https://cdn.discordapp.com/emojis/763397329541136397.png')
            .add_field(
                name='Your Progress',
                value='''<:b1:763397324994248714><:c:684852990980522060> **Bronze 1** - **Talk in voice channels and post all kinds of links**
<:b2:763397325208551484><:c:684852990980522060> **Bronze 2** - Participate in double XP events
<:b3:763397329096278056><:c:684852990980522060> **Bronze 3** - Stream in voice channels
<:s1:763397329079894016><:c:684852990980522060> **Silver 1** - File attachments and link embeds
<:s2:763397329499455508><:c:684852990980522060> **Silver 2** - Jumbo command (!jumbo)
<:s3:763397329541136397><:c:684852990980522060> **Silver 3** - **(Work in progress, stay tuned!)**
<:g1:763397329100734494><:clear:904125930467913789> **Gold 1** - Access the lounge, a special chat channel
<:g2:763397329067442256><:clear:904125930467913789> **Gold 2** - Ability to post in the FAQs channel
<:g3:763397329130094652><:clear:904125930467913789> **Gold 3** - Priority application for project teams
<:p:763397329788862524><:clear:904125930467913789> **Platinum** - Hoisted role, Choose your own color (\*color)''',
                inline=False,
            )
            .set_footer(
                text='This is an automatic message. Replies will not be seen, use Modmail to contact the mods.',
                icon_url='https://cdn.discordapp.com/emojis/684852991081447450.png',
            )
        ),
        (
            Embed(
                title='You leveled up to Gold 1 in **PlayStation**!',
                description='''You now have access to **#the-lounge**, a special chat channel!
You're currently at **10,000** <:point:756582101339471933>. Check your progress any time by using \`*xp\` in #bot-commands.

Your next level is <:g2:763397329067442256> **Gold 2** at **15,000**  <:point:756582101339471933>.''',
                colour=0xB38F4F,
            )
            .set_thumbnail(url='https://cdn.discordapp.com/emojis/763397329100734494.png')
            .add_field(
                name='Your Progress',
                value='''<:b1:763397324994248714><:c:684852990980522060> **Bronze 1** - **Talk in voice channels and post all kinds of links**
<:b2:763397325208551484><:c:684852990980522060> **Bronze 2** - Participate in double XP events
<:b3:763397329096278056><:c:684852990980522060> **Bronze 3** - Stream in voice channels
<:s1:763397329079894016><:c:684852990980522060> **Silver 1** - File attachments and link embeds
<:s2:763397329499455508><:c:684852990980522060> **Silver 2** - Jumbo command (!jumbo)
<:s3:763397329541136397><:c:684852990980522060> **Silver 3** - (Work in progress, stay tuned!)
<:g1:763397329100734494><:c:684852990980522060> **Gold 1** - **Access the lounge, a special chat channel**
<:g2:763397329067442256><:clear:904125930467913789> **Gold 2** - Ability to post in the FAQs channel
<:g3:763397329130094652><:clear:904125930467913789> **Gold 3** - Priority application for project teams
<:p:763397329788862524><:clear:904125930467913789> **Platinum** - Hoisted role, Choose your own color (\*color)''',
                inline=False,
            )
            .set_footer(
                text='This is an automatic message. Replies will not be seen, use Modmail to contact the mods.',
                icon_url='https://cdn.discordapp.com/emojis/684852991081447450.png',
            )
        ),
        (
            Embed(
                title='You leveled up to Gold 2 in **PlayStation**!',
                description='''You now have access to **double XP events**, earn double the points during special events!
You're currently at **10,000** <:point:756582101339471933>. Check your progress any time by using \`*xp\` in #bot-commands.

Your next level is <:b2:763397329130094652> **Gold 3** at **20,000** <:point:756582101339471933>.''',
                colour=0xCFB046,
            )
            .set_thumbnail(url='https://cdn.discordapp.com/emojis/763397329067442256.png')
            .add_field(
                name='Your Progress',
                value='''<:b1:763397324994248714><:c:684852990980522060> **Bronze 1** - **Talk in voice channels and post all kinds of links**
<:b2:763397325208551484><:c:684852990980522060> **Bronze 2** - Participate in double XP events
<:b3:763397329096278056><:c:684852990980522060> **Bronze 3** - Stream in voice channels
<:s1:763397329079894016><:c:684852990980522060> **Silver 1** - File attachments and link embeds
<:s2:763397329499455508><:c:684852990980522060> **Silver 2** - Jumbo command (!jumbo)
<:s3:763397329541136397><:c:684852990980522060> **Silver 3** - (Work in progress, stay tuned!)
<:g1:763397329100734494><:c:684852990980522060> **Gold 1** - Access the lounge, a special chat channel
<:g2:763397329067442256><:c:684852990980522060> **Gold 2** - **Ability to post in the FAQs channel**
<:g3:763397329130094652><:clear:904125930467913789> **Gold 3** - Priority application for project teams
<:p:763397329788862524><:clear:904125930467913789> **Platinum** - Hoisted role, Choose your own color (\*color)''',
                inline=False,
            )
            .set_footer(
                text='This is an automatic message. Replies will not be seen, use Modmail to contact the mods.',
                icon_url='https://cdn.discordapp.com/emojis/684852991081447450.png',
            )
        ),
        (
            Embed(
                title='You leveled up to Gold 3 in **PlayStation**!',
                description='''You now have access to **priority application for project teams**, be prioritized when applying for our special teams! Check <#719536356727980032> for more information, and message ModMail to apply.
You're currently at **20,000** <:point:756582101339471933>. Check your progress any time by using \`*xp\` in #bot-commands.

Your next level is <:b2:763397329788862524> **Platinum** at **30,000** <:point:756582101339471933>.''',
                colour=0xF2E14B,
            )
            .set_thumbnail(url='https://cdn.discordapp.com/emojis/763397329130094652.png')
            .add_field(
                name='Your Progress',
                value='''<:b1:763397324994248714><:c:684852990980522060> **Bronze 1** - **Talk in voice channels and post all kinds of links**
<:b2:763397325208551484><:c:684852990980522060> **Bronze 2** - Participate in double XP events
<:b3:763397329096278056><:c:684852990980522060> **Bronze 3** - Stream in voice channels
<:s1:763397329079894016><:c:684852990980522060> **Silver 1** - File attachments and link embeds
<:s2:763397329499455508><:c:684852990980522060> **Silver 2** - Jumbo command (!jumbo)
<:s3:763397329541136397><:c:684852990980522060> **Silver 3** - (Work in progress, stay tuned!)
<:g1:763397329100734494><:c:684852990980522060> **Gold 1** - Access the lounge, a special chat channel
<:g2:763397329067442256><:c:684852990980522060> **Gold 2** - Ability to post in the FAQs channel
<:g3:763397329130094652><:c:684852990980522060> **Gold 3** - **Priority application for project teams**
<:p:763397329788862524><:clear:904125930467913789> **Platinum** - Hoisted role, Choose your own color (\*color)''',
                inline=False,
            )
            .set_footer(
                text='This is an automatic message. Replies will not be seen, use Modmail to contact the mods.',
                icon_url='https://cdn.discordapp.com/emojis/684852991081447450.png',
            )
        ),
        (
            Embed(
                title='You leveled up to Platinum in **PlayStation**!',
                description='''You're now **hoisted (displayed on the member list sidebar)**, and have access to **custom colors (\*color command)**!
You're currently at **30,000** <:point:756582101339471933>. Check your progress any time by using \`*xp\` in #bot-commands.

This is the final level. Congratulations on completing our level road! We're working on more cool stuff for you, so stay tuned.''',
                colour=0x73BFF3,
            )
            .set_thumbnail(url='https://cdn.discordapp.com/emojis/763397329788862524.png')
            .add_field(
                name='Your Progress',
                value='''<:b1:763397324994248714><:c:684852990980522060> **Bronze 1** - **Talk in voice channels and post all kinds of links**
<:b2:763397325208551484><:c:684852990980522060> **Bronze 2** - Participate in double XP events
<:b3:763397329096278056><:c:684852990980522060> **Bronze 3** - Stream in voice channels
<:s1:763397329079894016><:c:684852990980522060> **Silver 1** - File attachments and link embeds
<:s2:763397329499455508><:c:684852990980522060> **Silver 2** - Jumbo command (!jumbo)
<:s3:763397329541136397><:c:684852990980522060> **Silver 3** - (Work in progress, stay tuned!)
<:g1:763397329100734494><:c:684852990980522060> **Gold 1** - Access the lounge, a special chat channel
<:g2:763397329067442256><:c:684852990980522060> **Gold 2** - Ability to post in the FAQs channel
<:g3:763397329130094652><:c:684852990980522060> **Gold 3** - Priority application for project teams
<:p:763397329788862524><:c:684852990980522060> **Platinum** - **Hoisted role, Choose your own color (\*color)**''',
                inline=False,
            )
            .set_footer(
                text='This is an automatic message. Replies will not be seen, use Modmail to contact the mods.',
                icon_url='https://cdn.discordapp.com/emojis/684852991081447450.png',
            )
        ),
    ]

    thresholds = [250, 750, 1250, 2500, 5000, 7500, 10000, 15000, 20000, 30000]
    level_roles = get_list('LEVEL_ROLES')
    names = [
        'None',
        'Bronze 1',
        'Bronze 2',
        'Bronze 3',
        'Silver 1',
        'Silver 2,',
        'Silver 3',
        'Gold 1',
        'Gold 2',
        'Gold 3',
        'Platinum',
    ]
    main_server = get_from_environment('MAIN_GUILD', int)
    xp_cooldown = {}

    def cooldown(self, id):
        if id not in self.xp_cooldown:
            return False
        return self.xp_cooldown[id] + 15 > time.time()

    async def get_xp(self, id):
        async with self.bot.db.acquire() as conn:
            record = await conn.fetch(
                '''
                SELECT xp FROM levels WHERE id = $1
                ''',
                id,
            )
            if record:
                xp = [x['xp'] for x in record][0]
            else:
                xp = None
        return xp

    @commands.Cog.listener()
    async def on_message(self, message):
        async with self.bot.db.acquire() as conn:
            record = await conn.fetch(
                '''
                SELECT doublexp FROM options WHERE beep = 'boop'
                '''
            )
            self.double = [x['doublexp'] for x in record][0]
        if message.guild.id != self.main_server:
            return
        else:
            xp = await self.get_xp(message.author.id)
            if not self.cooldown(message.author.id) and not message.author.bot:
                if self.double:
                    async with self.bot.db.acquire() as conn:
                        await conn.execute(
                            '''
                            UPDATE levels
                                SET xp = xp + 2
                            WHERE id = $1
                            ''',
                            message.author.id,
                        )
                elif xp == None:
                    async with self.bot.db.acquire() as conn:
                        await conn.execute(
                            '''
                            INSERT INTO levels (id, xp, lvl) VALUES ($1, 1, 0)
                            ''',
                            message.author.id,
                        )
                else:
                    async with self.bot.db.acquire() as conn:
                        await conn.execute(
                            '''
                            UPDATE levels
                                SET xp = xp + 1
                            WHERE id = $1
                            ''',
                            message.author.id,
                        )
                self.xp_cooldown[message.author.id] = time.time()
                if xp in self.thresholds:
                    index = self.thresholds.index(xp)
                    await message.author.send(embed=self.levelup[index])
                    role = get(message.guild.roles, id=self.level_roles[index - 1])
                    await message.author.remove_roles(role, reason='Leveled up.')
                    role = get(message.guild.roles, id=self.level_roles[index])
                    await message.author.add_roles(role, reason='Leveled up.')
                    logger = self.bot.get_channel(get_from_environment('LEVELS_CHANNEL', int))
                    await logger.send(f'{message.author.mention} leveled up to {self.names[index+1]}')

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if guild.id == self.main_server:
            xp = await self.get_xp(user.id)
            logger = self.bot.get_channel(get_from_environment('LEVELS_CHANNEL', int))
            async with self.bot.db.acquire() as conn:
                await conn.execute(
                    '''
                    DELETE FROM levels
                    WHERE id = $1
                    ''',
                    user.id,
                )
            await logger.send(f'**XP Wiped:** {user.mention} ({user.id}): {xp}')

    # @commands.Cog.listener()
    # async def on_member_join(self, member: discord.Member):
    #     if member.guild == 860585050838663188:
    #         async with self.bot.db.acquire() as conn:
    #             await conn.execute(
    #                 '''
    #                 INSERT INTO levels (id, xp, lvl) VALUES ($1, 0, 0)
    #                 ''',
    #                 member.id,
    #             )

    @commands.command(brief='Check your XP & more.', help='See your current XP, rank, and progress to next level.')
    async def xp(self, ctx: commands.Context):
        level = 0
        async with self.bot.db.acquire() as conn:
            xp = await self.get_xp(ctx.author.id)
            record = await conn.fetch(
                '''
                SELECT id, ROW_NUMBER () OVER (ORDER BY xp DESC) FROM levels
                ''',
            )
            for x in record:
                if x['id'] == ctx.author.id:
                    pos = x['row_number']
        for x in self.thresholds:
            if xp > x:
                level += 1
        rank = self.names[level]
        if level == 0:
            percent = math.floor(xp*100/250)
        elif level == 10:
            percent = 100
        else:
            percent = math.floor(
                ((xp - self.thresholds[level - 1]) / (self.thresholds[level] - self.thresholds[level - 1])) * 100
            )
        progressbar = f"{'<:p1:828359003712127068>' * math.floor(percent/10)}{'<:p2:828359003897593946>' * (10-math.floor(percent/10))}"
        desc = f'''**{rank}** ({xp} <:p_:828359003775303702>)
        {percent}% to next level
        {progressbar}'''
        if self.double:
            desc = desc + '\n<a:astrodance3:790935872844857405> **Double XP activated!**'
        embed = Embed(title=f'{ctx.author.name} (Rank #{pos})', description=desc).set_thumbnail(
            url=str(ctx.author.avatar.url)
        )
        await ctx.send(embed=embed)

    @commands.command(brief='Enable or disable double xp.', help='*doublexp toggle')
    @commands.has_permissions(administrator=True)
    async def doublexp(self, ctx: commands.Context, truthy: bool = None):
        if truthy and not self.double:
            async with self.bot.db.acquire() as conn:
                await conn.execute(
                    '''
                    UPDATE options
                        SET doublexp = TRUE
                    WHERE beep = 'boop'
                    '''
                )
            self.double = True
            await ctx.send('Double XP set to true')
        elif not truthy and self.double:
            async with self.bot.db.acquire() as conn:
                await conn.execute(
                    '''
                    UPDATE options
                        SET doublexp = FALSE
                    WHERE beep = 'boop'
                    '''
                )
                self.double = False
                await ctx.send('Double xp set to false.')
        else:
            await ctx.send(f'Try again. The current double xp status is: {self.double}')

    @commands.command(brief='Set a person\'s xp.', help='*setxp id xp')
    @commands.has_permissions(administrator=True)
    async def setxp(self, ctx: commands.Context, user: discord.User = None, xp: int = None):
        if user and xp:
            async with self.bot.db.acquire() as conn:
                await conn.execute(
                    '''
                    UPDATE levels
                        SET xp = $1
                    WHERE id = $2
                    ''',
                    xp,
                    user.id,
                )
            await ctx.send(f'Set {user.mention}\'s XP to {xp}.')
        else:
            await ctx.send(f'Please give an ID and XP to set to.')


    @commands.command(
        brief='See the top users by XP.',
        help='Put a number between one and ten after *leaderboard to see that page of the leaderboard. 15 second cooldown.',
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def leaderboard(self, ctx: commands.Context, *, args=None):
        string = ""
        num = 1
        if args is None or args == 1:
            async with self.bot.db.acquire() as conn:
                record = await conn.fetch(
                    '''
                    SELECT id, xp
                    FROM levels
                    ORDER BY xp DESC
                    LIMIT 10
                    '''
                )
        elif int(args) > 1 and int(args) <= 10:
            async with self.bot.db.acquire() as conn:
                record = await conn.fetch(
                    '''
                    SELECT id, xp
                    FROM levels
                    ORDER BY xp DESC
                    LIMIT 10
                    OFFSET $1
                    ''',
                    (int(args) - 1) * 10,
                )
                num = num + (int(args) - 1) * 10
        else:
            return await ctx.send(content='Only pages 1-10 of the leaderboard are available.')
        for x in record:
            try:
                user = self.bot.get_guild(self.main_server).get_member(x['id'])
                user = user.name
            except (discord.errors.NotFound, AttributeError) as e:
                user = "User left."
            string += f"{num}. {user} - **{x['xp']}** <:p_:828359003775303702>\n"
            num += 1
        embed = Embed(title='**Points leaderboard**', description=string)
        await ctx.send(embed=embed)


def setup(bot: AstroBot):
    bot.add_cog(Levels(bot))
