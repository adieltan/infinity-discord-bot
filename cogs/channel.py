import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime
from discord.ext import commands


class ChannelCog(commands.Cog, name='Channe;'):
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

    @commands.command(name="lock", aliases=['cock', 'l'])
    @commands.cooldown(1,3)
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, *, role:discord.Role=None):
        """Locks a channel for a certain role."""
        if role == None:
            role = ctx.guild.default_role
        await ctx.channel.set_permissions(role, send_messages=False)
        await ctx.reply(f'**`SUCCESSFULLY`** locked channel for {role.mention}', mention_author=False, allowed_mentions=None)

    @commands.command(name="unlock", aliases=['uncock', 'ul'])
    @commands.cooldown(1,3)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, *, role:discord.Role=None):
        """Unocks a channel for a certain role."""
        if role == None:
            role = ctx.guild.default_role
        await ctx.channel.set_permissions(role, send_messages=True)
        await ctx.reply(f'**`SUCCESSFULLY`** unlocked channel for {role.mention}', mention_author=False, allowed_mentions=None)

def setup(bot):
    bot.add_cog(ChannelCog(bot))