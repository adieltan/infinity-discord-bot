import discord, random, string, os, asyncio, sys, math, requests, json, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord import permissions
from discord.ext import commands, tasks
 
from psutil._common import bytes2human

class InfoCog(commands.Cog, name='Info'):
    """❕ Info about bot and related servers."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='links', aliases=['botinvite', 'infinity', 'support', 'server', 'website', 'webpage', 'supportserver', 'invite', 'appeal', 'info', 'botinfo', 'ping', 'servers'])
    async def links(self, ctx):
        """Gets the links related to the bot."""
        
        embed=discord.Embed(title = "Infinity Bot Info" , url=discord.utils.oauth_url(ctx.bot.application_id, permissions=discord.Permissions.all(), scopes=('bot','applications.commands')), description="A multipurpose bot that helps automate actions in your server. Features many unique utility commands such as bookmarking system that makes our life easier.", color=discord.Color.random(), timestamp=discord.utils.utcnow()).set_author(name=self.bot.user, icon_url=self.bot.user.avatar)
        embed.add_field(name="Owner", value=f"""{' '.join([f"<@{owner}>" for owner in self.bot.owners])}""")
        embed.add_field(name="Ping", value=f'<:ping:901051623416152095> {round (self.bot.latency * 1000)}ms ')
        d = discord.utils.utcnow() -self.bot.startuptime
        embed.add_field(name="Uptime", value=f"<a:timer:890234490100793404> {round(d.seconds/60/60,2)} hours")
        embed.add_field(name="Connected", value=f"<:discovery:894391371635499048> To **{format(len(self.bot.users),',')}** members in **{len(self.bot.guilds)}** guilds.", inline=False)
        v = discord.ui.View()
        v.add_item(discord.ui.Button(label="Bot Invite (No perms)", url=f"{discord.utils.oauth_url(ctx.bot.application_id, permissions=discord.Permissions.none(), scopes=('bot','applications.commands'))}"))
        v.add_item(discord.ui.Button(label="Bot Invite (All perms)", url=f"{discord.utils.oauth_url(ctx.bot.application_id, permissions=discord.Permissions.all(), scopes=('bot','applications.commands'))}"))
        v.add_item(discord.ui.Button(label="Support Server (Typical Pandas)", url='https://discord.gg/dHGqUZNqCu'))
        v.add_item(discord.ui.Button(label="Website", url='https://tynxen.netlify.app/'))
        await ctx.reply(embed=embed, mention_author=False, view=v)

        
    @commands.group(name='vote', aliases=['v'], invoke_without_command=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def vote(self, ctx):
        """Display vote websites and vote cooldowns."""
        bl = {
            'Top.gg':{'w':'https://top.gg/bot/732917262297595925/vote', 'v':None},
            'DBL':{'w':'https://discordbotlist.com/bots/infinity-5345/upvote', 'v':None},
            'BladeBL':{'w':'https://bladelist.gg/bots/732917262297595925', 'v':None},
            'VoidBots':{'w':'https://voidbots.net/bot/732917262297595925/vote','v':None},
            'ListCord':{'w':'https://listcord.gg/bot/732917262297595925','v':None},
            'BotLists':{'w':'https://botlists.com/bot/732917262297595925','v':None},
            'Fateslist':{'w':'https://fateslist.xyz/bot/732917262297595925/vote','v':None},
            'Blist':{'w':'https://blist.xyz/bot/732917262297595925','v':None},
            'MotionList':{'w':'https://www.motiondevelopment.top/bots/732917262297595925/vote','v':None},
            'DiscordServices':{'w':'https://discordservices.net/bot/732917262297595925','v':None},
            'BotList':{'w':'https://botlist.me/bots/732917262297595925/vote','v':None},
            'StellarBL':{'w':'https://stellarbotlist.com/bot/732917262297595925/vote','v':None},
            'InfinityBL':{'w':'https://infinitybotlist.com/bots/732917262297595925/vote', 'v':None},
            'Astralist':{'w':'https://astralist.tk/bot/732917262297595925/vote', 'v':None}
        }
        async with aiohttp.ClientSession() as cs:
            header={'Authorization':os.getenv('topgg_token')}
            async with cs.get(url=f"https://top.gg/api/bots/{self.bot.user.id}/check?userId={ctx.author.id}", headers=header, timeout=5) as data:
                json = await data.json()
                if json.get('voted') == 1:
                    bl['Top.gg']['v'] = True
            header['Authorization'] = os.getenv('voidbots_token')
            async with cs.get(url=f"https://api.voidbots.net/bot/voted/{self.bot.user.id}/{ctx.author.id}", headers=header, timeout=5) as data:
                json = await data.json()
                if json.get('voted') is True:
                    bl['VoidBots']['v'] = True
                    bl['VoidBots']['nextvote'] = round(datetime.datetime.now().timestamp()) + round(json['nextVote']['ms'] / 1000)
            header['Authorization'] = os.getenv('listcord_token')
            async with cs.get(url=f"https://listcord.gg/api/bot/{self.bot.user.id}/voted", headers=header, params={'user_id':f"{ctx.author.id}"}, timeout=5) as data:
                json = await data.json()
                if json.get('voted') is True:
                    bl['ListCord']['v'] = True
                    bl['ListCord']['nextvote'] = round(json['next_at'] / 1000)
            header['Authorization']=os.getenv('blist_token')
            async with cs.get(url=f"https://blist.xyz/api/v2/bot/{self.bot.user.id}/votes", headers=header, timeout=5) as data:
                json = await data.json()
                json['votes'].reverse()
                if str(ctx.author.id) in str(json['votes']):
                    if datetime.datetime.fromisoformat([vote for vote in json['votes'] if vote['user'] == str(ctx.author.id)][0]['time'][:-1]+'+00:00').timestamp() + 60*60*12 > discord.utils.utcnow().timestamp():
                        bl['Blist']['v'] = True
                        bl['Blist']['nextvote'] = round(datetime.datetime.fromisoformat([vote for vote in json['votes'] if vote['user'] == str(ctx.author.id)][0]['time'][:-1]+'+00:00').timestamp() + 60*60*12)
            
        if any(bl[item]['v'] is True for item in bl):
            voted = "**Votes On Cooldown:**\n" + '\n'.join([
            f"""[{item}]({bl[item]['w']}) {f"<t:{bl[item].get('nextvote')}:R>"if bl[item].get('nextvote') else ''}"""
            for item in bl if bl[item]['v'] is True
        ])
        else:
            voted = "You have not voted for Infinity in any sites."

        v = discord.ui.View()
        for val in bl:
            if bl[val]['v'] is not True:
                v.add_item(discord.ui.Button(label=val, url=bl[val]['w']))
        embed=discord.Embed(title="Vote for Infinity", description=f"{voted}\n\n{f'Yet to vote in {len(v.children)} sites. <:down:876079229744316456>' if len(v.children) > 0 else ''}", color=discord.Color.gold())
        await ctx.reply(embed=embed, view=v)


    @vote.command(name='topgg')
    async def topggvotes(self, ctx):
        """Shows last 1000 voters for the bot via top.gg"""
        async with aiohttp.ClientSession() as cs:
            header={'Authorization':os.getenv('topgg_token')}
            async with cs.get(url=f"https://top.gg/api/bots/{self.bot.user.id}/votes", headers=header) as data:
                json = await data.json()
        await cs.close()
        text = ''.join(
            f"Username: {vote['username']} • ID: {vote['id']}\n" for vote in json
        )

        buffer = io.BytesIO(text.encode('utf-8'))
        await ctx.reply(file=discord.File(buffer, filename='topgglast1000votes.txt'))

    @vote.command(name='blist')
    async def blistvotes(self, ctx):
        """Shows the votes for the bot in the past 12 hours via blist"""
        async with aiohttp.ClientSession() as cs:
            header={'Authorization':os.getenv('blist_token')}
            async with cs.get(url=f"https://blist.xyz/api/v2/bot/{self.bot.user.id}/votes", headers=header) as data:
                json = await data.json()
        await cs.close()
        json['votes'].reverse()
        text = ''.join(
            f"User: {vote['user']} • Time: {vote['time']}\n" for vote in json['votes']
        )
        await ctx.send(f"{[vote for vote in json['votes'] if vote['user'] == str(ctx.author.id)]} {str(ctx.author.id) in str(json['votes'])}")
        await ctx.send(f"{discord.utils.format_dt(datetime.datetime.fromisoformat([vote for vote in json['votes'] if vote['user'] == str(ctx.author.id)][0]['time'][:-1]+'+00:00'))}")

        buffer = io.BytesIO(text.encode('utf-8'))
        await ctx.reply(file=discord.File(buffer, filename='blistvotes.txt'))

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
        msg = await suggestchannel.send(embed=embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
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

def setup(bot):
    bot.add_cog(InfoCog(bot))
