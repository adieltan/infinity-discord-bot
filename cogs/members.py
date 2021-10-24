import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

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

class MembersCog(commands.Cog, name='Members'):
    """👤 Information / function about Users."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo', aliases=['ui', 'user', 'whois', 'i'])
    async def userinfo(self, ctx, *, member: typing.Union[discord.Member, discord.User]=None):
        """Gets info about the user."""
        if member is None:
            member = ctx.author
        if type(member) == discord.Member:
            if member.status == discord.Status.online:
                status = f"\🟢 Online"
            elif member.status == discord.Status.idle:
                status = f"\🟡 Idle"
            elif member.status == discord.Status.dnd:
                status = f"\🔴 DND"
            elif member.status == discord.Status.offline:
                status = f"\⚫ Offline"
            else:
                status = ''
            embed=discord.Embed(title="User Info", description=f"{member.mention} {str(member)} [Avatar]({member.display_avatar})\n{status}\n", color=member.color, timestamp = discord.utils.utcnow())
            if member.activity:
                embed.description += f"{member.activity.name}"
            embed.set_author(name=f"{member.name}", icon_url=f'{member.display_avatar}')
            embed.add_field(name="Joined", value=f"{discord.utils.format_dt(member.joined_at, style='F')}\n{discord.utils.format_dt(member.joined_at, style='R')}")
            embed.add_field(name="Registered", value=f"{discord.utils.format_dt(member.created_at, style='F')}\n{discord.utils.format_dt(member.created_at, style='R')}")
            if member.nick:
                embed.description = f"`{member.nick}` " + embed.description
            results = await self.bot.dba['server'].find_one({'_id':member.guild.id}) or {}
            dic = results.get('leaveleaderboard') or {}
            leavetimes = dic.get(f"{member.id}")
            if leavetimes is not None:
                embed.description += f"\nLeft the server {leavetimes} times."
            if member.bot:
                embed.description += f"\n🤖 Bot Account"
            if member.premium_since:
                embed.add_field(name="Server Boost", value=f"\nBoosting since: {discord.utils.format_dt(member.premium_since, style='f')}\n{discord.utils.format_dt(member.premium_since, style='R')}")
            embed.add_field(name="Roles", value=f"Top Role: {member.top_role.mention} `{member.top_role.id}`\nNumber of roles: {len(member.roles)}", inline=False)
            embed.set_thumbnail(url=member.display_avatar)
            embed.set_footer(text=f"ID: {member.id}")
        else:
            embed=discord.Embed(title="User Info", description=f"{member.mention} {str(member)} [Avatar]({member.avatar})", color=member.color, timestamp = discord.utils.utcnow())
            embed.set_author(name=f"{member.name}", icon_url=f'{member.avatar}')
            embed.add_field(name="Registered", value=f"{discord.utils.format_dt(member.created_at, style='F')}\n{discord.utils.format_dt(member.created_at, style='R')}")
            if member.bot:
                embed.description += f"\n🤖 Bot Account"
            results = await self.bot.dba['server'].find_one({'_id':ctx.guild.id}) or {}
            dic = results.get('leaveleaderboard')
            leavetimes = dic.get(f"{member.id}")
            if leavetimes is not None:
                embed.description += f"\nLeft the server {leavetimes} times."
            embed.set_thumbnail(url=member.avatar)
            embed.set_footer(text=f"ID: {member.id}")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='perms', aliases=['permissions', 'perm'])
    @commands.cooldown(1,5)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def check_permissions(self, ctx, object:typing.Union[discord.Member, discord.Role]=None):
        """Checks member's or role's permissions."""
        if object is None:
            object = ctx.author
        if type(object) == discord.Role:
            perms = "```"
            for perm, value in object.permissions:
                if value is True:
                    emoji = '✅'
                else:
                    emoji = '❌'
                perms += f" {emoji} - {perm.replace('_',' ').title()}\n"
            perms += '```'
        elif type(object) == discord.Member:
            perms = f"```\nServer - 🛑 \nCurrent Channel - 💬 \n"
            perms += f" 🛑 | 💬 \n"
            channel_perms = dict(iter(ctx.channel.permissions_for(object)))
            for perm, value in object.guild_permissions:
                if value is False and channel_perms[perm] is False:
                    pass
                else:
                    if value is True:
                        emoji = '✅'
                    else:
                        emoji = '❌'
                    if channel_perms[perm] is True:
                        cemoji = '✅'
                    else:
                        cemoji = '❌'
                    perms += f" {emoji} | {cemoji} - {perm.replace('_',' ').title()}\n"
            for perm, value in ctx.channel.permissions_for(object):
                if value is True and perm not in dict(iter(object.guild_permissions)):
                    perms += f" ❌ | ✅ - {perm.replace('_',' ').title()}\n"
            perms += '```'
        
        embed = discord.Embed(title='Permissions for:', description=object.mention+'\n'+perms, color=discord.Color.random())
        if object is discord.Member:
            embed.set_author(icon_url=object.avatar, name=str(object))
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="selfharm", aliases=["suicide", 'die'])
    async def selfharm(self, ctx, victim:discord.Member=None):
        """Gives you awareness about selfharm and useful contacts."""
        if victim is None:
            victim = ctx.author
        embed=discord.Embed(title="Suicide & Selfharm Prevention", url="https://www.who.int/health-topics/suicide", description="You are not alone. Everyone is special in their own ways and thats why you shouldn't give up.", color=discord.Color.blurple())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        embed.add_field(name="Get some help today.", value=f"[Suicide prevention](https://www.who.int/health-topics/suicide)\n[Contact Numbers](https://www.opencounseling.com/suicide-hotlines)\n[Crisis Lines](https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines)")
        embed.set_thumbnail(url="https://www.nursingcenter.com/getattachment/NCBlog/September-2016-(1)/World-Suicide-Prevention-Day/2016_wspd_ribbon_250X250.png.aspx?width=200&height=200")
        embed.set_image(url="https://sm.mashable.com/mashable_me/photo/default/gettyimages-6130324100_675p.jpg")
        try:
            await victim.send(embed=embed)
        except:
            await ctx.reply(f"Error sending message to {victim.mention}")
        else:
            await ctx.message.add_reaction("<a:verified:876075132114829342>")

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
        if colour_hex is None:
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
        if role is None:
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
    bot.add_cog(MembersCog(bot))