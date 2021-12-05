import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

import motor.motor_asyncio, motor.motor_tornado, traceback, pytz, ssl
try:
    from dotenv import load_dotenv
    load_dotenv()
except:pass

from discord.commands import permissions

from time import perf_counter
ori = perf_counter()

os.environ['JISHAKU_UNDERSCORE'] = 'True'
os.environ['JISHAKU_HIDE'] = 'True'
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'
os.environ['JISHAKU_NO_UNDERSCORE']= 'True'

async def get_prefix(bot, message):
    if not message.guild:
        return ('')
    results = await bot.db['server'].find_one({"_id":message.guild.id}) or {}
    pref = results.get("prefix", '=')
    return commands.when_mentioned_or(pref)(bot, message)

intents = discord.Intents.all()
intents.presences = False
intents.typing = False
intents.voice_states = False
intents.integrations = False
intents.webhooks = False
intents.invites = False

class Infinity(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = get_prefix, 
            description = '**__Infinity__**', 
            case_insensitive = True, 
            strip_after_prefix = True, 
            intents = intents, 
            allowed_mentions = discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True), 
            owner_ids = {701009836938231849,703135131459911740,708233854640455740},
            activity = discord.Activity(type = discord.ActivityType.watching, name='the startup process.')
            )

    async def cbl(self):
        #cache blacklisted
        b = set()
        async for doc in self.db['profile'].find({'bl':True}):
            b.add(doc['_id'])
        self.bled = b

    async def cmanagers(self):
        #cache managers
        managers = []
        async for doc in self.db['profile'].find({'manager':True}):
            managers.append(doc['_id'])
        self.managers = managers

    async def cache_ar(self):
        ar = {}
        async for doc in self.db['server'].find({}):
            if doc.get('autoresponse'):
                ar[str(doc['_id'])] = doc['autoresponse']
        self.ar = ar

    async def on_ready(self):
        ready = perf_counter()
        self.startuptime = discord.utils.utcnow()
        self.owners = self.owner_ids
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()
        self.db = motor.motor_asyncio.AsyncIOMotorClient(str(os.getenv("mongo_server")), ssl_cert_reqs=ssl.CERT_NONE).infinity
        self.snipedb = dict({})
        
        self.errors = self.get_channel(825900714013360199)
        self.logs = self.get_channel(874461656938340402)
        self.changes = self.get_channel(859779506038505532)
        status.start(self)
        performance.start(self)
        delete_snipecache.start(self)

        await self.cbl()
        await self.cmanagers()
        await self.cache_ar()

        await self.get_channel(813251835371454515).send(f"∞ Startup took {ready - ori :0.4f} seconds.")
        print(f"Startup took {ready - ori :0.4f} seconds.")
        print(f"\n{self.user} ~ UTC: {self.startuptime.strftime('%H:%M %d %b %Y')} ~ GMT +8: {datetime.datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).strftime('%H:%M %d %b %Y')}")

    async def on_error(self, event, *args, **kwargs):
        print('Ignoring exception in {}'.format(event), file=sys.stderr)
        text = traceback.format_exc()
        buffer = io.BytesIO(text.encode('utf-8'))
        await self.errors.send(f"{discord.utils.format_dt(discord.utils.utcnow(), style='t')} Ignoring exception in {event}", file=discord.File(buffer, filename='traceback.txt'))

    async def process_commands(self, message: discord.Message) -> None:
        if not self.is_ready():
            return
        if message.author.bot:
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)


bot = Infinity()
bot.load_extension('jishaku')
print(f"{os.path.dirname(os.path.abspath(__file__))}")
if '\\' in os.path.dirname(os.path.abspath(__file__)):
    slash = '\\'
elif '/' in os.path.dirname(os.path.abspath(__file__)):
    slash = '/'
for filename in os.listdir(os.path.dirname(os.path.abspath(__file__))+slash+'cogs'):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            print(e)

@bot.check
def blacklisted(ctx) -> bool:
    return (ctx.author.id not in ctx.bot.bled or ctx.author.id in ctx.bot.owners or ctx.author.id in ctx.bot.managers)


@tasks.loop(minutes=5, reconnect=True)
async def status(self):
    timenow = discord.utils.utcnow()
    d = timenow-self.startuptime
    await self.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.users)} members in {len(self.guilds)} servers for {round(d.seconds/60/60,2)} hours."))

@tasks.loop(minutes=30, reconnect=True)
async def performance(self):
    #Report on performance every 30 mins.
    pingvalue = round(self.latency *1000 ) if self.latency != float('inf') else "∞"
    cpuvalue = psutil.cpu_percent()
    memoryvalue= psutil.virtual_memory().percent
    embed=discord.Embed(title="Performance report", description=f"<:ping:901051623416152095> {pingvalue}ms\n<:cpu:901051865960181770> {cpuvalue}%\n<:memory:901049486242091049> {memoryvalue}%", color=discord.Color.random())
    embed.timestamp=discord.utils.utcnow()
    await self.logs.send(embed=embed)

@tasks.loop(minutes=30, reconnect=True)
async def delete_snipecache(self):
    for i in self.snipedb.copy():
        if round(self.snipedb[i].created_at.timestamp() + 60) < round(discord.utils.utcnow().timestamp()):
            self.snipedb.pop(i)


bot.run(os.getenv("DISCORD_TOKEN"), reconnect=True)
# bot.run(os.getenv("beta"), reconnect=True)
