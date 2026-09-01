from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List
from io import BytesIO

from discord import ButtonStyle, InteractionType, Message, File
from discord.ext import commands
from discord.member import Member
from discord.mentions import AllowedMentions
from discord.threads import Thread
from discord.ui import Button, View

from rapidocr.utils.output import RapidOCROutput

from .. import get_from_environment

if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)


class Mods(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot
        self.trending_role = get_from_environment("TRENDING_ROLE", int)

    def has_any(self, s: str, words: List[str]):
        return any(word in s.lower() for word in words)

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

    @commands.command(
        brief="Make a trending thread.", help="Queue a thread to be made at admin discretion. *trending Game - Desc"
    )
    @commands.has_permissions(ban_members=True)
    async def trending(self, ctx, *, args=None):
        forum = args.split(' - ', 1)
        if args is None or len(forum) != 2:
            await ctx.send(
                'Please include the game name, as well as a brief description in the format \'Game - Desc\'.'
            )
        else:
            admin = self.bot.get_channel(get_from_environment('ADMIN_CHANNEL', int))
            await admin.send(content=args, view=self.view_vote)
            await ctx.send('Sent to admins, awaiting approval.')

    @commands.command(
        brief="Edit a trending channel description.",
        help="Edit the first message in a trending channel. *tredit thread_id desc",
    )
    @commands.has_permissions(ban_members=True)
    async def tredit(self, ctx, trend: int, *, args=None):
        trendingChannel = await ctx.guild.fetch_channel(trend)
        if not trendingChannel:
            return await ctx.send("Please give a valid thread ID.")
        if not args:
            return await ctx.send("Please give text...")
        text = f'EDIT\n{trendingChannel.id}\n**__{trendingChannel.name}__**\n{args}'
        admin = self.bot.get_channel(get_from_environment('ADMIN_CHANNEL', int))
        await admin.send(content=text, view=self.view_vote)
        await ctx.send('Sent to admins, awaiting approval.')

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.type == InteractionType.component:
            if interaction.data['custom_id'] == 'yes':
                trending_announcement = self.bot.get_channel(get_from_environment('TRENDING_ANNOUNCEMENT_CHANNEL', int))
                if interaction.message.content.split('\n')[0] == "EDIT":
                    data = interaction.message.content.split('\n', 3)
                    trendingChannel = await interaction.guild.fetch_channel(data[1])
                    await trendingChannel.edit(archived=False)
                    message = await trendingChannel.fetch_message(trendingChannel.id)
                    await message.edit(content=f"**__{trendingChannel.name}__**\n{data[3]}")
                    await trending_announcement.send(
                        f"<#{trendingChannel.id}> has come back from the dead! <@&{self.trending_role}>",
                        allowed_mentions=AllowedMentions(roles=True),
                    )
                    await interaction.channel.send(f"<#{trendingChannel.id}> Done. Send Fish my regards.")
                    await interaction.response.defer()
                    await interaction.message.edit(
                        content=f'**Edited** ~~{interaction.message.content}~~', view=self.view_done
                    )

                else:
                    forum = interaction.message.content.split(' - ', 1)
                    trending = self.bot.get_channel(get_from_environment('TRENDING_CHANNEL', int))
                    game_thread = await trending.create_thread(
                        name=forum[0],
                        content=f'__**{forum[0]}**__\n{forum[1]}\n',
                        reason='Trending thread made at mod/admin discretion',
                    )
                    await trending_announcement.send(
                        content=f'We have a new trending channel <@&{self.trending_role}>! <#{game_thread.thread.id}>',
                        allowed_mentions=AllowedMentions(roles=True),
                    )
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

    @commands.Cog.listener()
    async def on_message(self, msg: Message):
        nsfw_invites_sent = self.nsfw_invite_filter(msg)
        ocr_detected = False

        author = msg.author
        if not isinstance(author, Member):
            return
        if (
            not (author.guild_permissions.attach_files or author.guild_permissions.embed_links)
            and len(msg.attachments) != 0
        ):
            ocr_detected = self.ocr_filter(msg)

        if not (ocr_detected or nsfw_invites_sent):
            return

        ban_reason = (
            'sending NSFW invites' if nsfw_invites_sent else 'sending images of NSFW content or cryptocurrency scams'
        )
        notified = await self.ban_author(msg, ban_reason)

        log_msg = f"""**User autobanned by AstroBot**
User: <@{msg.author.id}> ({msg.author.id})
Notified by DM: {'Yes' if notified else 'No'}
Reason: """

        files: List[File] = []
        if nsfw_invites_sent:
            log_msg += "NSFW invites sent\n"
            log_msg += f"Message content: `{msg.content}`"
        elif ocr_detected:
            log_msg += "OCR filter triggered with the following content"
            for f in msg.attachments:
                async with self.bot.session.get(f.url) as resp:
                    file = File(BytesIO(await resp.read()), filename=f.filename)
                    files.append(file)

        automod = self.bot.get_channel(get_from_environment('AUTOMOD_LOG_CHANNEL', int))
        await automod.send(log_msg, files=files)

    async def ban_author(self, msg: Message, reason: str):
        try:
            await msg.author.send(
                f"**You have been banned from the PlayStation Discord for {reason}.**\n* We are aware that your account was hacked.\n* Once you've recovered it and enabled 2 factor authentication, join our appeals server (https://discord.gg/CuG2mTQ) and appeal your ban.\n\nBelieve you've received this message in error? Join the ban appeals server and let us know."
            )
            informed = True
        except:
            informed = False
        await msg.guild.ban(
            msg.author, reason=f'Autoban for NSFW server invites. User was {"not" if not informed else ""} informed.'
        )
        return informed

    def nsfw_invite_filter(self, msg: Message):
        msg_lower = msg.content.lower()
        return (
            self.has_any(msg.content, ["nude", "leak", "onlyfan", "teen", "porn", "nsfw"])
            and ("@everyone" in msg_lower or "discord.gg" in msg_lower)
            and not msg.author.bot
        )

    def ocr_filter(self, msg: Message):
        bad_terms = (
            ["nude", "leak", "onlyfan", "teen", "porn", "nsfw", "naked", "sex", "on cam", "cam in"]
            + ["crypto", "bitcoin", "giveaway"]
            + ["@everyone", "discord.gg"]
        )
        ocr = self.bot.engine

        if len(msg.attachments) == 0:
            return False

        det = []
        for img in msg.attachments:
            result = ocr(img.url)
            assert isinstance(result, RapidOCROutput)
            if result.txts is None or result.scores is None:
                return False

            res = zip(result.txts, result.scores)
            for r, conf in res:
                if self.has_any(r, bad_terms) and conf > 0.9:
                    return True
        return False


async def setup(bot: AstroBot) -> None:
    await bot.add_cog(Mods(bot))
