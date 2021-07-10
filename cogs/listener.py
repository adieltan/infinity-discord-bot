import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt

import traceback
class ListenerCog(commands.Cog, name='Listener'):
    """*Listening Commands.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message (self, message: discord.Message):
        if ('732917262297595925') in message.clean_content.lower():
            await message.add_reaction("\U0000267e")
        elif message.author.bot is True:
            return
        else:
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
                            await message.reply(response)
                        except:pass
        if ('732917262297595925') in message.content.lower():
            try:
                await message.add_reaction("\U0000267e")
            except:pass



    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        changes = self.bot.get_channel(859779506038505532)
        embed=discord.Embed(title="Guild Join", description=f"Owner: {guild.owner.mention}\nMember Count: {guild.member_count}", color=discord.Color.green())
        embed.set_author(name=guild.name, icon_url=guild.icon_url)
        embed.set_thumbnail(url=f"{guild.icon_url}")
        if guild.banner_url is not None:
            embed.set_image(url=f"{guild.banner_url}")
        await changes.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        changes = self.bot.get_channel(859779506038505532)
        embed=discord.Embed(title="Guild Leave", description=f"Owner: {guild.owner.mention}\nMember Count: {guild.member_count}", color=discord.Color.red())
        embed.set_author(name=guild.name, icon_url=guild.icon_url)
        embed.set_thumbnail(url=f"{guild.icon_url}")
        if guild.banner_url is not None:
            embed.set_image(url=f"{guild.banner_url}")
        await changes.send(embed=embed)

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
        ignored = (commands.CommandNotFound)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(f"You don't have {', '.join(error.missing_perms)} perms")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(embed=discord.Embed(title="Command is on cooldown", description=f"Retry again in {error.retry_after} seconds.", color=discord.Color.dark_gold()))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(embed=discord.Embed(title="Missing Required Argument", description=f"`{error.param.name}`` is a required argument that is missing.", color=discord.Color.dark_teal()))
        elif isinstance(error, commands.NotOwner):
            embed=discord.Embed(title="Owner only command", description=f"Imagine using this.")
            embed.set_image(url="https://media1.tenor.com/images/ee1ac104f196033fc373abb7754d84d2/tenor.gif?itemid=17900652")
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            pass
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            embed=discord.Embed(title=f"{type(error)}", description=f"{str(error)}", color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=embed)
            #reporting
            reports = self.bot.get_channel(825900714013360199)
            embed=discord.Embed(title="Error", description=f"{ctx.author.mention}\nIgnoring exception in command {ctx.command}", color=discord.Color.random())
            embed.timestamp=datetime.datetime.utcnow()
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=ctx.author.id)
            embed.add_field(name="Info", value=f"{ctx.channel.mention} [{ctx.message.content}]({ctx.message.jump_url})\n`⬇` **Traceback**")
            tb_str = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
            text = ''.join(tb_str)
            chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
            page = 0
            for chunk in chunks:
                page += 1
                embed.add_field(name=f"Page {page} ", value=f"```py\n{chunk}\n```", inline=False)
            
            await reports.send(embed=embed)

def setup(bot):
    bot.add_cog(ListenerCog(bot))