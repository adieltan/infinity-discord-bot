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

    def udevent():
        def predicate(ctx):
            return ctx.guild.id==841654825456107530 or ctx.guild.id==830731085955989534 
        return commands.check(predicate)

    @commands.command(name="donolog", aliases=["dl"])
    @udevent()
    @commands.cooldown(1,7)
    @commands.has_permissions(administrator=True)
    async def logging(self, ctx, user:discord.User, item:str, value:str, proof:str):
        """Logs the dono."""
        raw = float(value.replace(",", ""))
        channel = self.bot.get_channel(842738964385497108)
        valu = math.trunc(raw)
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="Ultimate Dankers Event Donation", color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
        embed.add_field(name="Donator", value=f'{user.mention}', inline=True)
        embed.add_field(name="Donation", value=f"[{item} worth {valu}]({proof})", inline=True)
        embed.add_field(name="Logging command", value=f"`~dono add {user.id} {valu} {proof}`\n\nYou may log it in <#824211968021495871>", inline=False)
        embed.set_footer(text=f"React with a ✅ after logged.")
        await channel.send(embed=embed)
        await ctx.reply("Logged in <#842738964385497108>")




def setup(bot):
    bot.add_cog(customCog(bot))