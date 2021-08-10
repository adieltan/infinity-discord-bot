import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
try:from dotenv import load_dotenv
except:pass

import motor.motor_asyncio, motor.motor_tornado, traceback
from pretty_help import PrettyHelp, DefaultMenu

try:load_dotenv()  # take environment variables from .env.
except:pass
# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

clustera = motor.motor_tornado.MotorClient(str(os.getenv("mongo_server")))
dba = clustera["infinity"]

owners = set({701009836938231849,703135131459911740})
managers = set({})
bled = set({})

os.environ['JISHAKU_UNDERSCORE'] = 'True'
os.environ['JISHAKU_RETAIN'] = 'True'
os.environ['JISHAKU_HIDE'] = 'True'
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Hierarchy(commands.Converter):
    async def convert(self, ctx, target):
        target = await commands.MemberConverter().convert(ctx, target)

        if target.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            raise commands.BadArgument(f":x: **{ctx.author.name}**, you can't.", mention_author=False)

        return target

async def get_prefix(bot, message):
    if not message.guild:
        return ('')
    results= await dba['server'].find_one({"_id":message.guild.id})
    if results is not None:
        pref = results.get("prefix")
        return commands.when_mentioned_or(pref)(bot, message)
    else:
        await dba['server'].update_one({"_id":message.guild.id}, {"$set": {'prefix':'='}}, True)
        return commands.when_mentioned_or("=")(bot, message)

bot = MyBot(command_prefix=get_prefix, description='**__Infinity Help__**', case_insensitive=True, strip_after_prefix=True, intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True), owner_ids=owners)
bot.dba = dba
bot.bled = bled
bot.owners = owners
bot.managers = managers
bot.infinityemoji = "\U0000267e"
bot.serverdb = None
bot._BotBase__cogs = commands.core._CaseInsensitiveDict()
bot.snipedb = dict({})
bot.est = datetime.datetime.now()

menu = DefaultMenu(page_left="\U00002196", page_right="\U00002197", remove=bot.infinityemoji, active_time=20)
# Custom ending note
ending_note = "{ctx.bot.user.name}\n{help.clean_prefix}{help.invoked_with}"
bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note, color=discord.Color.random(), no_category='Others')

bot.load_extension('jishaku')

@bot.check
def blacklisted(ctx) -> bool:
    bls = bot.bled
    return (ctx.author.id not in bls or ctx.author.id in owners or ctx.author.id in bot.managers)

cogs = ['channel', 'cogcontroller', 'conversion', 'custom', 'data', 'economy', 'fun', 'image', 'info', 'listener', 'maths', 'members', 'minigames', 'moderation', 'music','others', 'owner', 'profile', 'rh', 'server', 'slash', 'utility']
for cog in cogs:
    bot.load_extension("cogs."+cog)

@bot.event
async def on_ready():
    #chaching
    bls = set({})
    blquery = {'bl':True}
    async for doc in dba['profile'].find(blquery):
        bls.add(doc['_id'])
    bot.bled = bls
    manag = set({})
    managquery = {'manager':True}
    async for doc in dba['profile'].find(managquery):
        manag.add(doc['_id'])
    bot.managers = manag
    DiscordComponents(bot)

    t = datetime.datetime.now()
    ti = t.strftime("%H:%M %a %d %b %Y")
    login = f"\n{bot.user}\n{ti}\n"
    print(login)
    bot.est = datetime.datetime.now()

@bot.event
async def on_error(event, *args, **kwargs):
    errors = bot.get_channel(855359960354652160)
    ctx = args[0] #Gets the message object
    try: author = ctx.author
    except: author = bot.user
    embed=discord.Embed(title="Error", description=f"{author.mention}\n{event}", color=discord.Color.random())
    embed.timestamp=datetime.datetime.utcnow()
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    embed.set_footer(text=author.id)
    embed.add_field(name="Info", value=f"{ctx.channel.mention} [{ctx.message.content}]({ctx.message.jump_url})")
    text = traceback.format_exc()
    chunks = [text[i:i+1014] for i in range(0, len(text), 1014)]
    for chunk in chunks:
        embed.add_field(name="Error", value=f"```py\n{chunk}\n```", inline=False)
    await errors.send(embed=embed)


@tasks.loop(minutes=5, reconnect=True)
async def status():
    await bot.wait_until_ready()
    timenow = datetime.datetime.now()
    d = timenow-bot.est
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} members in {len(bot.guilds)} servers for {round(d.seconds/60/60,2)} hours."))
status.start()

ping = []
time = []
cpu = []
memory = []
@tasks.loop(minutes=1, reconnect=True)
async def performanceupdate():
    await bot.wait_until_ready()
    if (len(ping) and len(time) and len(cpu) and len(memory) > 30):
        ping.pop(0)
        time.pop(0)
        cpu.pop(0)
        memory.pop(0)
    rawping = bot.latency
    if rawping != float('inf'): 
        pingvalue = round(rawping *1000 )
        ping.append(pingvalue)
    else:
        pingvalue = "∞"
        ping.append(0)
    cpuvalue = psutil.cpu_percent()
    memoryvalue= psutil.virtual_memory().percent
    timenow = datetime.datetime.now().strftime('%M')
    cpu.append(cpuvalue)
    memory.append(memoryvalue)
    time.append(timenow)
performanceupdate.start()

@tasks.loop(minutes=30, reconnect=True)
async def performance():
    #Report on performance every 30 mins.
    await bot.wait_until_ready()
    performance = bot.get_channel(847011689882189824)
    rawping = bot.latency
    if rawping != float('inf'): 
        pingvalue = round(rawping *1000 )
        ping.append(pingvalue)
    else:
        pingvalue = "∞"
        ping.append(0)
    cpuvalue = psutil.cpu_percent()
    memoryvalue= psutil.virtual_memory().percent
    timenow = datetime.datetime.now().strftime('%M')
    cpu.append(cpuvalue)
    memory.append(memoryvalue)
    time.append(timenow)
    embed=discord.Embed(title="Performance report", description=f"`Ping  :` {pingvalue}ms\n`CPU   :` {cpuvalue}%\n`Memory:` {memoryvalue}%", color=discord.Color.random())
    plt.plot(time, ping, label = "Ping (ms)")
    plt.plot(time, cpu, label = "CPU (%)")
    plt.plot(time, memory, label= "Memory (%)")
    plt.xlabel('Time (minute)')
    #plt.ylabel('')
    plt.title('Performance')
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    f = discord.File(fp=buf, filename="image.png")
    embed.set_image(url="attachment://image.png")
    embed.timestamp=datetime.datetime.utcnow()
    await performance.send(file=f, embed=embed)
    plt.close()
    buf.close()
performance.start()


token = str(os.getenv("DISCORD_TOKEN"))
bot.run(token, bot=True, reconnect=True)