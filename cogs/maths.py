import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math
from discord.ext import commands
from py_expression_eval import Parser
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
        await ctx.reply(f'Greatest common divisor of {input} and {input2}:\n***{output}***', mention_author=True)

    @commands.command(name= 'binary', aliases=['bin'])
    @commands.cooldown(1,5)
    async def bin (self, ctx, input:int):
        """Find the binary form of an integer"""
        output = bin(input)
        await ctx.reply(f'Binary form of {input}:\n***{output}***', mention_author=True)

    @commands.command(name= 'hexadecimal', aliases=['hex'])
    @commands.cooldown(1,5)
    async def hex (self, ctx, input:int):
        """Find the hexadecimal form of an integer"""
        output = hex(input)
        await ctx.reply(f'Hexadecimal form of {input}:\n***{output}***', mention_author=True)

    @commands.command(name= 'octaldecimal', aliases=['oct'])
    @commands.cooldown(1,5)
    async def oct (self, ctx, input:int):
        """Find the octaldecimal of an integer"""
        output = oct(input)
        await ctx.reply(f'Octaldecimal form of {input}:\n***{output}***', mention_author=True)

    @commands.command(name='calc')
    @commands.cooldown(1,3)
    async def calc (self, ctx, *, input):
        """Evaluates a maths equation."""
        out = parser.parse(input).evaluate({})
        formatted = format(out, ',')
        await ctx.reply(f'```json\n{input} = \n{out}\nFormatted: {formatted}```', mention_author=True)

    @commands.command(name='calchelp')
    @commands.cooldown(1,2)
    async def calchelp (self, ctx):
        """Shows help on the `calc` command."""
        embed=discord.Embed(title="Calc Help", description="Usable expressions\n `+` `-` `*` `/` `%` `^` `PI` `E` `sin(x)` `cos(x)` `tan(x)` `asin(x)` `acos(x)` `atan(x)` `log(x)` `log(x, base)` `abs(x)` `ceil(x)` `floor(x)` `round(x)` `exp(x)` `and` `or` `xor` `not` `in`") 
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.reply(embed=embed, mention_author=True)


def setup(bot):
    bot.add_cog(MathsCog(bot))