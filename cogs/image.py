import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math
from discord.ext import commands


class ImageCog(commands.Cog, name='Image'):
    """*Image Generation.*"""
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(ImageCog(bot))