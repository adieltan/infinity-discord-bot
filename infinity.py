import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

import motor.motor_asyncio, motor.motor_tornado, traceback, pytz, ssl
try:
    from dotenv import load_dotenv
    load_dotenv()
except:pass
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

class Context(commands.Context):
    async def tick(self, value):
        # reacts to the message with an emoji
        # depending on whether value is True or False
        # if its True, it'll add a green check mark
        # otherwise, it'll add a red cross mark
        emoji = '<a:verified:876075132114829342>' if value else '<:exclamation:876077084986966016>'
        try:
            # this will react to the command author's message
            await self.message.add_reaction(emoji)
        except discord.HTTPException:
            # sometimes errors occur during this, for example
            # maybe you don't have permission to do that
            # we don't mind, so we can just ignore them
            pass
    
    async def reply(self, content: typing.Optional[str] = None, **kwargs: typing.Any) -> discord.Message:
        try:
            return await super().reply(content=content, **kwargs)
        except:
            await super().send(content=content, **kwargs)

    async def delete(self, wait_after:float=0.0):
        await asyncio.sleep(wait_after)
        try:
            await super().message.delete()
        except:
            pass

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

    async def get_context(self, message, *, cls=Context):
        # when you override this method, you pass your new Context subclass to the super() method, which tells the bot to use the new Context class
        return await super().get_context(message, cls=cls)

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
        self.owners = self.owner_ids
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()
        self.db = motor.motor_asyncio.AsyncIOMotorClient(str(os.getenv("mongo_server")), ssl_cert_reqs=ssl.CERT_NONE).infinity
        self.snipedb = dict({})

        self.persistent_views_added = False
        
        self.errors = self.get_channel(926789023446499369)
        self.logs = self.get_channel(926789818455842876)
        self.changes = self.get_channel(926789039321919509)
        status.start()
        performance.start()
        delete_snipecache.start()

        print(f"Startup took {ready - ori :0.4f} seconds.")
        print(f"\n{self.user} ~ UTC: {discord.utils.utcnow().strftime('%H:%M %d %b %Y')} ~ GMT +8: {datetime.datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).strftime('%H:%M %d %b %Y')}")
        self.startuptime = discord.utils.utcnow()
        await self.cbl()
        await self.cmanagers()
        await self.cache_ar()

        self.load_extension('jishaku')
        print(f"{os.path.dirname(os.path.abspath(__file__))}")
        if '\\' in os.path.dirname(os.path.abspath(__file__)):
            slash = '\\'
        elif '/' in os.path.dirname(os.path.abspath(__file__)):
            slash = '/'
        for filename in os.listdir(os.path.dirname(os.path.abspath(__file__))+slash+'cogs'):
            if filename.endswith(".py"):
                try:
                    self.load_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    print(e)
        await self.get_channel(813251835371454515).send(f"∞ Startup took {ready - ori :0.4f} seconds.")

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

@bot.check
def blacklisted(ctx) -> bool:
    return (ctx.author.id not in ctx.bot.bled or ctx.author.id in ctx.bot.owners or ctx.author.id in ctx.bot.managers)


@tasks.loop(minutes=5, reconnect=True)
async def status():
    timenow = discord.utils.utcnow()
    d = timenow-bot.startuptime
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} members in {len(bot.guilds)} servers for {round(d.seconds/60/60,2)} hours."))

@tasks.loop(minutes=30, reconnect=True)
async def performance():
    #Report on performance every 30 mins.
    rawping = bot.latency
    pingvalue = round(rawping *1000 ) if rawping != float('inf') else "∞"
    cpuvalue = psutil.cpu_percent()
    memoryvalue= psutil.virtual_memory().percent
    timenow = datetime.datetime.now().strftime('%M')
    embed=discord.Embed(title="Performance report", description=f"<:ping:901051623416152095> {pingvalue}ms\n<:cpu:901051865960181770> {cpuvalue}%\n<:memory:901049486242091049> {memoryvalue}%", color=discord.Color.random())
    embed.timestamp=discord.utils.utcnow()
    await bot.logs.send(embed=embed)

@tasks.loop(hours=1, reconnect=True)
async def delete_snipecache():
    for i in bot.snipedb.copy():
        if round(bot.snipedb[i].created_at.timestamp() + 60) < round(discord.utils.utcnow().timestamp()):
            bot.snipedb.pop(i)


bot.run(os.getenv("DISCORD_TOKEN"), reconnect=True)
# bot.run(os.getenv("dc_beta"), reconnect=True)
