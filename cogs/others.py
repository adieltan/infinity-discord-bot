import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 


class OthersCog(commands.Cog, name='Others'):
    """*Other Commands*"""
    def __init__(self, bot):
        self.bot = bot
        


def setup(bot):
    bot.add_cog(OthersCog(bot))