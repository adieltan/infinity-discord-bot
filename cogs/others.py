import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime, requests
from discord.ext import commands


class OthersCog(commands.Cog, name='Others'):
    """*Other Commands*"""
    def __init__(self, bot):
        self.bot = bot
        


def setup(bot):
    bot.add_cog(OthersCog(bot))