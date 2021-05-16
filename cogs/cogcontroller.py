import discord, random, string, os, logging, asyncio, discord.voice_client
from discord.ext.commands.errors import ExtensionNotLoaded, TooManyArguments
from discord.ext import commands, tasks



class CogControllerCog(commands.Cog, name='CogController'):
    """*Cog that won't fail in updates.*"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='reload', aliases=['load'])
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Command which Reloads/loads a Module."""
        cog="cogs." + cog.removeprefix("cogs.")
        try:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except ExtensionNotLoaded:
                self.bot.load_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}', mention_author=False)
        else:
            await ctx.reply(f'**`SUCCESSFULLY`** *reloaded* __{cog}__', mention_author=False)

    @commands.command(name='unload')
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        cog="cogs." + cog.removeprefix("cogs.")
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}', mention_author=False)
        else:
            await ctx.reply(f'**`SUCCESSFULLY`** *unloaded* __{cog}__', mention_author=False)

def setup(bot):
    bot.add_cog(CogControllerCog(bot))