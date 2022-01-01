import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, re, aiohttp, typing
from discord.ext import commands, tasks

from thefuzz import process
import collections

from ._utils import Confirm, server, supporter
from .custom import DropdownRoles

class PersistantCog(commands.Cog, name='Persistant'):
    """Persistant stuff."""
    def __init__(self, bot):
        self.bot = bot
        self.COG_EMOJI = '🛅'

    @commands.Cog.listener()
    async def on_ready(self):
        """Loads the persistant stuff."""
        if not self.bot.persistent_views_added:
            self.bot.add_view(DropdownRoles())
            self.bot.persistent_views_added = True

def setup(bot):
    bot.add_cog(PersistantCog(bot))