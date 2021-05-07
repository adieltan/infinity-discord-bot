import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, requests, inspect, re, datetime
from discord.ext.commands.errors import ExtensionNotLoaded, TooManyArguments
from discord.ext import commands, tasks



class OwnerCog(commands.Cog, name='Owner'):
    """*Only owner can use this.*"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='reload', aliases=['load'])
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Command which Reloads/loads a Module."""
        cog="cogs." + cog.removeprefix("cogs.")
        try:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except ExtensionNotLoaded:
                self.bot.load_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}', mention_author=False)
        else:
            await ctx.reply(f'**`SUCCESSFULLY`** *reloaded* __{cog}__', mention_author=False)

    @commands.command(name='unload')
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        cog="cogs." + cog.removeprefix("cogs.")
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}', mention_author=False)
        else:
            await ctx.reply(f'**`SUCCESSFULLY`** *unloaded* __{cog}__', mention_author=False)

    @commands.command(name="update")
    @commands.is_owner()
    async def updates(self, ctx, status:str, *args):
        """Bot updates."""
        info = str(' '.join(args))
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="Bot updates", description=status , color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
        embed.add_field(name="Details", value=info, inline=False)
        embed.set_footer(text=f"Infinity Updates")
        channel = self.bot.get_channel(813251614449074206)
        try:
            await channel.send(embed=embed)
        except:
            await ctx.message.add_reaction("\U0000274c")
        else:
            await ctx.message.add_reaction("\U00002705") 

    @commands.command(name="timer", aliases=['countdown', 'cd'])
    @commands.is_owner()
    async def timer(self, ctx, time, name:str="Timer"):
        """Ever heard of a timer countdown?
            m=minutes
            s=seconds
            h=hours
        """
        lower = time.lower()
        digit = int(re.sub("[^\\d.]", "", time))
        if lower[-1] == "s":
            seconds = digit
        elif lower[-1] == "m":
            seconds = digit*60
        elif lower[-1] == "h":
            seconds = digit*60*60
        elif digit == None:
            await ctx.reply("Do you speak numbers？")
            raise BaseException
        else:
            seconds = digit
        secondint = int(seconds)
        if secondint < 0 or secondint == 0:
            await ctx.send("Do YoU SpEaK NuMbErS?")
            raise BaseException
        hex_int = random.randint(0,16777215)
        embed = discord.Embed(title=f"{name}", description=f"{seconds} seconds remaining" ,color=hex_int)
        message = await ctx.send(ctx.message.author.mention, embed=embed)
        while True:
            secondint = secondint - 1
            if secondint == 0:
                hex_int = random.randint(0,16777215)
                embed = discord.Embed(title=f"{name}", description="Ended" ,color=hex_int)
                await message.edit(embed=embed)
                break
            hex_int = random.randint(0,16777215)
            embed = discord.Embed(title=f"{name}", description=f"{secondint} seconds remaining" ,color=hex_int)
            await message.edit(embed=embed)
            await asyncio.sleep(1)
        await message.reply(ctx.message.author.mention + " Your countdown Has ended!")

    @commands.command(name='logout', aliases=['shutdown'])
    @commands.is_owner()
    async def logout(self, ctx):
        """Logs out."""
        await ctx.reply("👋")
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type= discord.ActivityType.playing, name="with the exit door."))
        await asyncio.sleep(8)
        await self.bot.close()

    @commands.command(name='execute', aliases=['eval ', 'exe'])
    @commands.is_owner()
    async def exe(self, ctx, *, code):
        """Executes some code."""
        try:
            exec(code)
        except:
            await ctx.message.add_reaction("\U0000274c")
        else:
            await ctx.message.add_reaction("\U00002705")

    @commands.command(name="break")
    @commands.cooldown(1,0)
    @commands.is_owner()
    async def b(self, ctx, slowmo:int=-1):
        """Designed definitly to break."""
        await ctx.channel.edit(slowmode_delay=slowmo)
        await ctx.reply("There sure is error!")

def setup(bot):
    bot.add_cog(OwnerCog(bot))