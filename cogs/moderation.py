import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 

class ModerationCog(commands.Cog, name='Moderation'):
    """*Moderation Commands.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban')
    @commands.cooldown(1,5)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.User, *, reason=None):
        """Bans a user."""
        if member == None or member == ctx.message.author:
            await ctx.reply("You cannot ban yourself.", mention_author=False)
            return
        mem = ctx.guild.get_member(member.id)
        if type(mem) is discord.Member:
            member = mem
            if (ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner.id) or member.id == ctx.guild.owner.id:
                await ctx.reply("Failed due to role hierarchy.")
                return
            else:
                reason1 = f"Banned by {ctx.author.name} for {reason}"
                try:
                    await ctx.guild.ban(member, reason=reason1)
                    await ctx.reply(f'**{member}** was ***BANNED***\nReason: __{reason}__', mention_author=False)
                    message = f"You have been banned from {ctx.guild.name} by {ctx.author.mention} for {reason}"
                    try:
                        await member.send(message)
                    except:
                        await ctx.message.add_reaction("\U0000274c")
                except:
                    await ctx.reply("Missing permissions.")
        elif type(member) is discord.User:
                reason = f"Banned by {ctx.author.name} for {reason}"
                await ctx.guild.ban(member, reason=reason)
                await ctx.reply(f'**{member}** was ***BANNED***\nReason: __{reason}__', mention_author=False)
        
    @commands.command(name='unban')
    @commands.cooldown(1,5)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User, *, reason=None):
        """Unbans a user."""
        bans = tuple([m.user for m in await ctx.guild.bans()])
        if member not in bans:
            await ctx.reply("User not banned.", mention_author=False)
        else:
            reason = f"Unbanned by {ctx.author.name} for {reason}"
            try:
                await ctx.guild.unban(member, reason=reason)
                await ctx.reply(f'**{member}** was ***UNBANNED***\nReason: __{reason}__', mention_author=False)
            except:
                await ctx.reply(f'Error?')

    @commands.command(name="massban")
    @commands.cooldown(1,10)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def massban(self, ctx, *, ids:str):
        """Massban users."""
        await ctx.trigger_typing()
        ids = ids.split(' ')
        reason = f"Massbanned by {ctx.author.name}"
        banned = []
        error = []
        for id in ids:
            try:
                await self.bot.http.ban(int(id), ctx.guild.id, delete_message_days=0)
            except:
                error.append(id)
            else:
                banned.append(id)
        await ctx.send(f"""Banned {len(banned)} users: {', '.join([f"<@{id}>" for id in banned])}\nFailed to ban {len(error)} users:{', '.join([f"<@{id}>" for id in error])}""")


    @commands.command(name='kick')
    @commands.cooldown(1,5)
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a user."""
        if member == None or member == ctx.message.author:
            await ctx.reply("You cannot kick yourself", mention_author=False)
            return
        elif (ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner.id) or member.id == ctx.guild.owner.id:
            await ctx.reply("Failed due to role hierarchy.")
            return
        message = f"You have been kicked from {ctx.guild.name} for {reason}"
        try:
            await member.send(message)
        except:
            await ctx.message.add_reaction("\U0000274c")
        await ctx.guild.kick(member, reason=reason)
        await ctx.reply(f'**{member}** was ***KICKED***\nReason: __{reason}__', mention_author=False)

def setup(bot):
    bot.add_cog(ModerationCog(bot))