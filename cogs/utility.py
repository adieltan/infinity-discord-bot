import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime, dateparser, motor.motor_asyncio, re
from discord.ext import commands


class utilityCog(commands.Cog, name='utility'):
    """*Utility commands for server.*"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='time')
    @commands.cooldown(1,2)
    async def time(self, ctx, *, expression:str): 
        """Time."""
        user_input = expression
        settings = {
            'TIMEZONE': 'UTC',
            'RETURN_AS_TIMEZONE_AWARE': True,
            'TO_TIMEZONE': 'UTC',
            'PREFER_DATES_FROM': 'future'
        }

        to_be_passed = f"in {user_input}"
        split = to_be_passed.split(" ")
        length = len(split[:7])
        out = None
        used = ""
        for i in range(length, 0, -1):
            used = " ".join(split[:i])
            out = dateparser.parse(used, settings=settings)
            if out is not None:
                break

        if out is None:
            raise commands.BadArgument('Provided time is invalid')

        now = ctx.message.created_at
        time = out.replace(tzinfo=now.tzinfo), ''.join(to_be_passed).replace(used, '')
        embed=discord.Embed(title="Time", description=expression)
        embed.timestamp=time[0]
        try:
            ts = time[0].timestamp()
        except:
            pass
        try:
            embed.set_footer(text=ts)
        except:
            pass
        await ctx.reply(time[0],embed=embed)

    @commands.command(name='creationdate', aliases=['createdate', 'created'])
    @commands.cooldown(1,2)
    async def created(self, ctx, argument:str): 
        """Time the snowflake id was created."""
        arg = int(re.sub("[^0-9]", "", argument))
        time = discord.utils.snowflake_time(arg)
        embed=discord.Embed(title="Creation Date Checker", description=argument)
        embed.timestamp=time
        try:
            ts = time.timestamp()
        except:
            pass
        try:
            embed.set_footer(text=ts)
        except:
            pass
        await ctx.reply(time,embed=embed)


def setup(bot):
    bot.add_cog(utilityCog(bot))