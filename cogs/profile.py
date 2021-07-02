import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
from dotenv import load_dotenv

import dateparser

class profileCog(commands.Cog, name='profile'):
    """*User based commands.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def set(self,ctx):
        """Sets up your own profile."""
        if ctx.invoked_subcommand is None:
            pass

    @set.command(name="weight", aliases=['w]'])
    async def setweight(self, ctx, kg:int):
        """Sets your own weight."""
        results = await self.bot.dba['profile'].find_one({"_id":ctx.author.id}) or {}
        results['weight'] = kg
        await self.bot.dba['profile'].replace_one({"_id":ctx.author.id}, results, True)
        results = await self.bot.dba['profile'].find_one({"_id":ctx.author.id})
        weightdb = results['weight']
        await ctx.reply(f"Your weight has been set to {weightdb} kg.")

    @set.command(name="height", aliases=['h]'])
    async def setheight(self, ctx, cm:int):
        """Sets your own height."""
        results = await self.bot.dba['profile'].find_one({"_id":ctx.author.id}) or {}
        results['height'] = cm
        await self.bot.dba['profile'].replace_one({"_id":ctx.author.id}, results, True)
        results = await self.bot.dba['profile'].find_one({"_id":ctx.author.id}) 
        heightdb = results['height']
        await ctx.reply(f"Your height has been set to {heightdb} cm.")
    
    @set.command(name="birthday", aliases=['b', 'bd', 'bday'])
    async def setbd(self, ctx, *, birthday:str):
        """Sets your own birthday."""
        user_input = birthday
        settings = {
            'TIMEZONE': 'UTC',
            'RETURN_AS_TIMEZONE_AWARE': True,
            'TO_TIMEZONE': 'UTC',
            'PREFER_DATES_FROM': 'future'
        }
        to_be_passed = f"in {user_input}"
        split = to_be_passed.split(" ")
        length = len(split[:7])
        out = None
        used = ""
        for i in range(length, 0, -1):
            used = " ".join(split[:i])
            out = dateparser.parse(used, settings=settings)
            if out is not None:
                break
        if out is None:
            raise commands.BadArgument('Provided time is invalid')
        now = ctx.message.created_at
        time = out.replace(tzinfo=now.tzinfo), ''.join(to_be_passed).replace(used, '')
        timestamp=time[0].timestamp()
        results = await self.bot.dba['profile'].find_one({"_id":ctx.author.id}) or {}
        results['bd'] = timestamp
        await self.bot.dba['profile'].replace_one({"_id":ctx.author.id}, results, True)
        results = await self.bot.dba['profile'].find_one({"_id":ctx.author.id})
        bd = datetime.datetime.fromtimestamp(results['bd'])
        await ctx.reply(f"Your birthday has been set to {bd}.")

    @commands.command(name="profile", aliases=['bmi'])
    async def profile(self, ctx, member:discord.Member=None):
        """Gets the profile of a member."""
        if member is None:
            member = ctx.author
        if await self.bot.dba['profile'].count_documents({"_id":member.id}) > 0:
            results= await self.bot.dba['profile'].find_one({"_id":member.id})
            try:
                weight = results["weight"]
            except:
                await self.bot.dba['profile'].update_one({"_id":member.id}, {"$inc":{"weight":0}}, True)
                weight = 0
            try:
                height = results['height']
            except:
                await self.bot.dba['profile'].update_one({"_id":member.id}, {"$inc":{"height":0}}, True)
                height = 0
            try:
                bd = results['bd']
            except:
                bd = member.joined_at.timestamp()
                await self.bot.dba['profile'].update_one({"_id":member.id}, {"$inc":{"bd":bd}}, True)
                bd = 0
        else:
            bd = member.joined_at.timestamp()
            await self.bot.dba['profile'].update_one({"_id":member.id}, {"$inc":{"weight":0, "height":0, 'bd':bd}}, True)
            weight = 0
            height = 0
            bd = 0
        try:
            bmi = weight / (height/100)**2
        except:
            bmi = 0
        if bmi <= 18.4:
            status="underweight"
        elif bmi <= 24.9:
            status="healthy"
        elif bmi <= 29.9:
            status="overweight"
        elif bmi <= 34.9:
            status="severely overweight"
        elif bmi <= 39.9:
            status="obese"
        else:
            status="severely obese"

        birthday = datetime.datetime.fromtimestamp(bd)
        
        embed=discord.Embed(title="Profile", color=discord.Color.random())
        embed.set_author(icon_url=member.avatar_url, name=member.display_name)
        embed.add_field(name="BMI", value=f"Height : {height} cm\nWeight : {weight} kg\nBMI : {bmi} ({status})")
        embed.set_footer(text="Birthday: ")
        embed.timestamp=birthday
        await ctx.reply(embed=embed, mention_author=True)

    
def setup(bot):
    bot.add_cog(profileCog(bot))