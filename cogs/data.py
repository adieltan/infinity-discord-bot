import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt

import lxml.html as lh
import blist, MotionBotList, topgg

class DataCog(commands.Cog, name='Data'):
    """*Data from websites or api*"""
    def __init__(self, bot):
        self.bot = bot
        self.autostatsposting.start()
        self.blist= blist.Blist(self.bot, token=os.getenv('blist_token'))
        self.motionlist = MotionBotList.connect(os.getenv('motionlist_token'))
        self.topgg= topgg.DBLClient(self.bot,token=os.getenv('topgg_token'),autopost=False)
        self.voterchannel = self.bot.get_channel(874461656938340402)
        
    @commands.command(name="amari", aliases=['amarigraph'])
    async def amari(self, ctx, serverid:int=None):
        """Plots the xp of the server's amari data in a chart."""
        try:
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
        except:
            await ctx.reply(f"Error\nCommon Issues: There is no amari data in the server.")

    @commands.command(name="youtubestats", aliases=['ytstats'])
    async def youtubestats(self, ctx, channelid:str):
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url=f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channelid}&key={os.getenv('googleapi')}") as data:
                    json = await data.json()
                    items = json.get('items')
            await cs.close()
            try:
                id=items[0]['id']
                stats= items[0]['statistics']
                embed=discord.Embed(title="Youtube Statistics", url=f"https://youtube.com/channel/{channelid}", description=f"{id}")
                embed.add_field(name="Subscribers", value=f"{format(int(stats['subscriberCount']), ',')}")
                embed.add_field(name="View Count", value=f"{format(int(stats['viewCount']), ',')}")
                embed.add_field(name="Video Count", value=f"{format(int(stats['videoCount']), ',')}")
                embed.set_footer(text="Google API")
                await ctx.reply(embed=embed)
            except:
                await ctx.reply(f"Error.\nCommon causes: Invalid channel id")

    @tasks.loop(hours=12, reconnect=True)
    async def autostatsposting(self):
        await self.bot.wait_until_ready()
        reports = self.bot.get_channel(825900714013360199)
        async with aiohttp.ClientSession() as cs:
            header={'Authorization':os.getenv('dbl_token')}
            data = {'users':len(self.bot.users), 'guilds':len(self.bot.guilds)}
            async with cs.post(url=f"https://discordbotlist.com/api/v1/bots/{self.bot.user.id}/stats", data=data, headers=header) as data:
                json = await data.json()
                if json.get('success') != True:
                    await reports.send(f"DiscordBotList\n{json}")
            header={'Authorization':os.getenv('voidbots_token')}
            data = {'server_count':len(self.bot.guilds)}
            #async with cs.post(url=f"https://api.voidbots.net/bot/stats/{self.bot.user.id}", json=data, headers=header) as data:
                #json = await data.json()
                #if json.get('message') != "Servercount updated!":
                    #await reports.send(f"VoidBots\n{json}")
            header={'Authorization':os.getenv('botlists_api')}
            data = {'status':'idle', 'guilds':len(self.bot.guilds), 'shards':1}
            async with cs.patch(url=f"https://api.botlists.com/bot/{self.bot.user.id}", json=data, headers=header) as data:
                json = await data.json()
                if json.get('status') != 200:
                    await reports.send(f"BotLists\n{json}")
            header={'Authorization':os.getenv('listcord_token')}
            data = {'server_count':len(self.bot.guilds)}
            async with cs.post(url=f"https://listcord.gg/api/bot/{self.bot.user.id}/stats", json=data, headers=header) as data:
                json = await data.json()
                if json.get('success') != True:
                    await reports.send(f"Listcord\n{json}")
            header={'Authorization':os.getenv('bladebot_token')}
            data = {'servercount':len(self.bot.guilds)}
            async with cs.post(url=f"https://bladebotlist.xyz/api/bots/{self.bot.user.id}/stats", json=data, headers=header) as data:
                json = await data.json()
                if json.get('errcode') != 200:
                    await reports.send(f"BladeBot\n{json}")
            header={'Authorization':os.getenv('discordservices_token')}
            data = {'servers':len(self.bot.guilds), 'shards':0}
            async with cs.post(url=f"https://api.discordservices.net/bot/{self.bot.user.id}/stats", json=data, headers=header) as data:
                json = await data.json()
                if json.get('code') != 200:
                    await reports.send(f"DiscordServices\n{json}")
            header={'Authorization':os.getenv('botlist_token')}
            data = {'server_count':len(self.bot.guilds)}
            async with cs.post(url=f"https://api.botlist.me/api/v1/bots/{self.bot.user.id}/stats", json=data, headers=header) as data:
                json = await data.json()
                if json.get('error') != False:
                    await reports.send(f"Botlist\n{json}")
        await cs.close()
        await blist.Blist.post_bot_stats(self.blist)
        self.motionlist.update(self.bot.user.id, len(self.bot.guilds))
        await self.topgg.post_guild_count(len(self.bot.guilds))

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        await self.voterchannel.send(f"{data}")

def setup(bot):
    bot.add_cog(DataCog(bot))