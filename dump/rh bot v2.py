import discord, random, string, os, logging, asyncio, discord.voice_client
from discord.ext import commands

bot = commands.Bot(command_prefix='=')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = ('NzMyOTE3MjYyMjk3NTk1OTI1.Xw7kZA.lOO0w_267o-AKP42NV05mKFYUxw')
guild = ('709711335436451901')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="=commands"))
    print(f"Logged in as {bot.user}")
    hello = ("I'm online now!", 'Hello.','Hi.', 'Peekaboo!')
    channel = bot.get_channel(783871340813090887)
    await channel.send(random.choice(hello))
    vc = bot.get_channel(736791916397723780)
    await vc.connect()
    #bubly
    channel2 = bot.get_channel(799885536844054559)
    await channel2.send(random.choice(hello))

@bot.listen()
async def on_message (message: discord.Message):
    if message.author.bot == True:
        return
    if message.author == bot.user:
        return
    if message.content == ('hi'):
        greeting = ('Hi', 'Hello', '안녕하세요 (Annyeonghaseyo)', '你好', 'こんにちは(Konnichiwa)', 'Bonjour')
        response = random.choice(greeting)
        await message.channel.send(response)
        pass
    if message.content == ('hello'):
        greeting = ('Hi', 'Hello', '안녕하세요 (Annyeonghaseyo)', '你好', 'こんにちは(Konnichiwa)', 'Bonjour')
        response = random.choice(greeting)
        await message.channel.send(response)
        pass

@bot.command()
async def ping(ctx):
    hex_int = random.randint(0,16777215)
    embed=discord.Embed(title='Ping',color=hex_int)
    embed.add_field(name="Pong!", value=f'{round (bot.latency * 1000)}ms ')
    embed.add_field(name="Definition:", value='Ping (latency is the technically more correct term) means the time it takes for a small data set to be transmitted from your device to a server on the Internet and back to your device again. ... \n Note that ping refers to two-way latency (aka round-trip delay), a value relevant for Internet usage.)')
    await ctx.send(embed=embed)

@bot.command(name= 'roll')
async def roll(ctx, number_of_dice:int, number_of_sides:int):
    if number_of_dice > 100: return
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command()
async def choose(ctx, choice1, choice2):
    cho=choice1, choice2
    ran=random.choice(cho)
    msg = await ctx.send(f'(*&^{choice1}%$^$#%%^&{choice2}**&(#&$&#^&))')
    await asyncio.sleep(1.0)
    await msg.edit(content=f'I choose {ran}')

@bot.command()
async def gift(ctx, number:int):
    if number > 4 :return
    for _ in range(number):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits)for _ in range(16)))
        await ctx.send('discord.gift/' + result_str)

@bot.command(aliases=['type'])
async def send(ctx, *args):
    hex_int = random.randint(0,16777215)
    mes=" ".join(args)
    embed=discord.Embed(title=mes, color=hex_int)
    await ctx.send(embed=embed)

@bot.command(aliases=['botinvite'])
async def invite(ctx):
    botinvite = str('https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot')
    await ctx.send(botinvite)

@bot.command(aliases=['support'])
async def server(ctx):
    hex_int = random.randint(0,16777215)
    embed=discord.Embed(title="RH Discord Server", url="https://discord.gg/dHGqUZNqCu", description="Join for:", color=hex_int)
    embed.set_author(name="RH server", url="https://discord.gg/dHGqUZNqCu")
    embed.set_thumbnail(url="https://media.giphy.com/media/MB6OMCu3uQQrgVIsSu/giphy.gif")
    embed.add_field(name="SFW COMMUNITY", value="NO NSFW ALLOWED", inline=False)
    embed.add_field(name="DISCUSSION", value="be polite", inline=False)
    embed.add_field(name="DANK MEMER CHANNELS", value="use `pls` commands all ya like", inline=False)
    embed.add_field(name="DANK MEMER GIVEAWAYS", value="woohoo", inline=False)
    embed.add_field(name="DANK MEMER HEISTS", value=" (FRIENDLY/NOT-FRIENDLY)", inline=False)
    embed.add_field(name="COUNTING CHANNEL", value="1234", inline=False)
    embed.add_field(name="CONTRIBUTE TO THE MAKING OF OUR SELF MADE BOT", value="DM me for the role", inline=False)
    embed.add_field(name="MUSIC TIME", value="RELAX", inline=False)
    embed.add_field(name="PARTNERSHIPS", value="LOW MEMBER COUNT ACCEPTED", inline=False)
    embed.add_field(name="DANK MEMER ROB AND HEIST DISABLED", value="NO WORRYING ABOUT MONEY BEING STOLEN HERE", inline=False)
    embed.add_field(name="SPECIAL SELF ROLES", value="BE SPECIAL", inline=False)
    embed.add_field(name="https://discord.gg/dHGqUZNqCu", value="** **", inline=False)
    embed.set_footer(text="Join when?")
    await ctx.send('discord.gg/dHGqUZNqCu', embed=embed)

@bot.command()
async def servers(ctx):
    hex_int = random.randint(0,16777215)
    embed = discord.Embed(title=f'{bot.user} is connected to the following guild(s):', color=hex_int)
    for guild in bot.guilds:
        if guild.name == guild:
            break
        embed.add_field(name=f'{guild.name}', value=f'id: {guild.id}', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def commands(ctx):
    hex_int = random.randint(0,16777215)
    embed = discord.Embed(
        title="RH bot",
        url=
        "https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot",
        description="Prefix = `=` Commands:",
        color=hex_int)
    embed.add_field(
        name="hi | hello", value="Warm Greetings. (No prefix needed)", inline=False)
    embed.add_field(name='=server | =support', value="Gets info about the support server.", inline=False)
    embed.add_field(name='=servers', value="Gets the connected guilds.", inline=False)
    embed.add_field(name='=invite | =botinvite', value="Gets the bot's invite link.", inline=False)
    embed.add_field(name='=ping', value='Gets the latency. In other words, delay.', inline=False)
    embed.add_field(name='=send | =type', value='Gets the bot to repeat a word.', inline=False)
    embed.add_field(name='=roll', value='Roll a dice. (below 100) Usage: `=roll <number_of_dice> <number_of_sides>`. Eg.:`=roll 1 6`', inline=False)
    embed.add_field(name='=choose', value='Chooses 1 between 2 choices. Usage: `=choose <choice1> <choice2>`. Eg.:`=choose 1 2`', inline=False)
    embed.add_field(name='=gift', value='Generates a Discord gift code. Usage: `=gift <number of codes(below 4)`> Eg.:`=gift 3`', inline=False)
    embed.set_footer(text="adieltan#3438")
    await ctx.send(embed=embed)

bot.run(token, bot=True, reconnect=True)