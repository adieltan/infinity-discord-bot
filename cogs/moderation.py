import discord, discord.voice_client, sys, traceback, json, pymongo, datetime, motor.motor_asyncio, re
from discord.enums import NotificationLevel
from discord.ext import commands
from discord.guild import Guild

class ModerationCog(commands.Cog, name='Moderation'):
    """*Moderation Commands.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prefix')
    @commands.cooldown(1,8)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, apref:str=None):
        """Changes the prefix for the bot in the server."""
        if apref is None:
            results = await self.bot.dba['server'].find_one({"_id":ctx.guild.id})
            pref = results["prefix"]
            await ctx.reply(f"The prefix for {ctx.guild.name} is `{pref}`", mention_author=False)
            pass
        elif len(apref) > 5:
            await ctx.reply("You can't have such a long prefix.", mention_author=False)
            pass
        else:
            #col.replace_one({"_id":ctx.guild.id}, {"$set":{"prefix":f"{apref}"}})
            results = await self.bot.dba['server'].find_one({"_id":ctx.guild.id}) or {}
            results['prefix'] = apref
            await self.bot.dba['server'].replace_one({"_id":ctx.guild.id}, results, True)
            await ctx.reply(f'Prefix changed to: {apref}', mention_author=False)
            name=f'[{apref}] Infinity'
            member=ctx.guild.get_member(732917262297595925)
            await member.edit(nick=name)
        

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
    async def massban(self, ctx, reason:str, *, ids:str):
        """Massban users."""
        await ctx.trigger_typing()
        ids.replace(",",'')
        people = re.findall("^(\d{18})$", ids)
        reason = f"Massbanned by {ctx.author.name} for {reason}"
        banned = []
        error = []
        for id in people:
            user = self.bot.get_user(id)
            try:
                await ctx.guild.ban(user, reason=reason)
            except:
                error.append(str(user))
            else:
                banned.append(str(user))
        await ctx.send(f"Banned {len(banned)} users: {', '.join(banned)}")
        await ctx.send(f"Failed to ban {len(error)} users:{', '.join(error)}")


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