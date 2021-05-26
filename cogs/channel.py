import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime
from discord.ext import commands


class ChannelCog(commands.Cog, name='Channel'):
    """*Channel Commands*"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="first", aliases=["firstmessage", "1"])
    @commands.cooldown(1,8)
    async def first(self, ctx):
        """Gets the first message of the channel."""
        await ctx.trigger_typing()
        meh = await ctx.channel.history(limit=1, oldest_first=True).flatten()
        message = meh[0]
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="First Message", url=message.jump_url, description=f"[Jump]({message.jump_url})\n{message.content}", color=hex_int)
        embed.timestamp = message.created_at
        embed.set_author(icon_url=message.author.avatar_url, name=message.author)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="hide")
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_channels=True)
    async def Hides(self, ctx, *, role:discord.Role=None):
        """Hides a channel for a certain role."""
        if role == None:
            role = ctx.guild.default_role
        overwrite = ctx.channel.overwrites_for(role)
        overwrite.view_channel=False
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** hidden channel for {role.mention}', mention_author=False, allowed_mentions=None)

    @commands.command(name="unhide", aliases=['uh'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_channels=True)
    async def unHide(self, ctx, *, role:discord.Role=None):
        """Unhides a channel for a certain role."""
        if role == None:
            role = ctx.guild.default_role
        overwrite = ctx.channel.overwrites_for(role)
        overwrite.send_messages=True
        overwrite.view_channel=True
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** unhidden channel for {role.mention}', mention_author=False, allowed_mentions=None)

    @commands.command(name="lock", aliases=['cock', 'l'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, *, role:discord.Role=None):
        """Locks a channel for a certain role."""
        if role == None:
            role = ctx.guild.default_role
        overwrite = ctx.channel.overwrites_for(role)
        overwrite.send_messages=False
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** locked channel for {role.mention}', mention_author=False, allowed_mentions=None)

    @commands.command(name="unlock", aliases=['uncock', 'ul'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, *, role:discord.Role=None):
        """Unocks a channel for a certain role."""
        if role == None:
            role = ctx.guild.default_role
        overwrite = ctx.channel.overwrites_for(role)
        overwrite.send_messages=True
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** unlocked channel for {role.mention}', mention_author=False, allowed_mentions=None)

    @commands.command(name="purge", aliases=["cleanup"])
    @commands.cooldown(1,1)
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx,no:int=100):
        """Purges a certain number of messages."""
        def pinc(msg):
            if msg.pinned == True:
                return False
            else:
                return True
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

    @commands.command(name="catdel", aliases=['categorydelete'])
    @commands.cooldown(1,8)
    @commands.has_permissions(administrator=True)
    async def catdel(self,ctx, category:discord.CategoryChannel, *, reason:str=None):
        """Deletes all the channels in the category."""
        channels = category.channels
        for channel in channels:
            await channel.delete(reason=f"Deleted by {ctx.author.name} for {reason}.")
        await category.delete(reason=f"Deleted by {ctx.author.name} for {reason}")

    @commands.command(name="chandel", aliases=['channeldelete'])
    @commands.cooldown(1,8)
    @commands.has_permissions(administrator=True)
    async def chandel(self,ctx, channel:discord.TextChannel, *, reason:str=None):
        """Deletes the channel."""
        await channel.delete(reason=f"Deleted by {ctx.author.name} for {reason}.")

    @commands.command(name="purgeallchannel")
    @commands.cooldown(1,8)
    @commands.has_permissions(administrator=True)
    async def purgeallchannel(self,ctx):
        """Deletes all the channels."""
        if ctx.author != ctx.guild.owner:
            await ctx.reply("You are not server owner.")
            return
        channels = ctx.guild.channels
        for channel in channels:
            try:
                await channel.delete(reason=f"Deleted by {ctx.author.name}.")
            except:
                pass

    @commands.command(name="muteoverwrites", aliases=['mo'])
    @commands.cooldown(1,6)
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx, muterole:discord.Role):
        """Updates mute role's perms for the whole server.."""
        overwrite = ctx.channel.overwrites_for(muterole)
        overwrite.send_messages=False
        channels = ctx.guild.channels
        categories = ctx.guild.categories
        for channel in channels:
            try:
                await channel.set_permissions(muterole, overwrite=overwrite)
            except:
                pass
        for category in categories:
            try:
                await category.set_permissions(muterole, overwrite=overwrite)
            except:
                pass
        await ctx.send("`DONE`")

def setup(bot):
    bot.add_cog(ChannelCog(bot))