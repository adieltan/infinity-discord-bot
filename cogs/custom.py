import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math
from discord.ext import commands


class customCog(commands.Cog, name='custom'):
    """*Custom commands for server.*"""
    def __init__(self, bot):
        self.bot = bot

    def rhserver():
        def predicate(ctx):
            return ctx.guild.id==709711335436451901
        return commands.check(predicate)

    @commands.command(name="heist")
    @rhserver()
    @commands.cooldown(1,18)
    async def heist(self, ctx, amount: float, sponsor: discord.Member):
        """Gets people ready for a heist."""






def setup(bot):
    bot.add_cog(customCog(bot))