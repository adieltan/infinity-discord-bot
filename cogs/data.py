import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
try:from dotenv import load_dotenv
except:pass

import lxml.html as lh

class DataCog(commands.Cog, name='Data'):
    """*Data from websites or api*"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="amari", aliases=['amarigraph'])
    async def amari(self, ctx, serverid:int=None):
        """Plots the xp of the server's amari data in a chart."""
        async with ctx.typing():
            rank = []
            xp = []
            if serverid is None:
                serverid = ctx.guild.id
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url=f"https://lb.amaribot.com/index.php?gID={serverid}") as data:
                    #soup = BeautifulSoup(data.text, "html.parser")
                    doc = lh.fromstring(await data.text())
            tr_elements = doc.xpath('//tr')
            firstxp = int(tr_elements[0][2].text_content())
            for t in tr_elements:
                rawrank=int(t[0].text_content())
                rawxp = int(t[2].text_content())
                if rawxp < (firstxp*0.005):
                    break
                else:
                    rank.append(rawrank)
                    xp.append(rawxp)
            plt.plot(rank, xp, label = "xp")
            plt.xlabel('Rank')
            plt.ylabel('XP')
            plt.title(f"{serverid}'s Amari Xp")
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            f = discord.File(fp=buf, filename="image.png")
            embed=discord.Embed(title=f"{serverid}'s Amari Xp", url=f"https://lb.amaribot.com/index.php?gID={serverid}")
            embed.set_image(url="attachment://image.png")
            embed.timestamp=datetime.datetime.utcnow()
            await ctx.reply(file=f, embed=embed)
            plt.close()
            buf.close()
            await cs.close()

def setup(bot):
    bot.add_cog(DataCog(bot))