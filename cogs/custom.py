import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 

class customCog(commands.Cog, name='custom'):
    """*Custom commands for server.*"""
    def __init__(self, bot):
        self.bot = bot
        
    def server(id:list):
        def predicate(ctx):
            return ctx.guild.id in id
        return commands.check(predicate)

    @commands.command(name="donolog", aliases=["dl"], hidden=True)
    #ud event
    async def logging(self, ctx, user:discord.User, quantity:float, item:str, value_per:str, *, proof:str):
        """Logs the dono."""
        guild = self.bot.get_guild(841654825456107530)
        admin = guild.get_role(841655266743418892).members
        if ctx.author not in admin:
            return
        raw = float(value_per.replace(",", ""))
        channel = self.bot.get_channel(842738964385497108)
        valu = math.trunc(raw)*quantity
        human = format(int(valu), ',')
        
        embed=discord.Embed(title="Ultimate Dankers Event Donation", description=f"**Donator** : {user.mention}\n**Donation** : {quantity} {item}(s) worth {human} [Proof]({proof})", color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=ctx.author.avatar_url, name=f"Logged by: {ctx.author.name}")
        embed.add_field(name="Logging command", value=f"`,d a {user.id} {valu:.2e} {proof}`\nLog in <#814490036842004520>", inline=False)
        embed.add_field(name="Raw", value=f"||`{ctx.message.content}`||", inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f"React with a ✅ after logged.")
        await channel.send(f"{user.id}", embed=embed)
        await ctx.reply("Logged in <#842738964385497108>")


def setup(bot):
    bot.add_cog(customCog(bot))