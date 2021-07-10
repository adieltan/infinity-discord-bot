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
        embed.add_field(name="Website", value="[Infinity Website](https://sites.google.com/view/rh6)")
        embed.timestamp=datetime.datetime.utcnow()
        
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='servers')
    @commands.cooldown(1,5)
    async def servs(self, ctx):
        """Shows the number of servers that the bot is in."""
        await ctx.reply(f"I am connected to {len(self.bot.guilds)} server(s).", mention_author=False)

    @commands.command(name='emoji')
    @commands.cooldown(1,1)
    async def emoji(self, ctx, emoji:discord.PartialEmoji):
        """Shows info about an emoji."""
        await ctx.reply(f"```Name:{emoji.name}\nId: {emoji.id}\n{emoji}```", mention_author=False)

    @commands.command(name='info', aliases=['botinfo', 'ping'])
    @commands.cooldown(1,4)
    async def info(self, ctx):
        """Info about the bot."""
        
        app = await self.bot.application_info()
        embed=discord.Embed(title="Bot Info", description="Info about the bot.", color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(name=self.bot.user, url=self.bot.user.avatar_url)
        embed.add_field(name="Owner", value=f"<@701009836938231849>")
        embed.add_field(name="Ping", value=f'{round (self.bot.latency * 1000)}ms ')
        embed.add_field(name="Connected", value=f"To **{format(len(self.bot.users),',')}** members in **{len(self.bot.guilds)}** guilds.", inline=False)
        embed.add_field(name="CPU", value=f'Count: {psutil.cpu_count()}\nUsage: {psutil.cpu_percent()}%', inline=False)
        memory = psutil.virtual_memory()
        embed.add_field(name="Memory", value=f"{bytes2human(memory.used)} / {bytes2human(memory.total)} ({memory.percent}% Used)")
        await ctx.reply(embed=embed, mention_author=False)
        
    @commands.command(name="managers", aliases=["staff"])
    async def managers(self, ctx):
        """Shows the managers of the bot."""
        managers = self.bot.managers
        embed=discord.Embed(title="Infinity Managers", description=f"{' '.join([f'<@{manag}>' for manag in managers])}", color=discord.Color.random())
        await ctx.reply(embed=embed)
                
    @commands.command(name='partners')
    @commands.cooldown(1,8, type=BucketType.channel)
    async def partners(self, ctx):
        """Servers/Bots this bot is partnered with."""
        partners = ['https://discord.gg/HUpye3bnzq']
        text = '\n'.join(partners)
        await ctx.send(text)

    @commands.command(name="newsupdate", aliases=['latestnews', 'news'])
    async def newsupdate(self, ctx):
        """Shows the update log of the bot."""
        updatechannel = self.bot.get_channel(813251614449074206)
        messagestop = await updatechannel.history(limit=5).flatten()
        embed=discord.Embed(title="News Update", description="<#813251614449074206>", colour=discord.Color.random())
        for message in messagestop:
            newsembed = message.embeds[0]
            field = newsembed.fields[0]
            embed.add_field(name=f"{newsembed.description} `{message.created_at.strftime('%Y %b %-d')}`", value=f"{field.value}", inline=False)
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(InfoCog(bot))