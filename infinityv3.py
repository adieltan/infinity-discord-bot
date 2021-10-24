import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks


import motor.motor_asyncio, motor.motor_tornado, traceback, pytz

try:
    from dotenv import load_dotenv
    load_dotenv()
except:pass

import ssl

os.environ['JISHAKU_UNDERSCORE'] = 'True'
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

class Infinity(commands.AutoShardedBot):
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
bot._BotBase__cogs = commands.core._CaseInsensitiveDict()
bot.dba = motor.motor_tornado.MotorClient(str(os.getenv("mongo_server")), ssl_cert_reqs=ssl.CERT_NONE)['infinity']
bot.bled = set({})
bot.owners = bot.owner_ids
bot.managers = set({})
bot.infinityemoji = "<a:infinity:874548940610097163>"
bot.serverdb = None
bot.snipedb = dict({})
bot.startuptime = discord.utils.utcnow()

bot.errors = bot.get_channel(825900714013360199)
bot.logs = bot.get_channel(874461656938340402)
bot.changes = bot.get_channel(859779506038505532)

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

    bot.errors = bot.get_channel(825900714013360199)
    bot.logs = bot.get_channel(874461656938340402)
    bot.changes = bot.get_channel(859779506038505532)
    status.start()
    performance.start()
    login = f"\n{bot.user} ~ UTC: {discord.utils.utcnow().strftime('%H:%M %d %b %Y')} ~ GMT +8: {datetime.datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).strftime('%H:%M %d %b %Y')}"
    print(login)
    bot.startuptime = discord.utils.utcnow()

@bot.event
async def on_error(event, *args, **kwargs):
    print('Ignoring exception in {}'.format(event), file=sys.stderr)
    text = traceback.format_exc()
    buffer = io.BytesIO(text.encode('utf-8'))
    await bot.errors.send(f"{discord.utils.format_dt(discord.utils.utcnow(), style='t')} Ignoring exception in {event}", file=discord.File(buffer, filename='traceback.txt'))

@tasks.loop(minutes=5, reconnect=True)
async def status():
    await bot.wait_until_ready()
    timenow = discord.utils.utcnow()
    d = timenow-bot.startuptime
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} members in {len(bot.guilds)} servers for {round(d.seconds/60/60,2)} hours."))

@tasks.loop(minutes=30, reconnect=True)
async def performance():
    #Report on performance every 30 mins.
    await bot.wait_until_ready()
    rawping = bot.latency
    pingvalue = round(rawping *1000 ) if rawping != float('inf') else "∞"
    cpuvalue = psutil.cpu_percent()
    memoryvalue= psutil.virtual_memory().percent
    timenow = datetime.datetime.now().strftime('%M')
    embed=discord.Embed(title="Performance report", description=f"<:ping:901051623416152095> {pingvalue}ms\n<:cpu:901051865960181770> {cpuvalue}%\n<:memory:901049486242091049> {memoryvalue}%", color=discord.Color.random())
    embed.timestamp=discord.utils.utcnow()
    await bot.logs.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"), reconnect=True)