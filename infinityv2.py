import discord, random, string, os, asyncio, discord.voice_client, sys, math, requests, json, pymongo, datetime, psutil,  motor.motor_asyncio, dns, motor.motor_tornado
from pymongo import MongoClient
from discord.ext import commands, tasks
from pretty_help import PrettyHelp, DefaultMenu
from psutil._common import bytes2human

global bot
#motor.motor_asyncio.AsyncIO
clustera = motor.motor_tornado.MotorClient("mongodb+srv://rh:1234@infinitycluster.yupj9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
dba = clustera["infinity"]
cola=dba["server"]

owners = {701009836938231849,703135131459911740}

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process_commands(self, message):
        results = await dba['profile'].find_one({"_id":message.author.id}) or {}
        try:
            out = results['bl']
        except:
            out = False
        if message.author.bot:
            return
        elif message.author.id in owners:
            pass
        elif out:
            return
        ctx = await self.get_context(message, cls=commands.Context)
        await self.invoke(ctx)

async def get_prefix(bot, message):
    if not message.guild:
        return ('')
    if await cola.count_documents({"_id":message.guild.id}) > 0:
        results= await cola.find_one({"_id":message.guild.id})
        pref = results["prefix"]
        return commands.when_mentioned_or(pref)(bot, message)
    else:
        await cola.insert_one({"_id":message.guild.id, "prefix": "="})
        return commands.when_mentioned_or("=")(bot, message)

bot = MyBot(command_prefix=get_prefix, description='**__Infinity Help__**', case_insensitive=True, strip_after_prefix=True, intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True), owner_ids=owners)
bot.dba = dba

global hex_int
hex_int = random.randint(0,16777215)

menu = DefaultMenu(page_left="\U00002196", page_right="\U00002197", remove="a:infi:851081962491478026", active_time=20)
# Custom ending note
ending_note = "{ctx.bot.user.name}\n{help.clean_prefix}{help.invoked_with}"
bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note, color=hex_int, no_category='Others')

bot.load_extension('jishaku')
os.environ["JISHAKU_NO_UNDERSCORE"]="true"



initial_extensions = ['cogs.info',
                      'cogs.members',
                      'cogs.fun',
                      'cogs.maths',
                      'cogs.owner',
                      'cogs.others',
                      'cogs.image',
                      'cogs.data',
                      'cogs.channel',
                      'cogs.utility',
                      'cogs.moderation',
                      'cogs.listener',
                      'cogs.currency',
                      'cogs.slash',
                      'cogs.custom', 
                      'cogs.rh',
                      'cogs.profile',
                      'cogs.cogcontroller']

breakable_extentions = ['cogs.conversion']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
    for extentsion in breakable_extentions:
        try:
            bot.load_extension(extentsion)
        except:
            print(f"{extentsion} can't be loaded.")

@bot.event
async def on_ready():
    t = datetime.datetime.now()
    ti = t.strftime("%H:%M %a %d %b %Y")
    print(f"\nLogged in as {bot.user}  ↯  {ti}  ↯\n")
    vc = bot.get_channel(736791916397723780)
    await vc.connect()
    hello = ["I'm online now!", 'Hello.','Hi.', 'Peekaboo!', "What’s kickin’, little chicken?", "Yipee!", "What’s crackin’?", "Yo!", "Whatsup?", "Aye, mate.", "Hola!", "Konnichiwa", "Yikes", "HO", "Hello everyone", "Hello guys", "Infinity is here", "Infinite Possibilities", "∞"]
    channel = bot.get_channel(813251835371454515)
    await channel.send(random.choice(hello))
    global est
    est = datetime.datetime.now()

@tasks.loop(seconds=100, reconnect=True)
async def status():
    await bot.wait_until_ready()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} members in {len(bot.guilds)} servers"))
status.start()

@tasks.loop(seconds=100, reconnect=True)
async def uptime():
    await bot.wait_until_ready()
    await asyncio.sleep(50)
    timenow = datetime.datetime.now()
    d = timenow-est
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name=f"with the infinity for {d.days} Days {round(d.seconds/60/60,2)} Hours "))
uptime.start()

@tasks.loop(minutes=15, reconnect=True)
async def performance():
    #Quartarly report on performance.
    await bot.wait_until_ready()
    performance = bot.get_channel(847011689882189824)
    hex_int = random.randint(0,16777215)
    embed=discord.Embed(title="Performance report", description=f"`Ping  :` {round(bot.latency * 1000)}ms\n`CPU   :` {psutil.cpu_percent()}%\n`Memory:` {psutil.virtual_memory().percent}%", color=hex_int)
    embed.timestamp=datetime.datetime.utcnow()
    await performance.send(embed=embed)
performance.start()


token = ('NzMyOTE3MjYyMjk3NTk1OTI1.Xw7kZA.i5ap8wowZz2WSb0zn9cM4K_5Fio')
bot.run(token, bot=True, reconnect=True)