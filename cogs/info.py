import discord, random, string, os, asyncio, sys, math, requests, json, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord import permissions
from discord.ext import commands, tasks
 
from psutil._common import bytes2human

class InfoCog(commands.Cog, name='Info'):
    """❕ Info about bot and related servers."""
    def __init__(self, bot):
        self.bot = bot
        self.bot_info.start()

    @commands.command(name='links', aliases=['botinvite', 'infinity', 'support', 'server', 'website', 'webpage', 'supportserver', 'invite', 'appeal', 'info', 'botinfo', 'ping', 'servers'])
    async def links(self, ctx):
        """Gets the links related to the bot."""
        
        embed=discord.Embed(title = "Infinity Bot Info" , url=discord.utils.oauth_url(ctx.bot.application_id, permissions=discord.Permissions.all(), scopes=('bot','applications.commands')), description="A multipurpose bot that helps automate actions in your server. Features many unique utility commands such as bookmarking system that makes our life easier.", color=discord.Color.random(), timestamp=discord.utils.utcnow()).set_author(name=self.bot.user, icon_url=self.bot.user.avatar)
        embed.add_field(name="Owner", value=f"""{' '.join([f"<@{owner}>" for owner in self.bot.owners])}""")
        embed.add_field(name="Ping", value=f'{round (self.bot.latency * 1000)}ms ')
        d = discord.utils.utcnow() -self.bot.startuptime
        embed.add_field(name="Uptime", value=f"{round(d.seconds/60/60,2)} hours")
        embed.add_field(name="Connected", value=f"To **{format(len(self.bot.users),',')}** members in **{len(self.bot.guilds)}** guilds.", inline=False)
        v = discord.ui.View()
        v.add_item(discord.ui.Button(label="Bot Invite (Without Admin)", url=f"{discord.utils.oauth_url(ctx.bot.application_id, permissions=discord.Permissions.none(), scopes=('bot','applications.commands'))}"))
        v.add_item(discord.ui.Button(label="Bot Invite (With Admin)", url=f"{discord.utils.oauth_url(ctx.bot.application_id, permissions=discord.Permissions.all(), scopes=('bot','applications.commands'))}"))
        v.add_item(discord.ui.Button(label="Support Server (Typical Pandas)", url='https://discord.gg/dHGqUZNqCu'))
        v.add_item(discord.ui.Button(label="Website", url='https://tynxen.netlify.app/'))
        await ctx.reply(embed=embed, mention_author=False, view=v)

        
    @commands.group(name='vote', aliases=['v'], invoke_without_command=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def vote(self, ctx):
        """Display vote websites and vote cooldowns."""
        bl = {
            'Top.gg':{'website':'https://top.gg/bot/732917262297595925/vote', 'vote':None},
            'DBL':{'website':'https://discordbotlist.com/bots/infinity-5345/upvote', 'vote':None},
            'BladeBotList':{'website':'https://bladelist.gg/bots/732917262297595925', 'vote':None},
            'VoidBots':{'website':'https://voidbots.net/bot/732917262297595925/vote','vote':None},
            'ListCord':{'website':'https://listcord.gg/bot/732917262297595925','vote':None},
            'BotLists':{'website':'https://botlists.com/bot/732917262297595925','vote':None},
            'Fateslist':{'website':'https://fateslist.xyz/bot/732917262297595925/vote','vote':None},
            'Blist':{'website':'https://blist.xyz/bot/732917262297595925','vote':False},
            'MotionList':{'website':'https://www.motiondevelopment.top/bots/732917262297595925/vote','vote':None},
            'DiscordServices':{'website':'https://discordservices.net/bot/732917262297595925','vote':None},
            'BotList':{'website':'https://botlist.me/bots/732917262297595925/vote','vote':None},
            'StellarBotList':{'website':'https://stellarbotlist.com/bot/732917262297595925/vote','vote':None},
            'InfinityBotList':{'website':'https://infinitybotlist.com/bots/732917262297595925/vote','vote':None},
            'Astralist':{'website':'https://astralist.tk/bot/732917262297595925/vote','vote':None}
        }
        async with aiohttp.ClientSession() as cs:
            header={'Authorization':os.getenv('topgg_token')}
            async with cs.get(url=f"https://top.gg/api/bots/{self.bot.user.id}/check?userId={ctx.author.id}", headers=header) as data:
                json = await data.json()
                if json.get('voted') == 1:
                    bl['Top.gg']['vote'] = True
            header={'Authorization':os.getenv('voidbots_token')}
            async with cs.get(url=f"https://api.voidbots.net/bot/voted/{self.bot.user.id}/{ctx.author.id}", headers=header) as data:
                json = await data.json()
                if json.get('voted') is True:
                    bl['VoidBots']['vote'] = True
                    bl['VoidBots']['nextvote'] = round(datetime.datetime.now().timestamp()) + round(json['nextVote']['ms'] / 1000)
            header={'Authorization':os.getenv('listcord_token')}
            async with cs.get(url=f"https://listcord.gg/api/bot/{self.bot.user.id}/voted", headers=header, params={'user_id':f"{ctx.author.id}"}) as data:
                json = await data.json()
                if json.get('voted') is True:
                    bl['ListCord']['vote'] = True
                    bl['ListCord']['nextvote'] = round(json['next_at'] / 1000)

        await cs.close()
        lists = '\n'.join([f"""{'🚫'if bl[item]['vote'] is False else ''}{'<:neutral:875345584805003295>'if bl[item]['vote'] is None else ''}{'✅'if bl[item]['vote'] else ''} [{item}]({bl[item]['website']}) {f"<t:{bl[item].get('nextvote')}:R>"if bl[item].get('nextvote') else ''}""" for item in bl])
        embed=discord.Embed(title="Vote for Infinity", description=f"{lists}\n\n✅ = Voted\n<:neutral:875345584805003295> = Available / Unable to get vote data\n🚫 = Not Available for Voting\n", color=discord.Color.gold())
        v = discord.ui.View()
        for val in bl:
            v.add_item(discord.ui.Button(label=val, url=bl[val]['website']))
        await ctx.reply(embed=embed, view=v)

    @vote.command(name='topgg')
    async def topggvotes(self, ctx):
        """Shows last 1000 voters for the bot via top.gg"""
        async with aiohttp.ClientSession() as cs:
            header={'Authorization':os.getenv('topgg_token')}
            async with cs.get(url=f"https://top.gg/api/bots/{self.bot.user.id}/votes", headers=header) as data:
                json = await data.json()
        await cs.close()
        text = ''
        for vote in json:
            text += f"Username: {vote['username']} • ID: {vote['id']}\n"
        buffer = io.BytesIO(text.encode('utf-8'))
        await ctx.reply(file=discord.File(buffer, filename='topgglast1000votes.txt'))


    @commands.command(name="managers", aliases=["staff"])
    async def managers(self, ctx):
        """Shows the managers of the bot."""
        managers = self.bot.managers
        embed=discord.Embed(title="Infinity Managers", description='\n'.join([f'<@{manag}>' for manag in managers]), color=discord.Color.random())
        await ctx.reply(embed=embed)

    @commands.group(name="suggest", invoke_without_command=True)
    async def suggest(self, ctx, *, suggestion:str):
        """Suggests a feature that you want added to the bot."""
        suggestchannel = self.bot.get_channel(827896302008139806)
        embed=discord.Embed(title="Suggestion", description=f"{suggestion}", color=discord.Color.blue())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        await suggestchannel.send(embed=embed)
        await ctx.message.add_reaction("<a:verified:876075132114829342>")

    @suggest.command(name='accept', aliases=['a'])
    @commands.is_owner()
    async def suggestionaccept(self, ctx, *, text:str=None):
        """Accepts a suggestion."""
        ref = ctx.message.reference
        if ctx.channel.id != 827896302008139806:
            return
        await ctx.message.delete()
        if ref == None:
            await ctx.send(f"{ctx.author.mention} Eh you gotta reply to the suggestion you wanna accept!", delete_after=5)
        else:
            message = await ctx.channel.fetch_message(ref.message_id)
            if message.author.id != self.bot.user.id:
                await ctx.message.delete()
                return
            embed=message.embeds[0]
            embed.color=discord.Color.green()
            embed.add_field(name="Accepted", value=f"{text}", inline=False)
            await message.edit(embed=embed)

    @suggest.command(name='deny', aliases=['d', 'x'])
    @commands.is_owner()
    async def suggestiondeny(self, ctx, *, text:str=None):
        """Denies a suggestion."""
        ref = ctx.message.reference
        if ctx.channel.id != 827896302008139806:
            return
        await ctx.message.delete()
        if ref == None:
            await ctx.send(f"{ctx.author.mention} Eh you gotta reply to the suggestion you wanna accept!", delete_after=5)
        else:
            message = await ctx.channel.fetch_message(ref.message_id)
            if message.author.id != self.bot.user.id:
                await ctx.message.delete()
                return
            embed=message.embeds[0]
            embed.color=discord.Color.red()
            embed.add_field(name="Denied", value=f"{text}", inline=False)
            await message.edit(embed=embed)

    @commands.command(name="emojiservers")
    async def emojiservers(self, ctx):
        """Gets the invite links to the bot's emoji servers."""
        await ctx.reply(embed=discord.Embed(title="Infinity Emoji Servers", description=f"[1](https://discord.gg/hM67fpgM3y) [2](https://discord.gg/T6dJHppueq)", color=discord.Color.random()))

    @tasks.loop(minutes=10, reconnect=True)
    async def bot_info(self):
        await self.bot.wait_until_ready()
        try:
            message = await self.bot.get_channel(878527673343815700).fetch_message(878542454717022238)
            if len(message.embeds) < 1:
                embed = discord.Embed(title="Bot Info", color=discord.Color.gold())
                embed.set_author(name=f"{self.bot.user.name}", url="https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot", icon_url=self.bot.user.avatar)
                embed.set_footer(text="Last updated on")
                embed.timestamp = discord.utils.utcnow()
                embed.add_field(name="System", value=f"Ping: {round (self.bot.latency * 1000)}ms\nCPU: {psutil.cpu_count()} core {psutil.cpu_percent()}%\nMemory: {psutil.virtual_memory().percent}%", inline=False)
                embed.add_field(name="Connection", value=f"Uptime: {round((discord.utils.utcnow()-self.bot.startuptime).seconds/60/60,2)} hours\nMembers: {format(len(self.bot.users),',')}\nServers: {len(self.bot.guilds)}", inline=False)
                embed.add_field(name="Processed Messages", value=f"{self.bot.processed_messages}")
                embed.add_field(name="Invoked Commands", value=f"{self.bot.commands_invoked}")
            else:
                oldembed = message.embeds[0]
                embed = discord.Embed(title="Bot Info", color=discord.Color.gold())
                embed.set_author(name=f"{self.bot.user.name}", url="https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot", icon_url=self.bot.user.avatar)
                embed.set_footer(text="Last updated on")
                embed.timestamp = discord.utils.utcnow()
                embed.add_field(name="System", value=f"Ping: {round (self.bot.latency * 1000)}ms\nCPU: {psutil.cpu_count()} core {psutil.cpu_percent()}%\nMemory: {psutil.virtual_memory().percent}%", inline=False)
                embed.add_field(name="Connection", value=f"Uptime: {round((discord.utils.utcnow()-self.bot.startuptime).seconds/60/60,2)} hours\nMembers: {format(len(self.bot.users),',')}\nServers: {len(self.bot.guilds)}", inline=False)
                try: proc = int(oldembed.fields[2].value)
                except: proc = 0
                try: invo = int(oldembed.fields[3].value)
                except: invo = 0
                embed.add_field(name="Processed Messages", value=f"{proc + self.bot.processed_messages}")
                embed.add_field(name="Invoked Commands", value=f"{invo + self.bot.commands_invoked}")
                self.bot.processed_messages = 0
                self.bot.commands_invoked = 0
            await message.edit('\u200b', embed=embed)
        except:
            pass

def setup(bot):
    bot.add_cog(InfoCog(bot))
