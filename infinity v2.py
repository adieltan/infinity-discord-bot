import discord, random, string, os, asyncio, discord.voice_client, sys, math, requests, json, pymongo, datetime, psutil,  motor.motor_asyncio
from pymongo import MongoClient
from discord.ext import commands, tasks
from pretty_help import PrettyHelp, Navigation
from psutil._common import bytes2human

global bot

import motor.motor_asyncio
clustera = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://rh:1234@infinitycluster.yupj9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
dba = clustera["infinity"]
cola=dba["server"]

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

bot = commands.Bot(command_prefix=get_prefix, description='**__Infinity Help__**', case_insensitive=True, strip_after_prefix=True, intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True), owner_ids={701009836938231849,703135131459911740})
bot.dba = dba

nav = Navigation('\U00002b06', '\U00002b07', '\U0000274c')
global hex_int
hex_int = random.randint(0,16777215)
bot.help_command = PrettyHelp(navigation=nav, color=hex_int, active_time=20, no_category='Others')

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
                      'cogs.conversion',
                      'cogs.currency',
                      'cogs.slash',
                      'cogs.custom', 
                      'cogs.rh',
                      'cogs.profile',
                      'cogs.cogcontroller']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

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