import discord, time, random, string
from discord.ext import commands
client = commands.Bot(command_prefix='r ')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="RH's server"))
    print(f"Logged in as {client.user}")
    channel = client.get_channel(783871340813090887)
    await channel.send("I'm online now.")

@client.command()
async def youtube(ctx):
    await ctx.send("https://www.youtube.com/channel/UCW4gBQyPWrTeyKN6EPV6sGA")

@client.command()
async def yt(ctx):
    await ctx.send("https://www.youtube.com/channel/UCW4gBQyPWrTeyKN6EPV6sGA")

@client.event
async def on_message(message):
        if message.content.startswith('ping'):
            await message.channel.send(f'Pong! {round (client.latency * 1000)}ms ')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round (client.latency * 1000)}ms ')

@client.command()
async def server(ctx):
    embed=discord.Embed(title="RH Discord Server", url="https://discord.gg/dHGqUZNqCu", description="Join for:", color=0x00fffb)
    embed.set_author(name="RH server", url="https://discord.gg/dHGqUZNqCu")
    embed.set_thumbnail(url="https://media.giphy.com/media/MB6OMCu3uQQrgVIsSu/giphy.gif")
    embed.add_field(name="SFW COMMUNITY", value="NO NSFW ALLOWED", inline=False)
    embed.add_field(name="DISCUSSION", value="be polite", inline=False)
    embed.add_field(name="DANK MEMER CHANNELS", value="use `pls` commands all ya like", inline=False)
    embed.add_field(name="DANK MEMER GIVEAWAYS", value="woohoo", inline=False)
    embed.add_field(name="DANK MEMER HEISTS", value=" (FRIENDLY/NOT-FRIENDLY)", inline=False)
    embed.add_field(name="COUNTING CHANNEL", value="1234", inline=False)
    embed.add_field(name="CONTRIBUTE TO THE MAKING OF OUR SELF MADE BOT", value="DM me for the role", inline=False)
    embed.add_field(name="MUSIC TIME", value="RELAX", inline=False)
    embed.add_field(name="PARTNERSHIPS", value="LOW MEMBER COUNT ACCEPTED", inline=False)
    embed.add_field(name="DANK MEMER ROB AND HEIST DISABLED", value="NO WORRYING ABOUT MONEY BEING STOLEN HERE", inline=False)
    embed.add_field(name="SPECIAL SELF ROLES", value="BE SPECIAL", inline=False)
    embed.set_footer(text="Join when?")
    await ctx.send(embed=embed)
    await ctx.send("discord.gg/dHGqUZNqCu")

@client.command()
async def invite(ctx):
    for a in range(5):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join(
            (random.choice(letters_and_digits) for i in range(10)))
        await ctx.send("https://discord.gg/" + result_str)

@client.command()
async def nitro(ctx):
    for a in range(3):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join(
            (random.choice(letters_and_digits) for i in range(16)))
        await ctx.send("discord.gift/" + result_str)

@client.command()
async def botinvite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&scope=bot")

client.remove_command('help')

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        title="RH bot",
        url=
        "https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&scope=bot",
        description="Prefix = `r` Commands:",
        color=0x00fffb)
    embed.add_field(
        name="r youtube | r yt", value="My YouTube channel link", inline=False)
    embed.add_field(name="r ping", value="Shows the bot's ping", inline=False)
    embed.add_field(
        name="r server", value="Shows the bot's server", inline=False)
    embed.add_field(
        name="r invite",
        value=
        "Generates 5 random server invite. (Generated using random alphanumeric characters)",
        inline=False)
    embed.add_field(
        name="r nitro",
        value=
        "Generates 3 random nitro codes. (Generated using random alphanumeric characters)",
        inline=False)
    embed.add_field(
        name="r botinvite",
        value=
        "Shows the bot's invite link",
        inline=False)
    embed.set_footer(text="adieltan#3438")
    await ctx.send(embed=embed)



token = ('NzMyOTE3MjYyMjk3NTk1OTI1.Xw7kZA.Ek7yChAd1MdZyTE_YYqCrEXDNzg')

client.run(token)
