import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from numpy import byte
from discord.ext.commands.core import check
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle
import matplotlib.pyplot as plt
 

from collections import Counter, OrderedDict
from PIL import Image


class ServerCog(commands.Cog, name='Server'):
    """🌐 Tools for your server."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prefix')
    @commands.cooldown(1,8)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix:str=None):
        """Changes the prefix for the bot in the server."""
        if prefix is None:
            results = await self.bot.dba['server'].find_one({"_id":ctx.guild.id})
            pref = results.get('prefix')
            await ctx.reply(f"The prefix for {ctx.guild.name} is `{pref}`", mention_author=False)
        elif len(prefix) > 5:
            await ctx.reply("You can't have such a long prefix.", mention_author=False)
        else:
            await self.bot.dba['server'].update_one({"_id":ctx.guild.id}, {"$set": {'prefix':prefix}}, True)
            await ctx.reply(f'Prefix changed to: `{prefix}`', mention_author=False)
            name=f'[{prefix}] Infinity'
            bot=ctx.guild.get_member(self.bot.user.id)
            await bot.edit(nick=name)

    @commands.group(name='emoji', invoke_without_command=True)
    async def emoji(self, ctx, emoji:discord.PartialEmoji):
        """Shows info about an emoji."""
        await ctx.reply(f"```Name:{emoji.name}\nId: {emoji.id}\n{emoji}\n{emoji.url}```", mention_author=False)

    @emoji.command(name="add")
    @commands.has_permissions(manage_emojis=True)
    async def emoji_add(self, ctx, name, *, emoji:discord.PartialEmoji):
        """Adds an emoji to the server."""
        img = emoji.url
        data = await img.read()
        emoji = await ctx.guild.create_custom_emoji(name=f"{name}", image=data)
        await ctx.reply(f"{emoji}")

    @emoji.command(name="list")
    async def list_emojies(self, ctx):
        """Lists the emojies of the server."""
        emojies = await ctx.guild.fetch_emojis()
        emlist = [f'{str(emoji)} {discord.utils.escape_markdown(emoji.name)} `{str(emoji)}`' for emoji in emojies]
        pages = [emlist[i:i + 12] for i in range(0, len(emlist), 12)]
        for page in pages:
            text = '\n'.join([emoji for emoji in page])
            await ctx.send(f"\u200B{text}")

    @commands.command(name='serverinfo', aliases=['guildinfo', 'si'])
    @commands.guild_only()
    async def serverinfo(self, ctx, *, guild_id: int = None):
        """Shows info about the current server."""

        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild

        roles = [role.name.replace('@', '@\u200b') for role in guild.roles]

        if not guild.chunked:
            async with ctx.typing():
                await guild.chunk(cache=True)

        # figure out what channels are 'secret'
        everyone = guild.default_role
        everyone_perms = everyone.permissions.value
        secret = Counter()
        totals = Counter()
        for channel in guild.channels:
            allow, deny = channel.overwrites_for(everyone).pair()
            perms = discord.Permissions((everyone_perms & ~deny.value) | allow.value)
            channel_type = type(channel)
            totals[channel_type] += 1
            if not perms.read_messages:
                secret[channel_type] += 1
            elif isinstance(channel, discord.VoiceChannel) and (not perms.connect or not perms.speak):
                secret[channel_type] += 1

        e = discord.Embed()
        e.title = guild.name
        e.description = f'**ID**: {guild.id}\n**Owner**: {guild.owner}'
        if guild.icon:
            e.set_thumbnail(url=guild.icon_url)

        channel_info = []
        key_to_emoji = {
            discord.TextChannel: '<:text_channel:874547994584829982>',
            discord.VoiceChannel: '<:voice_channel:874548222708826153>',
        }
        for key, total in totals.items():
            secrets = secret[key]
            try:
                emoji = key_to_emoji[key]
            except KeyError:
                continue

            if secrets:
                channel_info.append(f'{emoji} {total} ({secrets} locked)')
            else:
                channel_info.append(f'{emoji} {total}')

        info = []
        features = set(guild.features)
        all_features = {
            'PARTNERED': 'Partnered',
            'VERIFIED': 'Verified',
            'DISCOVERABLE': 'Server Discovery',
            'COMMUNITY': 'Community Server',
            'FEATURABLE': 'Featured',
            'WELCOME_SCREEN_ENABLED': 'Welcome Screen',
            'INVITE_SPLASH': 'Invite Splash',
            'VIP_REGIONS': 'VIP Voice Servers',
            'VANITY_URL': 'Vanity Invite',
            'COMMERCE': 'Commerce',
            'LURKABLE': 'Lurkable',
            'NEWS': 'News Channels',
            'ANIMATED_ICON': 'Animated Icon',
            'BANNER': 'Banner'
        }

        for feature, label in all_features.items():
            if feature in features:
                info.append(f'<a:verified:876075132114829342> {label}')

        if info:
            e.add_field(name='Features', value='\n'.join(info))

        e.add_field(name='Channels', value='\n'.join(channel_info))

        if guild.premium_tier != 0:
            boosts = f'Level {guild.premium_tier}\n{guild.premium_subscription_count} boosts'
            e.add_field(name='Boosts', value=boosts, inline=False)

        bots = sum(m.bot for m in guild.members)

        e.add_field(name='Members', value=f"Total: {guild.member_count} members\n{guild.member_count - bots} Humans\n{bots} Bots")
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles')

        emoji_stats = Counter()
        for emoji in guild.emojis:
            if emoji.animated:
                emoji_stats['animated'] += 1
                emoji_stats['animated_disabled'] += not emoji.available
            else:
                emoji_stats['regular'] += 1
                emoji_stats['disabled'] += not emoji.available

        fmt = f'Regular: {emoji_stats["regular"]}/{guild.emoji_limit}\n' \
              f'Animated: {emoji_stats["animated"]}/{guild.emoji_limit}\n' \

        if emoji_stats['disabled'] or emoji_stats['animated_disabled']:
            fmt = f'{fmt}Disabled: {emoji_stats["disabled"]} regular, {emoji_stats["animated_disabled"]} animated\n'

        fmt = f'{fmt}Total Emoji: {len(guild.emojis)}/{guild.emoji_limit*2}'
        e.add_field(name='Emoji', value=fmt, inline=False)
        e.set_footer(text='Created').timestamp = guild.created_at
        await ctx.reply(embed=e)

    @commands.group(name="leaveleaderboard", aliases=['ll'])
    @commands.guild_only()
    async def ll(self, ctx):
        """Sees who left the server the most."""
        results = await self.bot.dba['server'].find_one({'_id':ctx.guild.id}) or {}
        dic = results.get('leaveleaderboard')
        if dic is None:
            await ctx.reply(f"No data.")
            return
        sort = dict(sorted(dic.items(), key = lambda x: x[1], reverse = True))
        text='\n'.join([f"<@{k}> {sort[k]}"for k in list(sort)[:10]])
        await ctx.reply(embed=discord.Embed(title="Leave leaderboard", description=f"{text}", color=discord.Color.red()).set_footer(text="Sees who left the most times."))

    @ll.command(name='reset')
    @commands.has_guild_permissions(kick_members=True)
    async def llreset(self, ctx):
        """Resets the leave leaderboard."""
        await self.bot.dba['server'].update_one({'_id':ctx.guild.id}, {'$set':{'leaveleaderboard':dict()}})
        await ctx.message.add_reaction("<a:verified:876075132114829342>")

    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        if member.bot is True:
            return
        results = await self.bot.dba['server'].find_one({'_id':member.guild.id}) or {}
        dic = results.get('leaveleaderboard')
        if dic is None:
            dic = dict()
        mem = dic.get(f"{member.id}")
        if mem is None:
            mem = 0
        dic[f"{member.id}"] = mem + 1
        await self.bot.dba['server'].update_one({'_id':member.guild.id}, {'$set':{'leaveleaderboard':dic}})

    @commands.group(name="autoresponse", aliases=["ar"])
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def ar(self,ctx):
        """Autoresponse commands for the server."""
        if ctx.invoked_subcommand is None:
            await ctx.reply("Autoresponse commands: `add` `remove` `list`")

    @ar.command(name="add")
    async def add_ar(self, ctx, trigger:str):
        """Adds a text response for the trigger."""
        trigger = trigger.lower()
        results= await self.bot.dba['server'].find_one({"_id":ctx.guild.id}) or {}
        try:results['autoresponse']
        except:results['autoresponse'] = {}
        if len(list(results['autoresponse'].keys())) >= 10:
            await ctx.reply("This guild has reached the maximum number of autoresponse which is 10.")
            return
        def check(m):
            return m.author == ctx.author
        await ctx.reply(embed=discord.Embed(title="Autoresponse", description=f"Type the response you want for `{trigger}`."))
        try:
            response = await self.bot.wait_for('message', check=check, timeout=40.0)
        except asyncio.TimeoutError:
            return await ctx.reply(f'Sorry, you took too long.')
        if len(response.clean_content) >= 500:
            await ctx.reply("You can't have such a long text response.")
        else:
            results['autoresponse'][trigger] = f"{response.clean_content}"
            await self.bot.dba['server'].replace_one({"_id":ctx.guild.id}, results, True)
            await ctx.reply(embed=discord.Embed(title="New Autoresponse", description=f"Response for `{trigger}` set to `{response.clean_content}`"))
            results = self.bot.dba['server']
            self.bot.serverdb = results

    @ar.command(name="remove")
    async def remove_ar(self, ctx, trigger:str):
        """Removes the trigger."""
        trigger = trigger.lower()
        results= await self.bot.dba['server'].find_one({"_id":ctx.guild.id}) or {}
        try:results['autoresponse']
        except:results['autoresponse'] = {}
        try:
            results['autoresponse'].pop(f'{trigger}')
            await self.bot.dba['server'].replace_one({"_id":ctx.guild.id}, results, True)
            await ctx.reply(embed=discord.Embed(title="Removed Autoresponse", description=f"Removed response for `{trigger}`."))
            results = self.bot.dba['server']
            self.bot.serverdb = results
        except:await ctx.reply("Error")

    @ar.command(name="list")
    async def list_ar(self, ctx):
        """Lists the autoresponses that are registered in the guild."""
        results= await self.bot.dba['server'].find_one({"_id":ctx.guild.id}) or {}
        try:dic = results['autoresponse']
        except:dic =  {}
        text='\n'.join([f"{result} ➡ {dic[result]}"for result in dic])
        await ctx.reply(embed=discord.Embed(title=f"{ctx.guild.name}'s Autoresponses", description=f"{text}"))

    @commands.Cog.listener()
    async def on_message (self, message: discord.Message):
        self.bot.processed_messages += 1
        if ('732917262297595925') in message.clean_content.lower():
            await message.add_reaction("\U0000267e")
        elif message.author.bot is True:
            return
        else:
            try:
                server = await self.bot.dba['server'].find_one({"_id":message.guild.id})
                try:keys = list(server['autoresponse'].keys())
                except:return
                clean = message.content.lower()
                if any(key in clean for key in keys):
                    for key in keys:
                        if key in clean:
                            server = await self.bot.dba['server'].find_one({"_id":message.guild.id})
                            response = server['autoresponse'][f'{key}']
                            try:
                                await message.reply(response, allowed_mentions=discord.AllowedMentions.none(), mention_author=False, delete_after=100)
                            except:pass
            except:pass
        if ('732917262297595925') in message.content.lower():
            try:
                await message.add_reaction("\U0000267e")
            except:pass

    @commands.group(name="delete")
    @commands.guild_only()
    @commands.cooldown(1,8)
    @commands.has_guild_permissions(administrator=True)
    async def delete(self, ctx):
        """Warning: This might affect the server's structure."""
        if ctx.invoked_subcommand is None:
            await ctx.reply("Subcommands: `category` `channel` `allchannel`")

    @delete.command(name="category", aliases=['cat'])
    async def catdel(self,ctx, category:discord.CategoryChannel, *, reason:str=None):
        """Deletes all the channels in the category."""
        verificationletter = random.choice(string.ascii_lowercase)
        await ctx.reply(f"Send **{verificationletter}** to confirm your action.")
        def check(m):
            return m.content.lower() == verificationletter and m.author == ctx.author
        try:
            response = await self.bot.wait_for('message', check=check, timeout=20)
            if response.content.lower() != verificationletter:
                raise discord.InvalidArgument("Verification not successful.")
        except:
            await ctx.reply(f"Failed to verify.")
        else:
            await ctx.reply(f"Starting to delete {category.mention}")
            channels = category.channels
            for channel in channels:
                await channel.delete(reason=f"Deleted by {ctx.author.name} for {reason}.")
            await category.delete(reason=f"Deleted by {ctx.author.name} for {reason}")
            await ctx.reply(f"Deleted {category.name}")

    @delete.command(name="channel", aliases=['chan'])
    async def chandel(self,ctx, channel:discord.TextChannel, *, reason:str=None):
        """Deletes the channel."""
        verificationletter = random.choice(string.ascii_lowercase)
        await ctx.reply(f"Send **{verificationletter}** to confirm your action.")
        def check(m):
            return m.content.lower() == verificationletter and m.author == ctx.author
        try:
            response = await self.bot.wait_for('message', check=check, timeout=20)
            if response.content.lower() != verificationletter:
                raise discord.InvalidArgument("Verification not successful.")
        except:
            await ctx.reply(f"Failed to verify.")
        else:
            await ctx.reply(f"Starting to delete {channel.mention}")
            await channel.delete(reason=f"Deleted by {ctx.author.name} for {reason}.")
            await ctx.reply(f"Deleted {channel.name}")

    @delete.command(name="allchannel")
    async def purgeallchannel(self,ctx):
        """Deletes all the channels."""
        if ctx.author != ctx.guild.owner:
            await ctx.reply("You are not server owner.")
            return
        verificationletter = random.choice(string.ascii_lowercase)
        await ctx.reply(f"Send **{verificationletter}** to confirm your action.")
        def check(m):
            return m.content.lower() == verificationletter and m.author == ctx.author
        try:
            response = await self.bot.wait_for('message', check=check, timeout=20)
            if response.content.lower() != verificationletter:
                raise discord.InvalidArgument("Verification not successful.")
        except:
            await ctx.reply(f"Failed to verify.")
        else:
            await ctx.reply(f"Starting to delete all channels.")
            channels = ctx.guild.channels
            c=0
            for channel in channels:
                try:
                    await channel.delete(reason=f"Deleted by {ctx.author.name}.")
                    c += 1
                except:
                    pass
            await ctx.reply(f"Deleted {c} channels.")

    @commands.command(name="muteoverwrites")
    @commands.cooldown(1,6)
    @commands.has_permissions(administrator=True)
    async def mo(self, ctx, muterole:discord.Role):
        """Updates mute role's perms for the whole server.."""
        overwrite = ctx.channel.overwrites_for(muterole)
        overwrite.send_messages=False
        channels = ctx.guild.channels
        categories = ctx.guild.categories
        for channel in channels:
            try:
                await channel.set_permissions(muterole, overwrite=overwrite)
            except:
                pass
        for category in categories:
            try:
                await category.set_permissions(muterole, overwrite=overwrite)
            except:
                pass
        await ctx.send("`DONE`")
        
        
    @commands.command(name="snipe", aliases=["sn"])
    @commands.cooldown(1,4)
    async def snipe(self, ctx, channel:discord.TextChannel=None):
        """Snipes the last deleted message of the channel."""
        if channel is None:
            channel = ctx.message.channel
        deletedmsg = self.bot.snipedb.get(f"{channel.id}")
        if deletedmsg is None:
            await ctx.reply(f"No cached deleted message.")
        else:
            embed=discord.Embed(title="Snipe", description=deletedmsg.content, color=deletedmsg.author.color, timestamp=deletedmsg.created_at)
            embed.set_author(name=f"{deletedmsg.author.name}", icon_url=deletedmsg.author.avatar_url)
            await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message:discord.Message):
        self.bot.snipedb[f"{message.channel.id}"]= message

    @commands.command(name="first", aliases=["firstmessage", "1"])
    @commands.cooldown(1,8)
    async def first(self, ctx):
        """Gets the first message of the channel."""
        meh = await ctx.channel.history(limit=1, oldest_first=True).flatten()
        message = meh[0]
        
        embed=discord.Embed(title="First Message", url=message.jump_url, description=f"[Jump]({message.jump_url})\n{message.content}", color=discord.Color.random())
        embed.timestamp = message.created_at
        embed.set_author(icon_url=message.author.avatar_url, name=message.author)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="hide", aliases=['h'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def Hides(self, ctx, *, arg:str=None):
        """Hides a channel for a certain role / channel / user."""
        try:    argid = int(re.sub("[^0-9]", "", arg))
        except:   argid=0
        role = discord.utils.get(ctx.guild.roles, name=arg) or discord.utils.get(ctx.guild.roles, id=argid) or discord.utils.get(ctx.guild.members, name=arg) or discord.utils.get(ctx.guild.members, id=argid)
        channel = discord.utils.get(ctx.guild.channels, name=arg) or discord.utils.get(ctx.guild.channels, id=arg)
        if role == None:
            role = ctx.guild.default_role
        if channel == None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.view_channel=False
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** hidden {channel.mention} for {role.mention}', mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="unhide", aliases=['uh'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_permissions=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def unHide(self, ctx, *, arg:str=None):
        """Unhides a channel for a certain role / channel / user."""
        try:    argid = int(re.sub("[^0-9]", "", arg))
        except:   argid=0
        role = discord.utils.get(ctx.guild.roles, name=arg) or discord.utils.get(ctx.guild.roles, id=argid) or discord.utils.get(ctx.guild.members, name=arg) or discord.utils.get(ctx.guild.members, id=argid)
        channel = discord.utils.get(ctx.guild.channels, name=arg) or discord.utils.get(ctx.guild.channels, id=arg)
        if role == None:
            role = ctx.guild.default_role
        if channel == None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.view_channel=True
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** unhidden {channel.mention} for {role.mention}', mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="lock", aliases=['l'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_permissions=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def lock(self, ctx, *, arg:str=None):
        """Locks a channel for a certain role / channel / user."""
        try:    argid = int(re.sub("[^0-9]", "", arg))
        except:   argid=0
        role = discord.utils.get(ctx.guild.roles, name=arg) or discord.utils.get(ctx.guild.roles, id=argid) or discord.utils.get(ctx.guild.members, name=arg) or discord.utils.get(ctx.guild.members, id=argid)
        channel = discord.utils.get(ctx.guild.channels, name=arg) or discord.utils.get(ctx.guild.channels, id=arg)
        if role == None:
            role = ctx.guild.default_role
        if channel == None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages=False
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** locked {channel.mention} for {role.mention}', mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="unlock", aliases=['ul'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_permissions=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def unlock(self, ctx, *, arg:str=None):
        """Unhides a channel for a certain role / channel / user."""
        try:    argid = int(re.sub("[^0-9]", "", arg))
        except:   argid=0
        role = discord.utils.get(ctx.guild.roles, name=arg) or discord.utils.get(ctx.guild.roles, id=argid) or discord.utils.get(ctx.guild.members, name=arg) or discord.utils.get(ctx.guild.members, id=argid)
        channel = discord.utils.get(ctx.guild.channels, name=arg) or discord.utils.get(ctx.guild.channels, id=arg)
        if role == None:
            role = ctx.guild.default_role
        if channel == None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages=True
        await ctx.channel.set_permissions(role, overwrite=overwrite)
        await ctx.reply(f'**`SUCCESSFULLY`** unlocked {channel.mention} for {role.mention}', mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="export")
    @commands.cooldown(1,40, commands.BucketType.category)
    @commands.has_permissions(administrator=True)
    async def export(self, ctx, destination, first_message_id:typing.Optional[int]=None, limit:int=100):
        """Exports chat messages to another channel.\n<first_message_id> is the id of the first message you wanna start exporting from.\n<limit> is the max number of messages to export."""
        destination_channel = self.bot.get_channel(int(re.sub("[^0-9]", "", destination)))
        if first_message_id is None:
            try:
                first_message_id = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            except:
                pass
        elif len(f"{first_message_id}") < 18:
            limit = first_message_id
            first_message_id = None
        else:
            first_message_id = await ctx.channel.fetch_message(first_message_id)


        channel_perms = dict(iter(destination_channel.permissions_for(ctx.author)))
        if channel_perms.get('administrator') is not True:
            raise commands.MissingPermissions(missing_perms=['administrator'])
        bot_perms_in_channel = dict(iter(destination_channel.permissions_for(await destination_channel.guild.fetch_member(self.bot.user.id))))
        if bot_perms_in_channel.get('manage_webhooks') is not True:
            raise commands.BotMissingPermissions(missing_perms=['manage_webhooks'])
        presentwebhooks = await destination_channel.webhooks()
        if any(w for w in presentwebhooks if w.name == 'Export'): #len(presentwebhooks) > 0:
            w = [w for w in presentwebhooks if w.name == 'Export']
            webhook = w[0]
        else:
            webhook = await destination_channel.create_webhook(name="Export")
        await ctx.message.add_reaction('<a:loading:880695857048072213>')
        last_message = None
        last_webhookmsg = None

        async for m in ctx.channel.history(limit=limit, after=first_message_id, oldest_first=True):
            try:
                if last_message is None:
                    raise
                elif m.author.id == last_message.author.id:
                    attachments = m.attachments
                    for attachment in attachments:
                        m.content += f"\n {str(attachment)}"
                    content = f"{last_message.content}\n" + f"[<t:{round(m.created_at.timestamp())}:d>]({m.jump_url}) {m.content if m.content else ''}"
                    msg = await last_webhookmsg.edit(content=content, embeds=last_message.embeds + m.embeds)
                    last_webhookmsg = msg
                    m.content = content
                    last_message = m
                else:
                    raise
            except:
                attachments = m.attachments
                for attachment in attachments:
                    m.content += f"\n {str(attachment)}"
                content = f"[<t:{round(m.created_at.timestamp())}:d>]({m.jump_url}) {m.content if m.content else ''}"
                msg = await webhook.send(content=content, wait=True, username=m.author.name, avatar_url=m.author.avatar_url, embeds=m.embeds if m.embeds else None, allowed_mentions=discord.AllowedMentions.none())
                last_webhookmsg = msg
                m.content = content
                last_message = m
            
        await ctx.reply("Done")

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self,ctx, no:int=None):
        """Purges a number of messages."""
        if no is None:
            await ctx.reply(f"Purge commands: `user` `pins` `bot` `human`")
            return
        def pinc(msg):
            if msg.pinned:
                return False
            else:
                return True
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)
    
    @purge.command()
    async def user(self, ctx, user:discord.Member, no:int=100):
        """Purges messages from a user."""
        def pinc(msg):
            if msg.author == user and msg.pinned is not True:
                return True
            else:
                return False
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)

    @purge.command()
    async def pins(self, ctx, no:int=100):
        """Purges a number of pinned messages."""
        def pinc(msg):
            if msg.pinned:
                return True
            else:
                return False
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)

    @purge.command(name='bot', aliases=['bots'])
    async def bot(self, ctx, no:int=100):
        """Purges messages from bots."""
        def pinc(msg):
            if msg.author.bot == True and msg.pinned is not True:
                return True
            else:
                return False
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)

    @purge.command(name='human', aliases=['humans'])
    async def human(self, ctx, no:int=100):
        """Purges messages from humans."""
        def pinc(msg):
            if msg.author.bot is False and msg.pinned is not True:
                return True
            else:
                return False
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)

    @commands.command(name="slowmode", aliases=["sm"])
    @commands.cooldown(1,3)
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self,ctx,seconds:int=0):
        """Sets the slowmode for the channel."""
        if seconds < 0:
            seconds = seconds *-1
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.reply(f"The slowmode delay for this channel is now {seconds} seconds!")

    @commands.command(name="attachments", aliases=['attachment'])
    async def attachments(self, ctx, channelid_or_messageid:str=None):
        """Gets the url of all the attachments in the message referenced."""
        ref = ctx.message.reference
        msg = None
        if channelid_or_messageid is None and ref is not None:
            msg = await ctx.channel.fetch_message(ref.message_id)
        elif channelid_or_messageid is None and ref is None:
            await ctx.reply(f"You have to reply to or provide the message id to the message.")
        else:
            ids = re.findall("\d{18}", channelid_or_messageid)
            if len(ids) < 1:
                await ctx.reply(f"Can't find id.")
            elif len(ids) < 2:
                msg = await ctx.channel.fetch_message(int(ids[0]))
            elif len(ids) < 3:
                channel = ctx.guild.get_channel(int(ids[0]))
                msg = await channel.fetch_message(int(ids[1]))
            elif len(ids) <4:
                channel = ctx.guild.get_channel(int(ids[1]))
                msg = await channel.fetch_message(int(ids[2]))
        if msg:
            text = f"Message: {msg.jump_url}\nAttachments:\n"
            attachments = msg.attachments
            for attachment in attachments:
                text += str(attachment)  + '\n'
            await ctx.reply(text)

    @commands.command(name='rename', aliases=['channelrename'])
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def channel_rename(self, ctx, channel:typing.Union[discord.TextChannel, discord.VoiceChannel, discord.StageChannel, discord.CategoryChannel]=None, *, name=None):
        """Renames a channel or channels."""
        if channel is not None:
            await channel.edit(name=name)
            await ctx.reply(channel.mention)
        else:
            msg = await ctx.reply(embed=discord.Embed(title="Channel Rename", description=f"Starting interactive session to rename all channels.", color=discord.Color.blue()))
            edited = []
            await msg.add_reaction("<:right:876079229710762005>")
            def msg_check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            def reaction_check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "<:right:876079229710762005>" and reaction.message == msg
            for channel in ctx.guild.channels:
                embed = msg.embeds[0]
                embed.description = f"Target: {channel.mention}\nSend the channel name in chat to edit. (Timeout: 180 seconds)\nTo skip: React with <:right:876079229710762005>\n\nIf the bot reacts with <a:loading:880695857048072213> for a prolonged period of time, the bot is ratelimited from editing to that channel."
                await msg.edit(embed=embed)
                try: 
                    done, pending = await asyncio.wait([
                    self.bot.wait_for('message', check=msg_check, timeout=180),
                    self.bot.wait_for('reaction_add', check=reaction_check, timeout=180)
                ], return_when=asyncio.FIRST_COMPLETED)

                    stuff = done.pop().result()
                    if type(stuff) == tuple:
                        await msg.remove_reaction(str(stuff[0].emoji), ctx.author)
                        #its an emoji
                        pass
                    else:
                        edited.append(tuple((channel.mention, channel.name, stuff.content,)))
                        await stuff.add_reaction(f"<a:loading:880695857048072213>")
                        await channel.edit(name=stuff.content)
                        await stuff.add_reaction(f"<a:verified:876075132114829342>")
                        await stuff.delete()
                except ...:
                    pass
                for future in done:
                    # If any exception happened in any other done tasks
                    # we don't care about the exception, but don't want the noise of
                    # non-retrieved exceptions
                    future.exception()
                for future in pending:
                    future.cancel()  # we don't need these anymore
            text = '\n'.join([f"{edits[0]}: {edits[1]} -> {edits[2]}" for edits in edited])
            result = await ctx.reply(embed=discord.Embed(title="Channel Rename", description=text, color=discord.Color.green()))
            embed = msg.embeds[0]
            embed.description=f"Session Ended\nResult: {result.jump_url}"
            await msg.edit(embed=embed)
            await msg.clear_reactions()

def setup(bot):
    bot.add_cog(ServerCog(bot))