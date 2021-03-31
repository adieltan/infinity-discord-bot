import discord, random, string, os, logging, asyncio, discord.voice_client, sys, traceback, datetime
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
        embed=discord.Embed(title="User Info", description=member.mention, color=hex_int)
        embed.set_author(name=member.display_name, icon_url=f'{member.avatar_url}')
        embed.add_field(name="User ID", value=member.id)
        embed.add_field(name="Nickname", value=member.display_name)
        embed.add_field(name="Top Role", value=f"{member.top_role.mention}\n{member.top_role.id}")
        embed.add_field(name="Date Joined", value=member.joined_at.strftime("%a %Y %b %d , %H:%M:%S %Z"))
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text="Date created")
        embed.timestamp = member.created_at
        await ctx.reply(embed=embed, mention_author=False)
    
    @commands.command(name='perms', aliases=['permissions'])
    @commands.cooldown(1,5)
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        """Checks member's permissions."""
        await ctx.trigger_typing()
        if not member:
            member = ctx.author
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)
        hex_int = random.randint(0,16777215)
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.add_field(name='\uFEFF', value=perms)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.reply(embed=embed, mention_author=False)
        
    @commands.command(name='roleperms', aliases=['rolepermissions', 'rp'])
    @commands.cooldown(1,5)
    @commands.guild_only()
    async def role_check_permissions(self, ctx, *, role: discord.Role=None):
        """Checks role's permissions."""
        await ctx.trigger_typing()
        if not role:
            role = ctx.guild.default_role
        perms = '\n'.join(perm for perm, value in role.permissions if value)
        hex_int = random.randint(0,16777215)
        embed = discord.Embed(title='Permissions for:', description=role.mention, color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.add_field(name='\uFEFF', value=f'\uFEFF'+perms)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(MembersCog(bot))