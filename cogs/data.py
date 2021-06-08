import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime, requests, urllib, aiohttp, re
from discord.ext import commands

class DataCog(commands.Cog, name='Data'):
    """*Data from websites or api*"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="youtube", aliases=['yt'])
    async def youtube(self, ctx, *, search:str):
        pass

def setup(bot):
    bot.add_cog(DataCog(bot))