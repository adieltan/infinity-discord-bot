import discord, random, string, os, asyncio, discord.voice_client, sys, math, requests, json
from discord.ext import commands, tasks
from pretty_help import PrettyHelp, Navigation

def get_prefix(bot, message):
    if not message.guild:
        return '='
    else:
        with open('D:\TRH\code\py\discord bot\prefix.json', 'r') as f: 
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_prefix, description='**__Infinity Help__**', case_insensitive=True)
nav = Navigation('\U00002b06', '\U00002b07', '\U0000274c')
hex_int = random.randint(0,16777215)

bot.help_command = PrettyHelp(navigation=nav, color=hex_int, active_time=20, no_category='Others')



initial_extensions = ['cogs.info',
                      'cogs.members',
                      'cogs.fun',
                      'cogs.maths',
                      'cogs.owner',
                      'cogs.others',
                      'cogs.moderation',
                      'cogs.listener',
                      'cogs.conversion',
                      'cogs.youtube']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == guild:
            break
        with open('D:\TRH\code\py\discord bot\prefix.json', 'r') as f: 
            prefixes = json.load(f)
        if guild.id not in prefixes:
            with open('D:\TRH\code\py\discord bot\prefix.json', 'w') as f: 
                prefixes = json.load(f)
            prefixes[str(guild.id)] = '='
            json.dump(prefixes, f, indent=4)

    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="=help"))
    print(f"Logged in as {bot.user}")
    vc = bot.get_channel(736791916397723780)
    await vc.connect()
    hello = ["I'm online now!", 'Hello.','Hi.', 'Peekaboo!', "What’s kickin’, little chicken?", "Yipee!", "What’s crackin’?", "Yo!", "Whatsup?", "Aye, mate.", "Hola!", "Konnichiwa", "Yikes", "HO", "I don't know you, you don't know me", "Hello everyone", "Hello guys", "Infinity is here", "Infinite Possibilities", "∞", ]
    channellist = [813251835371454515,799885536844054559,779939454978490418,792711767644962816]
    for int in channellist:
        channel = bot.get_channel(int)
        await channel.send(random.choice(hello))

token = ('NzMyOTE3MjYyMjk3NTk1OTI1.Xw7kZA.lOO0w_267o-AKP42NV05mKFYUxw')
bot.run(token, bot=True, reconnect=True)