import discord, random, string, os, asyncio, discord.voice_client, sys, math, requests, json, pymongo, datetime
from pymongo import MongoClient
from discord.ext import commands, tasks
from pretty_help import PrettyHelp, Navigation

cluster = MongoClient("mongodb+srv://rh:1234@infinitycluster.yupj9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["infinity"]
col=db["server"]


def get_prefix(bot, message):
    if not message.guild:
        return ('')
    if col.count_documents({"_id":message.guild.id}) > 0:
        results= col.find_one({"_id":message.guild.id})
        pref = results["prefix"]
        return commands.when_mentioned_or(pref)(bot, message)
    else:
        col.insert_one({"_id":message.guild.id, "prefix": "="})
        return commands.when_mentioned_or("=")(bot, message)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, description='**__Infinity Help__**', case_insensitive=True, strip_after_prefix=True, intents=intents)
nav = Navigation('\U00002b06', '\U00002b07', '\U0000274c')
hex_int = random.randint(0,16777215)
bot.help_command = PrettyHelp(navigation=nav, color=hex_int, active_time=20, no_category='Others')


initial_extensions = ['cogs.info',
                      'cogs.members',
                      'cogs.fun',
                      'cogs.maths',
                      'cogs.owner',
                      'cogs.others',
                      'cogs.image',
                      'cogs.data',
                      'cogs.channel',
                      'cogs.moderation',
                      'cogs.listener',
                      'cogs.conversion',
                      'cogs.currency',
                      'cogs.slash',
                      'cogs.custom']

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
    
estimated_startup_time = datetime.datetime.now()

@tasks.loop(seconds=100, reconnect=True)
async def status():
    await bot.wait_until_ready()
    ser=bot.guilds
    m=0
    for s in ser:
        m += s.member_count
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{m} members in {len(ser)} servers"))
status.start()

@tasks.loop(seconds=100, reconnect=True)
async def uptime():
    await bot.wait_until_ready()
    await asyncio.sleep(50)
    timenow = datetime.datetime.now()
    d = timenow-estimated_startup_time
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name=f"with the infinity for {d.days} Days {d.seconds/60/60} Hours "))
uptime.start()

token = ('NzMyOTE3MjYyMjk3NTk1OTI1.Xw7kZA.i5ap8wowZz2WSb0zn9cM4K_5Fio')
bot.run(token, bot=True, reconnect=True)