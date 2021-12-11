import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

from collections import Counter, OrderedDict
from PIL import Image
from ._utils import Database, Menu, Confirm, is_owner


class ServerCog(commands.Cog, name='Server'):
    """Tools for your server."""
    def __init__(self, bot):
        self.bot = bot
        self.COG_EMOJI = '🌐'

    @commands.command(name='prefix')
    @commands.cooldown(1,8)
    async def prefix(self, ctx, prefix:str=None):
        """Shows / changes the prefix for the bot in the server."""
        if not prefix:
            results = await Database.get_server(self, ctx.guild.id)
            await ctx.reply(f"The prefix for {ctx.guild.name} is `{results.get('prefix', '=')}`", mention_author=False)
        elif len(prefix) > 5:
            await ctx.reply("You can't have such a long prefix.")
        else:
            perms = dict(iter(ctx.channel.permissions_for(ctx.author)))
            if perms.get('administrator') is not True:
                raise commands.MissingPermissions(missing_perms=['administrator'])
            await Database.edit_server(self, ctx.guild.id, {'prefix':prefix})
            await ctx.reply(f'Prefix changed to: `{prefix}`', mention_author=False)
            await ctx.me.edit(nick=f'[{prefix}] Infinity')

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
        emlist = [
            f'{emoji} {discord.utils.escape_markdown(emoji.name)} `{emoji}`'
            for emoji in emojies
        ]

        pages = [emlist[i:i + 12] for i in range(0, len(emlist), 12)]
        for page in pages:
            text = '\n'.join(page)
            await ctx.send(f"\u200b{text}")

    @commands.command(name='serverinfo', aliases=['guildinfo', 'si'])
    @commands.guild_only()
    async def serverinfo(self, ctx, *, guild_id: int = None):
        """Shows info about the current server."""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if not guild:
                return await ctx.send('Invalid Guild ID given.')
        else:
            guild = ctx.guild
        if not guild.chunked:
            async with ctx.typing():
                await guild.chunk(cache=True)
        e = discord.Embed(title=guild.name, description=f'**ID**: {guild.id}\n**Owner**: {guild.owner}', color=discord.Color.random())
        if guild.icon:
            e.set_thumbnail(url=guild.icon)
        info = [f"<a:verified:876075132114829342> {feature.replace('_', ' ').lower().title()}" for feature in guild.features]
        if info:
            e.add_field(name='Features', value='\n'.join(info), inline=False)
        channels = [channel for channel in guild.channels if type(channel) is discord.TextChannel]
        vc = [channel for channel in guild.channels if type(channel) is discord.VoiceChannel]
        category = [channel for channel in guild.channels if type(channel) is discord.CategoryChannel]
        e.add_field(name='Channels', value=f"<:text_channel:874547994584829982> {len(channels)}\n<:voice_channel:874548222708826153> {len(vc)}")

        if guild.premium_tier != 0:
            boosts = f'Level {guild.premium_tier}\n{guild.premium_subscription_count} boosts'
            e.add_field(name='Boosts', value=boosts)

        bots = sum(m.bot for m in guild.members)

        e.add_field(name='Members', value=f"{guild.member_count} members\n👤 {guild.member_count - bots} humans\n🤖 {bots} bots")
        e.add_field(name='Roles', value=f'<:Role_Icon:882098706437001276> {len(guild.roles)} roles')

        emoji_stats = Counter()
        for emoji in guild.emojis:
            if emoji.animated:
                emoji_stats['animated'] += 1
                emoji_stats['animated_disabled'] += not emoji.available
            else:
                emoji_stats['regular'] += 1
                emoji_stats['disabled'] += not emoji.available

        fmt = f'Regular: {emoji_stats["regular"]}/{guild.emoji_limit}\n' \
              f'Animated: {emoji_stats["animated"]}/{guild.emoji_limit}\n'
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
        results = await Database.get_server(self, ctx.guild.id)
        dic = results.get('leaveleaderboard')
        if not dic:
            await ctx.reply('No data.')
            return
        sort = dict(sorted(dic.items(), key = lambda x: x[1], reverse = True))
        text = '\n'.join(f"<@{k}> {sort[k]}" for k in list(sort))

        buffer = io.BytesIO(text.encode('utf-8'))
        await ctx.reply('Leave Leaderboard', file=discord.File(buffer, filename=f'{ctx.guild.id}_leaveleaderboard.txt'))

    @ll.command(name='reset')
    @commands.has_guild_permissions(kick_members=True)
    async def llreset(self, ctx):
        """Resets the leave leaderboard."""
        await Database.edit_server(self, ctx.guild.id, {'leaveleaderboard':None})
        await ctx.message.add_reaction("<a:verified:876075132114829342>")

    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        if member.bot is True:
            return
        results = await Database.get_server(self, member.guild.id)
        dic = results.get('leaveleaderboard')
        if not dic:
            dic = {}
        mem = dic.get(f"{member.id}", 0)
        dic[f"{member.id}"] = mem + 1
        await Database.edit_server(self, member.guild.id, {'leaveleaderboard':dic})

    @commands.group(name="autoresponse", aliases=["ar"])
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def ar(self,ctx):
        """Autoresponse commands for the server."""
        if not ctx.invoked_subcommand:
            await ctx.reply("Autoresponse commands: `add` `remove` `list`")

    @ar.command(name="add")
    async def add_ar(self, ctx, *,trigger:str):
        """Adds a text response for the trigger."""
        trigger = trigger.lower()
        results = await Database.get_server(self, ctx.guild.id)
        if len(list(results.get('autoresponse', {}).keys())) >= 10:
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
            edit = results.get('autoresponse', {})[trigger] = f"{response.clean_content}"
            results['autoresponse'] = edit
            await Database.edit_server(self, ctx.guild.id, results)
            await ctx.reply(embed=discord.Embed(title="New Autoresponse", description=f"Response for `{trigger}` set to `{response.clean_content}`"))
            self.bot.ar[f'{ctx.guild.id}'] = results['autoresponse']

    @ar.command(name="remove")
    async def remove_ar(self, ctx, *,trigger:str):
        """Removes the trigger."""
        trigger = trigger.lower()
        results= await Database.get_server(self, ctx.guild.id)
        try:
            results.get('autoresponse', {}).pop(f'{trigger}')
            await Database.edit_server(self, ctx.guild.id, results)
            await ctx.reply(embed=discord.Embed(title="Removed Autoresponse", description=f"Removed response for `{trigger}`."))
            self.bot.ar[f'{ctx.guild.id}'] = results['autoresponse']
        except:await ctx.reply("Error")

    @ar.command(name="list")
    async def list_ar(self, ctx):
        """Lists the autoresponses that are registered in the guild."""
        results= await Database.get_server(self, ctx.guild.id)
        dic = results.get('autoresponse', {})
        text = '\n'.join(f"{result}\n> {dic[result]}" for result in dic)
        await ctx.reply(embed=discord.Embed(title=f"{ctx.guild.name}'s Autoresponses", description=f"{text}"))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot is True:
            return
        try:
            keys = self.bot.ar.get(f'{message.guild.id}', {}).keys()
            clean = message.content.lower()
            if any(key in clean for key in keys):
                text = '\n'.join(self.bot.ar.get(f'{message.guild.id}', {})[key] for key in keys if key in clean)
                await message.reply(text, allowed_mentions=discord.AllowedMentions.none(), delete_after=60)
        except:
            pass

    @commands.group(name="delete", aliases=['del'])
    @commands.guild_only()
    @commands.max_concurrency(1, commands.BucketType.guild, wait=True)
    @commands.has_guild_permissions(administrator=True)
    async def deletechannels(self, ctx):
        """Warning: This might affect the server's structure."""
        if not ctx.invoked_subcommand:
            await ctx.reply("Subcommands: `category` `channel` `allchannel`")

    @deletechannels.command(name='role', aliases=['r'])
    async def roledel(self, ctx, roles:commands.Greedy[discord.Role]=None):
        """Deletes all roles."""
        if not roles:
            roles = ctx.guild.roles
        v = Confirm(ctx)
        rolesn = 0
        errors = []
        embed = discord.Embed(title="Role Deletion", description=f"Deleting {len(roles)} roles.\n{' '.join([role.mention for role in roles])}\nClick Confirm.", color=discord.Color.brand_red())
        v.msg = await ctx.reply(embed=embed, view=v)
        msgv = discord.ui.View.from_message(v.msg)
        for vd in msgv.children:
            vd.disabled = True
        await v.wait()
        if v.value is False:
            embed.description = 'Cancelled.'
            embed.color = discord.Color.red()
            await v.msg.edit(embed=embed, view=msgv)
        elif v.value:
            embed.description += '\nConfirmed.'
            embed.color = discord.Color.green()
            await v.msg.edit(embed=embed, view=msgv)
            for role in roles:
                try:
                    await role.delete(reason=f"Deleted by {ctx.author.name}.")
                except:
                    errors.append(role.id)
                else:
                    rolesn += 1
            err = 'Errors:\n' + ' '.join([f'<@&{id}>' for error in errors if error])
            await ctx.reply(f"Deleted {rolesn} roles.\n{err if errors else ''}")

    @deletechannels.command(name="category", aliases=['cat'])
    async def catdel(self,ctx, categorys:commands.Greedy[discord.CategoryChannel]):
        """Deletes all the channels in the category."""
        v = Confirm(ctx)
        channels = 0
        errors = []
        embed = discord.Embed(title="Category Deletion", description=f"Deleting {len(categorys)} categories.\n{' '.join([cate.mention for cate in categorys])}\nClick Confirm.", color=discord.Color.brand_red())
        v.msg = await ctx.reply(embed=embed, view=v)
        msgv = discord.ui.View.from_message(v.msg)
        for vd in msgv.children:
            vd.disabled = True
        await v.wait()
        if v.value is False:
            embed.description = 'Cancelled.'
            embed.color = discord.Color.red()
            await v.msg.edit(embed=embed, view=msgv)
        elif v.value:
            embed.description += '\nConfirmed.'
            embed.color = discord.Color.green()
            await v.msg.edit(embed=embed, view=msgv)
            for category in categorys:
                for channel in category.channels:
                    try:
                        await channel.delete(reason=f"Deleted by {ctx.author.name}.")
                    except:
                        errors.append(channel.id)
                    else:
                        channels += 1
                await category.delete(reason=f"Deleted by {ctx.author.name}.")
            err = 'Errors:\n' + ' '.join([f'<#{id}>' for error in errors if error])
            await ctx.reply(f"Deleted {channels} channels.\n{err if errors else ''}")

    @deletechannels.command(name="channel", aliases=['chan'])
    async def chandel(self,ctx, channels:commands.Greedy[typing.Union[discord.TextChannel, discord.VoiceChannel, discord.StageChannel, discord.Thread]]=[]):
        """Deletes the channel."""
        v = Confirm(ctx)
        channelno = 0
        errors = []
        if len(channels) == 0:
            channels.append(ctx.channel)
        embed = discord.Embed(title="Channel Deletion", description=f"Deleting {len(channels)} channels.\n{' '.join([chan.mention for chan in channels])}\nClick Confirm.", color=discord.Color.brand_red())
        v.msg = await ctx.reply(embed=embed, view=v)
        msgv = discord.ui.View.from_message(v.msg)
        for vd in msgv.children:
            vd.disabled = True
        await v.wait()
        if v.value is False:
            embed.description = 'Cancelled.'
            embed.color = discord.Color.red()
            await v.msg.edit(embed=embed, view=msgv)
        elif v.value:
            embed.description += '\nConfirmed.'
            embed.color = discord.Color.green()
            await v.msg.edit(embed=embed, view=msgv)
            for channel in channels:
                try:
                    await channel.delete()
                except:
                    errors.append(channel.id)
                else:
                    channelno += 1
            err = 'Errors:\n' + ' '.join([f'<#{id}>' for error in errors if error])
            await ctx.reply(f"Deleted {channelno} channels.\n{err if errors else ''}")

    @deletechannels.command(name="allchannel", aliases=['all', 'allchannels'])
    async def purgeallchannel(self,ctx):
        """Deletes all the channels."""
        if ctx.author != ctx.guild.owner:
            await ctx.reply("You are not server owner.")
            return
        """Deletes all channels in the server."""
        v = Confirm(ctx)
        embed = discord.Embed(title="Guild Channel Deletion", description=f"Deleting {len(ctx.guild.channels)} channels.\nClick Confirm.", color=discord.Color.brand_red())
        v.msg = await ctx.reply(embed=embed, view=v)
        msgv = discord.ui.View.from_message(v.msg)
        for vd in msgv.children:
            vd.disabled = True
        await v.wait()
        if v.value is False:
            embed.description = 'Cancelled.'
            embed.color = discord.Color.red()
            await v.msg.edit(embed=embed, view=msgv)
        elif v.value:
            embed.description += '\nConfirmed.'
            embed.color = discord.Color.green()
            await v.msg.edit(embed=embed, view=msgv)
            channels = 0
            errors = []
            for channel in ctx.guild.channels:
                try:
                    await channel.delete(reason=f"Deleted by {ctx.author.name}.")
                except:
                    errors.append(channel.id)
                else:
                    channels += 1
            err = 'Errors:\n' + ' '.join(f'<#{id}>' for error in errors if error)
            await ctx.reply(f"Deleted {channels} channels.\n{err if errors else ''}")

    @commands.command(name="first", aliases=["firstmessage", "1"])
    @commands.cooldown(1,8)
    async def first(self, ctx):
        """Gets the first message of the channel."""
        m = await ctx.channel.history(limit=1, oldest_first=True).flatten()
        msg = m[0]
        embed=discord.Embed(title="First Message", url=msg.jump_url, description=f"[Jump]({msg.jump_url})\n{msg.content}", color=discord.Color.random(), timestamp=msg.created_at)
        embed.set_author(icon_url=msg.author.avatar, name=msg.author)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="hide", aliases=['h'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def hide(self, ctx, channels:commands.Greedy[typing.Union[discord.CategoryChannel, discord.TextChannel, discord.VoiceChannel, discord.StageChannel]]=[], target:typing.Union[discord.Role, discord.Member]=None):
        """Hides a channel for a certain role / channel / member."""
        async def overwrite(channel):
            o = channel.overwrites_for(target)
            if not o.view_channel:
                return
            o.view_channel=False
            await channel.set_permissions(target, overwrite=o)
        if not target:
            target = ctx.guild.default_role
        if not channels:
            channels = [ctx.channel]
        for c in channels:
            if type(c) is discord.CategoryChannel:
                for cc in c.channels:
                    await overwrite(cc)
            await overwrite(c)
        c = '\n'.join([c.mention for c in channels])
        e = discord.Embed(title='Channel Hide', description=f"Hidden {len(channels)} channel(s):\n{c}\nfor {target.mention}", color=discord.Color.random())
        await ctx.reply(embed=e)

    @commands.command(name="unhide", aliases=['uh'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_permissions=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def unhide(self, ctx, channels:commands.Greedy[typing.Union[discord.CategoryChannel, discord.TextChannel, discord.VoiceChannel, discord.StageChannel]]=[], target:typing.Union[discord.Role, discord.Member]=None):
        """Unhides a channel for a certain role / channel / member."""
        async def overwrite(channel):
            o = channel.overwrites_for(target)
            if o.view_channel:
                return
            o.view_channel=True
            await channel.set_permissions(target, overwrite=o)
        if not target:
            target = ctx.guild.default_role
        if not channels:
            channels = [ctx.channel]
        for c in channels:
            if type(c) is discord.CategoryChannel:
                for cc in c.channels:
                    await overwrite(cc)
            await overwrite(c)
        c = '\n'.join([c.mention for c in channels])
        e = discord.Embed(title='Channel Unide', description=f"Unhidden {len(channels)} channel(s):\n{c}\nfor {target.mention}", color=discord.Color.random())
        await ctx.reply(embed=e)

    @commands.command(name="lock", aliases=['l'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_permissions=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def lock(self, ctx, channels:commands.Greedy[typing.Union[discord.CategoryChannel, discord.TextChannel, discord.VoiceChannel, discord.StageChannel]]=[], target:typing.Union[discord.Role, discord.Member]=None):
        """Locks a channel for a certain role / channel / member."""
        async def overwrite(channel):
            o = channel.overwrites_for(target)
            if not o.send_messages:
                return
            o.send_messages=False
            await channel.set_permissions(target, overwrite=o)
        if not target:
            target = ctx.guild.default_role
        if not channels:
            channels = [ctx.channel]
        for c in channels:
            if type(c) is discord.CategoryChannel:
                for cc in c.channels:
                    await overwrite(cc)
            await overwrite(c)
        c = '\n'.join([c.mention for c in channels])
        e = discord.Embed(title='Channel Lock', description=f"Locked {len(channels)} channel(s):\n{c}\nfor {target.mention}", color=discord.Color.random())
        await ctx.reply(embed=e)

    @commands.command(name="unlock", aliases=['ul'])
    @commands.cooldown(1,2)
    @commands.has_permissions(manage_permissions=True)
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True)
    async def unlock(self, ctx, channels:commands.Greedy[typing.Union[discord.CategoryChannel, discord.TextChannel, discord.VoiceChannel, discord.StageChannel]]=[], target:typing.Union[discord.Role, discord.Member]=None):
        """Unlocks a channel for a certain role / channel / member."""
        async def overwrite(channel):
            o = channel.overwrites_for(target)
            if o.send_messages:
                return
            o.send_messages=True
            await channel.set_permissions(target, overwrite=o)
        if not target:
            target = ctx.guild.default_role
        if not channels:
            channels = [ctx.channel]
        for c in channels:
            if type(c) is discord.CategoryChannel:
                for cc in c.channels:
                    await overwrite(cc)
            await overwrite(c)
        c = '\n'.join([c.mention for c in channels])
        e = discord.Embed(title='Channel Unlock', description=f"Unlocked {len(channels)} channel(s):\n{c}\nfor {target.mention}", color=discord.Color.random())
        await ctx.reply(embed=e)

    @commands.command(name="export")
    @commands.max_concurrency(1, commands.BucketType.channel)
    @commands.has_permissions(administrator=True)
    async def export(self, ctx, destination, first_message_id:typing.Optional[int]=None, limit:typing.Optional[int]=100, mode:typing.Literal['clean']=None):
        """Exports chat messages to another channel.\n<first_message_id> is the id of the first message you wanna start exporting from.\n<limit> is the max number of messages to export."""
        destination_channel = self.bot.get_channel(int(re.sub("[^0-9]", "", destination)))
        if len(f"{first_message_id}") < 18:
            limit = first_message_id
            first_message_id = None
        if first_message_id:
            first_message_id = await ctx.channel.fetch_message(first_message_id)
        elif ctx.message.reference:
            first_message_id = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        
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
            if m == ctx.message:
                break
            try:
                if last_message is None or m.author.id != last_message.author.id:
                    raise
                attachments = m.attachments
                for attachment in attachments:
                    m.content += f'\n {attachment}'
                content = f"{last_message.content}\n" + (f"[{discord.utils.format_dt(m.created_at, style='d')}]({m.jump_url}) " if mode is None else '') + m.content if m.content else '\u200b'
                msg = await last_webhookmsg.edit(content=content, embeds=last_message.embeds + m.embeds, allowed_mentions=discord.AllowedMentions.none())
                last_webhookmsg = msg
                m.content = content
                last_message = m
            except:
                attachments = m.attachments
                for attachment in attachments:
                    m.content += f'\n {attachment}'
                content = (
                    (
                        f"[{discord.utils.format_dt(m.created_at, style='d')}]({m.jump_url}) "
                        if mode is None
                        else ''
                    )
                    + m.content
                    if m.content
                    else '\u200b'
                )
                if len(content) > 2000:
                    buffer = io.BytesIO(content.encode('utf-8'))
                    msg = await webhook.send(file=discord.File(buffer, filename='export.txt'), wait=True, username=m.author.name, avatar_url=m.author.avatar, embeds=last_message.embeds + m.embeds, allowed_mentions=discord.AllowedMentions.none())
                else:
                    msg = await webhook.send(content=content, wait=True, username=m.author.name, avatar_url=m.author.avatar, embeds=m.embeds, allowed_mentions=discord.AllowedMentions.none())
                    last_webhookmsg = msg
                    m.content = content
                    last_message = m

        await ctx.reply("Done")

    @commands.command(name='rename', aliases=['channelrename'])
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.max_concurrency(1, commands.BucketType.guild)
    async def channel_rename(self, ctx, channel:typing.Union[discord.TextChannel, discord.VoiceChannel, discord.StageChannel, discord.CategoryChannel]=None, *, name=None):
        """Renames a channel or channels."""
        if channel is not None:
            await channel.edit(name=name)
            await ctx.reply(channel.mention)
        else:
            e = discord.Embed(title="Channel Rename", description=f"Starting interactive session to rename all channels.", color=discord.Color.blue())
            msg = await ctx.reply(embed=e)
            edits = []
            def msg_check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            for channel in ctx.guild.channels:
                e.description = f"Target: {channel.mention}\nSend the channel name in chat to edit. Send `skip` to skip and `end` or `quit` to end the current session."
                await msg.edit(embed=e)
                try: 
                    response = await self.bot.wait_for('message', check=msg_check, timeout=180)
                    if 'skip' in response.content.lower():
                        pass
                    elif 'end' in response.content.lower() or 'quit' in response.content.lower():
                        break
                    else:
                        edits.append(tuple((channel, channel.name, response.content)))
                    await response.delete()
                except:
                    pass
            e.description = f"Renaming {len(edits)} channels."
            await msg.edit(embed=e, view=None)
            for chan in edits:
                await chan[0].edit(name=chan[2])
            result = await ctx.reply(embed=discord.Embed(title="Channel Rename", description='\n'.join(f"{chan[0].mention} {chan[1]} -> {chan[2]}" for chan in edits), color=discord.Color.green()))
            e.description=f"Session Ended\n[Result]({result.jump_url})"
            await msg.edit(embed=e)

    @commands.group(name='overwrites', aliases=['ow'], invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def overwrites(self, ctx, channel:typing.Optional[typing.Union[discord.CategoryChannel, discord.TextChannel, discord.VoiceChannel, discord.StageChannel]]=None, target:commands.Greedy[typing.Union[discord.Role, discord.Member]]=None):
        """Lists out permission overwrites in this channel."""
        if not channel:
            channel = ctx.channel
        text = f"Channel overwrites for {channel.name}\n"
        try:
            if channel.permissions_synced:
                text += f"Synced with {channel.category.name}"
        except:
            pass
        overwrites = channel.overwrites if not target else target
        for o in overwrites:
            text += f"""\n{o.id} {o.name}\n"""
            for perm, value in channel.overwrites_for(o):
                if value in (True, False):
                    emoji = '✅' if value else '❌'
                    text += f"▪ {emoji} {perm.replace('_', ' ').title()}\n"
        buffer = io.BytesIO(text.encode('utf-8'))
        await ctx.reply(file=discord.File(buffer, filename='overwrites.txt'))

    @overwrites.command(name='sync', aliases=['s'])
    async def overwrites_remove(self, ctx, channel:typing.Optional[typing.Union[discord.CategoryChannel, discord.TextChannel, discord.VoiceChannel, discord.StageChannel]]=None):
        """Syncs the channel permission with the category permissions."""
        if not channel:
            channel = ctx.channel
        if not channel.category:
            return await ctx.reply('No category.')
        await channel.edit(sync_permissions=True)
        await ctx.reply(f"Permission for {channel.mention} has been synced with {channel.category.mention}.")



def setup(bot):
    bot.add_cog(ServerCog(bot))