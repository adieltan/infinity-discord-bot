import discord, random, asyncio, discord.voice_client, datetime
from discord.emoji import Emoji
from discord.ext import commands

class InfoCog(commands.Cog, name='Info'):
    """*Info about bot and related servers.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='invite', aliases=['botinvite', 'infinity'])
    @commands.cooldown(1,5)
    async def inv(self, ctx):
        """Gets the invite link for the bot."""
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title = "Infinity" , url="https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot", description="[Invite Link](https://discord.com/api/oauth2/authorize?client_id=732917262297595925&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FRJFfFHH&scope=bot)", color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='supportserver', aliases=['support', 'server'])
    @commands.cooldown(1,5)
    async def serv(self, ctx):
        """Gets the details invite link for the support server."""
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="RH Discord Server", url="https://discord.gg/dHGqUZNqCu", description="[Join Now](https://discord.gg/dHGqUZNqCu)", color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(name="RH server", url="https://discord.gg/dHGqUZNqCu")
        embed.set_image(url="https://media.giphy.com/media/MB6OMCu3uQQrgVIsSu/giphy.gif")
        await ctx.reply('discord.gg/dHGqUZNqCu', mention_author=False, embed=embed)

    @commands.command(name='servers', aliases=['connectedservers'])
    @commands.cooldown(1,5)
    async def servs(self, ctx):
        """Shows servers that the bot is in."""
        hex_int = random.randint(0,16777215)
        embed = discord.Embed(title=f'{self.bot.user} is connected to the following guild(s):', color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        for guild in self.bot.guilds:
            if guild.name == guild:
                break
            embed.add_field(name=f'{guild.name}', value=f'Id: {guild.id} Members: {len(guild.members)}', inline=False)
            embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='ping', aliases=['delay', 'latency'])
    @commands.cooldown(1,5)
    async def p(self, ctx):
        """Shows the ping for the bot."""
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title='Ping',color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.add_field(name="Pong!", value=f'{round (self.bot.latency * 1000)}ms ')
        embed.add_field(name="Definition:", value='Ping (latency is the technically more correct term) means the time it takes for a small data set to be transmitted from your device to a server on the Internet and back to your device again. ... \n Note that ping refers to two-way latency (aka round-trip delay), a value relevant for Internet usage.)')
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.reply(embed=embed, mention_author=False)
        
    @commands.command(name="website", aliases=["webpage"])
    @commands.cooldown(1,3)
    async def website(self, ctx):
        """Takes you to the bot's website."""
        embed=discord.Embed(title="Website", url="https://sites.google.com/view/rh6")
        embed.timestamp=datetime.datetime.utcnow()
        embed.add_field(title="Website Link", value="[Infinity Website](https://sites.google.com/view/rh6)")
        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='credits', aliases=['credit'])
    @commands.cooldown(1,5)
    async def botcredits(self, ctx):
        """Shows the info about the people who helped in the making of the bot."""
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title='Credits',description="The bot won't have been working without you guys!", color=hex_int, timestamp=datetime.datetime.now())
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(name="Thank you!!")
        embed.add_field(name='Editors', value='<@701009836938231849>', inline=False)
        embed.add_field(name="Testers", value='<@718646498950250557> <@768884619835211776>', inline=False)
        embed.add_field(name="Media Editor", value="<@715784737083359293> Hey! I'm a Music [Youtube](https://youtube.com/DheepeshYT)r with 150+ Subscribers. I have participated in a few concerts, and I play the keyboard. [Discord](https://discord.gg/uBKrT4n6BE) Now, you may be wondering, why do i have to join? How is this guy different from other music YouTubers? Well, I'm always open to suggestions, and I try to change myself for the better. So, to become a part of the growing community, join now!", inline=False)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='emoji')
    @commands.cooldown(1,3)
    async def emoji(self, ctx, emoji:discord.Emoji or discord.PartialEmoji):
        """Shows info about an emoji."""
        await ctx.reply(f"```Name:{emoji.name}\nId: {emoji.id}\n{emoji}```", mention_author=False)

    @commands.command(name='info', aliases=['botinfo'])
    @commands.cooldown(1,4)
    async def info(self, ctx):
        """Info about the bot."""
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="Bot Info", description="Info about the bot.", color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(name=self.bot.user, url=self.bot.user.avatar_url)
        embed.add_field(name="", value="")
        await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(InfoCog(bot))