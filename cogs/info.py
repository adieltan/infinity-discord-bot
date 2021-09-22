import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, 
import matplotlib.pyplot as plt
 

 
from psutil._common import bytes2human

class InfoCog(commands.Cog, name='Info'):
    """*Info about bot and related servers.*"""
    def __init__(self, bot):
        self.bot = bot
        self.bot_info.start()

    @commands.command(name='links', aliases=['botinvite', 'infinity', 'support', 'server', 'website', 'webpage', 'supportserver', 'invite', 'appeal'])
    async def links(self, ctx):
        """Gets the links related to the bot."""
        
        embed=discord.Embed(title = "Infinity" , url="https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot", description="Invite link: [Admin](https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot)  [~~Admin~~](https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=0&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot)", color=discord.Color.random())
        embed.add_field(name="Support Server", value="[Typical Pandas](https://discord.gg/dHGqUZNqCu)\nAppeal <:up:876079229748539393> [<a:infinity:874548940610097163>](https://discord.gg/dHGqUZNqCu) <#851637967952412723>")
        embed.add_field(name="Website", value="[Tynxen](https://tynxen.netlify.app/)")
        embed.timestamp=datetime.datetime.utcnow()
        
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='servers')
    @commands.cooldown(1,5)
    async def servs(self, ctx):
        """Shows the number of servers that the bot is in."""
        await ctx.reply(f"I am connected to {len(self.bot.guilds)} server(s).", mention_author=False)

    @commands.command(name='info', aliases=['botinfo', 'ping'])
    @commands.cooldown(1,4)
    async def info(self, ctx):
        """Info about the bot."""
        app = await self.bot.application_info()
        embed=discord.Embed(title="Bot Info", description="A multipurpose bot that helps automate actions in your server. Features many unique utility commands such as bookmarking system that makes our life easier.", color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(name=self.bot.user, url=self.bot.user.avatar_url)
        embed.add_field(name="Owner", value=f"""{' '.join([f"<@{owner}>" for owner in self.bot.owners])}""")
        embed.add_field(name="Ping", value=f'{round (self.bot.latency * 1000)}ms ')
        embed.add_field(name="CPU", value=f'Count: {psutil.cpu_count()}\nUsage: {psutil.cpu_percent()}%')
        memory = psutil.virtual_memory()
        embed.add_field(name="Memory", value=f"{bytes2human(memory.used)} / {bytes2human(memory.total)} ({memory.percent}% Used)")
        d = datetime.datetime.utcnow() -self.bot.startuptime
        embed.add_field(name="Uptime", value=f"{round(d.seconds/60/60,2)} hours")
        embed.add_field(name="Connected", value=f"To **{format(len(self.bot.users),',')}** members in **{len(self.bot.guilds)}** guilds.", inline=False)
        bot_lists = {
            'Top.gg':'https://top.gg/bot/732917262297595925',
            'DBL':'https://discordbotlist.com/bots/infinity-5345',
            'BladeBotList':'https://bladebotlist.xyz/bot/732917262297595925',
            'VoidBots':'https://voidbots.net/bot/732917262297595925/',
            'ListCord':'https://listcord.gg/bot/732917262297595925',
            'BotLists':'https://botlists.com/bot/732917262297595925',
            'Fateslist':'https://fateslist.xyz/bot/732917262297595925',
            'Blist':'https://blist.xyz/bot/732917262297595925',
            'MotionList':'https://www.motiondevelopment.top/bots/732917262297595925',
            'DiscordServices':'https://discordservices.net/bot/732917262297595925',
            'BotList':'https://botlist.me/bots/732917262297595925',
            'StellarBotList':'https://stellarbotlist.com/bot/732917262297595925',
            'InfinityBotList':'https://infinitybotlist.com/bots/732917262297595925',
            'Astralist':'https://astralist.tk/bot/732917262297595925/vote'
        }
        embed.add_field(name="Bot Lists", value=f"""{' | '.join([f"[{item}]({bot_lists[item]})" for item in bot_lists])}""", inline=False)
        await ctx.reply(embed=embed, mention_author=False)
        
    @commands.command(name="managers", aliases=["staff"])
    async def managers(self, ctx):
        """Shows the managers of the bot."""
        managers = self.bot.managers
        embed=discord.Embed(title="Infinity Managers", description='\n'.join([f'<@{manag}>' for manag in managers]), color=discord.Color.random())
        await ctx.reply(embed=embed)

    @commands.command(name="newsupdate", aliases=['latestnews', 'news'])
    async def newsupdate(self, ctx):
        """Shows the update log of the bot."""
        updatechannel = self.bot.get_channel(813251614449074206)
        messagestop = await updatechannel.history(limit=5).flatten()
        embed=discord.Embed(title="News Update", description="<#813251614449074206>", colour=discord.Color.random())
        for message in messagestop:
            if message.author.id != self.bot.user.id:
                return
            newsembed = message.embeds[0]
            field = newsembed.fields[0]
            embed.add_field(name=f"{newsembed.description} <t:{round(message.created_at.timestamp())}>", value=f"{field.value}", inline=False)
        await ctx.reply(embed=embed)

    @commands.group(name="suggest", invoke_without_command=True)
    async def suggest(self, ctx, *, suggestion:str):
        """Suggests a feature that you want added to the bot."""
        suggestchannel = self.bot.get_channel(827896302008139806)
        embed=discord.Embed(title="Suggestion", description=f"{suggestion}", color=discord.Color.blue())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
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
                embed.set_author(name=f"{self.bot.user.name}", url="https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot", icon_url=self.bot.user.avatar_url)
                embed.set_footer(text="Last updated on")
                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(name="System", value=f"Ping: {round (self.bot.latency * 1000)}ms\nCPU: {psutil.cpu_count()} core {psutil.cpu_percent()}%\nMemory: {psutil.virtual_memory().percent}%", inline=False)
                embed.add_field(name="Connection", value=f"Uptime: {round((datetime.datetime.utcnow()-self.bot.startuptime).seconds/60/60,2)} hours\nMembers: {format(len(self.bot.users),',')}\nServers: {len(self.bot.guilds)}", inline=False)
                embed.add_field(name="Processed Messages", value=f"{self.bot.processed_messages}")
                embed.add_field(name="Invoked Commands", value=f"{self.bot.commands_invoked}")
            else:
                oldembed = message.embeds[0]
                embed = discord.Embed(title="Bot Info", color=discord.Color.gold())
                embed.set_author(name=f"{self.bot.user.name}", url="https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot", icon_url=self.bot.user.avatar_url)
                embed.set_footer(text="Last updated on")
                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(name="System", value=f"Ping: {round (self.bot.latency * 1000)}ms\nCPU: {psutil.cpu_count()} core {psutil.cpu_percent()}%\nMemory: {psutil.virtual_memory().percent}%", inline=False)
                embed.add_field(name="Connection", value=f"Uptime: {round((datetime.datetime.utcnow()-self.bot.startuptime).seconds/60/60,2)} hours\nMembers: {format(len(self.bot.users),',')}\nServers: {len(self.bot.guilds)}", inline=False)
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
