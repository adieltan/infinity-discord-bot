import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
try:from dotenv import load_dotenv
except:pass

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
        

    @commands.command(name="coinflip", aliases=["flip", 'cf'])
    @commands.cooldown(1,10)
    async def coinflip(self, ctx, amount:int, guess:str=None):
        """Flips a coin ... Maybe giving you bonus if you guess the right face. Guess will be randomised if you didn't provide one so..."""
        face = ["heads", "tails"]
        if guess == None:
            guess = random.choice(face)
        else: 
            guess = guess.lower()
            if guess[0] == "h":
                guess = "heads"
            elif guess[0] == "t":
                guess = "tails"
            else:
                guess = random.choice(face)
        correct = random.choice(face)
        embed = discord.Embed(title="CoinFlip Machine", description=f"{ctx.author.mention}'s guess = {guess}", color=16776960)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.set_image("https://cdn.dribbble.com/users/58530/screenshots/2323771/coin-flip.gif")
        message = await ctx.reply(embed=embed, mention_author=True)

        if guess == correct:
            embed = discord.Embed(title="CoinFlip Machine", description=f"{ctx.author.mention}", color=1900331)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            embed.timestamp=datetime.datetime.utcnow()
            message.edit(embed=embed)

        elif guess != correct:
            embed = discord.Embed(title="CoinFlip Machine", description=f"{ctx.author.mention}", color=16711680)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            embed.timestamp=datetime.datetime.utcnow()
            message.edit(embed=embed)
            

        

def setup(bot):
    bot.add_cog(CurrencyCog(bot))