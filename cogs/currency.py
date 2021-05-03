import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime, requests
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://rh:1234@infinitycluster.yupj9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["infinity"]["wealth"]

class CurrencyCog(commands.Cog, name='Currency'):
    """*Currency Commands*"""
    def __init__(self, bot):
        self.bot = bot
        self.db = db
        
def updatebal(userid, amount):
    bal = int(db.find({},{'_id':userid, 'balance':1}))
    query = {'_id':userid}
    newval = {"$set" :{"balance" : amount+bal}}
    db.update_one(query, newval)

    @commands.command(name="balance", aliases=["bal", 'b'])
    @commands.cooldown(3,1)
    async def bal(self,ctx, user:discord.User=None):
        hex_int = random.randint(0,16777215)
        if user == None:
            user = ctx.author
        bal = int(db.find({},{'_id':user.id, 'balance':1}))
        embed = discord.Embed(title="Balance", color=hex_int)
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        embed.add_field(name="Wallet", value=bal, inline=True)
        await ctx.reply(embed=embed, mention_author=False)

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