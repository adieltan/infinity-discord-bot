import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle
import matplotlib.pyplot as plt

from PIL import Image, ImageDraw, ImageFont
import blist, MotionBotList, topgg

def is_manager():
    def predicate(ctx):
        return ctx.message.author.id in ctx.bot.managers
    return commands.check(predicate)

class OwnerCog(commands.Cog, name='Owner'):
    """🔐 Only owner/managers can use this."""
    def __init__(self, bot):
        self.bot = bot
        self.blist= blist.Blist(self.bot, token=os.getenv('blist_token'))
        self.motionlist = MotionBotList.connect(os.getenv('motionlist_token'))
        self.topgg= topgg.DBLClient(self.bot,token=os.getenv('topgg_token'),autopost=False)

    @commands.command(name='adm')
    @commands.cooldown(1,3)
    @is_manager()
    async def adm(self,ctx, user: discord.User, *, message:str):
        """Anounymous DM."""
        try:
            await user.send(message)
        except:
            await ctx.message.add_reaction("<:exclamation:876077084986966016>")
        else:
            await ctx.message.add_reaction("<a:verified:876075132114829342>")

    @commands.command(name='dm')
    @commands.cooldown(1,3)
    @is_manager()
    async def dm(self,ctx, member: discord.Member, *, message:str):
        """Gets the bot to DM your friend."""
        
        embed=discord.Embed(title="Message from your friend", color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
        embed.add_field(name="Message", value=message, inline=False)
        embed.add_field(name="Specially for you by", value=f"{ctx.author.name} <@{ctx.author.id}> [Jump]({ctx.message.jump_url})", inline=False)
        embed.add_field(name="To reply:", value=f"Type\n`dm {ctx.author.id} <your message>` . UPDATE: ENABLED FOR INFINITY MANAGERS ONLY.")
        embed.set_footer(text=f"DM function.")
        try:
            await member.send(embed=embed)
        except:
            await ctx.message.add_reaction("<:exclamation:876077084986966016>")
        else:
            await ctx.message.add_reaction("<a:verified:876075132114829342>")

    @commands.command(name='blacklist', aliases=['bl'])
    @is_manager()
    async def blacklist(self, ctx, user:discord.User, *, reason:str=None):
        """Blacklists a member from using the bot."""
        if user.id in self.bot.managers:
            await ctx.reply("You can't blacklist them.")
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
        await ctx.reply(embed=discord.Embed(title="Blacklist",description=f"Blacklisted {user.mention} `{user.id}`.", color=discord.Color.red()))
        await user.send(f"You have been blacklisted by a bot moderator ({ctx.author.mention}) for {reason}\nTo appeal or provide context, join our support server at https://discord.gg/dHGqUZNqCu and head to <#851637967952412723>.")
        embed=discord.Embed(title="Blacklist", description=f"{user.mention} for {reason}", color=discord.Color.red())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await self.bot.changes.send(embed=embed)

    @commands.command(name='unblacklist', aliases=['ubl'])
    @is_manager()
    async def unblacklist(self, ctx, user:discord.User, *, reason:str=None):
        """unBlacklists a member from using the bot."""
        if user.id in self.bot.managers:
            await ctx.reply("You can't unblacklist them.")
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
        await ctx.reply(embed=discord.Embed(title="Unblacklist",description=f"Unlacklisted {user.mention} `{user.id}`.", color=discord.Color.green()))
        await user.send(f"You have been unblacklisted by a bot manager ({ctx.author.mention}).\nSorry if there are any inconvinences caused and please do continue to use and support our bot.")
        embed=discord.Embed(title="Unlacklist", description=f"{user.mention} for {reason}", color=discord.Color.green())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await self.bot.changes.send(embed=embed)

    @commands.command(name='blacklistcheck', aliases=['blc'])
    @is_manager()
    async def blacklistcheck(self, ctx, user:discord.User):
        """Checks if a member is blacklisted from using the bot."""
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
    @is_manager()
    async def blacklisted(self, ctx):
        bled = set({})
        async for doc in self.bot.dba['profile'].find({'bl':True}):
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
        embed=discord.Embed(title="Promoted to manager", description=f"{user.mention}", color=discord.Color.blurple())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await self.bot.changes.send(embed=embed)

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
        try:
            guild = self.bot.get_guild(709711335436451901)
            member = await guild.fetch_member(user.id)
            role = guild.get_role(843375370627055637)
            await member.remove_roles(role)
        except:
            pass
        embed=discord.Embed(title="Demoted from manager", description=f"{user.mention}", color=discord.Color.dark_orange())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await self.bot.changes.send(embed=embed)

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
            await ctx.message.add_reaction("<:exclamation:876077084986966016>")
        else:
            await ctx.message.add_reaction("<a:verified:876075132114829342>") 

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
        await self.bot.logs.send(f"The bot is being shut down by {ctx.author.name}.")
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
                        await message.add_reaction("<:exclamation:876077084986966016>")
                    else:
                        await message.add_reaction("<a:verified:876075132114829342>")
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
        else:
            await ctx.reply(f"Activity Type {activitytype} not recognised.")
            return
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=activity, name=title, details=info, url=link))
        await ctx.reply("Done")

    @commands.command(name="remove")
    @commands.is_owner()
    async def remove(self, ctx):
        """Removes the referenced message."""
        ref = ctx.message.reference
        if ref == None:
            await ctx.reply("Eh you gotta reply to the message you wanna remove!", mention_author=True)
        else:
            message = await ctx.channel.fetch_message(ref.message_id)
            await message.delete()
            try:    await ctx.message.delete()
            except: pass

    @commands.command(name="mutual")
    @commands.is_owner()
    async def mutual(self, ctx, user:discord.User):
        """Returns the servers that are shared with the user."""
        servers = '\n'.join([f"`{guild.id}` {guild.name}" for guild in user.mutual_guilds])
        embed=discord.Embed(title="Mutual servers", description=servers, color=discord.Color.random(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_footer(text=f"{len(user.mutual_guilds)} servers")
        await ctx.reply(embed=embed)

    @commands.command(name="allcommands")
    @commands.is_owner()
    async def all_commands(self, ctx):
        """Returns all the commands + description."""
        text = ''
        for cog in self.bot.cogs:
            cogobj = self.bot.get_cog(cog)

            try:
                text += ('+' + '-' * 105 + '+' +'\n')
                text += ('| ' + cogobj.qualified_name.upper() + '\n')
                if cogobj.description:
                    text += ('| ' + cogobj.description + '\n')
                text += ('+' + '-' * 105 + '+' + '\n')
            except AttributeError:
                pass # Idk how to make a no category category

            for c in cogobj.get_commands():
                text += (f"• {c.name} {c.signature.replace('_', '')}".ljust(35, ' ') + f' {c.help}' + '\n')
                if isinstance(c, commands.Group):
                    for sc in c.commands:
                        text += (''.ljust(5, ' ') + f"▪ {sc.name} {sc.signature.replace('_', '')}".ljust(35, ' ') + f' {sc.help}' + '\n')
            text += ('\n')
        buffer = io.BytesIO(text.encode('utf-8'))
        await ctx.reply(file=discord.File(buffer, filename='allcommands.txt'))


    @commands.command(name='poststats')
    async def autostatsposting(self, ctx):
        """Post stats."""
        await self.bot.wait_until_ready()
        text = ''
        async with aiohttp.ClientSession() as cs:
            header={'Authorization':os.getenv('dbl_token')}
            data = {'users':len(self.bot.users), 'guilds':len(self.bot.guilds)}
            async with cs.post(url=f"https://discordbotlist.com/api/v1/bots/{self.bot.user.id}/stats", data=data, headers=header) as data:
                json = await data.json()
                text += f"DiscordBotList\n{json}"
            #header={'Authorization':os.getenv('voidbots_token')}
            #data = {'server_count':len(self.bot.guilds)}
            #async with cs.post(url=f"https://api.voidbots.net/bot/stats/{self.bot.user.id}", json=data, headers=header) as data:
                #json = await data.json()
                #if json.get('message') != "Servercount updated!":
                    #await reports.send(f"VoidBots\n{json}")
            header={'Authorization':os.getenv('botlists_api')}
            data = {'status':'idle', 'guilds':len(self.bot.guilds), 'shards':1}
            async with cs.patch(url=f"https://api.botlists.com/bot/{self.bot.user.id}", json=data, headers=header) as data:
                json = await data.json()
                text += f"BotLists\n{json}"
            header={'Authorization':os.getenv('listcord_token')}
            data = {'server_count':len(self.bot.guilds)}
            async with cs.post(url=f"https://listcord.gg/api/bot/{self.bot.user.id}/stats", json=data, headers=header) as data:
                json = await data.json()
                text += f"Listcord\n{json}"
            header={'Authorization':os.getenv('bladebot_token')}
            data = {'servercount':len(self.bot.guilds)}
            async with cs.post(url=f"https://bladebotlist.xyz/api/bots/{self.bot.user.id}/stats", json=data, headers=header) as data:
                json = await data.json()
                text += f"BladeBot\n{json}"
            header={'Authorization':os.getenv('discordservices_token')}
            data = {'servers':len(self.bot.guilds), 'shards':0}
            async with cs.post(url=f"https://api.discordservices.net/bot/{self.bot.user.id}/stats", json=data, headers=header) as data:
                json = await data.json()
                text += f"DiscordServices\n{json}"
            header={'Authorization':os.getenv('botlist_token')}
            data = {'server_count':len(self.bot.guilds)}
            async with cs.post(url=f"https://api.botlist.me/api/v1/bots/{self.bot.user.id}/stats", json=data, headers=header) as data:
                json = await data.json()
                text += f"Botlist\n{json}"
        await cs.close()
        await blist.Blist.post_bot_stats(self.blist)
        self.motionlist.update(self.bot.user.id, len(self.bot.guilds))
        await self.topgg.post_guild_count(len(self.bot.guilds))

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        await self.voterchannel.send(f"{data}")

    @commands.command(name='test')
    @commands.is_owner()
    async def test(self, ctx, *, input):
        pass


def setup(bot):
    bot.add_cog(OwnerCog(bot))