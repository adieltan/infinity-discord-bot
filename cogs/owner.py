import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 

class OwnerCog(commands.Cog, name='Owner'):
    """*Only owner/managers can use this.*"""
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name='blacklist', aliases=['bl'])
    async def blacklist(self, ctx, user:discord.User, *, reason:str=None):
        """Blacklists a member from using the bot."""
        if ctx.author.id not in self.bot.managers:
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
        changes = self.bot.get_channel(859779506038505532)
        embed=discord.Embed(title="Blacklist", description=f"{user.mention} for {reason}", color=discord.Color.red())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await changes.send(embed)

    @commands.command(name='unblacklist', aliases=['ubl'])
    async def unblacklist(self, ctx, user:discord.User, *, reason:str=None):
        """unBlacklists a member from using the bot."""
        if ctx.author.id not in self.bot.managers:
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
        await user.send(f"You have been unblacklisted by a bot manager ({ctx.author.mention}).\nSorry if there are any inconvinences caused and please do continue to use and support our bot.")
        changes = self.bot.get_channel(859779506038505532)
        embed=discord.Embed(title="Unlacklist", description=f"{user.mention} for {reason}", color=discord.Color.green())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await changes.send(embed)

    @commands.command(name='blacklistcheck', aliases=['blc'])
    async def blacklistcheck(self, ctx, user:discord.User):
        """Checks if a member is blacklisted from using the bot."""
        if ctx.author.id not in self.bot.managers:
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

    @commands.command(name='blacklisted')
    async def blacklisted(self, ctx):
        if ctx.author.id not in self.bot.managers:
            return
        blquery = {'bl':True}
        bled = set({})
        async for doc in self.bot.dba['profile'].find(blquery):
            bled.add(doc['_id'])
        self.bot.bled = bled
        await ctx.send(f"{' '.join([f'<@{bl}>' for bl in bled])}")
    
    @commands.command(name="manageradd", aliases=['ma'])
    @commands.is_owner()
    async def manageradd(self, ctx, user:discord.User):
        results = await self.bot.dba['profile'].find_one({"_id":user.id}) or {}
        results['manager'] = True
        await self.bot.dba['profile'].replace_one({"_id":user.id}, results, True)
        managquery = {'manager':True}
        managers = []
        async for doc in self.bot.dba['profile'].find(managquery):
            managers.append(doc['_id'])
        self.bot.managers = managers
        await ctx.reply(f"Added {user.mention} as Infinity Managers.")
        guild = self.bot.get_guild(709711335436451901)
        member = await guild.fetch_member(user.id)
        role = guild.get_role(843375370627055637)
        await member.add_roles(role)
        changes = self.bot.get_channel(859779506038505532)
        embed=discord.Embed(title="Promoted to manager", description=f"{user.mention}", color=discord.Color.blurple())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await changes.send(embed)

    @commands.command(name="managerremove", aliases=['mr'])
    @commands.is_owner()
    async def managerremove(self, ctx, user:discord.User):
        results = await self.bot.dba['profile'].find_one({"_id":user.id}) or {}
        results['manager'] = False
        await self.bot.dba['profile'].replace_one({"_id":user.id}, results, True)
        managquery = {'manager':True}
        managers = []
        async for doc in self.bot.dba['profile'].find(managquery):
            managers.append(doc['_id'])
        self.bot.managers = managers
        await ctx.reply(f"Removed {user.mention} as Infinity Managers.")
        guild = self.bot.get_guild(709711335436451901)
        member = await guild.fetch_member(user.id)
        role = guild.get_role(843375370627055637)
        await member.remove_roles(role)
        changes = self.bot.get_channel(859779506038505532)
        embed=discord.Embed(title="Demoted from manager", description=f"{user.mention}", color=discord.Color.dark_orange())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await changes.send(embed)

    @commands.command(name="update")
    @commands.is_owner()
    async def updates(self, ctx, status:str, *args):
        """Bot updates."""
        info = str(' '.join(args))
        embed=discord.Embed(title="Bot updates", description=status , color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
        embed.add_field(name="Details", value=info, inline=False)
        embed.set_footer(text=f"Infinity Updates")
        channel = self.bot.get_channel(813251614449074206)
        ping = channel.guild.get_role(848814884330537020)
        try:
            await channel.send(ping.mention, embed=embed, allowed_mentions=discord.AllowedMentions(roles=True))
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
        
        embed = discord.Embed(title=f"{name}", description=f"{seconds} seconds remaining" ,color=discord.Color.random())
        message = await ctx.send(ctx.message.author.mention, embed=embed)
        while True:
            secondint = secondint - 1
            if secondint == 0:
                
                embed = discord.Embed(title=f"{name}", description="Ended" ,color=discord.Color.random())
                await message.edit(embed=embed)
                break
            
            embed = discord.Embed(title=f"{name}", description=f"{secondint} seconds remaining" ,color=discord.Color.random())
            await message.edit(embed=embed)
            await asyncio.sleep(1)
        await message.reply(ctx.message.author.mention + " Your countdown Has ended!")

    @commands.command(name='logout', aliases=['shutdown'])
    @commands.is_owner()
    async def logout(self, ctx):
        """Logs out."""
        channel = self.bot.get_channel(813251835371454515)
        await channel.send(f"<@701009836938231849> <@703135131459911740>\nThe bot is being shut down by {ctx.author.mention}.")
        await ctx.reply("👋")
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type= discord.ActivityType.playing, name="with the exit door."))
        await asyncio.sleep(0.5)
        await self.bot.logout()

    @commands.command(name="gg")
    @commands.cooldown(1,0)
    @commands.is_owner()
    async def gg(self, ctx, invite:str):
        """Frames your discord invite link"""
        try:
            inv = await self.bot.fetch_invite(url=f'https://discord.gg/{invite}', with_counts=True)
        except:
            member = 0
            online = 0
        else:
            member = format(inv.approximate_member_count,',')
            online = format(inv.approximate_presence_count, ',')
        await ctx.reply(f'https://discord.gg/{invite}\nOnline: {online} Members: {member}')

    @commands.command(name='dm')
    @commands.cooldown(1,3)
    @commands.is_owner()
    async def dm(self,ctx, member: discord.Member, *, message:str):
        """Gets the bot to DM your friend."""
        
        embed=discord.Embed(title="Message from your friend", color=discord.Color.random())
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

    @commands.command(name="chat", aliases=['broadcast'])
    @commands.is_owner()
    async def chat(self, ctx, channel:discord.TextChannel):
        to = 60
        await ctx.reply(f'Type messages that you want to send through the bot to {channel.mention}\nType `quit` to exit.\nSession will timeout after {to} seconds of inactivity.', mention_author=False)
        def author(m):
            return m.author == ctx.author
        quit = False
        while quit is not True:
            try:
                message = await self.bot.wait_for('message', check=author, timeout=to)
                if message.content.lower() in ['quit','exit']:
                    quit = True
                    await message.reply("Session ended.")
                else:
                    try:
                        await channel.send(message.content, allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False))
                    except:
                        await message.add_reaction("\U0000274c")
                    else:
                        await message.add_reaction("\U00002705")
            except asyncio.TimeoutError:
                quit = True
                return await ctx.reply(f'Session timeout. The broadcast session has ended.', mention_author=False)

    @commands.command(name="botstatus")
    @commands.is_owner()
    async def botstatus(self, ctx, activitytype, title, info=None, link=None):
        if link is None:
            link = 'https://discord.gg//RJFfFHH'
        if info is None:
            info = "._."
        if 'play' in activitytype.lower():
            activity = discord.ActivityType.playing
        elif 'stream' in activitytype.lower():
            activity = discord.ActivityType.streaming
        elif 'listen' in activitytype.lower():
            activity = discord.ActivityType.listening
        elif 'watch' in activitytype.lower():
            activity = discord.ActivityType.watching
        elif 'custom' in activitytype.lower():
            activity = discord.ActivityType.custom
        elif 'competing' in activitytype.lower():
            activity = discord.ActivityType.competing
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=activity, name=title, details=info, url=link))
        await ctx.reply("Done")

    @commands.command(name='test')
    @commands.is_owner()
    async def test(self, ctx):
        server = self.bot.dba['server']
        await ctx.send(f"{server}")



def setup(bot):
    bot.add_cog(OwnerCog(bot))