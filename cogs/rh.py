import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime
from discord.ext import commands
from discord.ext.commands import BucketType


class rhCog(commands.Cog, name='rh'):
    """*Custom commands for rh's server.*"""
    def __init__(self, bot):
        self.bot = bot

    def rhserver():
        def predicate(ctx):
            return ctx.guild.id==709711335436451901
        return commands.check(predicate)

    @commands.command(name="heist")
    @commands.has_role(783134076772941876)
    @rhserver()
    @commands.cooldown(1,5, type=BucketType.user)
    async def heist(self, ctx, amount: float, *, msg:str=None):
        """Gets people ready for a heist."""
        heistping = ctx.guild.get_role(807925829009932330)
        hex_int = random.randint(0,16777215)
        embed = discord.Embed(title='Heist', description=f'{amount}', color=hex_int)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_image(url="https://media3.giphy.com/media/5QMOICVmXremPSa0k7/giphy.gif")
        embed.add_field(name='Info', value=f"{msg} ", inline=False)
        embed.set_footer(text='Remember to thank them !')
        await ctx.reply(content=f"{heistping.mention()}", embed=embed, allowed_mentions=True,  mention_author=False)

    @commands.command(name="verify")
    @commands.has_permissions(manage_roles=True)
    @rhserver()
    async def verify(self, ctx, member:discord.Member):
        """Gives someone the verified role."""
        panda= ctx.guild.get_role(717957198675968024)
        await member.add_roles(panda, reason="Verification")
        await ctx.reply(f"Verified {member.mention}")


def setup(bot):
    bot.add_cog(rhCog(bot))