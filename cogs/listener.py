import discord, random, string, os, logging, asyncio, discord.voice_client, sys, traceback, json, datetime
from discord.ext.commands.errors import CheckFailure
from discord.ext import commands, tasks
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://rh:1234@infinitycluster.yupj9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["infinity"]
col=db["server"]

class ListenerCog(commands.Cog, name='Listener'):
    """*Listening Commands.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message (self, message: discord.Message):
        if message.author.bot == True:
            return
        elif message.author == self.bot.user:
            return
        elif ('*f*') in message.content.lower():
            await message.add_reaction("a:f_:819009528204099624")
            pass
        elif ("701009836938231849") in message.content.lower():
            emoji =["a:heartgif:813391491552641044"]
            for emj in emoji:
                await message.add_reaction(emj)
        elif ("732917262297595925") in message.content.lower():
            await message.add_reaction("♾️")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        changes = self.bot.get_channel(859779506038505532)
        embed=discord.Embed(title="Guild Join", description=f"Owner: {guild.owner.mention}\nMember Count: {guild.member_count}")
        embed.set_author(name=guild.name, icon_url=guild.icon)
        await changes.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        changes = self.bot.get_channel(859779506038505532)
        embed=discord.Embed(title="Guild Leave", description=f"Owner: {guild.owner.mention}\nMember Count: {guild.member_count}")
        embed.set_author(name=guild.name, icon_url=guild.icon)
        await changes.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error (self, ctx, error):
        er = str(error)
        #skips wrong command
        if ("is not found") in er:
            return
        elif ("check functions for command") in er:
            return
        else:
            await ctx.reply(er, mention_author=False)

        if ("cooldown") in er:
            return
        elif ("not found") in er:
            return
        elif ("failed for parameter") in er:
            return
        elif ("is a required argument that is missing.") in er:
            return
        elif ("You do not own this bot.") in er:
            return
        elif ("permission(s) to run this command.") in er:
            return
        else:
            reports = self.bot.get_channel(825900714013360199)
            
            embed=discord.Embed(title="Error", description=f"{ctx.author.mention}\n{er}", color=discord.Color.random())
            embed.timestamp=datetime.datetime.utcnow()
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=ctx.author.id)
            embed.add_field(name="Info", value=f"{ctx.channel.mention}\n[{ctx.message.content}]({ctx.message.jump_url})")
            await reports.send(embed=embed)

def setup(bot):
    bot.add_cog(ListenerCog(bot))