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


class Levels(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    double = False

    #async def cog_before_invoke(self, ctx):
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
    # level_roles=[763810437593694238, 718538246069420124, 763810438210650185, 763810441570418738, 718538600559411252, 763810443130437683, 763810720881049641, 718538637490389133, 763810724509384774, 718538533668651040]
    level_roles = [
        904115857003778058,
        904115901803155486,
        904115930303442966,
        904115976897974272,
        904116096989266010,
        904116124562632764,
        904116155759882261,
        904116183802974208,
        904116212043235339,
        904116235237752832,
    ]
    main_server = 860585050838663188
    xp_cooldown = {}

    def cooldown(self, id):
        if id not in self.xp_cooldown:
            return False
        return self.xp_cooldown[id] + 15 > time.time()

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
                async with self.bot.db.acquire() as conn:
                    record = await conn.fetch(
                        '''
                        SELECT xp FROM levels WHERE id = $1
                        ''',
                        message.author.id,
                    )
                    if record:
                        xp = [x['xp'] for x in record][0]
                    else: xp = None
                if xp in self.thresholds:
                    index = self.thresholds.index(xp)
                    await message.author.send(embed=self.levelup[index])
                    role = get(message.guild.roles, id=self.level_roles[index - 1])
                    await message.author.remove_roles(role, reason='Leveled up.')
                    role = get(message.guild.roles, id=self.level_roles[index])
                    await message.author.add_roles(role, reason='Leveled up.')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        async with self.bot.db.acquire() as conn:
            await conn.execute(
                '''
                INSERT INTO levels (id, xp, lvl) VALUES ($1, 0, 0)
                ''',
                member.id,
            )

    @commands.command()
    async def xp(self, ctx: commands.Context):
        async with self.bot.db.acquire() as conn:
            record = await conn.fetch(
                '''
                SELECT xp FROM levels WHERE id = $1
                ''',
                ctx.author.id,
            )
            xp = [x['xp'] for x in record][0]
        await ctx.send(xp)

    @commands.command()
    async def doublexp(self, ctx: commands.Context, message: str = None):
        if message == 'toggle':
            async with self.bot.db.acquire() as conn:
                await conn.execute(
                    '''
                    UPDATE options
                        SET doublexp = NOT doublexp
                    WHERE beep = 'boop'
                    '''
                )
            self.double = not self.double
            await ctx.send('Toggled double XP.')
        else:
            await ctx.send(self.double)

    @commands.command()
    async def setxp(self, ctx: commands.Context, *, args):
        if args is not None:
            set = args.split(' ')
            if len(set) != 2:
                return await ctx.send(f'Please give an ID and XP to set to, and only those.')
            async with self.bot.db.acquire() as conn:
                await conn.execute(
                    '''
                    UPDATE levels
                        SET xp = $1
                    WHERE id = $2
                    ''',
                    int(set[1]),
                    int(set[0]),
                )
            await ctx.send(f'Set <@{set[0]}>\'s XP to {set[1]}.')


def setup(bot: AstroBot):
    bot.add_cog(Levels(bot))
