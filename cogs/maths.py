import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math
from discord.ext import commands
from py_expression_eval import Parser
parser = Parser()

class MathsCog(commands.Cog, name='Maths'):
    """*Maths commands.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name= 'tax', aliases=['taxchart','dmctaxchart'])
    @commands.cooldown(1,2)
    async def taxchart(self, ctx):
        """Dank Memer Tax Chart"""
        await ctx.send("```1 - 25,000           | 0%\n25,001 - 50,000      | 1%\n50,001 - 100,000     | 3%\n100,001 - 749,999    | 5%\n750,000 - 2,499,999  | 8%\n2,500,000+           | 15%```")

    @commands.command(name= 'tc', aliases=['dmt', 'taxcalc', 'taxcalculator', 'dmtc'])
    @commands.cooldown(1,5)
    async def tax(self, ctx, amount:float):
        """Dank Memer Tax Calculator."""
        if amount < 25_001:
            tax = 0.00
        elif amount < 49_500:
            tax = 0.01
        elif amount < 97_000:
            tax = 0.03
        elif amount < 712_500:
            tax = 0.05
        elif amount < 2_300_000:
            tax = 0.08
        elif amount > 2_299_999:
            tax = 0.15
        hex_int = random.randint(0,16777215)
        #calculations
        #abt= amount before tax ; atpwt = amount to pay with tax
        abt = format(round(amount), ',')
        taxrate = round(tax*100)
        atpwtwf = round(amount/(1-tax))
        atpwt = format(round(amount/(1-tax)), ',')
        taxamount = format(round(amount/(1-tax)-amount), ',')
        embed = discord.Embed(title=f"Dank Memer Tax Calculator",description=f"Amount Entered: ⏣{abt}\nTax Rate: {taxrate}%\n Amount to Pay (with tax): ⏣{atpwt}\n Tax Amount: ⏣{taxamount}" , color=hex_int)
        embed.set_author(icon_url=ctx.author.avatar_url, name=str(ctx.author))
        embed.set_footer(text=atpwtwf)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/discords-bots/images/d/d7/Dank_Memer-1.png/revision/latest?cb=20200510093229")
        await ctx.reply(embed=embed, mention_author=True)

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
        await ctx.reply(f'```{input} = \n{out}\nFormatted: {formatted}```', mention_author=True)

    @commands.command(name='calchelp')
    @commands.cooldown(1,2)
    async def calchelp (self, ctx):
        """Shows help on the `calc` command."""
        embed=discord.Embed(title="Calc Help", description="Usable expressions\n `+` `-` `*` `/` `%` `^` `PI` `E` `sin(x)` `cos(x)` `tan(x)` `asin(x)` `acos(x)` `atan(x)` `log(x)` `log(x, base)` `abs(x)` `ceil(x)` `floor(x)` `round(x)` `exp(x)` `and` `or` `xor` `not` `in`") 
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.reply(embed=embed, mention_author=True)


def setup(bot):
    bot.add_cog(MathsCog(bot))