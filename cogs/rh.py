import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math
from discord.ext import commands


class rhCog(commands.Cog, name='rh'):
    """*Commands specially for RH server.*"""
    def __init__(self, bot):
        self.bot = bot
    
#    @commands.cog_check()
#    def servercheck(ctx):
#        if ctx.guild.id==709711335436451901:
#            pass
#        else:
#            return

    @commands.command(name="heist")
    @commands.cooldown(1,180)
    async def heist(self, ctx, amount: float, sponsor: discord.Member):
        """Gets people ready for a heist."""






def setup(bot):
    bot.add_cog(rhCog(bot))