import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext.commands.errors import PrivateMessageOnly
from discord.ext import commands, tasks



import traceback
from thefuzz import process
class ListenerCog(commands.Cog, name='Listener'):
    """📢 Listening Commands."""
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.bot.process_commands(after)

    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        if not guild.owner:
            return
        embed=discord.Embed(title="Guild Join", description=f"Owner: {guild.owner.mention}\nMember Count: {guild.member_count}", color=discord.Color.green())
        embed.set_author(name=guild.name, icon_url=guild.icon or 'https://tenor.com/bjHxN.gif')
        embed.set_thumbnail(url=guild.icon or 'https://tenor.com/bjHxN.gif')
        if guild.banner is not None:
            embed.set_image(url=f"{guild.banner}")
        try:
            await self.bot.changes.send(embed=embed)
        except:
            await self.bot.changes.send(f"**Guild Join**\n{guild.name}\nOwner{guild.owner.mention}\nMember Count: {guild.member_count}", allowed_mentions=discord.AllowedMentions.none())

    @commands.Cog.listener()
    async def on_guild_remove(self, guild:discord.Guild):
        if not guild.owner:
            return
        embed=discord.Embed(title="Guild Leave", description=f"Owner: {guild.owner.mention}\nMember Count: {guild.member_count}", color=discord.Color.red())
        embed.set_author(name=guild.name, icon_url=guild.icon or 'https://tenor.com/bjHxN.gif')
        embed.set_thumbnail(url=guild.icon or 'https://tenor.com/bjHxN.gif')
        if guild.banner is not None:
            embed.set_image(url=f"{guild.banner}")
        try:
            await self.bot.changes.send(embed=embed)
        except:
            await self.bot.changes.send(f"**Guild Join**\n{guild.name}\nOwner{guild.owner.mention}\nMember Count: {guild.member_count}", allowed_mentions=discord.AllowedMentions.none())

    @commands.Cog.listener()
    async def on_message(self, msg):
        await self.bot.wait_until_ready()
        if type(msg.channel) != discord.Thread:
            return
        if msg.channel.parent_id != 900699395639623711 or msg.author.id == self.bot.user.id or msg.content.startswith('=') or str(msg.author.id) == msg.channel.name:
            return
        try:
            supportuser = self.bot.get_user(int(msg.channel.name))
            e = discord.Embed(title="Support Reply", description=msg.content).set_author(name=msg.author.name, icon_url=msg.author.avatar)
            await msg.add_reaction('<a:verified:876075132114829342>')
            def check(reaction, user):
                return str(reaction.emoji) == '<a:verified:876075132114829342>'
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=check)
            await supportuser.send(embeds = [e]+msg.embeds)
            await msg.clear_reactions()
        except:
            await msg.add_reaction('<:exclamation:876077084986966016>')
        
        

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):  # sourcery no-metrics
        await self.bot.wait_until_ready()
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return
        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog and cog._get_overridden_method(cog.cog_command_error) is not None:
            return
        ignored = (discord.Forbidden)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return
        if type(ctx.channel) is discord.Thread and ctx.channel.parent_id == 900699395639623711:
            return
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'`{ctx.command}` can not be used in Private Messages.')
            except discord.HTTPException:
                return
        elif isinstance(error, commands.PrivateMessageOnly):
            return await ctx.reply(f"`{ctx.command}` can only be used in Private Messages.")
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.reply(f"You don't have {', '.join(error.missing_permissions)} perms")
        elif isinstance(error, commands.CheckFailure):
            return await ctx.message.add_reaction('⛔')
        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(f"The bot dosen't have {', '.join(error.missing_permissions)} perms", mention_author=True)
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.reply(embed=discord.Embed(title="Command is on cooldown", description=f"Retry again in {round(error.retry_after)} seconds.", color=discord.Color.dark_gold()))
        elif isinstance(error, commands.MaxConcurrencyReached):
            return await ctx.reply(embed=discord.Embed(title='Too many Concurrent Uses', description=f"{error.number} concurrent uses per {error.per}"))
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.reply(embed=discord.Embed(title="Missing Required Argument", description=f"`{error.param.name}` is a required argument that is missing.\n\nUsage:\n```\n{ctx.prefix}{ctx.invoked_with}{ctx.command.signature}\n```", color=discord.Color.dark_teal()))
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="Owner only command", description='Imagine using this.').set_image(url="https://media1.tenor.com/images/ee1ac104f196033fc373abb7754d84d2/tenor.gif?itemid=17900652")
            return await ctx.reply(embed=embed)
        elif isinstance(error, commands.CommandNotFound) and type(ctx.channel) is discord.DMChannel:
            channel = ctx.bot.get_channel(900699395639623711)
            tchannel = channel.threads
            tnames = [tc.name for tc in tchannel]
            e = discord.Embed(title="Support Ticket", description=ctx.message.content).set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            if str(ctx.author.id) in tnames:
                await tchannel[tnames.index(str(ctx.author.id))].send(embed=e)
            else:
                msg = await channel.send(embed=e)
                thread = await channel.create_thread(name=f"{ctx.author.id}", message=msg)
                await thread.send(f'<@&843375370627055637>\n{ctx.author.mention} opened a support ticket.\nDO NOT SPAM\nReact with <a:verified:876075132114829342> after the bot reacts to send your message.', allowed_mentions=discord.AllowedMentions.all())
            return await ctx.message.add_reaction('<a:verified:876075132114829342>')
        elif isinstance(error, commands.CommandNotFound):
            try:
                return await ctx.message.add_reaction("<:exclamation:876077084986966016>")
            except:
                return
        elif isinstance(error, discord.errors.NotFound):
            codes = {10003}
            if error.code in codes:
                return

        embed = discord.Embed(
                title=f"{type(error).__name__}",
                description=f'{error}',
                color=discord.Color.red(),
                timestamp = discord.utils.utcnow()
            )
        try:
            await ctx.reply(embed=embed)
        except:
            await ctx.send(embed=embed)
        text = ''.join(traceback.format_exception(type(error), value=error, tb=error.__traceback__))
        buffer = io.BytesIO(text.encode('utf-8'))
        await self.bot.errors.send(f"{discord.utils.format_dt(discord.utils.utcnow())} {ctx.author.mention} {ctx.author.name} `{ctx.author.id}`\nIgnoring exception in command {ctx.command}\n```fix\n{ctx.message.content}```{ctx.message.jump_url}\n", file=discord.File(buffer, filename='command_error_traceback.txt'), allowed_mentions=discord.AllowedMentions.none())

def setup(bot):
    bot.add_cog(ListenerCog(bot))