import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, 
import matplotlib.pyplot as plt


class MusicCog(commands.Cog, name='music'):
    """*Musical commands.*"""

    def __init__(self, bot):
        self.bot = bot
    

def setup(bot):
    bot.add_cog(MusicCog(bot))