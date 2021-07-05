import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 

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

    @commands.command(name="youtube", aliases=['yt'])
    async def youtube(self, ctx, channelid:str):
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url=f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channelid}&key={os.getenv('googleapi')}") as data:
                    json = await data.json()
                    items = json['items']
            id=items[0]['id']
            stats= items[0]['statistics']
            embed=discord.Embed(title="Youtube Statistics", url=f"https://youtube.com/channel/{channelid}", description=f"{id}")
            embed.add_field(name="Subscribers", value=f"{format(int(stats['subscriberCount']), ',')}")
            embed.add_field(name="View Count", value=f"{format(int(stats['viewCount']), ',')}")
            embed.add_field(name="Video Count", value=f"{format(int(stats['videoCount']), ',')}")
            embed.set_footer(text="Google API")
            await ctx.reply(embed=embed)
            await cs.close()

def setup(bot):
    bot.add_cog(DataCog(bot))