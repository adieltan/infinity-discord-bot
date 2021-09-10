import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 

import dateparser, pycountry

class profileCog(commands.Cog, name='profile'):
    """*User based commands.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def set(self,ctx):
        """Sets up your own profile."""
        if ctx.invoked_subcommand is None:
            await ctx.reply("Available subcommands are `weight` , `height` , `country` & `birthday` .")

    @set.command(name='delete')
    async def setdelete(self, ctx):
        """Deletes your profile data."""
        await self.bot.dba['profile'].delete_one({'_id':ctx.author.id})
        await ctx.reply(f"Profile deleted.")

    @set.command(name="weight", aliases=['w'])
    async def setweight(self, ctx, kilogram):
        """Sets your own weight."""
        kg = int(re.sub("[^0-9]", "", kilogram))
        await self.bot.dba['profile'].update_one({"_id":ctx.author.id}, {"$set": {'weight':kg}}, True)
        profile = await self.bot.dba['profile'].find_one({'_id':ctx.author.id}) or {}
        await ctx.reply(f"Your weight has been set to {profile.get('weight')} kg.")

    @set.command(name="height", aliases=['h'])
    async def setheight(self, ctx, centimeters):
        """Sets your own height."""
        cm = int(re.sub("[^0-9]", "", centimeters))
        await self.bot.dba['profile'].update_one({"_id":ctx.author.id}, {"$set": {'height':cm}}, True)
        profile = await self.bot.dba['profile'].find_one({"_id":ctx.author.id}) or {}
        await ctx.reply(f"Your height has been set to {profile.get('height')} cm.")
    
    @set.command(name="country", aliases=['c'])
    async def setcountry(self, ctx, *, country:str):
        """Sets your country."""
        fuzzy = pycountry.countries.search_fuzzy(country)
        await self.bot.dba['profile'].update_one({"_id":ctx.author.id}, {"$set": {'country':fuzzy[0].name}}, True)
        profile = await self.bot.dba['profile'].find_one({"_id":ctx.author.id}) or {}
        await ctx.reply(f"Your country has been set to {profile.get('country')}")

    @set.command(name="birthday", aliases=['b', 'bd', 'bday'])
    async def setbd(self, ctx, *, birthday:str):
        """Sets your own birthday."""
        user_input = birthday
        settings = {
            'TIMEZONE': 'UTC',
            'RETURN_AS_TIMEZONE_AWARE': True,
            'TO_TIMEZONE': 'UTC',
            'PREFER_DATES_FROM': 'past'
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
        await self.bot.dba['profile'].update_one({"_id":ctx.author.id}, {"$set": {'bd':timestamp}}, True)
        profile = await self.bot.dba['profile'].find_one({"_id":ctx.author.id}) or {}
        bd = datetime.datetime.fromtimestamp(profile.get('bd'))
        await ctx.reply(f"Your birthday has been set to {bd}.")

    @commands.command(name="profile", aliases=['bmi'])
    async def profile(self, ctx, member:discord.User=None):
        """Gets the profile of a member."""
        if member is None:
            member = ctx.author
        results= await self.bot.dba['profile'].find_one({"_id":member.id})
        if results is None:
            await ctx.reply(f"This user does not have a profile.")
        else:
            weight = results.get('weight')
            height = results.get('height') 
            bd = results.get('bd')
            if weight is None:
                weight = 0
            if height is None:
                height = 0
            if bd is None:
                bd = 0

            try:
                bmi = weight / (height/100)**2
            except:
                bmi = 0
            if bmi == 0:
                status = "None"
            elif bmi <= 18.4:
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

            desc = "\u200B"
            loca = "\u200B"
            if results.get('bl'):
                desc += '<:exclamation:876077084986966016> **Blacklisted**' + '\n'
            if results.get('manager'):
                desc += '<a:infinity:874548940610097163> **Infinity Managers**' + '\n'
            if results.get('country'):
                fuzzy = pycountry.countries.search_fuzzy(results.get('country'))
                loca += f":flag_{fuzzy[0].alpha_2.lower()}: {fuzzy[0].name}" + '\n'
            
            embed=discord.Embed(title="Profile", description=desc, color=discord.Color.random())
            embed.set_author(icon_url=member.avatar_url, name=member.display_name)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="BMI", value=f"Height: {height} cm\nWeight: {weight} kg\n**BMI: {round(bmi, 2)} ({status})**")
            embed.add_field(name="Location", value=loca)
            embed.set_footer(text="Birthday: ")
            embed.timestamp=birthday
            await ctx.reply(embed=embed, mention_author=True)

    
def setup(bot):
    bot.add_cog(profileCog(bot))