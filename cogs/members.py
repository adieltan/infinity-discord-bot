import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

import dateparser, pycountry
from ._utils import Database

from discord.commands import user_command
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

        results= await Database.get_user(self, member.id)
        if not results:
            return await ctx.reply('This user does not have a profile.')
        embed=discord.Embed(title="Profile", description="", color=discord.Color.random())
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
            embed.add_field(name='Birthday', value=f"<t:{round(bd)}:D>")
        if member.id in self.bot.owner_ids:
            embed.description += '<a:crown:902048071343538176> **Bot Owner**\n'
        if results.get('bl'):
            embed.description += '<:exclamation:876077084986966016> **Blacklisted**\n'
        if results.get('manager'):
            embed.description += '<a:infinity:874548940610097163> **Infinity Managers**\n'
        premium = results.get('premium', False)
        if premium is True or premium > round(discord.utils.utcnow().timestamp()):
            embed.description += f"<:infinity_coin:874548715338227722> **Premium User** {f'until <t:{premium}:d>'if type(premium) is int else ''}"
        if results.get('bio'):
            embed.add_field(name="Bio", value=f"{results.get('bio')}\n", inline=False)
        await ctx.reply(embed=embed)

    @profile.command(name='delete')
    async def setdelete(self, ctx):
        """Deletes your profile data."""
        await Database.del_user(self, ctx.author.id)
        await ctx.reply('Profile deleted.')

    @profile.command(name="weight", aliases=['w'])
    async def setweight(self, ctx, kilograms:int):
        """Sets your own weight."""
        await Database.edit_user(self, ctx.author.id, {'weight':kilograms})
        await ctx.reply(f"Your weight has been set to {kilograms} kg.")

    @profile.command(name="height", aliases=['h'])
    async def setheight(self, ctx, centimeters:int):
        """Sets your own height."""
        await Database.edit_user(self, ctx.author.id, {'height':centimeters})
        await ctx.reply(f"Your height has been set to {centimeters} cm.")
    
    @profile.command(name="country", aliases=['c'])
    async def setcountry(self, ctx, *, country:str):
        """Sets your country."""
        fuz = pycountry.countries.search_fuzzy(country)
        await Database.edit_user(self, ctx.author.id, {'country':fuz[0].name})
        await ctx.reply(f"Your country has been set to {fuz[0].name}")

    @profile.command(name='biography', aliases=['bio'])
    async def setbiography(self, ctx, *, bio:str):
        """Sets your biography."""
        if len(bio) > 200:
            return await ctx.reply(f"You bio is too long. ({len(bio)}/200 characters)")
        await Database.edit_user(self, ctx.author.id, {'bio':discord.utils.remove_markdown(bio)})
        await ctx.reply(f"Your bio has been set to ```\n{bio}\n```")

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
        timestamp=round(time[0].timestamp())
        await Database.edit_user(self, ctx.author.id, {'bd':timestamp})
        await ctx.reply(f"Your birthday has been set to <t:{timestamp}:D>.")

    @user_command(name='Profile')
    async def app_profile(self, ctx, member: discord.Member):
        """User command for showing profile."""
        results= await Database.get_user(self, member.id)
        if not results:
            return await ctx.respond('This user does not have a profile.')
        embed=discord.Embed(title="Profile", description="", color=discord.Color.random())
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
            embed.add_field(name='Birthday', value=f"<t:{round(bd)}:D>")
        if member.id in self.bot.owner_ids:
            embed.description += '<a:crown:902048071343538176> **Bot Owner**\n'
        if results.get('bl'):
            embed.description += '<:exclamation:876077084986966016> **Blacklisted**\n'
        if results.get('manager'):
            embed.description += '<a:infinity:874548940610097163> **Infinity Managers**\n'
        premium = results.get('premium', False)
        if premium is True or premium > round(discord.utils.utcnow().timestamp()):
            embed.description += f"<:infinity_coin:874548715338227722> **Premium User** {f'until <t:{premium}:d>'if type(premium) is int else ''}"
        if results.get('bio'):
            embed.add_field(name="Bio", value=f"{results.get('bio')}\n", inline=False)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(UsersCog(bot))