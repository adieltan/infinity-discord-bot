import discord, random, string, os, logging, asyncio, discord.voice_client, sys, traceback, datetime
from discord.ext import commands


class MembersCog(commands.Cog, name='Members'):
    """*Information about members.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo', aliases=['ui', 'user'])
    @commands.cooldown(1,5)
    @commands.guild_only()
    async def userinfo(self, ctx, *, member: discord.Member=None):
        """Gets info about the user."""
        if member is None:
            member = ctx.author
        await ctx.trigger_typing()
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="User Info", url=member.avatar_url, description=member.mention, color=hex_int)
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)
        embed.add_field(name="Nickname", value=member.display_name)
        embed.add_field(name="Top Role", value=member.top_role)
        embed.set_footer(text="Date created")
        embed.timestamp = member.created_at

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='joined', aliases=['datejoined', 'date_joined'])
    @commands.cooldown(1,5)
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member=None):
        """Says when a member joined the server."""
        if member is None:
            member = ctx.author
        await ctx.reply(f'**{member.display_name}** joined the server on **{member.joined_at}**', mention_author=False)

    @commands.command(name='toprole', aliases=['top_role'])
    @commands.cooldown(1,5)
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        """Shows the members Top Role."""
        if member is None:
            member = ctx.author
        await ctx.send(f'The top role for **{member.display_name}** is **{member.top_role.name}**', mention_author=False)
    
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

    @commands.command(name='avatar', aliases=['av'])
    @commands.cooldown(1,5)
    async def ava(self, ctx, *, member: discord.Member=None):
        """Shows the avatar for a user."""
        if not member:
            member = ctx.author
        hex_int = random.randint(0,16777215)
        embed = discord.Embed(title=f"{member}'s", description='Avatar', color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.reply(embed=embed, mention_author=False)
        

def setup(bot):
    bot.add_cog(MembersCog(bot))