import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math
from discord.ext import commands
from pymongo import MongoClient
from discord_slash import cog_ext, SlashContext

cluster = MongoClient("mongodb+srv://rh:1234@infinitycluster.yupj9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["infinity"]
col=db["server"]

class SlashCog(commands.Cog, name='Slash'):
    """*Slash Commands*"""
    def __init__(self, bot):
        self.bot = bot
        
    @cog_ext.cog_slash(name="prefix")
    async def prefix(self, ctx: SlashContext):
        def prefix():
            if col.count_documents({"_id":ctx.guild.id}) > 0:
                results= col.find_one({"_id":ctx.guild.id})
                pref = results["prefix"]
                yield pref
            else:
                col.insert_one({"_id":ctx.guild.id, "prefix": "="})
                pass
        text = f"The prefix for {ctx.guild.name} is {prefix()}"
        await ctx.send(text=text)
def setup(bot):
    bot.add_cog(SlashCog(bot))