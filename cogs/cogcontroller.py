import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing, traceback
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, 
import matplotlib.pyplot as plt
 



class CogControllerCog(commands.Cog, name='CogController'):
    """*Cog that won't fail in updates.*"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='reload', aliases=['load', 'rl'])
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Command which Reloads/loads a Module."""
        cog="cogs." + cog.removeprefix("cogs.")
        try:
            try:
                self.bot.reload_extension(cog)
            except commands.errors.ExtensionNotLoaded:
                self.bot.load_extension(cog)
        except Exception as e:
            await ctx.reply(embed=discord.Embed(title=f'**`ERROR:`** {type(e).__name__}', description=traceback.format_exc(), mention_author=False))
        else:
            await ctx.reply(f'**`SUCCESSFULLY`** *(re)loaded* __{cog}__', mention_author=False)

    @commands.command(name='unload')
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Unloads a Module."""
        cog="cogs." + cog.removeprefix("cogs.")
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.reply(embed=discord.Embed(title=f'**`ERROR:`** {type(e).__name__}', description=traceback.format_exc(), mention_author=False))
        else:
            await ctx.reply(f'**`SUCCESSFULLY`** *unloaded* __{cog}__', mention_author=False)

def setup(bot):
    bot.add_cog(CogControllerCog(bot))