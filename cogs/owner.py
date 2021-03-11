import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, requests, inspect
from discord.ext.commands.errors import TooManyArguments
from discord.ext import commands, tasks


class OwnerCog(commands.Cog, name='Owner'):
    """*Only owner can use this.*"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='reload')
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}', mention_author=False)
        else:
            await ctx.reply(f'**`SUCCESSFULLY`** *reloaded* __{cog}__', mention_author=False)

    @commands.command(name='unload')
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}', mention_author=False)
        else:
            await ctx.reply(f'**`SUCCESSFULLY`** *unloaded* __{cog}__', mention_author=False)

    @commands.command(name='load')
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}', mention_author=False)
        else:
            await ctx.reply(f'**`SUCCESSFULLY`** *loaded* __{cog}__', mention_author=False)

    @commands.command(name='eval', aliases=['ev'])
    @commands.is_owner()
    async def eval(self, ctx, *, command):
        """Evaluate"""
        res = eval(command)
        if inspect.isawaitable(res):
            await ctx.reply(await res, mention_author=False)
        else:
            await ctx.reply(res, mention_author=False)


'''blacklisted = {''}

    @bot.check
    def blacklistedguys(ctx):
        if ctx.author.id in blacklisted:
            return False
        else:
            return True

    @bot.command(name='blacklistadd', aliases=['bla', 'blacklist', 'bl'])
    @commands.is_owner()
    async def bla(ctx, *, member: discord.Member=None):
        """Command to blacklist a user."""
        if member is None:
            return
        blacklisted.add(member.id)
        await ctx.reply(f'<@{ctx.author.id}>\n***SUCESSFULLY BLACKLISTED {member}***', mention_author=False)

    @bot.command(name='blacklistremove', aliases=['blr', 'unblacklist'])
    @commands.is_owner()
    async def blr(ctx, *, member: discord.Member=None):
        """Command to unblacklist a user."""
        if member is None:
            return
        blacklisted.discard(member.id)
        await ctx.reply(f'<@{ctx.author.id}>\n***SUCESSFULLY UNBLACKLISTED {member}***', mention_author=False)

    @bot.command(name='blacklistlist', aliases=['bll'])
    @commands.is_owner()
    async def bll(ctx):
        """Show blacklisted users."""
        await ctx.send(f'<@{ctx.author.id}>')
        await ctx.reply(blacklisted, mention_author=False)'''

def setup(bot):
    bot.add_cog(OwnerCog(bot))