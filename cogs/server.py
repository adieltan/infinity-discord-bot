import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

from collections import Counter, OrderedDict
from PIL import Image
from ._utils import Database
class Menu(discord.ui.View):
    def __init__(self, ctx, pages:list[discord.Embed]) -> None:
        super().__init__(timeout=60)
        self.current_page = 0
        self.pages = pages
        self.ctx = ctx
        self.value = None

    async def interaction_check(self, interaction:discord.Interaction):
        return interaction.user.id == self.ctx.author.id

    @discord.ui.button(emoji='<:rewind:899651431294967908>', style=discord.ButtonStyle.blurple)
    async def first_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[0])
        self.current_page = 0

    @discord.ui.button(emoji='<:left:876079229769482300>', style=discord.ButtonStyle.blurple)
    async def before_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[(self.current_page - 1) % len(self.pages)])
        self.current_page = (self.current_page - 1) % len(self.pages)

    @discord.ui.button(emoji='<:right:876079229710762005>', style=discord.ButtonStyle.blurple)
    async def next_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[(self.current_page + 1) % len(self.pages)])
        self.current_page = (self.current_page + 1) % len(self.pages)

    @discord.ui.button(emoji='<:forward:899651567869906994>', style=discord.ButtonStyle.blurple)
    async def last_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[len(self.pages) -1 ])
        self.current_page = len(self.pages) - 1

