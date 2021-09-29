import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle
import matplotlib.pyplot as plt
 
import dateparser, pytz
from discord.http import Route
from discordTogether import DiscordTogether
import qrcode
from translate import Translator

from py_expression_eval import Parser
from fractions import Fraction
parser = Parser()

import lxml.html as lh

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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        if payload.event_type == "REACTION_ADD" and payload.emoji.name == "🔖" and payload.member is not None:
            try:
                message_channel = self.bot.get_channel(payload.channel_id)
                m = await message_channel.fetch_message(payload.message_id)
                try:m.clean_content
                except:content = None
                else:content = m.clean_content
                embed=discord.Embed(title="Bookmark", description=f"You have bookmarked [this message]({m.jump_url}) on <t:{round(m.created_at.timestamp())}>\nAt {message_channel.mention} in {m.guild.name}", timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(0,255,255))
                embed.set_author(name=m.author.name, icon_url=m.author.avatar_url)
                embed.set_footer(text=m.guild.name, icon_url=m.guild.icon_url)
                embed.add_field(name="Remark", value="Reply to this message with `remark <remark>` to add your remark.", inline=False)
                message = await payload.member.send(content=content, embed=embed)
                pins = await payload.member.dm_channel.pins()
                if len(pins)>=50:
                    pins.reverse()
                    await pins[0].unpin()
                    await pins[0].reply("This message has been unpinned due to the pin limit in this channel.")
                await message.pin()
                history = await payload.member.dm_channel.history(limit=1).flatten()
                await history[0].delete()
            except:pass
        else:
            pass

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
        
    @commands.command(name="define", aliases=["meaning"])
    @commands.cooldown(1,3, commands.BucketType.guild)
    async def define(self, ctx, *, phrase:str):
        """Defines a word."""
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as cs:
            header={'Authorization':f"Token {os.getenv('owlbot')}"}
            async with cs.get(url=f"https://owlbot.info/api/v4/dictionary/{phrase}", headers=header) as data:
                json = await data.json()
        await cs.close()
        if type(json) is list:
            json = json[0]
        if json.get('detail') is not None:
            await ctx.reply(f"{json.get('detail')}")
        elif json.get('message') is not None:
            await ctx.reply(f"{json.get('message')}")
        else:
            embed=discord.Embed(title=json.get('word'), description=f"*Pronounciation:* {json.get('pronounciation')}", color=discord.Color.random())
            for defi in json.get('definitions'):
                if defi.get('image_url') is not None:
                    embed.set_thumbnail(url=defi.get('image_url'))
                if defi.get('emoji') is None:
                    defi['emoji'] = ''
                text = ""
                if defi.get('definition') is not None:
                    definition = str(defi.get('definition'))
                    definition = definition.replace('<b>', '**')
                    definition = definition.replace('</b>', '**')
                    definition = definition.replace('<i>', '*')
                    definition = definition.replace('</i>', '*')
                    text += f"\nDefinition: \u2800{definition}"
                if defi.get('example') is not None:
                    example = str(defi.get('example'))
                    example = example.replace('<b>', '**')
                    example = example.replace('</b>', '**')
                    example = example.replace('<i>', '*')
                    example = example.replace('</i>', '*')
                    text += f"\nEg: \u2800\u2800\u2800\u2800\u2800{example}"
                embed.add_field(name=f"{defi.get('emoji')} {defi.get('type')}", value=text, inline=False)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="translate", aliases=['tr'])
    @commands.cooldown(1,6)
    async def translate(self, ctx,language:str, *,text:str):
        """Translates a term."""
        translator= Translator(to_lang=language)
        translation = translator.translate(f"{text}")
        embed=discord.Embed(title="Translator", description=f"{text}", color=discord.Color.random())
        embed.add_field(name=language, value=translation, inline=False)
        await ctx.reply(embed=embed)

    @commands.command(name='qrcode', aliases=['qr'])
    @commands.cooldown(1,6)
    async def qr(self, ctx, *,text:str=None):
        """Generates a qr code."""
        ctx.typing()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=3)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        f = discord.File(buffer, filename="qr.png")
        
        embed=discord.Embed(title="Qr Generator", description=f"{text}", color=discord.Color.random())
        embed.set_image(url="attachment://qr.png")
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(file=discord.File(buffer, filename="qr.png"), embed=embed, mention_author=True)

    @commands.group(name='morse', invoke_without_command=True)
    async def morse(self, ctx, *, text:str):
        """Encodes the text to morse code."""
        morse = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-', ' ':' '}
        txt = text.upper()
        cipher = '' 
        for letter in txt: 
            cipher += morse[letter] + ' '
        embed=discord.Embed(title=text, description=cipher, color=discord.Color.random())
        embed.set_footer(text="Morse Encoder")
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=True)

    @morse.command(name='decode', aliases=['de'])
    async def morse_to_eng(self, ctx, *, morsecode:str): 
        """Decodes the morse code to text."""
        morse = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'}
        morsecode += ' '
        decipher = '' 
        citext = '' 
        for letter in morsecode: 
            # checks for space 
            if (letter != ' '): 
                # counter to keep track of space 
                i = 0
                # storing morse code of a single character 
                citext += letter 
            # in case of space 
            else: 
                # if i = 1 that indicates a new character 
                i += 1
                # if i = 2 that indicates a new word 
                if i == 2 : 
                    # adding space to separate words 
                    decipher += ' '
                else: 
                    # accessing the keys using their values (reverse of encryption) 
                    decipher += list(morse.keys())[list(morse.values()).index(citext)] 
                    citext = '' 
        embed=discord.Embed(title="Morse Decoder", description=decipher, color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=True)


    @commands.group(name= 'binary', aliases=['bin'], invoke_without_command=True)
    @commands.cooldown(1,3)
    async def bin (self, ctx, *, input:str):
        """Find the binary form of a text"""
        binlist = [bin(ord(n))[2:] for n in input]
        text = ''
        for b in binlist:
            text = text + ' ' + b
        
        embed=discord.Embed(title="Binary converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @bin.command(name= 'decode', aliases=['de'])
    @commands.cooldown(1,3)
    async def binde (self, ctx, *, input:str):
        """Find the binary form of a text reversed"""
        binlist = input.split(' ')
        text = ''
        for b in binlist:
            b = int(b, 2)
            text = text + chr(b)
        
        embed=discord.Embed(title="Binary converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.group(name= 'hexadecimal', aliases=['hex'], invoke_without_command=True)
    @commands.cooldown(1,3)
    async def hex (self, ctx, *, input:str):
        """Find the hexadecimal form of a text"""
        binlist = [hex(ord(n))[2:] for n in input]
        text = ''
        for b in binlist:
            text = text + ' ' + b
        
        embed=discord.Embed(title="Hexadecimal converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @hex.command(name= 'decode', aliases=['de'])
    @commands.cooldown(1,3)
    async def hexde (self, ctx, *, input:str):
        """Find the hexadecimal form of a text reversed"""
        binlist = input.split(' ')
        text = ''
        for b in binlist:
            b = int(b, 16)
            text = text + chr(b)
        
        embed=discord.Embed(title="Hexadecimal converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.group(name= 'octadecimal', aliases=['oct'], invoke_without_command=True)
    @commands.cooldown(1,3)
    async def oct (self, ctx, *, input:str):
        """Find the octadecimal form of a text"""
        binlist = [oct(ord(n))[2:] for n in input]
        text = ''
        for b in binlist:
            text = text + ' ' + b
        
        embed=discord.Embed(title="Octadecimal converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @oct.command(name= 'decode', aliases=['de'])
    @commands.cooldown(1,3)
    async def octde (self, ctx, *, input:str):
        """Find the octadecimal form of a text reversed"""
        binlist = input.split(' ')
        text = ''
        for b in binlist:
            b = int(b, 8)
            text = text + chr(b)
        
        embed=discord.Embed(title="Octadecimal converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='calc', aliases=['c', '='])
    @commands.cooldown(1,2)
    async def calc (self, ctx, *, input):
        """Evaluates a maths equation."""
        inp = input.replace(",", "")
        try:
            out = parser.parse(inp).evaluate({})
            formatted = format(out, ',')
            floated = "{:e}".format(out)
            frac = Fraction(out).limit_denominator()
            await ctx.reply(f'```json\n{input} = \n{out}\n```Formatted : **{formatted}**\nSci               : **{floated}**\nFraction     : **{frac}**', mention_author=False)
            
        except:
            embed=discord.Embed(title="Calc Help", description="Usable expressions\n `+` `-` `*` `/` `%` `^` `PI` `E` `sin(x)` `cos(x)` `tan(x)` `asin(x)` `acos(x)` `atan(x)` `log(x)` `log(x, base)` `abs(x)` `ceil(x)` `floor(x)` `round(x)` `exp(x)` `and` `or` `xor` `not` `in`") 
            embed.set_footer(text=f'Requested by {ctx.author}')
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="amari", aliases=['amarigraph'])
    async def amari(self, ctx, serverid:int=None):
        """Plots the xp of the server's amari data in a chart."""
        try:
            async with ctx.typing():
                rank = []
                xp = []
                if serverid is None:
                    serverid = ctx.guild.id
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(url=f"https://lb.amaribot.com/index.php?gID={serverid}") as data:
                        #soup = BeautifulSoup(data.text, "html.parser")
                        doc = lh.fromstring(await data.text())
                tr_elements = doc.xpath('//tr')
                firstxp = int(tr_elements[0][2].text_content())
                for t in tr_elements:
                    rawrank=int(t[0].text_content())
                    rawxp = int(t[2].text_content())
                    if rawxp < (firstxp*0.005):
                        break
                    else:
                        rank.append(rawrank)
                        xp.append(rawxp)
                plt.plot(rank, xp, label = "xp")
                plt.xlabel('Rank')
                plt.ylabel('XP')
                plt.title(f"{serverid}'s Amari Xp")
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                f = discord.File(fp=buf, filename="image.png")
                embed=discord.Embed(title=f"{serverid}'s Amari Xp", url=f"https://lb.amaribot.com/index.php?gID={serverid}")
                embed.set_image(url="attachment://image.png")
                embed.timestamp=datetime.datetime.utcnow()
                await ctx.reply(file=f, embed=embed)
                plt.close()
                buf.close()
                await cs.close()
        except:
            await ctx.reply(f"Error\nCommon Issues: There is no amari data in the server.")

    @commands.command(name="youtubestats", aliases=['ytstats'])
    async def youtubestats(self, ctx, channelid:str):
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url=f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channelid}&key={os.getenv('googleapi')}") as data:
                    json = await data.json()
                    items = json.get('items')
            await cs.close()
            try:
                id=items[0]['id']
                stats= items[0]['statistics']
                embed=discord.Embed(title="Youtube Statistics", url=f"https://youtube.com/channel/{channelid}", description=f"{id}")
                embed.add_field(name="Subscribers", value=f"{format(int(stats['subscriberCount']), ',')}")
                embed.add_field(name="View Count", value=f"{format(int(stats['viewCount']), ',')}")
                embed.add_field(name="Video Count", value=f"{format(int(stats['videoCount']), ',')}")
                embed.set_footer(text="Google API")
                await ctx.reply(embed=embed)
            except:
                await ctx.reply(f"Error.\nCommon causes: Invalid channel id")

def setup(bot):
    bot.add_cog(utilityCog(bot))