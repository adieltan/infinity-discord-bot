import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
from dotenv import load_dotenv

class DataCog(commands.Cog, name='Data'):
    """*Data from websites or api*"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="youtube", aliases=['yt'])
    async def youtube(self, ctx, *, search:str):
        pass

def setup(bot):
    bot.add_cog(DataCog(bot))