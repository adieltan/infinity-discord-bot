import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 
import dateparser, pytz
from discord.http import Route
from discordTogether import DiscordTogether
class utilityCog(commands.Cog, name='utility'):
    """*Utility commands for server.*"""
    def __init__(self, bot):
        self.bot = bot
        self.togetherControl = DiscordTogether(bot)
        
    @commands.command(name='cleandm')
    @commands.dm_only()
    async def cleandm(self, ctx):
        """Cleans the messages in your dm with the bot."""
        history = await ctx.author.dm_channel.history(limit=None).flatten()
        for message in history:
            if message.pinned is False:
                try:
                    await message.delete()
                except:pass
        await ctx.message.add_reaction("<a:verified:876075132114829342>")

    @commands.command(name="remark")
    @commands.dm_only()
    async def remark(self, ctx, *, remark:str):
        """Adds a remark to the referenced bookmark."""
        ref = ctx.message.reference
        if ref == None:
            await ctx.reply("Eh you gotta reply to the message you wanna add a remark!", mention_author=True)
        else:
            message = await ctx.channel.fetch_message(ref.message_id)
            try:
                embed = message.embeds[0]
                embed.add_field(name="Remark", value=remark, inline=False)
                await message.edit(embed=embed)
                await ctx.message.add_reaction("<a:verified:876075132114829342>")
            except:await ctx.reply("Error")

    @commands.command(name="bookmark")
    @commands.guild_only()
    async def bookmarkinfo(self, ctx):
        """Info about the bookmarking system."""
        embed=discord.Embed(title="Bookmark System", description="React to a message with :bookmark: to bookmark the message.\nThe bot will send and pin a message in your dms which contain the content and jump link to the message you bookmarked.\nRefering to the bookmark message with `remark <remark>` can add a field to the embed containing the remark you made.")
        await ctx.reply(embed=embed)

    @commands.command(name='time')
    @commands.cooldown(1,2)
    async def time(self, ctx, *, expression:str): 
        """Time."""
        user_input = expression
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
        embed=discord.Embed(title="Time", description=expression)
        embed.timestamp=time[0]
        try:
            ts = time[0].timestamp()
        except:
            pass
        try:
            embed.set_footer(text=ts)
        except:
            pass
        await ctx.reply(f"{time[0]}",embed=embed)

    @commands.command(name='creationdate', aliases=['createdate', 'created'])
    @commands.cooldown(1,2)
    async def created(self, ctx, argument:str): 
        """Time the snowflake id was created."""
        arg = int(re.sub("[^0-9]", "", argument))
        time = discord.utils.snowflake_time(arg)
        embed=discord.Embed(title="Creation Date Checker", description=argument)
        embed.timestamp=time
        try:
            ts = time.timestamp()
        except:
            pass
        try:
            embed.set_footer(text=ts)
        except:
            pass
        await ctx.reply(f"{time} <t:{round(time.timestamp())}>",embed=embed)

    @commands.command(name="weather", aliases=['w', 'temperature', 'climate', 'windspeed', 'rain', 'snow', 'humidity'])
    @commands.cooldown(1,5)
    async def weather(self, ctx, *, city_name:str):
        """Weather infomation."""
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url=f"http://api.openweathermap.org/data/2.5/weather?appid=e18ed14fc4fe401e9b9133ef3e1ccee6&units=metric&q={city_name}") as w:
                x = await w.json()
        if x["cod"] != "404":
            y = x["main"]
            try:current_temperature = y["temp"]
            except:current_temperature=None
            try:current_pressure = y["pressure"]
            except:current_pressure=None
            try:current_humidity = y["humidity"]
            except:current_humidity=None
            z = x["weather"]
            weather_description = z[0]["description"]
            sys = x['sys']
            embed = discord.Embed(title=f"Weather in {x['name']}",description=f"**Country**: {sys['country']}\n**Coordinates:** {x['coord']['lon']}, {x['coord']['lat']}", color=discord.Colour.random(),timestamp=datetime.datetime.fromtimestamp(x['dt'], pytz.timezone("UTC")))
            embed.set_footer(text="Updated on")
            embed.add_field(name="Description", value=f"{weather_description}", inline=False)
            embed.add_field(name="Temperature", value=f"{current_temperature}°C", inline=True)
            embed.add_field(name="Humidity(%)", value=f"{current_humidity}%", inline=True)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"{current_pressure} hPa", inline=False)
            try:windspeed = x['wind']['speed']
            except:windspeed = None
            try:windheading = x['wind']['deg']
            except:windheading = None
            try:windgust = x['wind']['gust']
            except: windgust= None
            embed.add_field(name="Wind", value=f"Speed: {windspeed} m/s\nHeading: {windheading}°\nGust: {windgust} m/s", inline=False)
            embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{z[0]['icon']}@2x.png")
            {"coord":{"lon":101.9381,"lat":2.7297},"weather":[{"id":501,"main":"Rain","description":"moderate rain","icon":"10d"}],"base":"stations","main":{"temp":303.66,"feels_like":310.66,"temp_min":302.81,"temp_max":304.9,"pressure":1007,"humidity":78,"sea_level":1007,"grnd_level":1001},"visibility":10000,"wind":{"speed":1.52,"deg":229,"gust":2.94},"rain":{"1h":2.37},"clouds":{"all":94},"dt":1624614690,"sys":{"type":2,"id":131486,"country":"MY","sunrise":1624575985,"sunset":1624620187},"timezone":28800,"id":1734810,"name":"Seremban","cod":200}
        else:
            embed=discord.Embed(title="City Not Found", description=f"{city_name} is not found.", color=discord.Colour.red())
        await ctx.reply(embed=embed, mention_author=False)
        await cs.close()

    @commands.command(name='app')
    async def app(self, ctx, activity=None, voicechannel=None):
        """Discord Party Games"""
        defaultApplications = {  # Credits to RemyK888
            'youtube': '755600276941176913',
            'poker': '755827207812677713',
            'betrayal': '773336526917861400',
            'fishing': '814288819477020702',
            'chess': '832012586023256104'
            }
        if activity not in defaultApplications.keys():
            avi = '\n'.join(defaultApplications.keys())
            await ctx.reply(f"**Avalible activities:**\n{avi}")
            return
        if voicechannel is None:
            try:
                voicechannelid = ctx.author.voice.channel.id
            except:
                await ctx.reply(f"You have to join a voice channel first.")
                return
        else:
            voicechannelid = int(re.sub("[^0-9]", "", voicechannel))
        if activity and (str(activity).lower().replace(" ", "") in defaultApplications.keys()):   

            data = {
                'max_age': 86400,
                'max_uses': 0,
                'target_application_id': defaultApplications[str(activity).lower().replace(" ","")],
                'target_type': 2,
                'temporary': False,
                'validate': None
            }
            
            try:
                result = await self.bot.http.request(
                    Route("POST", f"/channels/{voicechannelid}/invites"), json = data
                )
            #Error Handling
            except Exception as e:
                if "10003" in str(e):
                    raise discord.InvalidArgument("Voice Channel ID is invalid.")
                elif "50013" in str(e):
                    raise discord.InvalidArgument("Bot can't create link to the channel.")  
                elif "130000" in str(e):
                    raise ConnectionError("API resource is currently overloaded. Try again a little later.")      
                else:
                    raise ConnectionError("An error occurred while retrieving data from Discord API.")
            
            await ctx.send(f"Click on the blue link. <#{voicechannelid}>\nhttps://discord.com/invite/{result['code']}")

    @commands.command(name="youtube", aliases=['yt'])
    async def youtube(self, ctx):
        """Discord Party Games"""
        try:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
            await ctx.send(f"Click the blue link!\n{link}")
        except:
            await ctx.reply(f"You have to join a voice channel first.")

    @commands.command(name="fishing")
    async def fishing(self, ctx):
        """Discord Party Games"""
        try:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'fishing')
            await ctx.send(f"Click the blue link!\n{link}")
        except:
            await ctx.reply(f"You have to join a voice channel first.")

    @commands.group(name="poll", invoke_without_command=True)
    @commands.bot_has_permissions(add_reactions=True)
    async def poll(self, ctx,*, question):
        """Creates a simple poll."""
        embed=discord.Embed(title="Simple Poll", description=f"{ctx.author.mention} asks: **{question}**", color=discord.Color.random())
        msg = await ctx.reply(embed=embed, mention_author=False)
        await msg.add_reaction("\U0001f44d")
        await msg.add_reaction("\U0001f44e")

    @poll.command(name="check")
    @commands.bot_has_permissions(add_reactions=True)
    async def checkpoll(self, ctx,*, question):
        """Poll to see how many people supports it."""
        embed=discord.Embed(title="Check Poll", description=f"{ctx.author.mention} asks: **{question}**", color=discord.Color.random())
        msg = await ctx.reply(embed=embed, mention_author=False)
        await msg.add_reaction("<a:verified:876075132114829342>")

def setup(bot):
    bot.add_cog(utilityCog(bot))