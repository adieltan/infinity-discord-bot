import discord, random, string, os, asyncio, sys, math, requests, json, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.ext.commands.errors import PrivateMessageOnly
from discord.ext import commands, tasks



import traceback
from thefuzz import process
class ListenerCog(commands.Cog, name='Listener'):
    """📢 Listening Commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.bot.commands_invoked += 1


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.bot.process_commands(after)

    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        embed=discord.Embed(title="Guild Join", description=f"Owner: {guild.owner.mention}\nMember Count: {guild.member_count}", color=discord.Color.green())
        try:
            embed.set_author(name=guild.name, icon_url=guild.icon if guild.icon else discord.embeds.MaybeEmpty)
            embed.set_thumbnail(url=f"{guild.icon}")
        except Exception as e:
            await self.bot.changes.send(f"Error\n{e}")
        if guild.banner is not None:
            embed.set_image(url=f"{guild.banner}")
        await self.bot.changes.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild:discord.Guild):
        embed=discord.Embed(title="Guild Leave", description=f"Owner: {guild.owner.mention}\nMember Count: {guild.member_count}", color=discord.Color.red())
        try:
            embed.set_author(name=guild.name, icon_url=guild.icon if guild.icon else discord.embeds.MaybeEmpty)
            embed.set_thumbnail(url=f"{guild.icon}")
        except Exception as e:
            await self.bot.changes.send(f"Error\n{e}")
        if guild.banner is not None:
            embed.set_image(url=f"{guild.banner}")
        await self.bot.changes.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error (self, ctx, error):
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
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        ignored = (discord.Forbidden)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'`{ctx.command}` can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.reply(f"`{ctx.command}` can only be used in Private Messages.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(f"You don't have {', '.join(error.missing_permissions)} perms")
        elif isinstance(error, commands.CheckFailure):
            await ctx.message.add_reaction('⛔')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"The bot dosen't have {', '.join(error.missing_permissions)} perms", mention_author=True)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(embed=discord.Embed(title="Command is on cooldown", description=f"Retry again in {round(error.retry_after)} seconds.", color=discord.Color.dark_gold()))
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.reply(embed=discord.Embed(title='Too many Concurrent Uses', description=f"{error.number} concurrent uses per {error.per}"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(embed=discord.Embed(title="Missing Required Argument", description=f"`{error.param.name}` is a required argument that is missing.\n\nUsage:\n```\n{ctx.prefix}{ctx.command.signature}\n```", color=discord.Color.dark_teal()))
        elif isinstance(error, commands.NotOwner):
            embed=discord.Embed(title="Owner only command", description=f"Imagine using this.")
            embed.set_image(url="https://media1.tenor.com/images/ee1ac104f196033fc373abb7754d84d2/tenor.gif?itemid=17900652")
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            try:
                await ctx.message.add_reaction("<:exclamation:876077084986966016>")
            except:
                pass
        elif isinstance(error, discord.errors.NotFound):
            codes = {10003}
            if error.code in codes:
                return

        else:            # All other Errors not returned come here. And we can just print the default TraceBack.
            embed=discord.Embed(title=f"{type(error).__name__}", description=f"{str(error)}", color=discord.Color.red())
            embed.timestamp = discord.utils.utcnow()
            try:
                await ctx.reply(embed=embed)
            except:
                await ctx.send(embed=embed)
            embed=discord.Embed(title="Error", description=f"{ctx.author.mention}\nIgnoring exception in command {ctx.command}", color=discord.Color.random())
            embed.timestamp=discord.utils.utcnow()
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            embed.set_footer(text=ctx.author.id)
            embed.add_field(name="Info", value=f"[{ctx.message.content}]({ctx.message.jump_url})\n`⬇` **Traceback**")
            tb_str = traceback.format_exception(type(error), value=error, tb=error.__traceback__)
            text = ''.join(tb_str)
            chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
            for chunk in chunks:
                embed.add_field(name="\u200b", value=f"```py\n{chunk}\n```", inline=False)
            await self.bot.errors.send(embed=embed)

def setup(bot):
    bot.add_cog(ListenerCog(bot))