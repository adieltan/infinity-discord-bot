import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing, traceback
from discord.ext import commands, tasks

class CogControllerCog(commands.Cog, name='CogController'):
    """*Cog that won't fail in updates.*"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='reload', aliases=['load', 'rl'], hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str=None):
        """Command which Reloads/loads a Module."""
        
        def load_reload(cog):
            cog="cogs." + cog.removeprefix("cogs.")
            try:
                self.bot.reload_extension(cog)
                return f"<a:verified:876075132114829342> (re)loaded `{cog}`"
            except:
                try:
                    self.bot.load_extension(cog)
                    return f"<a:verified:876075132114829342> (re)loaded `{cog}`"
                except:
                    try:
                        cog=cog.removeprefix("cogs.")
                        self.bot.reload_extension(cog)
                        return f"<a:verified:876075132114829342> (re)loaded `{cog}`"
                    except:
                        try:
                            self.bot.load_extension(cog)
                            return f"<a:verified:876075132114829342> (re)loaded `{cog}`"
                        except:
                            return f"<:exclamation:876077084986966016> Error while loading `{cog}`\n```\n{traceback.format_exc()}\n```"

        if cog is None:
            cogs = []
            load_reload('jishaku')
            if '\\' in os.path.dirname(os.path.abspath(__file__)):
                slash = '\\'
            else: slash = '/'
            for filename in os.listdir(os.path.dirname(os.path.abspath(__file__))+slash):
                if filename.endswith(".py"):
                    cogs.append(load_reload(filename[:-3]))
            await ctx.reply('\n'.join(cogs))
        else:
            await ctx.reply(load_reload(cog))

    @commands.command(name='unload', hidden=True)
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