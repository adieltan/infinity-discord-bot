import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime, dateparser, motor.motor_asyncio
from discord.ext import commands


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
        await self.bot.dba['profile'].update_one({"_id":ctx.author.id}, {"$inc":{"weight":kg}}, True)
        results = await self.bot.dba['profile'].find_one({"_id":ctx.author.id})
        weightdb = results['weight']
        await ctx.reply(f"Your weight has been set to {weightdb} kg.")

    @set.command(name="height", aliases=['h]'])
    async def setheight(self, ctx, cm:int):
        """Sets your own height."""
        await self.bot.dba['profile'].update_one({"_id":ctx.author.id}, {"$inc":{"height":cm}}, True)
        results = await self.bot.dba['profile'].find_one({"_id":ctx.author.id})
        heightdb = results['height']
        await ctx.reply(f"Your height has been set to {heightdb} cm.")

    @commands.command(name="profile")
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
        else:
            await self.bot.dba['profile'].update_one({"_id":member.id}, {"$inc":{"weight":0, "height":0}}, True)
            weight = 0
            height = 0
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

        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="Profile", color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=member.avatar_url, name=member.display_name)
        embed.add_field(name="BMI", value=f"Height : {height} cm\nWeight : {weight} kg\nBMI : {bmi} ({status})")
        await ctx.reply(embed=embed, mention_author=True)

    
def setup(bot):
    bot.add_cog(profileCog(bot))