import discord, random, string, os, asyncio, discord.voice_client, sys, math, requests, json, pymongo, datetime, psutil,  motor.motor_asyncio, dns, motor.motor_tornado, io
from discord.ext import commands, tasks
from pretty_help import PrettyHelp, DefaultMenu
from psutil._common import bytes2human
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt

try:
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
except:
    pass

global bot
clustera = motor.motor_tornado.MotorClient("mongodb+srv://rh:1234@infinitycluster.yupj9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
dba = clustera["infinity"]
cola=dba["server"]

owners = set({701009836938231849,703135131459911740})
managers = set({})

bled = set({})


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
    if await cola.count_documents({"_id":message.guild.id}) > 0:
        results= await cola.find_one({"_id":message.guild.id})
        pref = results["prefix"]
        return commands.when_mentioned_or(pref)(bot, message)
    else:
        await cola.insert_one({"_id":message.guild.id, "prefix": "="})
        return commands.when_mentioned_or("=")(bot, message)

bot = MyBot(command_prefix=get_prefix, description='**__Infinity Help__**', case_insensitive=True, strip_after_prefix=True, intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True), owner_ids=owners)
bot.dba = dba
bot.bled = bled
bot.owner = owners
bot.managers = managers



menu = DefaultMenu(page_left="\U00002196", page_right="\U00002197", remove="a:infi:851081962491478026", active_time=20)
# Custom ending note
ending_note = "{ctx.bot.user.name}\n{help.clean_prefix}{help.invoked_with}"
bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note, color=discord.Color.random(), no_category='Others')

bot.load_extension('jishaku')
os.environ["JISHAKU_NO_UNDERSCORE"]="true"

@bot.check
def blacklisted(ctx) -> bool:
    bls = bot.bled
    return (ctx.author.id not in bls or ctx.author.id in owners or ctx.author.id in bot.managers)

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
                      'cogs.server',
                      'cogs.minigames',
                      'cogs.cogcontroller']

breakable_extentions = ['cogs.conversion', 'cogs.fun']

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
    #blacklisted chaching
    bls = set({})
    blquery = {'bl':True}
    async for doc in dba['profile'].find(blquery):
        bls.add(doc['_id'])
    bot.bled = bls
    guild = bot.get_guild(709711335436451901)
    bot.managers = set(guild.get_role(843375370627055637).members)
    DiscordComponents(bot)

    t = datetime.datetime.now()
    ti = t.strftime("%H:%M %a %d %b %Y")
    login = f"\n{bot.user}\n{ti}\n"
    print(login)
    vc = bot.get_channel(736791916397723780)
    try:
        await vc.connect()
    except:
        pass

    channel = bot.get_channel(813251835371454515)
    await channel.send("∞")
    global est
    est = datetime.datetime.now()
    try:
        toaster.show_toast("Infinity",
                   login,
                   icon_path="D:\TRH\code\py\infinity discord bot\infinity.ico",
                   duration=15,
                   threaded=True)
    except:pass

@bot.event
async def on_error(event, *args, **kwargs):
    errors = bot.get_channel(855359960354652160)
    await errors.send(f"```\n{event}\n\n{''.join(args)}\n\n{''.join(kwargs)}\n```")
    pass

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


token = ('NzMyOTE3MjYyMjk3NTk1OTI1.Xw7kZA.OYcA4UssHArLl_7HyYFKSMNhCE0')
bot.run(token, bot=True, reconnect=True)