import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 


class ChannelCog(commands.Cog, name='Channel'):
    """*Channel Commands*"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="snipe", aliases=["sn"])
    @commands.cooldown(1,4)
    async def snipe(self, ctx, channel:discord.TextChannel=None):
        """Snipes the last deleted message of the channel."""
        if channel is None:
            channel = ctx.message.channel
        deletedmsg = self.bot.snipedb.get(f"{channel.id}")
        if deletedmsg is None:
            await ctx.reply(f"No cached deleted message.")
        else:
            embed=discord.Embed(title="Snipe", description=deletedmsg.content, color=deletedmsg.author.color, timestamp=deletedmsg.created_at)
            embed.set_author(name=f"{deletedmsg.author.name}", icon_url=deletedmsg.author.avatar_url)

            await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message:discord.Message):
        self.bot.snipedb[f"{message.channel.id}"]= message

    @commands.command(name="first", aliases=["firstmessage", "1"])
    @commands.cooldown(1,8)
    async def first(self, ctx):
        """Gets the first message of the channel."""
        await ctx.trigger_typing()
        meh = await ctx.channel.history(limit=1, oldest_first=True).flatten()
        message = meh[0]
        
        embed=discord.Embed(title="First Message", url=message.jump_url, description=f"[Jump]({message.jump_url})\n{message.content}", color=discord.Color.random())
        embed.timestamp = message.created_at
        embed.set_author(icon_url=message.author.avatar_url, name=message.author)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="hide")
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def Hides(self, ctx, *, arg:str=None):
        """Hides a channel for a certain role / channel / user."""
        try:    argid = int(re.sub("[^0-9]", "", arg))
        except:   argid=0
        role = discord.utils.get(ctx.guild.roles, name=arg) or discord.utils.get(ctx.guild.roles, id=argid) or discord.utils.get(ctx.guild.members, name=arg) or discord.utils.get(ctx.guild.members, id=argid)
        channel = discord.utils.get(ctx.guild.channels, name=arg) or discord.utils.get(ctx.guild.channels, id=arg)
        if role == None:
            role = ctx.guild.default_role
        if channel == None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.view_channel=False
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** hidden {channel.mention} for {role.mention}', mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="unhide", aliases=['uh'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_permissions=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def unHide(self, ctx, *, arg:str=None):
        """Unhides a channel for a certain role / channel / user."""
        try:    argid = int(re.sub("[^0-9]", "", arg))
        except:   argid=0
        role = discord.utils.get(ctx.guild.roles, name=arg) or discord.utils.get(ctx.guild.roles, id=argid) or discord.utils.get(ctx.guild.members, name=arg) or discord.utils.get(ctx.guild.members, id=argid)
        channel = discord.utils.get(ctx.guild.channels, name=arg) or discord.utils.get(ctx.guild.channels, id=arg)
        if role == None:
            role = ctx.guild.default_role
        if channel == None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.view_channel=True
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** unhidden {channel.mention} for {role.mention}', mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="lock", aliases=['cock', 'l'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_permissions=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def lock(self, ctx, *, arg:str=None):
        """Locks a channel for a certain role / channel / user."""
        try:    argid = int(re.sub("[^0-9]", "", arg))
        except:   argid=0
        role = discord.utils.get(ctx.guild.roles, name=arg) or discord.utils.get(ctx.guild.roles, id=argid) or discord.utils.get(ctx.guild.members, name=arg) or discord.utils.get(ctx.guild.members, id=argid)
        channel = discord.utils.get(ctx.guild.channels, name=arg) or discord.utils.get(ctx.guild.channels, id=arg)
        if role == None:
            role = ctx.guild.default_role
        if channel == None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages=False
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** locked {channel.mention} for {role.mention}', mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="unlock", aliases=['uncock', 'ul'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_permissions=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def unlock(self, ctx, *, arg:str=None):
        """Unhides a channel for a certain role / channel / user."""
        try:    argid = int(re.sub("[^0-9]", "", arg))
        except:   argid=0
        role = discord.utils.get(ctx.guild.roles, name=arg) or discord.utils.get(ctx.guild.roles, id=argid) or discord.utils.get(ctx.guild.members, name=arg) or discord.utils.get(ctx.guild.members, id=argid)
        channel = discord.utils.get(ctx.guild.channels, name=arg) or discord.utils.get(ctx.guild.channels, id=arg)
        if role == None:
            role = ctx.guild.default_role
        if channel == None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages=True
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** unlocked {channel.mention} for {role.mention}', mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="export")
    @commands.cooldown(1,40, BucketType.category)
    @commands.has_permissions(administrator=True)
    async def export(self, ctx, destination, limit:int=None):
        """Exports chat messages to another channel."""
        channelid = int(re.sub("[^0-9]", "", destination))
        destination_channel = self.bot.get_channel(channelid)
        presentwebhooks = await destination_channel.webhooks() or []
        if len(presentwebhooks) > 0:
            webhook = presentwebhooks[0]
        else:
            webhook = await destination_channel.create_webhook(name="Export")
        messagestop = await ctx.channel.history(limit=limit).flatten()
        messagestop.reverse()
        await ctx.send(f"Estimated time: {len(messagestop)} seconds.")
        for m in messagestop:
            try:m.files
            except:files = None
            else:files = m.files
            try:m.embeds
            except:embeds = None
            else:embeds = m.embeds
            try:m.clean_content
            except:content = None
            else:content = m.clean_content
            await webhook.send(content=content, username=m.author.name, avatar_url=m.author.avatar_url, files=files, embeds=embeds, allowed_mentions=discord.AllowedMentions.none())
        await ctx.reply("Done")

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self,ctx, no:int=100):
        """Purges a number of messages."""
        def pinc(msg):
            if msg.pinned:
                return False
            else:
                return True
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)
    
    @purge.command()
    async def user(self, ctx, user:discord.Member, no:int=100):
        """Purges messages from a user."""
        def pinc(msg):
            if msg.author == user:
                return True
            else:
                return False
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)

    @purge.command()
    async def pins(self, ctx, no:int=100):
        """Purges a number of pinned messages."""
        def pinc(msg):
            if msg.pinned:
                return True
            else:
                return False
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)

    @purge.command()
    async def bot(self, ctx, no:int=100):
        """Purges messages from bots."""
        def pinc(msg):
            if msg.author.bot == True:
                return True
            else:
                return False
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)

    @commands.command(name="slowmode", aliases=["sm"])
    @commands.cooldown(1,3)
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self,ctx,seconds:int=0):
        """Sets the slowmode for the channel."""
        if seconds < 0:
            seconds = seconds *-1
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.reply(f"The slowmode delay for this channel is now {seconds} seconds!")

    @commands.command(name="raw")
    async def raw(self, ctx):
        """Sends the raw message that you referred."""
        ref = ctx.message.reference
        if ref == None:
            await ctx.reply("Eh you gotta reply to the message you wanna see!", mention_author=True)
        else:
            message = await ctx.channel.fetch_message(ref.message_id)
            await ctx.reply(f"```\n{message}\n```")

    @commands.command(name="attachments", aliases=['attachment'])
    async def attachments(self, ctx, channelid_or_messageid:str=None):
        """Gets the url of all the attachments in the message referenced."""
        ref = ctx.message.reference
        msg = None
        if channelid_or_messageid is None and ref is not None:
            msg = await ctx.channel.fetch_message(ref.message_id)
        elif channelid_or_messageid is None and ref is None:
            await ctx.reply(f"You have to reply to or provide the message id to the message.")
        else:
            ids = re.findall("\d{18}", channelid_or_messageid)
            if len(ids) < 1:
                await ctx.reply(f"Can't find id.")
            elif len(ids) < 2:
                msg = await ctx.channel.fetch_message(int(ids[0]))
            elif len(ids) < 3:
                channel = ctx.guild.get_channel(int(ids[0]))
                msg = await channel.fetch_message(int(ids[1]))
            elif len(ids) <4:
                channel = ctx.guild.get_channel(int(ids[1]))
                msg = await channel.fetch_message(int(ids[2]))
        if msg:
            text = f"Message: {msg.jump_url}\nAttachments:\n"
            attachments = msg.attachments
            for attachment in attachments:
                text += str(attachment)  + '\n'
            await ctx.reply(text)


def setup(bot):
    bot.add_cog(ChannelCog(bot))