from click import pass_context
import discord, random, string, os, logging, asyncio, discord.voice_client, sys, traceback, datetime, re
from discord.member import Member
from discord.ext import commands


class MembersCog(commands.Cog, name='Members'):
    """*Information about members.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo', aliases=['ui', 'user', 'whois'])
    @commands.cooldown(1,5)
    @commands.guild_only()
    async def userinfo(self, ctx, *, member: discord.Member=None):
        """Gets info about the user."""
        if member is None:
            member = ctx.author
        await ctx.trigger_typing()
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="User Info", description=f"{member.mention} [Avatar]({member.avatar_url_as(static_format='png')})\n`Status  :` {member.raw_status}\n`Activity:` {member.activity}", color=hex_int)
        embed.set_author(name=f"{member.name}", icon_url=f'{member.avatar_url}')
        embed.add_field(name="User ID", value=f"`{member.id}`")
        embed.add_field(name="Nickname", value=member.display_name)
        embed.add_field(name="Date Joined", value=member.joined_at.strftime("%a %Y %b %d , %H:%M:%S %Z"))
        embed.add_field(name="Roles", value=f"`Top Role:` {member.top_role.mention}\n`{member.top_role.id}`\n`Number of roles:` {len(member.roles)}", inline=False)
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text="User creation date")
        embed.timestamp = member.created_at
        await ctx.reply(embed=embed, mention_author=False)
    
    @commands.command(name='perms', aliases=['permissions', 'perm'])
    @commands.cooldown(1,5)
    @commands.guild_only()
    async def check_permissions(self, ctx, *, who=None):
        """Checks member's or role's permissions."""
        await ctx.trigger_typing()
        if who == None:
            who = f"{ctx.author.id}"
        id = int(re.sub("[^\\d.]", "", who))
        who = ctx.guild.get_member(id)
        if who:
            perms = '\n'.join(perm for perm, value in who.guild_permissions if value)
        if who == None:
            who = ctx.guild.get_role(id)
            perms = '\n'.join(perm for perm, value in who.permissions if value)
        hex_int = random.randint(0,16777215)
        embed = discord.Embed(title='Permissions for:', description=who.mention, color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        if who is discord.Member:
            embed.set_author(icon_url=who.avatar_url, name=str(who))
        embed.add_field(name='\uFEFF', value=f'\uFEFF'+perms)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='random', aliases=['randommember'])
    @commands.cooldown(1,2)
    @commands.guild_only()
    async def random(self, ctx, howmany:int=1, role:discord.Role=None):
        """Finds random peoples from the server or from roles."""
        await ctx.trigger_typing()
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
        hex_int = random.randint(0,16777215)
        text= "\n".join([f'{winner.mention} `{winner.id}`' for winner in winners])
        embed = discord.Embed(title='Member randomizer', description=f'{text}', color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_footer(text=f'Drawn {len(winners)} winners.')
        await ctx.reply(embed=embed, mention_author=False)

    @commands.group(pass_context=True, aliases=['r'])
    async def role(self, ctx):
        """Role utilities."""
        if ctx.invoked_subcommand is None:
            pass
    
    @role.command(pass_context=True)
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def delete(self,ctx, role:discord.Role, *, reason:str=None):
        """Deletes the role."""
        try:
            await role.delete(reason=f"Deleted by {ctx.author.name} for {reason}.")
        except:
            await ctx.reply("Failed")
        else:
            await ctx.reply(f"{role.name} deleted.")

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
            await ctx.reply(f"{role.mention} created.")

    @role.command(pass_context=True)
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def add(self,ctx, member:discord.Member, *,  role:discord.Role):
        """Adds a role to a person."""
        try:
            await member.add_roles(role)
        except:
            await ctx.reply("Failed")
        else:
            await ctx.reply(f"Added {role.mention} to {member.mention}")

    @role.command(pass_context=True)
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def remove(self,ctx, member:discord.Member, *, role:discord.Role):
        """Removes a role from a person."""
        try:
            await member.remove_roles(role)
        except:
            await ctx.reply("Failed")
        else:
            await ctx.reply(f"Removed {role.mention} from {member.mention}")

    @role.command(pass_context=True, aliases=['i'])
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def info(self,ctx, *, role:discord.Role=None):
        """Shows infomation about a role."""
        if role is None:
            role = ctx.guild.default_role
        embed = discord.Embed(title="Role Info", description=f"{role.mention} `{role.id}`\nMembers: {len(role.members)}" , color=role.color)
        embed.add_field(name="Permissions", value='`🎈`'.join(perm for perm, value in role.permissions if value))
        embed.set_footer(text="Role created at")
        embed.timestamp = role.created_at
        await ctx.reply(embed=embed, mention_author=True)

    @role.command(pass_context=True, aliases=['d'])
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def dump(self,ctx, *, role:discord.Role):
        """Dumps members from the role."""
        people = role.members
        text ="```css\n" + '\n'.join((f'{m.name} ({m.id})')for m in people) + "```"
        await ctx.reply(text)
    
    @role.command(pass_context=True)
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def clear(self,ctx, *, role:discord.Role):
        """Clears members from that role."""
        people = role.members
        for m in people:
            await m.remove_roles(role, reason="Role member clear command.")
        await ctx.reply(f"Removed {role.mention} from {len(people)} member(s).")

def setup(bot):
    bot.add_cog(MembersCog(bot))