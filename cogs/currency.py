import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime, requests
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://rh:1234@infinitycluster.yupj9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["infinity"]["wealth"]

class CurrencyCog(commands.Cog, name='Currency'):
    """*Currency Commands*"""
    def __init__(self, bot):
        self.bot = bot
        self.db = db
        


def setup(bot):
    bot.add_cog(CurrencyCog(bot))