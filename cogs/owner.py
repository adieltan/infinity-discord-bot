import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, requests, inspect
from discord.ext.commands.errors import ExtensionNotLoaded, TooManyArguments
from discord.ext import commands, tasks


class OwnerCog(commands.Cog, name='Owner'):
    """*Only owner can use this.*"""
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

    @commands.command(name='eval', aliases=['e'])
    @commands.is_owner()
    async def eval(self, ctx, *, command):
        """Evaluate"""
        res = eval(command)
        if inspect.isawaitable(res):
            await ctx.reply(await res, mention_author=False)
        else:
            await ctx.reply(res, mention_author=False)

    @commands.command(name='logout', aliases=['shutdown', 'gosleep'])
    @commands.is_owner()
    async def logout(self, ctx):
        """Logs out."""
        await ctx.reply("👋")
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type= discord.ActivityType.playing, name="with the exit door."))
        await asyncio.sleep(8)
        await self.bot.logout()

    @commands.command(name="spam")
    @commands.is_owner()
    async def spam(self, ctx, number:int=100):
        """Spams the channel."""
        strings = string.ascii_lowercase + string.ascii_uppercase + string.digits
        for _ in range(1,number):
            no = "".join(random.choice(strings) for _ in range(1,10))
            await ctx.send(no)
        await ctx.send("Done")


def setup(bot):
    bot.add_cog(OwnerCog(bot))