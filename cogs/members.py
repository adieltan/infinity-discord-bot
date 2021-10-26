import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

import dateparser, pycountry
class UsersCog(commands.Cog, name='User'):
    """👤 Information / function about Users."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="selfharm", aliases=["suicide", 'die'])
    async def selfharm(self, ctx, victim:discord.Member=None):
        """Gives you awareness about selfharm and useful contacts."""
        if not victim:
            victim = ctx.author
        embed=discord.Embed(title="Suicide & Selfharm Prevention", url="https://www.who.int/health-topics/suicide", description="You are not alone. Everyone is special in their own ways and thats why you shouldn't give up.", color=discord.Color.blurple())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        embed.add_field(name="Get some help today.", value='[Suicide prevention](https://www.who.int/health-topics/suicide)\n[Contact Numbers](https://www.opencounseling.com/suicide-hotlines)\n[Crisis Lines](https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines)',)
        embed.set_thumbnail(url="https://www.nursingcenter.com/getattachment/NCBlog/September-2016-(1)/World-Suicide-Prevention-Day/2016_wspd_ribbon_250X250.png.aspx?width=200&height=200")
        embed.set_image(url="https://sm.mashable.com/mashable_me/photo/default/gettyimages-6130324100_675p.jpg")
        try:
            await victim.send(embed=embed)
        except:
            await ctx.reply(f"Error sending message to {victim.mention}")
        else:
            await ctx.message.add_reaction("<a:verified:876075132114829342>")

    @commands.group(name="profile", aliases=['me'], invoke_without_command=True)
    async def profile(self, ctx, member:discord.User=None):
        """Gets the profile of yourself / another user."""
        if not member:
            member = ctx.author
        results= await self.bot.dba['profile'].find_one({"_id":member.id})
        if not results:
            return await ctx.reply('This user does not have a profile.')
        embed=discord.Embed(title="Profile", description="\u200b", color=discord.Color.random())
        embed.set_author(icon_url=member.avatar, name=member.display_name)
        embed.set_thumbnail(url=member.avatar)
        weight = results.get('weight')
        height = results.get('height')
        bd = results.get('bd')
        if weight and height:
            bmi = weight / (height/100)**2
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
            embed.add_field(name="BMI", value=f"📏 {height} cm\n⚖️ {weight} kg\nBMI: **{round(bmi, 2)}** ({status})")
        if results.get('country'):
            fuz = pycountry.countries.search_fuzzy(results.get('country'))
            embed.add_field(name="Location", value=f":flag_{fuz[0].alpha_2.lower()}: {fuz[0].name}" + '\n')
        if bd:
            embed.add_field(name='Birthday', value=f"{discord.utils.format_dt(datetime.datetime.fromtimestamp(bd), style='D')}")
        if member.id in self.bot.owner_ids:
            embed.description += '<a:crown:902048071343538176> **Bot Owner**\n'
        if results.get('bl'):
            embed.description += '<:exclamation:876077084986966016> **Blacklisted**\n'
        if results.get('manager'):
            embed.description += '<a:infinity:874548940610097163> **Infinity Managers**\n'
        premium = results.get('premium')
        if premium:
            if type(premium) is float and premium < round(discord.utils.utcnow().timestamp()):
                return
            embed.description += f"<:infinity_coin:874548715338227722> **Premium User** {f'until <t:{premium}:d>'if type(premium) is int else ''}"

        await ctx.reply(embed=embed)

    @profile.command(name='delete')
    async def setdelete(self, ctx):
        """Deletes your profile data."""
        await self.bot.dba['profile'].delete_one({'_id':ctx.author.id})
        await ctx.reply('Profile deleted.')

    @profile.command(name="weight", aliases=['w'])
    async def setweight(self, ctx, kilograms:float):
        """Sets your own weight."""
        await self.bot.dba['profile'].update_one({"_id":ctx.author.id}, {"$set": {'weight':round(kilograms)}}, True)
        profile = await self.bot.dba['profile'].find_one({'_id':ctx.author.id}) or {}
        await ctx.reply(f"Your weight has been set to {profile.get('weight')} kg.")

    @profile.command(name="height", aliases=['h'])
    async def setheight(self, ctx, centimeters:float):
        """Sets your own height."""
        await self.bot.dba['profile'].update_one({"_id":ctx.author.id}, {"$set": {'height':round(centimeters)}}, True)
        profile = await self.bot.dba['profile'].find_one({"_id":ctx.author.id}) or {}
        await ctx.reply(f"Your height has been set to {profile.get('height')} cm.")
    
    @profile.command(name="country", aliases=['c'])
    async def setcountry(self, ctx, *, country:str):
        """Sets your country."""
        fuzzy = pycountry.countries.search_fuzzy(country)
        await self.bot.dba['profile'].update_one({"_id":ctx.author.id}, {"$set": {'country':fuzzy[0].name}}, True)
        profile = await self.bot.dba['profile'].find_one({"_id":ctx.author.id}) or {}
        await ctx.reply(f"Your country has been set to {profile.get('country')}")

    @profile.command(name="birthday", aliases=['b', 'bd', 'bday'])
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
        if not out:
            raise commands.BadArgument('Provided time is invalid')
        now = ctx.message.created_at
        time = out.replace(tzinfo=now.tzinfo), ''.join(to_be_passed).replace(used, '')
        timestamp=time[0].timestamp()
        await self.bot.dba['profile'].update_one({"_id":ctx.author.id}, {"$set": {'bd':timestamp}}, True)
        profile = await self.bot.dba['profile'].find_one({"_id":ctx.author.id}) or {}
        bd = datetime.datetime.fromtimestamp(profile.get('bd'))
        await ctx.reply(f"Your birthday has been set to {bd}.")

def setup(bot):
    bot.add_cog(UsersCog(bot))