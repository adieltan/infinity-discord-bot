import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

import dateparser, pytz
import qrcode

from py_expression_eval import Parser
from fractions import Fraction
parser = Parser()

class UtilityCog(commands.Cog, name='Utility'):
    """🛠️ Commands to improve user experience, draw data, integration with APIs."""
    def __init__(self, bot):
        self.bot = bot
        
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
        if not out:
            raise commands.BadArgument('Provided time is invalid')
        now = ctx.message.created_at
        time = out.replace(tzinfo=now.tzinfo), ''.join(to_be_passed).replace(used, '')
        embed=discord.Embed(title="Time", description=f"{time[0]} {expression}")
        embed.timestamp=time[0]
        embed.set_footer(text=f"{round(time[0].timestamp())}")
        styles = ['t', 'T', 'd', 'D', 'f', 'F', 'R']
        text = '\n'.join(discord.utils.format_dt(time[0], style=style) for style in styles)
        embed.add_field(name='Text Formatting', value=f"{text}\n```\n{text}\n```")
        await ctx.reply(embed=embed)

    @commands.command(name='creationdate', aliases=['createdate', 'created'])
    @commands.cooldown(1,2)
    async def created(self, ctx, argument:str): 
        """Time the snowflake id was created."""
        arg = int(re.sub("[^0-9]", "", argument))
        time = discord.utils.snowflake_time(arg)
        embed=discord.Embed(title="Creation Date Checker", description=argument)
        embed.timestamp=time
        embed.set_footer(text=round(time.timestamp()))
        await ctx.reply(discord.utils.format_dt(time),embed=embed)

    @commands.command(name="weather", aliases=['w', 'temperature', 'climate', 'windspeed', 'rain', 'snow', 'humidity'])
    @commands.cooldown(1,5)
    async def weather(self, ctx, *, city_name:str):
        """Weather infomation."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url=f"http://api.openweathermap.org/data/2.5/weather?appid=e18ed14fc4fe401e9b9133ef3e1ccee6&units=metric&q={city_name}") as w:
                x = await w.json()
        if x["cod"] != "404":
            y = x["main"]
            z = x["weather"]
            sys = x['sys']
            embed = discord.Embed(title=f"Weather in {x['name']}",description=f"**Country**: {sys['country']}\n**Coordinates:** {x['coord']['lon']}, {x['coord']['lat']}", color=discord.Colour.random(),timestamp=datetime.datetime.fromtimestamp(x['dt'], pytz.timezone("UTC")))
            embed.set_footer(text="Updated on")
            embed.add_field(name="Description", value=f"{z[0].get('description').title()}", inline=False)
            embed.add_field(name="Temperature", value=f"{y.get('temp')}°C", inline=True)
            embed.add_field(name="Humidity(%)", value=f"{y.get('humidity')}%", inline=True)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"{y.get('pressure')} hPa", inline=False)
            embed.add_field(name="Wind", value=f"Speed: {x.get('wind', {}).get('speed')} m/s\nHeading: {x.get('wind', {}).get('deg')}°\nGust: {x.get('wind', {}).get('gust')} m/s", inline=False)
            embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{z[0]['icon']}@2x.png")
        else:
            embed=discord.Embed(title="City Not Found", description=f"{city_name} is not found.", color=discord.Colour.red())
        await ctx.reply(embed=embed, mention_author=False)

    @commands.group(name="poll", invoke_without_command=True)
    @commands.bot_has_permissions(add_reactions=True)
    async def poll(self, ctx,*, question):
        """Creates a simple poll."""
        embed=discord.Embed(title="Simple Poll", description=f"{ctx.author.mention} asks: **{question}**", color=discord.Color.random())
        msg = await ctx.send(embed=embed, mention_author=False)
        await msg.add_reaction("\U0001f44d")
        await msg.add_reaction("\U0001f44e")
        await ctx.message.delete()

    @poll.command(name="check")
    @commands.bot_has_permissions(add_reactions=True)
    async def checkpoll(self, ctx,*, question):
        """Poll to see how many people supports it."""
        embed=discord.Embed(title="Check Poll", description=f"{ctx.author.mention} asks: **{question}**", color=discord.Color.random())
        msg = await ctx.send(embed=embed, mention_author=False)
        await msg.add_reaction("<a:verified:876075132114829342>")
        await ctx.message.delete()
        
    @commands.command(name="define", aliases=["meaning"])
    @commands.cooldown(1,3, commands.BucketType.guild)
    async def define(self, ctx, *, phrase:str):
        """Defines a word."""
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
                if not defi.get('emoji'):
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

    @commands.command(name='qrcode', aliases=['qr'])
    @commands.cooldown(1,6)
    async def qr(self, ctx, *,text:str=None):
        """Generates a qr code."""
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
        embed.timestamp=discord.utils.utcnow()
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
        cipher = ''.join(morse[letter] + ' ' for letter in txt)
        embed=discord.Embed(title=text, description=cipher, color=discord.Color.random())
        embed.set_footer(text="Morse Encoder")
        embed.timestamp=discord.utils.utcnow()
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
        embed.timestamp=discord.utils.utcnow()
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
        embed.timestamp=discord.utils.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @bin.command(name= 'decode', aliases=['de'])
    @commands.cooldown(1,3)
    async def binde(self, ctx, *, input:str):
        """Find the binary form of a text reversed"""
        binlist = input.split(' ')
        text = ''
        for b in binlist:
            b = int(b, 2)
            text += chr(b)

        embed=discord.Embed(title="Binary converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=discord.utils.utcnow()
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
        embed.timestamp=discord.utils.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @hex.command(name= 'decode', aliases=['de'])
    @commands.cooldown(1,3)
    async def hexde(self, ctx, *, input:str):
        """Find the hexadecimal form of a text reversed"""
        binlist = input.split(' ')
        text = ''
        for b in binlist:
            b = int(b, 16)
            text += chr(b)

        embed=discord.Embed(title="Hexadecimal converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=discord.utils.utcnow()
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
        embed.timestamp=discord.utils.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @oct.command(name= 'decode', aliases=['de'])
    @commands.cooldown(1,3)
    async def octde(self, ctx, *, input:str):
        """Find the octadecimal form of a text reversed"""
        binlist = input.split(' ')
        text = ''
        for b in binlist:
            b = int(b, 8)
            text += chr(b)

        embed=discord.Embed(title="Octadecimal converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=discord.utils.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='calc', aliases=['c', '='])
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
                await ctx.reply('Error.\nCommon causes: Invalid channel id')

    @commands.group(name='amari', aliases=['am'], invoke_without_command=True)
    async def amari(self, ctx):
        """Amari Api."""
        pass

    @amari.command(name='reward', aliases=['role', 'r'])
    @commands.cooldown(10, 1, commands.BucketType.member)
    @commands.bot_has_permissions(manage_roles=True)
    async def amari_reward(self, ctx, target:discord.Member=None):
        """Add and remove roles according to the member's rank in Amari's xp system."""
        if not target:
            target = ctx.author
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
            async with cs.get(url=f'https://amaribot.com/api/v1/guild/rewards/{ctx.guild.id}', headers={'Authorization':os.getenv('amari')}) as data:
                json = await data.json()
            async with cs.get(url=f"https://amaribot.com/api/v1/guild/{ctx.guild.id}/member/{target.id}", headers={'Authorization':os.getenv('amari')}) as data:
                user = await data.json()
        if not json.get('data'):
            return await ctx.reply("Guild has no Amari Reward Roles.")
        add = []
        remove = []
        for r in json['data']:
            role = ctx.guild.get_role(int(r['roleID']))
            if role > ctx.me.top_role:
                return await ctx.reply(f"Bot highest role below {role.mention}.", allowed_mentions=discord.AllowedMentions.none())
            if r['level'] < user['level'] and role not in target.roles:
                add.append(role)
            elif r['level'] > user['level'] and role in target.roles:
                remove.append(role)
        await target.add_roles(*add)
        await target.remove_roles(*remove)
        await ctx.reply(embed=discord.Embed(title="Amari Reward Roles", description=f"{target.mention}\nLevel {user['level']}", color=discord.Color.random()).add_field(name='Roles Added', value='\u200b' + '\n'.join(r.mention for r in add)).add_field(name='Roles Removed', value='\u200b' + '\n'.join(r.mention for r in remove)).set_thumbnail(url='https://amaribot.com/images/Logo.png'))

    @commands.group(name='space', invoke_without_command=True)
    async def space(self, ctx):
        """Returns the current number of people in space. """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
            async with cs.get(url='http://api.open-notify.org/astros.json') as data:
                json = await data.json()
            async with cs.get(url='http://api.open-notify.org/iss-now.json') as data:
                iss = await data.json()
            async with cs.get(url=f"https://api.nasa.gov/planetary/apod?api_key={os.getenv('nasa')}") as data:
                img = await data.json()
        astraunauts = ''
        for astraunaut in json.get('people'):
            current = json.get('people').index(astraunaut)
            if json.get('people')[current-1]['craft'] == astraunaut['craft']:
                astraunauts += f"\n\u2800\u2800\u2800 {astraunaut['name']}"
            else:
                astraunauts += f"""\n**{astraunaut['craft']}**:{f" Position {iss.get('iss_position')['latitude']}, {iss.get('iss_position')['longitude']}"if astraunaut['craft'] == 'ISS' else ''}\n\u2800\u2800\u2800 {astraunaut['name']}"""
                
        e = discord.Embed(title='Space', description=f"**People in Space Right Now:**\nNumber of people: {json.get('number')}\n{astraunauts}\n\n**Astronomy Picture of the Day**:\n{img.get('explanation', '')}\n{img.get('title', '')} [<:down:876079229744316456>]({img.get('hdurl')})", color=discord.Color.random())
        e.set_image(url=img.get('hdurl'))
        await ctx.reply(embed=e)

    @commands.command(name="attachments", aliases=['attachment'])
    async def attachments(self, ctx, channelid_or_messageid:str=None):
        """Gets the url of all the attachments in the message referenced."""
        ref = ctx.message.reference
        msg = None
        if channelid_or_messageid is None and ref is not None:
            msg = await ctx.channel.fetch_message(ref.message_id)
        elif not channelid_or_messageid:
            await ctx.reply('You have to reply to or provide the message id to the message.')

        else:
            ids = re.findall("\d{18}", channelid_or_messageid)
            if len(ids) < 1:
                await ctx.reply("Can't find id.")
            elif len(ids) < 2:
                msg = await ctx.channel.fetch_message(int(ids[0]))
            elif len(ids) < 3:
                channel = ctx.guild.get_channel(int(ids[0]))
                msg = await channel.fetch_message(int(ids[1]))
            elif len(ids) <4:
                channel = ctx.guild.get_channel(int(ids[1]))
                msg = await channel.fetch_message(int(ids[2]))
        if msg:
            text = f"Message: {msg.jump_url}\nAttachments:\n"
            attachments = msg.attachments
            for attachment in attachments:
                text += str(attachment)  + '\n'
            await ctx.reply(text)

    @commands.command(name='id')
    async def id(self, ctx, objects:commands.Greedy[discord.Object]):
        """Returns the id of given objects."""
        await ctx.reply(' '.join(str(o.id) for o in objects) if objects else 'None')

def setup(bot):
    bot.add_cog(UtilityCog(bot))