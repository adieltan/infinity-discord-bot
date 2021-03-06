import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

from PIL import Image, ImageDraw, ImageFont
import dateparser
from ._utils import *


class OwnerCog(commands.Cog, name="Owner"):
    """Only owner/managers can use this."""

    def __init__(self, bot):
        self.bot = bot
        self.COG_EMOJI = "🔐"

    @commands.command(name="dm", aliases=["adm"])
    @is_manager()
    async def dm(self, ctx, user: discord.User, *, message: str):
        """Anounymous DM."""
        try:
            await user.send(message)
            await ctx.tick(True)
        except:
            await ctx.tick(False)

    @commands.command(name="status")
    @commands.is_owner()
    async def status(
        self, ctx, status: typing.Literal["dnd", "online", "idle", "offline"]
    ):
        """Edit's the bot's status."""
        await self.bot.db.bot.update_one(
            {"_id": "status"}, {"$set": {"status": status}}, upsert=True
        )
        await self.bot.change_status()
        await ctx.message.add_reaction("✅")

    @commands.command(name="activity")
    @commands.is_owner()
    async def activity(self, ctx, *, activity=None):
        """Edit's the bot's activity."""
        await self.bot.db.bot.update_one(
            {"_id": "status"}, {"$set": {"activity": activity}}, upsert=True
        )
        await self.bot.change_status()
        await ctx.message.add_reaction("✅")

    @commands.command(name="activitytype")
    @commands.is_owner()
    async def activitytype(
        self, ctx, activityType: typing.Literal["playing", "listening", "watching"]
    ):
        """Edit's the bot's activityType."""
        await self.bot.db.bot.update_one(
            {"_id": "status"}, {"$set": {"activityType": activityType}}, upsert=True
        )
        await self.bot.change_status()
        await ctx.message.add_reaction("✅")

    @commands.command(name="blacklist", aliases=["bl"])
    @is_manager()
    async def blacklist(self, ctx, user: discord.User, *, reason: str = None):
        """Blacklists a member from using the bot."""
        if user.id in self.bot.managers:
            await ctx.reply("You can't blacklist them.")
            return
        await Database.edit_user(
            self,
            user.id,
            {
                "bl": True,
                "blreason": reason + f"\nResponsible manager: {ctx.author.id}",
            },
        )
        await self.bot.cbl()
        await ctx.reply(
            embed=discord.Embed(
                title="Blacklist",
                description=f"Blacklisted {user.mention} `{user.id}`.",
                color=discord.Color.red(),
            )
        )
        await user.send(
            f"You have been blacklisted by a bot moderator ({ctx.author.mention}) for {reason}\nTo appeal or provide context, join our support server at https://discord.gg/dHGqUZNqCu and head to <#851637967952412723>."
        )
        embed = discord.Embed(
            title="Blacklist",
            description=f"{user.mention} for {reason}",
            color=discord.Color.red(),
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        await self.bot.changes.send(embed=embed)

    @commands.command(name="unblacklist", aliases=["ubl"])
    @is_manager()
    async def unblacklist(self, ctx, user: discord.User, *, reason: str):
        """unBlacklists a member from using the bot."""
        await Database.edit_user(self, user.id, {"bl": None, "blreason": None})
        await self.bot.cbl()
        await ctx.reply(
            embed=discord.Embed(
                title="Unblacklist",
                description=f"Unlacklisted {user.mention} `{user.id}`.",
                color=discord.Color.green(),
            )
        )
        await user.send(
            f"You have been unblacklisted by a bot manager ({ctx.author.mention}).\nYou can now continue using bot commands as usual."
        )
        embed = discord.Embed(
            title="Unbacklist",
            description=f"{user.mention} for {reason}",
            color=discord.Color.green(),
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        await self.bot.changes.send(embed=embed)

    @commands.command(name="blacklistcheck", aliases=["blc"])
    @is_manager()
    async def blacklistcheck(self, ctx, user: discord.User):
        """Checks if a member is blacklisted from using the bot."""
        results = await Database.get_user(self, user.id)
        await ctx.reply(
            embed=discord.Embed(
                description=f"{user.mention}'s blacklist status: {results.get('bl')}.\nReason: {results.get('blreason')}"
            )
        )

    @commands.command(name="blacklisted")
    @is_manager()
    async def blacklisted(self, ctx):
        bled = set({})
        text = ""
        async for doc in self.bot.db["profile"].find({"bl": True}):
            bled.add(doc["_id"])
            text += f"{doc['_id']} {doc['blreason']}\n"
        self.bot.bled = bled
        buffer = io.BytesIO(text.encode("utf-8"))
        await ctx.reply(file=discord.File(buffer, filename="blacklisted.txt"))

    @commands.command(name="gg")
    @is_manager()
    async def gg(self, ctx, invite: str):
        """Frames your discord invite link"""
        # invite regex = (?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?
        url = "https://discord.gg/" + re.sub(
            "(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/+/?", "", invite
        )
        try:
            inv: discord.Invite = await self.bot.fetch_invite(url=url)
        except:
            return await ctx.reply(f"Invalid link.")

        e = discord.Embed(
            title=f"{inv.guild.name if inv.guild else inv.channel.name}",
            url=url,
            description=f"{url}\n",
            colour=discord.Color.random(),
        )
        if inv.guild:
            member = format(inv.approximate_member_count, ",")
            online = format(inv.approximate_presence_count, ",")
            e.description += f"Online Members: {online} / {member} members.\nChannel: {inv.channel.mention} `{inv.channel.name}`\nUses: {inv.uses} / {inv.max_uses}\nTemporary Membership: {True if inv.temporary else False}\nExpiry: {f'<t:{round(inv.expires_at.timestamp())}>' if inv.expires_at else 'None'}"
            try:
                e.set_thumbnail(url=inv.guild.icon)
            except:
                pass
        if inv.inviter:
            e.description += f"\nInvitor: {inv.inviter.mention} `{inv.inviter.id}`"
        v = discord.ui.View()
        v.add_item(discord.ui.Button(label="Link", url=url))
        await ctx.reply(embed=e, view=v)

    @commands.command(name="chat", aliases=["broadcast"])
    @commands.is_owner()
    async def chat(self, ctx, channel: TextChannel):
        to = 60
        await ctx.reply(
            f"Type messages that you want to send through the bot to {channel.mention}\nType `quit` to exit.\nSession will timeout after 60 seconds of inactivity.",
            mention_author=False,
        )

        def author(m):
            return m.author == ctx.author and m.channel.id == ctx.channel.id

        quit = False
        while quit is not True:
            try:
                message = await self.bot.wait_for("message", check=author, timeout=to)
                if message.content.lower() in ["quit", "exit"]:
                    quit = True
                    await message.reply("Session ended.")
                else:
                    try:
                        await channel.send(
                            message.content,
                            allowed_mentions=discord.AllowedMentions(
                                everyone=False, users=True, roles=False
                            ),
                        )
                    except:
                        await message.add_reaction("<:exclamation:876077084986966016>")
                    else:
                        await message.add_reaction("<a:verified:876075132114829342>")
            except asyncio.TimeoutError:
                quit = True
                await ctx.reply(
                    f"Session timeout. The broadcast session has ended.",
                    mention_author=False,
                )

    @commands.command(name="remove")
    @commands.is_owner()
    async def remove(self, ctx):
        """Removes the referenced message."""
        ref = ctx.message.reference
        if not ref:
            await ctx.reply(
                "Eh you gotta reply to the message you wanna remove!",
                mention_author=True,
            )
        else:
            message = await ctx.channel.fetch_message(ref.message_id)
            await message.delete()
            try:
                await ctx.message.delete()
            except:
                pass

    @commands.command(name="mutual")
    @commands.is_owner()
    async def mutual(self, ctx, user: discord.User):
        """Returns the servers that are shared with the user."""
        servers = "\n".join(
            f"`{guild.id}` {guild.name}" for guild in user.mutual_guilds
        )

        embed = discord.Embed(
            title="Mutual servers",
            description=servers,
            color=discord.Color.random(),
            timestamp=discord.utils.utcnow(),
        )
        embed.set_author(name=user.name, icon_url=user.avatar)
        embed.set_footer(text=f"{len(user.mutual_guilds)} servers")
        await ctx.reply(embed=embed)

    @commands.command(name="allcommands")
    @commands.is_owner()
    async def all_commands(self, ctx):
        """Returns all the commands + description."""
        text = ""
        for cog in self.bot.cogs:
            cogobj = self.bot.get_cog(cog)

            try:
                text += "+" + "-" * 105 + "+" + "\n"
                text += "| " + cogobj.qualified_name.upper() + "\n"
                if cogobj.description:
                    text += "| " + cogobj.description + "\n"
                text += "+" + "-" * 105 + "+" + "\n"
            except AttributeError:
                pass  # Idk how to make a no category category

            for c in cogobj.get_commands():
                text += (
                    f"• {c.name} {c.signature.replace('_', '')}".ljust(35, " ")
                    + f" {c.help}"
                    + "\n"
                )
                if isinstance(c, commands.Group):
                    for sc in c.commands:
                        text += (
                            "".ljust(5, " ")
                            + f"▪ {sc.name} {sc.signature.replace('_', '')}".ljust(
                                35, " "
                            )
                            + f" {sc.help}"
                            + "\n"
                        )
            text += "\n"
        buffer = io.BytesIO(text.encode("utf-8"))
        await ctx.reply(file=discord.File(buffer, filename="allcommands.txt"))

    @commands.command(name="poststats")
    @commands.is_owner()
    async def autostatsposting(self, ctx):
        """Post stats."""
        await self.bot.wait_until_ready()
        text = ""
        async with aiohttp.ClientSession() as cs:
            header = {"Authorization": os.getenv("dbl_token")}
            data = {"users": len(self.bot.users), "guilds": len(self.bot.guilds)}
            async with cs.post(
                url=f"https://discordbotlist.com/api/v1/bots/{self.bot.user.id}/stats",
                data=data,
                headers=header,
            ) as data:
                json = await data.json()
                text += f"DiscordBotList\n{json}"
            # header={'Authorization':os.getenv('voidbots_token')}
            # data = {'server_count':len(self.bot.guilds)}
            # async with cs.post(url=f"https://api.voidbots.net/bot/stats/{self.bot.user.id}", json=data, headers=header) as data:
            #     json = await data.json()
            #     if json.get('message') != "Servercount updated!":
            #         await reports.send(f"VoidBots\n{json}")
            header = {"Authorization": os.getenv("botlists_api")}
            data = {"status": "idle", "guilds": len(self.bot.guilds), "shards": 1}
            async with cs.patch(
                url=f"https://api.botlists.com/bot/{self.bot.user.id}",
                json=data,
                headers=header,
            ) as data:
                json = await data.json()
                text += f"BotLists\n{json}"
            header = {"Authorization": os.getenv("listcord_token")}
            data = {"server_count": len(self.bot.guilds)}
            async with cs.post(
                url=f"https://listcord.gg/api/bot/{self.bot.user.id}/stats",
                json=data,
                headers=header,
            ) as data:
                json = await data.json()
                text += f"Listcord\n{json}"
            # header={'Authorization':os.getenv('bladebot_token')}
            # data = {'servercount':len(self.bot.guilds)}
            # async with cs.post(url=f"https://bladebotlist.xyz/api/bots/{self.bot.user.id}/stats", json=data, headers=header) as data:
            #     json = await data.json()
            #     text += f"BladeBot\n{json}"
            header = {"Authorization": os.getenv("discordservices_token")}
            data = {"servers": len(self.bot.guilds), "shards": 0}
            async with cs.post(
                url=f"https://api.discordservices.net/bot/{self.bot.user.id}/stats",
                json=data,
                headers=header,
            ) as data:
                json = await data.json()
                text += f"DiscordServices\n{json}"
            header = {"Authorization": os.getenv("botlist_token")}
            data = {"server_count": len(self.bot.guilds)}
            async with cs.post(
                url=f"https://api.botlist.me/api/v1/bots/{self.bot.user.id}/stats",
                json=data,
                headers=header,
            ) as data:
                json = await data.json()
                text += f"Botlist\n{json}"
        await ctx.send(text)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        await self.voterchannel.send(f"{data}")

    @commands.command(name="gift")
    @commands.is_owner()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def gift(self, ctx, user: discord.User, expiry: str = None):
        """Gifts a user premium."""
        if user.bot or user.id in self.bot.bled:
            return await ctx.reply("They won't get to use it.")
        results = await Database.get_user(self, user.id)
        if expiry:
            settings = {
                "TIMEZONE": "UTC",
                "RETURN_AS_TIMEZONE_AWARE": True,
                "TO_TIMEZONE": "UTC",
                "PREFER_DATES_FROM": "future",
            }
            to_be_passed = f"in {expiry}"
            split = to_be_passed.split(" ")
            length = len(split[:7])
            out = None
            used = ""
            for i in range(length, 0, -1):
                used = " ".join(split[:i])
                out = dateparser.parse(used, settings=settings)
                if out is not None:
                    break
            if not out:
                raise commands.BadArgument("Provided time is invalid")
            now = ctx.message.created_at
            time = out.replace(tzinfo=now.tzinfo), "".join(to_be_passed).replace(
                used, ""
            )
            expiry = round(time[0].timestamp())
            if expiry < discord.utils.utcnow().timestamp() + 86400:
                return await ctx.reply("You might as well don't give.")
        else:
            expiry = True
        if results.get("premium") is True:
            return await ctx.reply("User already has premium.")
        await Database.edit_user(self, user.id, {"premium": expiry})
        e = discord.Embed(
            title="Infinity Premium 👑",
            description=f"{user.mention} received {'Lifetime Premium.' if expiry is True else f'Premium that expires on <t:{expiry}:D>'}",
            color=discord.Color.gold(),
        )
        await ctx.reply(embed=e)
        await self.bot.changes.send(embed=e)

    @commands.command(name="snipe", aliases=["sn"])
    @commands.is_owner()
    async def snipe(self, ctx, channel: TextChannel = None):
        """Snipes the last deleted message of the channel."""
        if not channel:
            channel = ctx.message.channel
        deletedmsg = self.bot.snipedb.get(f"{channel.id}")
        if not deletedmsg:
            await ctx.reply("No cached deleted message.")
        else:
            e = discord.Embed(
                title="Snipe",
                description=deletedmsg.content,
                color=deletedmsg.author.color,
                timestamp=deletedmsg.created_at,
            )
            e.set_author(
                name=f"{deletedmsg.author.name}",
                icon_url=deletedmsg.author.avatar or e.Empty,
            )
            await ctx.reply(embeds=[e] + deletedmsg.embeds)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if not message.content:
            message.content = ""
        for a in message.attachments:
            message.content += f"{a} \n"
        self.bot.snipedb[f"{message.channel.id}"] = message


def setup(bot):
    bot.add_cog(OwnerCog(bot))
