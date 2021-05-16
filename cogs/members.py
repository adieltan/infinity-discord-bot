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

def setup(bot):
    bot.add_cog(MembersCog(bot))