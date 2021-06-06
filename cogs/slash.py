import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://rh:1234@infinitycluster.yupj9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["infinity"]
col=db["server"]

class SlashCog(commands.Cog, name='Slash'):
    """*Slash Commands*"""
    def __init__(self, bot):
        self.bot = bot
        
def setup(bot):
    bot.add_cog(SlashCog(bot))