import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, requests, inspect, re, datetime, requests, aiohttp
from discord.ext import commands, tasks
try:
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
except:
    pass



class OwnerCog(commands.Cog, name='Owner'):
    """*Only owner/managers can use this.*"""
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name='blacklist', aliases=['bl'], hidden=True)
    async def blacklist(self, ctx, user:discord.User, *, reason:str=None):
        """Blacklists a member from using the bot."""
        guild = self.bot.get_guild(709711335436451901)
        managers = guild.get_role(843375370627055637).members
        if ctx.author not in managers:
            return
        results = await self.bot.dba['profile'].find_one({"_id":user.id}) or {}
        results['bl'] = True
        results['blreason'] = reason
        await self.bot.dba['profile'].replace_one({"_id":user.id}, results, True)
        blquery = {'bl':True}
        bled = []
        async for doc in self.bot.dba['profile'].find(blquery):
            bled.append(doc['_id'])
        self.bot.bled = bled
        await ctx.reply(f"Blacklisted {user.mention}.")
        await user.send(f"You have been blacklisted by a bot moderator ({ctx.author.mention}) for {reason}\nTo appeal or provide context, join our support server at https://discord.gg/dHGqUZNqCu and head to <#851637967952412723>.")

    @commands.command(name='unblacklist', aliases=['ubl'], hidden=True)
    async def unblacklist(self, ctx, user:discord.User, *, reason:str=None):
        """unBlacklists a member from using the bot."""
        guild = self.bot.get_guild(709711335436451901)
        managers = guild.get_role(843375370627055637).members
        if ctx.author not in managers:
            return
        results = await self.bot.dba['profile'].find_one({"_id":user.id}) or {}
        results['bl'] = False
        results['blreason'] = reason
        await self.bot.dba['profile'].replace_one({"_id":user.id}, results, True)
        blquery = {'bl':True}
        bled = []
        async for doc in self.bot.dba['profile'].find(blquery):
            bled.append(doc['_id'])
        self.bot.bled = bled
        await ctx.reply(f"unBlacklisted {user.mention}.")
        await user.send(f"You have been unblacklisted by a bot manager ({ctx.author.mention}).\nSorry if there are any inconvinences caused and do continue to use and support our bot.")

    @commands.command(name='blacklistcheck', aliases=['blc'], hidden=True)
    async def blacklistcheck(self, ctx, user:discord.User):
        """Checks if a member is blacklisted from using the bot."""
        guild = self.bot.get_guild(709711335436451901)
        managers = guild.get_role(843375370627055637).members
        if ctx.author not in managers:
            return
        results = await self.bot.dba['profile'].find_one({"_id":user.id}) or {}
        try:
            out = results['bl']
        except:
            out = False
        try:
            reason = results['blreason']
        except:
            reason = None
        await ctx.reply(f"{user.mention}'s blacklist status: {out}.\nReason: {reason}")

    @commands.command(name='blacklisted', hidden=True)
    async def blacklisted(self, ctx):
        guild = self.bot.get_guild(709711335436451901)
        managers = guild.get_role(843375370627055637).members
        if ctx.author not in managers:
            return
        blquery = {'bl':True}
        bled = []
        async for doc in self.bot.dba['profile'].find(blquery):
            bled.append(doc['_id'])
        self.bot.bled = bled
        await ctx.send(f"{bled}")

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
        ping = channel.guild.get_role(848814884330537020)
        try:
            await channel.send(text=f"{ping.mention}", embed=embed, allowed_mentions=discord.AllowedMentions(roles=True))
        except:
            await ctx.message.add_reaction("\U0000274c")
        else:
            await ctx.message.add_reaction("\U00002705") 

    @commands.command(name="timer", aliases=['countdown', 'cd'])
    @commands.is_owner()
    async def timer(self, ctx, time=None, name:str="Timer"):
        """Ever heard of a timer countdown?"""
        if time==None:
            await ctx.reply("Ever heard of a timer countdown?\nm=minutes\ns=seconds\nh=hours")
            return
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
        try:
            toaster.show_toast("Infinity",
                   "Is shutting down.",
                   icon_path="D:\TRH\code\py\infinity discord bot\infinity.ico",
                   duration=10,
                   threaded=True)
        except:pass
        channel = self.bot.get_channel(813251835371454515)
        await channel.send(f"<@701009836938231849> <@703135131459911740>\nThe bot is shutting down.")
        await ctx.reply("👋")
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type= discord.ActivityType.playing, name="with the exit door."))
        await asyncio.sleep(0.5)
        await self.bot.logout()

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

    @commands.command(name="gg")
    @commands.cooldown(1,0)
    @commands.is_owner()
    async def gg(self, ctx, invite:str):
        """Frames your discord invite link"""
        await ctx.reply(f'https://discord.gg/{invite}')

    @commands.command(name="addrole")
    @commands.cooldown(1,0)
    @commands.is_owner()
    async def addrole(self, ctx, role:discord.Role):
        await ctx.author.add_role(role)

    @commands.command(name="nitro")
    @commands.is_owner()
    async def nitro(self, ctx, times:int=200):
        """Generates nitro codes."""
        error = 0
        while times > 0:
            letters_and_digits = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(letters_and_digits)for _ in range(16)))
            semaphore = asyncio.Semaphore(1)
            async with semaphore:
                async with aiohttp.ClientSession() as session:
                    validator = f"https://discord.com/api/v9/entitlements/gift-codes/{result_str}?with_application=false&with_subscription_plan=true"
                    async with session.get(validator) as resp:
                        content = await resp.json()
                try:
                    if content['code'] == 10038:
                        error += 1
                        pass
                    else:
                        await ctx.author.send('https://discord.gift/' + result_str)
                    times -= 1
                except:
                    await asyncio.sleep(content['retry_after'])
        await ctx.send(f"`Done` with {error} fails.")

    @commands.command(name='dm')
    @commands.cooldown(1,3)
    @commands.is_owner()
    async def dm(self,ctx, member: discord.Member, *, message:str):
        """Gets the bot to DM your friend."""
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="Message from your friend", color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
        embed.add_field(name="Message", value=message, inline=False)
        embed.add_field(name="Specially for you by", value=f"{ctx.author.name} <@{ctx.author.id}> [Jump]({ctx.message.jump_url})", inline=False)
        embed.add_field(name="To reply:", value=f"Type\n`dm {ctx.author.id} <your message>`")
        embed.set_footer(text=f"DM function.")
        try:
            await member.send(embed=embed)
        except:
            await ctx.message.add_reaction("\U0000274c")
        else:
            await ctx.message.add_reaction("\U00002705")

    @commands.command(name='test')
    @commands.is_owner()
    async def test(self, ctx):
        pass

def setup(bot):
    bot.add_cog(OwnerCog(bot))