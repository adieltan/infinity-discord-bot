import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime
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
    @commands.has_role(783134076772941876)
    @rhserver()
    @commands.cooldown(1,18)
    async def heist(self, ctx, amount: float, sponsor: discord.Member=None, *, msg:str=None):
        """Gets people ready for a heist."""
        if sponsor == None:
            sponsor = ctx.author
        heistping = ctx.guild.get_role(807925829009932330)
        hex_int = random.randint(0,16777215)
        embed = discord.Embed(title='Heist', description=f'{amount}', color=hex_int)
        embed.set_author(name=sponsor.display_name, icon_url=sponsor.avatar.url)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_image(url="https://media3.giphy.com/media/5QMOICVmXremPSa0k7/giphy.gif")
        embed.add_field(name='Additional info', value=f"{msg} ", inline=False)
        embed.set_footer(text='Remember to thank them !')
        await ctx.reply(content=f"{heistping.mention()}", embed=embed, allowed_mentions=True,  mention_author=False)







def setup(bot):
    bot.add_cog(customCog(bot))