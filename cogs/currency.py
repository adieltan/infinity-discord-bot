import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 

class CurrencyCog(commands.Cog, name='Currency'):
    """*Currency Commands*"""
    def __init__(self, bot):
        self.bot = bot

        
    global updatebal
    async def updatebal(self, who:discord.User, amount:int=None):
        userid = who.id
        profile = await self.bot.dba["currency"].find_one({'_id':userid})
        bal = int(profile['bal'])
        if amount == None:
            yield bal
        else:
            await self.bot.dba["currency"].update_one({'_id':userid}, {"$inc":{"bal":amount}}, True)
            profile = await self.bot.dba["currency"].find_one({'_id':userid})
            bal = int(profile['bal'])
            yield bal


    @commands.command(name="balance", aliases=["bal", 'b'])
    @commands.cooldown(3,1)
    async def bal(self,ctx, user:discord.User=None):
        
        if user == None:
            user = ctx.author
        bal = await updatebal(self, who=user)
        embed = discord.Embed(title="Balance", color=discord.Color.random())
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        embed.add_field(name="Wallet", value=format(bal,','), inline=True)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="addbal")
    @commands.is_owner()
    async def addbal(self, ctx, user:discord.User=None, adjustment:int=None):
        if user == None:
            user = ctx.author
        if adjustment == None:
            adjustment = 10
        bal = await updatebal(self, who=user, amount=adjustment)
        if adjustment < 0:
            await ctx.send(f"Subtracted {adjustment} from {user.mention}'s balance.")
        elif adjustment > 0:
            await ctx.send(f"Added {adjustment} to {user.mention}'s balance.")


def setup(bot):
    bot.add_cog(CurrencyCog(bot))