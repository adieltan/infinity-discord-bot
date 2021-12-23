import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

from unicodedata import normalize
from ._utils import Menu, Database, ImprovedRoleConverter
class ModerationCog(commands.Cog, name='Moderation'):
    """Commands to keep your server safe."""
    def __init__(self, bot):
        self.bot = bot
        self.COG_EMOJI = '🔨'

    @commands.command(name='decancer')
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def decancer(self, ctx, member: discord.Member=None):
        """Changes the member's nickname to something pingable."""
        if not member:
            member = ctx.author
        ori = member.nick
        await member.edit(nick=normalize('NFKD', member.nick).encode("ascii","ignore").decode())
        await ctx.reply(f"{member.mention}'s name edited from {ori} to {member.nick}.")

    @commands.command(name='ban')
    @commands.cooldown(1,5)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.User, *, reason=None):
        """Bans a user."""
        if member is None or member == ctx.message.author:
            await ctx.reply("You cannot ban yourself.", mention_author=False)
            return
        mem = ctx.guild.get_member(member.id)
        if type(mem) is discord.Member:
            member = mem
            if (ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner.id) or member.id == ctx.guild.owner.id:
                await ctx.reply("Failed due to role hierarchy.")
                return
            else:
                try:
                    await ctx.guild.ban(member, delete_message_days=0, reason=f"Banned by {ctx.author.name} ({ctx.author.id}) for {reason}")
                    await ctx.reply(f'**{member}** was ***BANNED***\nReason: __{reason}__', mention_author=False)
                    message = f"You have been banned from {ctx.guild.name} by {ctx.author.mention} for {reason}"
                    try:
                        await member.send(message)
                    except:
                        await ctx.message.add_reaction("<:exclamation:876077084986966016>")
                except:
                    await ctx.reply("Missing permissions.")
        elif type(member) is discord.User:
                await ctx.guild.ban(member, delete_message_days=0, reason=f"Banned by {ctx.author.name} ({ctx.author.id}) for {reason}")
                await ctx.reply(f'**{member}** was ***BANNED***\nReason: __{reason}__', mention_author=False)
        
    @commands.command(name='unban')
    @commands.cooldown(1,5)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User, *, reason=None):
        """Unbans a user."""
        await ctx.guild.unban(member, reason=f"Unbanned by {ctx.author.name} for {reason}")
        await ctx.reply(f'**{member}** was ***UNBANNED***\nReason: __{reason}__', mention_author=False)

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
        if member is None or member == ctx.message.author:
            await ctx.reply("You cannot kick yourself", mention_author=False)
            return
        elif (ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner.id) or member.id == ctx.guild.owner.id:
            await ctx.reply("Failed due to role hierarchy.")
            return
        message = f"You have been kicked from {ctx.guild.name} for {reason}"
        try:
            await member.send(message)
        except:
            await ctx.message.add_reaction("<:exclamation:876077084986966016>")
        await ctx.guild.kick(member, reason=reason)
        await ctx.reply(f'**{member}** was ***KICKED***\nReason: __{reason}__', mention_author=False)

    @commands.command(name='setnick', aliases=['nick'])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def setnick(self, ctx, member:discord.Member, *, nickname:str):
        """Sets the nickname for someone."""
        if ctx.author.top_role < member.top_role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        await member.edit(nick=nickname, reason=f"Edited by {ctx.author.name}")
        await ctx.reply(embed=discord.Embed(title='Nickname Changed', description=f"{member.mention}'s nickname set to {nickname}", color=member.color))

    @commands.command(name='mynick')
    @commands.guild_only()
    @commands.has_permissions(change_nickname=True)
    async def mynick(self, ctx, *, nickname:str):
        """Sets your own nickname."""
        await ctx.author.edit(nick=nickname, reason="Edited by themselves.")
        await ctx.reply("Nickname changed.")

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
            perms = '```\nServer - 🛑 \nCurrent Channel - 💬 \n 🛑 | 💬 \n'
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
    
    @role.command(name='clearpermissions', aliases=['cp', 'clearperms', 'clearperm'])
    @commands.has_permissions(manage_roles=True)
    async def role_clearpermissions(self, ctx, roles:commands.Greedy[ImprovedRoleConverter]):
        """Clears role permissions for role(s)."""
        for role in roles:
            await role.edit(permissions=discord.Permissions.none())
        await ctx.reply(embed=discord.Embed(title="Role Clear Permissions", description='\n'.join(role.mention for role in roles)))

    @role.command(name='colour', aliases=['color', 'c'])
    @commands.has_permissions(manage_roles=True)
    async def role_colour(self, ctx, role:discord.Role, colour_hex:str=None):
        "Changes/views the role colour."
        if not colour_hex:
            embed=discord.Embed(description=f"{role.mention}\nRGB: {role.colour.to_rgb()}\nInt: {role.colour.value}\nHex: {str(hex(role.colour.value))[2:]}", color=role.color)
            return await ctx.reply(embed=embed, mention_author=False)
        elif 'random' in colour_hex.lower():
            await role.edit(colour=random.randint(0, 16777215))
            return await ctx.reply('Role colour randomized.')
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
        v.msg = await ctx.reply(embed=pagess[0], view=v)

    @role.command(name='random', aliases=['randommember'])
    @commands.cooldown(1,2)
    @commands.guild_only()
    async def random(self, ctx, role:discord.Role=None, howmany:int=1):
        """Finds random peoples from the whole server or from roles."""
        if role is None:
            role = ctx.guild.default_role
        people = role.members
        winners = []
        howmany = min(howmany, len(people))
        while len(winners) < howmany:
            win = random.choice(people)
            winners.append(win)
            people.remove(win)

        text = "\n".join(f'{winner.mention} `{winner.id}`' for winner in winners)
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
            else:
                status = "⚫ Offline"
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

def setup(bot):
    bot.add_cog(ModerationCog(bot))