class Confirm(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.value = None
        self.ctx = ctx
    
    async def interaction_check(self, interaction:discord.Interaction):
        return interaction.user.id == self.ctx.author.id

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = False
        self.stop()

class ServerCog(commands.Cog, name='Server'):
    """🌐 Tools for your server."""
    def __init__(self, bot):
        self.bot = bot        

    @commands.command(name='prefix')
    @commands.cooldown(1,8)
    @commands.guild_only()
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
            results['autoresponse'][trigger] = f"{response.clean_content}"
            await Database.edit_server(self, ctx.guild.id, results)
            await ctx.reply(embed=discord.Embed(title="New Autoresponse", description=f"Response for `{trigger}` set to `{response}`"))
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

    @deletechannels.command(name="category", aliases=['cat'])
    async def catdel(self,ctx, categorys:commands.Greedy[discord.CategoryChannel]):
        """Deletes all the channels in the category."""
        view = Confirm(ctx)
        channels = 0
        errors = []
        embed = discord.Embed(title="Category Deletion", description=f"Deleting {len(categorys)} categories.\n{' '.join([cate.mention for cate in categorys])}\nClick Confirm.", color=discord.Color.brand_red())
        msg = await ctx.reply(embed=embed, view=view)
        msgv = discord.ui.View.from_message(msg)
        for v in msgv.children:
            v.disabled = True
        await view.wait()
        if not view.value:
            embed.description = 'Timeout.'
            await msg.edit(embed=embed, view=msgv)
        elif view.value:
            embed.description += '\nConfirmed.'
            embed.color = discord.Color.green()
            await msg.edit(embed=embed, view=msgv)
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
        else:
            embed.description = 'Cancelled.'
            embed.color = discord.Color.red()
            await msg.edit(embed=embed, view=msgv)

    @deletechannels.command(name="channel", aliases=['chan'])
    async def chandel(self,ctx, channels:commands.Greedy[typing.Union[discord.TextChannel, discord.VoiceChannel, discord.StageChannel, discord.Thread]]=[]):
        """Deletes the channel."""
        view = Confirm(ctx)
        channelno = 0
        errors = []
        if len(channels) == 0:
            channels.append(ctx.channel)
        embed = discord.Embed(title="Channel Deletion", description=f"Deleting {len(channels)} channels.\n{' '.join([chan.mention for chan in channels])}\nClick Confirm.", color=discord.Color.brand_red())
        msg = await ctx.reply(embed=embed, view=view)
        msgv = discord.ui.View.from_message(msg)
        for v in msgv.children:
            v.disabled = True
        await view.wait()
        if not view.value:
            embed.description = 'Timeout.'
            await msg.edit(embed=embed, view=msgv)
        elif view.value:
            embed.description += '\nConfirmed.'
            embed.color = discord.Color.green()
            await msg.edit(embed=embed, view=msgv)
            for channel in channels:
                try:
                    await channel.delete()
                except:
                    errors.append(channel.id)
                else:
                    channelno += 1
            err = 'Errors:\n' + ' '.join([f'<#{id}>' for error in errors if error])
            await ctx.reply(f"Deleted {channelno} channels.\n{err if errors else ''}")
        else:
            embed.description = 'Cancelled.'
            embed.color = discord.Color.red()
            await msg.edit(embed=embed, view=msgv)

    @deletechannels.command(name="allchannel")
    async def purgeallchannel(self,ctx):
        """Deletes all the channels."""
        if ctx.author != ctx.guild.owner:
            await ctx.reply("You are not server owner.")
            return
        """Deletes the channel."""
        view = Confirm(ctx)
        embed = discord.Embed(title="Guild Channel Deletion", description=f"Deleting {len(ctx.guild.channels)} channels.\nClick Confirm.", color=discord.Color.brand_red())
        msg = await ctx.reply(embed=embed, view=view)
        msgv = discord.ui.View.from_message(msg)
        for v in msgv.children:
            v.disabled = True
        await view.wait()
        if not view.value:
            embed.description = 'Timeout.'
            await msg.edit(embed=embed, view=msgv)
        else:
            embed.description += '\nConfirmed.'
            embed.color = discord.Color.green()
            await msg.edit(embed=embed, view=msgv)
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
        meh = await ctx.channel.history(limit=1, oldest_first=True).flatten()
        message = meh[0]
        
        embed=discord.Embed(title="First Message", url=message.jump_url, description=f"[Jump]({message.jump_url})\n{message.content}", color=discord.Color.random())
        embed.timestamp = message.created_at
        embed.set_author(icon_url=message.author.avatar, name=message.author)
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
            channels.append(channel)
        if not target:
            target = ctx.guild.default_role
        if not channels:
            channels.append(ctx.channel)
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
            channels.append(channel)
        if not target:
            target = ctx.guild.default_role
        if not channels:
            channels.append(ctx.channel)
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
            channels.append(channel)
        if not target:
            target = ctx.guild.default_role
        if not channels:
            channels.append(ctx.channel)
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
            channels.append(channel)
        if not target:
            target = ctx.guild.default_role
        if not channels:
            channels.append(ctx.channel)
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
        if not first_message_id and ctx.message.reference:
            first_message_id = await ctx.channel.fetch_message(ctx.message.reference.message_id)
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

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self,ctx, no:int=None):
        """Purges a number of messages."""
        if not no:
            await ctx.reply(f"Purge commands: `user` `pins` `bot` `human`")
            return
        def pinc(msg):
            return not msg.pinned
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)
    
    @purge.command()
    async def user(self, ctx, user:discord.Member, no:int=100):
        """Purges messages from a user."""
        def pinc(msg):
            return msg.author == user and msg.pinned is not True
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)

    @purge.command()
    async def pins(self, ctx, no:int=100):
        """Purges a number of pinned messages."""
        def pinc(msg):
            return bool(msg.pinned)
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)

    @purge.command(name='bot', aliases=['bots'])
    async def bot(self, ctx, no:int=100):
        """Purges messages from bots."""
        def pinc(msg):
            return msg.author.bot == True and msg.pinned is not True
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)

    @purge.command(name='human', aliases=['humans'])
    async def human(self, ctx, no:int=100):
        """Purges messages from humans."""
        def pinc(msg):
            return msg.author.bot is False and msg.pinned is not True
        deleted = await ctx.channel.purge(limit=no+1, check=pinc)
        await ctx.send("Deleted *{}* message(s).".format(len(deleted)-1), delete_after=10)

    @commands.command(name="slowmode", aliases=["sm"])
    @commands.cooldown(1,3)
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self,ctx,seconds:int=0):
        """Sets the slowmode for the channel."""
        if seconds < 0:
            seconds *= -1
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.reply(f"The slowmode delay for this channel is now {seconds} seconds!")

    @commands.command(name="attachments", aliases=['attachment'])
    async def attachments(self, ctx, channelid_or_messageid:str=None):
        """Gets the url of all the attachments in the message referenced."""
        ref = ctx.message.reference
        msg = None
        if channelid_or_messageid is None and ref is not None:
            msg = await ctx.channel.fetch_message(ref.message_id)
        elif not channelid_or_messageid:
            await ctx.reply('You have to reply to or provide the message id to the message.')

        else:
            ids = re.findall("\d{18}", channelid_or_messageid)
            if len(ids) < 1:
                await ctx.reply("Can't find id.")
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


    @commands.command(name='userinfo', aliases=['ui', 'user', 'whois', 'i'])
    async def userinfo(self, ctx, *, member: typing.Union[discord.Member, discord.User]=None):
        """Gets info about the user."""
        if not member:
            member = ctx.author
        results = await Database.get_server(self, ctx.guild.id)
        leaves = results.get('leaveleaderboard', {}).get(f'{member.id}')
        if type(member) == discord.Member:
            if member.status == discord.Status.online:
                status = "🟢 Online"
            elif member.status == discord.Status.idle:
                status = "🟡 Idle"
            elif member.status == discord.Status.dnd:
                status = "🔴 DND"
            elif member.status == discord.Status.offline:
                status = "⚫ Offline"
            else:
                status = ''
            embed = discord.Embed(title="User Info", description=f'{member.mention} {member} [Avatar]({member.display_avatar})\n{status}\n', color=member.color, timestamp=discord.utils.utcnow(),)

            if member.activity:
                embed.description += f"{member.activity.name}"
            embed.set_author(name=f"{member.name}", icon_url=f'{member.display_avatar}')
            embed.add_field(name="Joined", value=f"{discord.utils.format_dt(member.joined_at, style='F')}\n{discord.utils.format_dt(member.joined_at, style='R')}")
            embed.add_field(name="Registered", value=f"{discord.utils.format_dt(member.created_at, style='F')}\n{discord.utils.format_dt(member.created_at, style='R')}")
            if member.nick:
                embed.description = f"`{member.nick}` " + embed.description
            
            if leaves:
                embed.description += f"\nLeft the server {leaves} times."
            if member.bot:
                embed.description += '\n🤖 Bot Account'
            if member.premium_since:
                embed.add_field(name="Server Boost", value=f"\nBoosting since: {discord.utils.format_dt(member.premium_since, style='f')}\n{discord.utils.format_dt(member.premium_since, style='R')}")
            embed.add_field(name="Roles", value=f"Top Role: {member.top_role.mention} `{member.top_role.id}`\nNumber of roles: {len(member.roles)}", inline=False)
            embed.set_thumbnail(url=member.display_avatar)
        else:
            embed = discord.Embed(
                title="User Info",
                description=f'{member.mention} {member} [Avatar]({member.avatar})',
                color=member.color,
                timestamp=discord.utils.utcnow(),
            )

            embed.set_author(name=f"{member.name}", icon_url=f'{member.avatar}')
            embed.add_field(name="Registered", value=f"{discord.utils.format_dt(member.created_at, style='F')}\n{discord.utils.format_dt(member.created_at, style='R')}")
            if member.bot:
                embed.description += '\n🤖 Bot Account'
            if leaves:
                embed.description += f"\nLeft the server {leaves} times."
            embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=f"ID: {member.id}")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='perms', aliases=['permissions', 'perm'])
    @commands.cooldown(1,5)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def check_permissions(self, ctx, object:typing.Union[discord.Member, discord.Role]=None):
        """Checks member's or role's permissions."""
        if not object:
            object = ctx.author
        if type(object) == discord.Role:
            perms = "```"
            for perm, value in object.permissions:
                emoji = '✅' if value is True else '❌'
                perms += f" {emoji} - {perm.replace('_',' ').title()}\n"
            perms += '```'
        elif type(object) == discord.Member:
            perms = '```\nServer - 🛑 \nCurrent Channel - 💬 \n'
            perms += ' 🛑 | 💬 \n'
            channel_perms = dict(iter(ctx.channel.permissions_for(object)))
            for perm, value in object.guild_permissions:
                if value is not False or channel_perms[perm] is not False:
                    emoji = '✅' if value is True else '❌'
                    cemoji = '✅' if channel_perms[perm] is True else '❌'
                    perms += f" {emoji} | {cemoji} - {perm.replace('_',' ').title()}\n"
            for perm, value in ctx.channel.permissions_for(object):
                if value is True and perm not in dict(iter(object.guild_permissions)):
                    perms += f" ❌ | ✅ - {perm.replace('_',' ').title()}\n"
            perms += '```'

        embed = discord.Embed(title='Permissions for:', description=object.mention+'\n'+perms, color=discord.Color.random())
        if object is discord.Member:
            embed.set_author(icon_url=object.avatar, name=str(object))
        await ctx.reply(embed=embed, mention_author=False)

    @commands.group(aliases=['r'], invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def role(self,ctx, member:discord.Member, *,  role:discord.Role):
        """Role Utilities."""
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        if role in member.roles:
            try:
                await member.remove_roles(role)
            except:
                await ctx.reply("Failed")
            else:
                embed = discord.Embed(title='User role remove', description=f"Removed {role.mention} from {member.mention}", color=role.color)
                embed.timestamp=discord.utils.utcnow()
                await ctx.reply(embed=embed, mention_author=False)
            return
        try:
            await member.add_roles(role)
        except:
            await ctx.reply("Failed")
        else:
            embed = discord.Embed(title='User role add', description=f"Added {role.mention} to {member.mention}", color=role.color)
            embed.timestamp=discord.utils.utcnow()
            await ctx.reply(embed=embed, mention_author=False)
    
    @role.command(name='colour', aliases=['color', 'c'])
    @commands.has_permissions(manage_roles=True)
    async def role_colour(self, ctx, role:discord.Role, colour_hex:str=None):
        "Changes/views the role colour."
        if not colour_hex:
            embed=discord.Embed(description=f"{role.mention}\nRGB: {role.colour.to_rgb()}\nInt: {role.colour.value}\nHex: {str(hex(role.colour.value))[2:]}", color=role.color)
            await ctx.reply(embed=embed, mention_author=False)
            return
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        c = tuple(int(colour_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        await role.edit(colour=discord.Colour.from_rgb(c[0], c[1], c[2]), reason="Changed by {ctx.author.name}.")
        embed = discord.Embed(title='Role Colour', description=f"{role.mention} colour edit.", color=discord.Colour.from_rgb(c[0], c[1], c[2]))
        embed.timestamp=discord.utils.utcnow()
        await ctx.reply(embed=embed, mention_author=False)


    @role.command()
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def delete(self,ctx, role:discord.Role, *, reason:str=None):
        """Deletes the role."""
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        try:
            await role.delete(reason=f"Deleted by {ctx.author.name} for {reason}.")
        except:
            await ctx.reply("Failed")
        else:
            
            embed = discord.Embed(title='Role deletion', description=f"{role.name} deleted.", color=discord.Color.random())
            embed.timestamp=discord.utils.utcnow()
            await ctx.reply(embed=embed, mention_author=False)

    @role.command()
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def create(self,ctx, rolename:str):
        """Creates the role."""
        try:
            role = await ctx.guild.create_role(name=rolename)
        except:
            await ctx.reply("Failed")
        else:
            
            embed = discord.Embed(title='Role creation', description=f"{role.mention} created.", color=role.color)
            embed.timestamp=discord.utils.utcnow()
            await ctx.reply(embed=embed, mention_author=False)

    @role.command()
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def add(self,ctx, member:discord.Member, *,  role:discord.Role):
        """Adds a role to a person."""
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        if role in member.roles:
            await ctx.reply("User already has role.")
            return
        try:
            await member.add_roles(role)
        except:
            await ctx.reply("Failed")
        else:
            embed = discord.Embed(title='User role add', description=f"Added {role.mention} to {member.mention}", color=role.color)
            embed.timestamp=discord.utils.utcnow()
            await ctx.reply(embed=embed, mention_author=False)

    @role.command()
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def remove(self,ctx, member:discord.Member, *, role:discord.Role):
        """Removes a role from a person."""
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        if role not in member.roles:
            await ctx.reply("User dosen't have the role.")
            return
        try:
            await member.remove_roles(role)
        except:
            await ctx.reply("Failed")
        else:
            embed = discord.Embed(title='User role remove', description=f"Removed {role.mention} from {member.mention}", color=role.color)
            embed.timestamp=discord.utils.utcnow()
            await ctx.reply(embed=embed, mention_author=False)

    @role.command(aliases=['i'])
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def info(self,ctx, *, role:discord.Role=None):
        """Shows infomation about a role."""
        if not role:
            role = ctx.guild.default_role
        embed = discord.Embed(title="Role Info", description=f"{role.mention} Pos: {role.position} `{role.id}`\nMembers: {len(role.members)}" , color=role.color)
        embed.add_field(name="Permissions", value='\u200b'+'\n'.join(perm.replace('_',' ').title() for perm, value in role.permissions if value))
        embed.set_footer(text="Role created at")
        embed.timestamp = role.created_at
        await ctx.reply(embed=embed, mention_author=True)

    @role.command(aliases=['d'])
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def dump(self,ctx, *, role:discord.Role):
        """Dumps members from the role."""
        people = role.members
        text ="```css\n" + '\n'.join((f'{m.name} ({m.id})')for m in people) + "```"
        await ctx.reply(text)

    @role.command(name="list", aliases=['l'])
    @commands.cooldown(1,7,commands.BucketType.channel)
    @commands.has_permissions(manage_roles=True)
    async def list(self, ctx):
        """Lists all the roles of the guild in a paginated way."""
        roles = ctx.guild.roles
        roles.reverse()
        n = 10
        pages = [roles[i:i + n] for i in range(0, len(roles), n)]
        pagess = [discord.Embed(title=f"{ctx.guild.name}'s Roles", description='\n'.join([f'{r.mention} `{r.id}`' for r in page]), color=discord.Color.random()).set_footer(text=f"{pages.index(page) + 1} / {len(pages)} pages").set_thumbnail(url=ctx.guild.icon) for page in pages]
        v = Menu(ctx, pagess)
        msg = await ctx.reply(embed=pagess[0], view=v)
        vd = discord.ui.View.from_message(msg)
        for item in vd.children:
            item.disabled = True
        await v.wait()
        await msg.edit(view=vd)

    @role.command(name='random', aliases=['randommember'])
    @commands.cooldown(1,2)
    @commands.guild_only()
    async def random(self, ctx, role:discord.Role=None, howmany:int=1):
        """Finds random peoples from the whole server or from roles."""
        if role == None:
            role = ctx.guild.default_role
        people = role.members
        winners = []
        if howmany > len(people):
            howmany = len(people)
        while len(winners) < howmany:
            win = random.choice(people)
            winners.append(win)
            people.remove(win)
        
        text= "\n".join([f'{winner.mention} `{winner.id}`' for winner in winners])
        embed = discord.Embed(title='Member randomizer', description=f'{text}', color=discord.Color.random())
        embed.timestamp=discord.utils.utcnow()
        embed.set_footer(text=f'Drawn {len(winners)} winners.')
        await ctx.reply(embed=embed, mention_author=False)

    @role.command(name="clear")
    @commands.cooldown(1,2)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def clear(self,ctx,*, member:discord.Member):
        """Removes all role from a member."""
        if ctx.author.top_role < member.top_role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        roles = member.roles
        roles.pop(0)
        await member.remove_roles(*tuple(roles), reason=f"`role clear` command by {ctx.author.name} ({ctx.author.id})")
        embed = discord.Embed(title='User role remove all', description=f"Removed **{len(roles)}** roles\n{' '.join([r.mention for r in roles])}", color=discord.Color.red())
        embed.timestamp=discord.utils.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @role.command(name="all")
    @commands.cooldown(1,2)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def roleall(self, ctx,*, role:discord.Role):
        """Adds a role to all members in the server."""
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        members = ctx.guild.members
        await ctx.reply(f"Trying to add `{role.name}` to {len(members)} members.")
        success = 0
        for m in members:
            if role not in m.roles:
                try:    await m.add_roles(role, reason=f"`role all` command by {ctx.author.name} ({ctx.author.id})")
                except: pass
                else:   success += 1
        await ctx.reply(embed=discord.Embed(title="Role all command", description=f"Sucessfully added {role.mention} to **{success}** members out of {len(members)} members.", color=discord.Color.green()))

    @role.command(name="bots")
    @commands.cooldown(1,2)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def rolebots(self, ctx,*, role:discord.Role):
        """Adds a role to all bots in the server."""
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        members = ctx.guild.members
        await ctx.reply(f"Trying to add `{role.name}` to bots in {len(members)} members.")
        success = 0
        for m in members:
            if m.bot is True and role not in m.roles:
                try:    await m.add_roles(role, reason=f"`role bots` command by {ctx.author.name} ({ctx.author.id})")
                except: pass
                else:   success += 1
        await ctx.reply(embed=discord.Embed(title="Role bots command", description=f"Sucessfully added {role.mention} to **{success}** bots out of {len(members)} members.", color=discord.Color.green()))

    @role.command(name="humans")
    @commands.cooldown(1,2)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def rolehumans(self, ctx,*, role:discord.Role):
        """Adds a role to all humans in the server."""
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        members = ctx.guild.members
        await ctx.reply(f"Trying to add `{role.name}` to humans in {len(members)} members.")
        success = 0
        for m in members:
            if m.bot is False and role not in m.roles:
                try:    await m.add_roles(role, reason=f"`role humans` command by {ctx.author.name} ({ctx.author.id})")
                except: pass
                else:   success += 1
        await ctx.reply(embed=discord.Embed(title="Role humans command", description=f"Sucessfully added {role.mention} to **{success}** humans out of {len(members)} members.", color=discord.Color.green()))

    @role.command(name="rall")
    @commands.cooldown(1,2)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def rolerall(self, ctx,*, role:discord.Role):
        """Removes a role from all members in the server."""
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        members = ctx.guild.members
        await ctx.reply(f"Trying to remove `{role.name}` from {len(members)} members.")
        success = 0
        for m in members:
            if role in m.roles:
                try:    await m.remove_roles(role, reason=f"`role rall` command by {ctx.author.name} ({ctx.author.id})")
                except: pass
                else:   success += 1
        await ctx.reply(embed=discord.Embed(title="Role rall command", description=f"Sucessfully removed {role.mention} from **{success}** members out of {len(members)} members.", color=discord.Color.red()))

    @role.command(name="rbots")
    @commands.cooldown(1,2)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def rolerbots(self, ctx,*, role:discord.Role):
        """Removes a role from all bots in the server."""
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        members = role.members
        await ctx.reply(f"Trying to remove `{role.name}` from bots in {len(members)} members.")
        success = 0
        for m in members:
            if m.bot is True and role in m.roles:
                try:    await m.remove_roles(role, reason=f"`role rbots` command by {ctx.author.name} ({ctx.author.id})")
                except: pass
                else:   success += 1
        await ctx.reply(embed=discord.Embed(title="Role rbots command", description=f"Sucessfully removed {role.mention} from **{success}** bots out of {len(members)} members.", color=discord.Color.red()))

    @role.command(name="rhumans")
    @commands.cooldown(1,2)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def rolerhumans(self, ctx,*, role:discord.Role):
        """Removes a role from all humans in the server."""
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        members = role.members
        await ctx.reply(f"Trying to remove `{role.name}` from humans in {len(members)} members.")
        success = 0
        for m in members:
            if m.bot is False and role in m.roles:
                try:    await m.remove_roles(role, reason=f"`role rhumans` command by {ctx.author.name} ({ctx.author.id})")
                except: pass
                else:   success += 1
        await ctx.reply(embed=discord.Embed(title="Role rhumans command", description=f"Sucessfully removed {role.mention} from **{success}** humans out of {len(members)} members.", color=discord.Color.green()))

def setup(bot):
    bot.add_cog(ServerCog(bot))