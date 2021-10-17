import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle
import matplotlib.pyplot as plt
try:from dotenv import load_dotenv
except:pass

import motor.motor_asyncio, motor.motor_tornado, traceback, pytz
from pretty_help import PrettyHelp, DefaultMenu

try:load_dotenv()
except:pass

import ssl

os.environ['JISHAKU_UNDERSCORE'] = 'True'
#os.environ['JISHAKU_RETAIN'] = 'True'
os.environ['JISHAKU_HIDE'] = 'True'
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'
os.environ['JISHAKU_NO_UNDERSCORE']= 'True'

async def get_prefix(bot, message):
    if not message.guild:
        return ('')
    results= await bot.dba['server'].find_one({"_id":message.guild.id})
    if results is not None:
        pref = results.get("prefix")
        return commands.when_mentioned_or(pref)(bot, message)
    else:
        await bot.dba['server'].update_one({"_id":message.guild.id}, {"$set": {'prefix':'='}}, True)
        return commands.when_mentioned_or("=")(bot, message)

class Infinity(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
intents = discord.Intents.all()
intents.presences = False
intents.typing = False
intents.voice_states = False
intents.integrations = False
intents.webhooks = False
intents.invites = False

bot = Infinity(
command_prefix=get_prefix, description='**__Infinity__**', case_insensitive=True, strip_after_prefix=True, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True))
bot.owner_ids = set({701009836938231849,703135131459911740,708233854640455740})
bot.dba = motor.motor_tornado.MotorClient(str(os.getenv("mongo_server")), ssl_cert_reqs=ssl.CERT_NONE)['infinity']
bot.bled = set({})
bot.owners = bot.owner_ids
bot.managers = set({})
bot.infinityemoji = "<a:infinity:874548940610097163>"
bot._BotBase__cogs = commands.core._CaseInsensitiveDict()
bot.serverdb = None
bot.snipedb = dict({})
bot.startuptime = datetime.datetime.utcnow()

bot.errors = bot.get_channel(825900714013360199)
bot.logs = bot.get_channel(874461656938340402)
bot.changes = bot.get_channel(859779506038505532)

bot.processed_messages = 0
bot.commands_invoked = 0

bot.load_extension('jishaku')
print(f"{os.path.dirname(os.path.abspath(__file__))}")
if '\\' in os.path.dirname(os.path.abspath(__file__)):
    slash = '\\'
elif '/' in os.path.dirname(os.path.abspath(__file__)):
    slash = '/'
for filename in os.listdir(os.path.dirname(os.path.abspath(__file__))+slash+'cogs'):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.check
def blacklisted(ctx) -> bool:
    return (ctx.author.id not in ctx.bot.bled or ctx.author.id in ctx.bot.owners or ctx.author.id in ctx.bot.managers)

menu = DefaultMenu(page_left="<:left:876079229769482300>", page_right="<:right:876079229710762005>", remove=bot.infinityemoji, active_time=20)
ending_note = "{ctx.bot.user.name}\n{help.clean_prefix}{help.invoked_with}"
bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note, color=discord.Color.random(), no_category='Others')

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    bls = set({})
    async for doc in bot.dba['profile'].find({'bl':True}):
        bls.add(doc['_id'])
    bot.bled = bls
    manag = set({})
    async for doc in bot.dba['profile'].find({'manager':True}):
        manag.add(doc['_id'])
    bot.managers = manag
    DiscordComponents(bot)

    t = datetime.datetime.utcnow()
    ti = t.strftime("%H:%M %d %b %Y")
    tgmt8 = datetime.datetime.now(pytz.timezone("Asia/Kuala_Lumpur"))
    tigmt8 = tgmt8.strftime("%H:%M %d %b %Y")
    login = f"\n{bot.user}\u2800\u2800UTC: {ti}\u2800\u2800GMT +8: {tigmt8}"
    print(login)
    bot.startuptime = datetime.datetime.utcnow()

    bot.errors = bot.get_channel(825900714013360199)
    bot.logs = bot.get_channel(874461656938340402)
    bot.changes = bot.get_channel(859779506038505532)
    status.start()
    performanceupdate.start()
    performance.start()

@bot.event
async def on_error(event, *args, **kwargs):
    print('Ignoring exception in {}'.format(event), file=sys.stderr)
    embed=discord.Embed(title='Ignoring exception in {}'.format(event), timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_gold())
    embed.description = discord.utils.escape_markdown(traceback.format_exc())
    await bot.errors.send(embed=embed)

@tasks.loop(minutes=5, reconnect=True)
async def status():
    await bot.wait_until_ready()
    timenow = datetime.datetime.utcnow()
    d = timenow-bot.startuptime
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} members in {len(bot.guilds)} servers for {round(d.seconds/60/60,2)} hours."))

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

@tasks.loop(minutes=30, reconnect=True)
async def performance():
    #Report on performance every 30 mins.
    await bot.wait_until_ready()
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
    await bot.logs.send(file=f, embed=embed)
    plt.close()
    buf.close()


token = str(os.getenv("DISCORD_TOKEN"))
bot.run(token, bot=True, reconnect=True)