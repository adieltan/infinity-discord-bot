import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 

from discord.ext.commands.cooldowns import BucketType
from psutil._common import bytes2human

class InfoCog(commands.Cog, name='Info'):
    """*Info about bot and related servers.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='links', aliases=['botinvite', 'infinity', 'support', 'server', 'website', 'webpage', 'supportserver', 'invite', 'appeal'])
    async def links(self, ctx):
        """Gets the links related to the bot."""
        
        embed=discord.Embed(title = "Infinity" , url="https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot", description="Invite link: [Admin](https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot)  [~~Admin~~](https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=0&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot)", color=discord.Color.random())
        embed.add_field(name="Support Server", value="[Typical Pandas](https://discord.gg/dHGqUZNqCu)\nAppeal :arrow_up: [<a:jump:856511832486969364>](https://discord.gg/dHGqUZNqCu) <#851637967952412723>")
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
        embed=discord.Embed(title="Bot Info", description=app.description, color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(name=self.bot.user, url=self.bot.user.avatar_url)
        embed.add_field(name="Owner", value=f"<@701009836938231849>")
        embed.add_field(name="Ping", value=f'{round (self.bot.latency * 1000)}ms ')
        embed.add_field(name="Connected", value=f"To **{format(len(self.bot.users),',')}** members in **{len(self.bot.guilds)}** guilds.", inline=False)
        embed.add_field(name="CPU", value=f'Count: {psutil.cpu_count()}\nUsage: {psutil.cpu_percent()}%')
        memory = psutil.virtual_memory()
        embed.add_field(name="Memory", value=f"{bytes2human(memory.used)} / {bytes2human(memory.total)} ({memory.percent}% Used)")
        d = datetime.datetime.now() -self.bot.est
        embed.add_field(name="Uptime", value=f"{round(d.seconds/60/60,2)} hours")
        embed.add_field(name="Bot Lists", value=f"[Top.gg](https://top.gg/bot/732917262297595925)\n[DBL](https://discordbotlist.com/bots/infinity-5345)\n[BladeBotList](https://bladebotlist.xyz/bot/732917262297595925)\n[VoidBots](https://voidbots.net/bot/732917262297595925/)\n[ListCord](https://listcord.gg/bot/732917262297595925)\n[BotLists](https://botlists.com/bot/732917262297595925)\n[Fateslist](https://fateslist.xyz/bot/732917262297595925)\n[Blist](https://blist.xyz/bot/732917262297595925)\n[MotionList](https://www.motiondevelopment.top/bots/732917262297595925)\n[DiscordServices](https://discordservices.net/bot/732917262297595925)\n[BotList](https://botlist.me/bots/732917262297595925)\n[StellarBotList](https://stellarbotlist.com/bot/732917262297595925)")
        embed.add_field(name="Info", value=f"A multipurpose bot that helps automate actions in your server. Features many unique utility commands such as bookmarking system that makes our life easier.", inline=False)
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
        await ctx.message.add_reaction("\U00002705")

    @suggest.command(name='accept', aliases=['a'])
    @commands.is_owner()
    async def suggestionaccept(self, ctx, *, text:str=None):
        """Accepts a suggestion."""
        ref = ctx.message.reference
        if ref == None:
            await ctx.reply("You gotta reply to the suggestion you wanna accept!", mention_author=True)
        else:
            message = await ctx.channel.fetch_message(ref.message_id)
            embed=message.embeds[0]
            embed.color=discord.Color.green()
            embed.add_field(name="Accepted", value=f"{text}", inline=False)
            await message.edit(embed=embed)
            await ctx.message.delete()

    @suggest.command(name='deny', aliases=['d', 'x'])
    @commands.is_owner()
    async def suggestiondeny(self, ctx, *, text:str=None):
        """Denies a suggestion."""
        ref = ctx.message.reference
        if ref == None:
            await ctx.reply("Eh you gotta reply to the suggestion you wanna accept!", mention_author=True)
        else:
            message = await ctx.channel.fetch_message(ref.message_id)
            embed=message.embeds[0]
            embed.color=discord.Color.red()
            embed.add_field(name="Denied", value=f"{text}", inline=False)
            await message.edit(embed=embed)
            await ctx.message.delete()

    @commands.command(name="emojiservers")
    async def emojiservers(self, ctx):
        """Gets the invite links to the bot's emoji servers."""
        await ctx.reply(embed=discord.Embed(title="Infinity Emoji Servers", description=f"[1](https://discord.gg/hM67fpgM3y) [2](https://discord.gg/T6dJHppueq)", color=discord.Color.random()))

def setup(bot):
    bot.add_cog(InfoCog(bot))
