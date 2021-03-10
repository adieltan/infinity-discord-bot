import discord, random, string, asyncio, discord.voice_client
from discord import message
from discord.ext import commands, tasks

class FunCog(commands.Cog, name='Fun'):
    """*Fun commands.*"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name= 'roll', aliases=['dice', 'throw'])
    @commands.cooldown(1,5)
    async def roll(self, ctx, number_of_dice:int, number_of_sides:int):
        """Randomly rolls dices. [number_of_dice] cannot be higher than 25."""
        if number_of_dice > 25: 
            await ctx.send(f"*number_of_dice* cannot be over 25.\nYour input: **{number_of_dice}**")
            return
        hex_int = random.randint(0,16777215)
        embed = discord.Embed(title=f"{ctx.author}'s Rolling Game", color=hex_int)
        embed.set_author(icon_url=ctx.author.avatar_url, name=str(ctx.author))
        for _ in range(number_of_dice):
            embed.add_field(name='\uFEFF', value=f'{random.choice(range(1,number_of_sides + 1))}', inline=True)
        await ctx.reply(embed=embed, mention_author=True)

    @commands.command()
    @commands.cooldown(1,5)
    async def choose(self, ctx, choice1, choice2):
        """Randomly helps you choose one between two choices."""
        cho=choice1, choice2
        ran=random.choice(cho)
        msg = await ctx.reply(f'(*&^{choice1}%$^$#%%^&{choice2}**&(#&$&#^&))', mention_author=True)
        await asyncio.sleep(1.0)
        await msg.edit(content=f'I choose **{ran}**')

    @commands.command()
    @commands.cooldown(1,5)
    async def gift(self, ctx):
        """Generates few alphanumeric letters to join to become a discord gift code. You are VERY lucky if you managed to get one."""
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits)for _ in range(16)))
        await ctx.reply('discord.gift/' + result_str, mention_author=True)

    @commands.command(name='type', aliases=['say'])
    @commands.cooldown(1,3)
    async def send(self, ctx, member: discord.Member=None, *args):
        """Gets the bot to repeat after you. Isn't that cool?"""
        if not member:
            member = ctx.author
        hex_int = random.randint(0,16777215)
        mes=" ".join(args)
        embed=discord.Embed(title='SECRET MESSAGE', color=hex_int)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.add_field(name="\uFEFF", value=mes, inline=False)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='dm')
    @commands.cooldown(1,3)
    async def dm(self,ctx, member: discord.Member, *args):
        hex_int = random.randint(0,16777215)
        """Gets the bot to DM your friend."""
        mes = " ".join(args)
        embed=discord.Embed(title="Message from your friend", color=hex_int)
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
        embed.add_field(name="Message", value=mes, inline=False)
        embed.add_field(name="Specially for you by", value=f"{ctx.author.name} <@{ctx.author.id}>", inline=False)
        embed.set_footer(text=f"DM function.")
        try:
            await member.send(embed=embed)
        except:
            await ctx.message.add_reaction("\U0000274c")
        else:
            await ctx.message.add_reaction("\U00002705")


    @commands.command(name='guess')
    @commands.cooldown(1,5)
    async def guess(self, ctx):
        """Guessing game"""
        await ctx.reply('Guess a number between 1 and 10.', mention_author=True)
        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()
        answer = random.randint(1, 10)

        try:
            guess = await self.bot.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.reply(f'Sorry, you took too long it was **__{answer}__**.', mention_author=True)

        if int(guess.content) == answer:
            await guess.reply('Congrats!', mention_author=True)
        else:
            await guess.reply(f'No It is actually **__{answer}__**.', mention_author=True)


def setup(bot):
    bot.add_cog(FunCog(bot))