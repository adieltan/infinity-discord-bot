import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext.commands.core import check
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 

from collections import Counter


class ServerCog(commands.Cog, name='server'):
    """*Server Commands*"""
    def __init__(self, bot):
        self.bot = bot


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
            discord.TextChannel: '<:text_channel:863265248585056316>',
            discord.VoiceChannel: '<:voice_channel:863265294240055316>',
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
                info.append(f'\U00002705 {label}')

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

    @commands.group(name="autoresponse", aliases=["ar"])
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def ar(self,ctx):
        """Autoresponse commands for the server."""
        if ctx.invoked_subcommand is None:
            await ctx.reply("Its `= ar add` nabbie. Depending on your prefix tho.")

    @ar.command(name="add")
    async def add_ar(self, ctx, trigger:str):
        """Adds a text response for the trigger."""
        trigger = trigger.lower()
        results= await self.bot.dba['server'].find_one({"_id":ctx.guild.id}) or {}
        try:results['autoresponse']
        except:results['autoresponse'] = {}
        if len(list(results['autoresponse'].keys())) >= 5:
            await ctx.reply("This guild has reached the maximum number of autoresponse which is 5.")
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
            response = self.bot.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
            verify = False
        else:
            verify = True
        if verify is True:
            await ctx.reply(f"Starting to delete {category.mention}")
        elif verify is False:
            await ctx.reply(f"Failed to verify.")
            return
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
            response = self.bot.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
            verify = False
        else:
            verify = True
        if verify is True:
            await ctx.reply(f"Starting to delete {channel.mention}")
        elif verify is False:
            await ctx.reply(f"Failed to verify.")
            return
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
            response = self.bot.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
            verify = False
        else:
            verify = True
        if verify is True:
            await ctx.reply(f"Starting to delete all channels.")
        elif verify is False:
            await ctx.reply(f"Failed to verify.")
            return
        channels = ctx.guild.channels
        c=0
        for channel in channels:
            try:
                await channel.delete(reason=f"Deleted by {ctx.author.name}.")
                c += 1
            except:
                pass
        await ctx.reply(f"Deleted {c} channels.")

def setup(bot):
    bot.add_cog(ServerCog(bot))