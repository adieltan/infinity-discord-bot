import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 
from py_expression_eval import Parser
from fractions import Fraction
parser = Parser()

class MathsCog(commands.Cog, name='Maths'):
    """*Maths commands.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name= 'greatestcommondivisor', aliases=['gcd'])
    @commands.cooldown(1,5)
    async def gcd (self, ctx, input:int, input2:int):
        """Find the greatest common divisor of the two integers"""
        output = math.gcd(input, input2)
        await ctx.reply(f'Greatest common divisor of {input} and {input2}:\n***{output}***', mention_author=False)

    @commands.command(name='calc', aliases=['c', '='])
    @commands.cooldown(1,2)
    async def calc (self, ctx, *, input):
        """Evaluates a maths equation."""
        inp = input.replace(",", "")
        try:
            out = parser.parse(inp).evaluate({})
            formatted = format(out, ',')
            floated = "{:e}".format(out)
            frac = Fraction(out).limit_denominator()
            await ctx.reply(f'```json\n{input} = \n{out}\n```Formatted : **{formatted}**\nSci               : **{floated}**\nFraction     : **{frac}**', mention_author=False)
            
        except:
            embed=discord.Embed(title="Calc Help", description="Usable expressions\n `+` `-` `*` `/` `%` `^` `PI` `E` `sin(x)` `cos(x)` `tan(x)` `asin(x)` `acos(x)` `atan(x)` `log(x)` `log(x, base)` `abs(x)` `ceil(x)` `floor(x)` `round(x)` `exp(x)` `and` `or` `xor` `not` `in`") 
            embed.set_footer(text=f'Requested by {ctx.author}')
            await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(MathsCog(bot))