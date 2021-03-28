import discord, random, string, os, logging, asyncio, discord.voice_client, sys, traceback, json, pymongo, datetime
from discord.enums import NotificationLevel
from pymongo import MongoClient
from discord.ext import commands
from discord.guild import Guild

cluster = MongoClient("mongodb+srv://rh:1234@infinitycluster.yupj9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["infinity"]
col=db["server"]

class ModerationCog(commands.Cog, name='Moderation'):
    """*Moderation Commands.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prefix')
    @commands.cooldown(1,100)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, apref:str=None):
        """Changes the prefix for the bot in the server."""
        if apref is None:
            results= col.find_one({"_id":ctx.guild.id})
            pref = results["prefix"]
            await ctx.reply(f"The prefix for {ctx.guild.name} is `{pref}`", mention_author=False)
            pass
        elif len(apref) > 5:
            await ctx.reply("You can't have such a long prefix.", mention_author=False)
            pass
        else:
            #col.replace_one({"_id":ctx.guild.id}, {"$set":{"prefix":f"{apref}"}})
            col.replace_one({"_id":ctx.guild.id}, {"prefix":apref})
            await ctx.reply(f'Prefix changed to: {apref}', mention_author=False)
            name=f'[{apref}] Infinity'
            member=ctx.guild.get_member(732917262297595925)
            await member.edit(nick=name)
        

    @commands.command(name='ban')
    @commands.cooldown(1,5)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a user."""
        if member == None or member == ctx.message.author:
            await ctx.channel.reply("You cannot ban yourself", mention_author=False)
        else:
            message = f"You have been banned from {ctx.guild.name} for {reason}"
            await member.send(message)
            await ctx.guild.ban(member, reason=reason)
            await ctx.reply(f'**{member}** was ***BANNED***\nReason: __{reason}__', mention_author=False)
        
    @commands.command(name='kick')
    @commands.cooldown(1,5)
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a user."""
        if member == None or member == ctx.message.author:
            await ctx.channel.reply("You cannot kick yourself", mention_author=False)
        else:
            message = f"You have been kicked from {ctx.guild.name} for {reason}"
            await member.send(message)
            await ctx.guild.kick(member, reason=reason)
            await ctx.reply(f'**{member}** was ***KICKED***\nReason: __{reason}__', mention_author=False)

def setup(bot):
    bot.add_cog(ModerationCog(bot))