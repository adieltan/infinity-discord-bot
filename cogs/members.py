import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 

from discord.ext.commands.cooldowns import BucketType


class MembersCog(commands.Cog, name='Members'):
    """*Information about members.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo', aliases=['ui', 'user', 'whois', 'i'])
    @commands.cooldown(1,5)
    @commands.guild_only()
    async def userinfo(self, ctx, *, member: discord.Member=None):
        """Gets info about the user."""
        if member is None:
            member = ctx.author
        await ctx.trigger_typing()
        
        embed=discord.Embed(title="User Info", description=f"{member.mention} [Avatar]({member.avatar_url_as(static_format='png')})\n`Status  :` {member.raw_status}\n`Activity:` {member.activity}", color=discord.Color.random())
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
        
        embed = discord.Embed(title='Permissions for:', description=who.mention, color=discord.Color.random())
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
        
        text= "\n".join([f'{winner.mention} `{winner.id}`' for winner in winners])
        embed = discord.Embed(title='Member randomizer', description=f'{text}', color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_footer(text=f'Drawn {len(winners)} winners.')
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="mutual")
    async def mutual(self, ctx, user:discord.User):
        """Returns the servers that are shared with the user."""
        servers = '\n'.join([f"`{guild.id}` {guild.name}" for guild in user.mutual_guilds])
        embed=discord.Embed(title="Mutual servers", description=servers, color=discord.Color.random(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_footer(text=f"{len(user.mutual_guilds)} servers")
        await ctx.reply(embed=embed)

    @commands.command(name="selfharm", aliases=["suicide", 'die'])
    async def selfharm(self, ctx, victim:discord.Member=None):
        """Gives you awareness about selfharm and useful contacts."""
        if victim is None:
            victim = ctx.author
        embed=discord.Embed(title="Suicide & Selfharm Prevention", url="https://www.who.int/health-topics/suicide", description="You are not alone. Everyone is special in their own ways and thats why you shouldn't give up.", color=discord.Color.blurple())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Get some help today.", value=f"[Suicide prevention](https://www.who.int/health-topics/suicide)\n[Contact Numbers](https://www.opencounseling.com/suicide-hotlines)\n[Crisis Lines](https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines)")
        embed.set_thumbnail(url="https://www.nursingcenter.com/getattachment/NCBlog/September-2016-(1)/World-Suicide-Prevention-Day/2016_wspd_ribbon_250X250.png.aspx?width=200&height=200")
        embed.set_image(url="https://sm.mashable.com/mashable_me/photo/default/gettyimages-6130324100_675p.jpg")
        try:
            await victim.send(embed=embed)
        except:
            await ctx.reply(f"Error sending file to {victim.mention}")
        else:
            await ctx.add_reaction("\U00002705")

    @commands.group(aliases=['r'])
    @commands.guild_only()
    async def role(self, ctx):
        """Role utilities."""
        if ctx.invoked_subcommand is None:
            pass
    
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
            embed.timestamp=datetime.datetime.utcnow()
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
            embed.timestamp=datetime.datetime.utcnow()
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
            embed.timestamp=datetime.datetime.utcnow()
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
            embed.timestamp=datetime.datetime.utcnow()
            await ctx.reply(embed=embed, mention_author=False)

    @role.command(aliases=['i'])
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def info(self,ctx, *, role:discord.Role=None):
        """Shows infomation about a role."""
        if role is None:
            role = ctx.guild.default_role
        embed = discord.Embed(title="Role Info", description=f"{role.mention} `{role.id}`\nMembers: {len(role.members)}" , color=role.color)
        embed.add_field(name="Permissions", value='❤'+'`🎈`'.join(perm for perm, value in role.permissions if value))
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
    
    @role.command()
    @commands.cooldown(1,4)
    @commands.has_permissions(manage_roles=True)
    async def clear(self,ctx, *, role:discord.Role):
        """Clears members from that role."""
        if ctx.author.top_role < role:
            await ctx.reply("Failed due to role hierarchy.")
            return
        people = role.members
        for m in people:
            await m.remove_roles(role, reason="Role member clear command.")
        await ctx.reply(f"Removed {role.mention} from {len(people)} member(s).")

    @role.command(name="list", aliases=['all', 'l'])
    @commands.cooldown(1,7,BucketType.channel)
    @commands.has_permissions(manage_roles=True)
    async def list(self, ctx):
        """Lists all the roles of the guild in a paginated way."""
        await ctx.trigger_typing()
        roles = ctx.guild.roles
        roles.reverse()
        n = 10
        pageno = 0
        pages = [roles[i:i + n] for i in range(0, len(roles), n)]
        
        embed=discord.Embed(title=f"{ctx.guild.name}'s Roles", color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        lis = [f'{r.mention} `{r.id}`' for r in pages[pageno]]
        text = '\n'.join(lis)
        embed.description=text
        msg = await ctx.reply(embed=embed,
                components = [ #Use any button style you wish to :)
            [
                Button(
                    label = "Prev",
                    id = "back",
                    style = ButtonStyle.green
                ),
                Button(
                    label = f"Page {int( pages.index( pages[pageno])) + 1}/{len( pages)}",
                    id = "cur",
                    style = ButtonStyle.grey,
                ),
                Button(
                    label = "Next",
                    id = "front",
                    style = ButtonStyle.green
                )]])
        while True:
            #Try and except blocks to catch timeout and break
            try:
                interaction = await self.bot.wait_for("button_click",check = lambda i: i.component.id in ["back", "front", "cur"] and i.user == ctx.author,timeout = 20.0)
                #Getting the right list index
                if interaction.component.id == "back":
                    pageno -= 1
                elif interaction.component.id == "front":
                    pageno += 1
                elif interaction.component.id == "cur":
                    raise asyncio.TimeoutError
                #If its out of index, go back to start / end
                if pageno == len( pages):
                    pageno = 0
                elif pageno < 0:
                    pageno = len( pages) - 1

                #Edit to new page + the center counter changes
                await interaction.respond(type = InteractionType.UpdateMessage,embed=discord.Embed(title=f"{ctx.guild.name}'s Roles", description= '\n'.join([f'{r.mention} `{r.id}`' for r in pages[pageno]]),color=discord.Color.random(), timestamp=datetime.datetime.utcnow()),
                    components = [
                        [   Button(
                                label = "Prev",
                                id = "back",
                                style = ButtonStyle.green
                            ),
                            Button(
                                label = f"Page {int( pages.index( pages[pageno])) + 1}/{len( pages)}",
                                id = "cur",
                                style = ButtonStyle.grey,
                            ),
                            Button(
                                label = "Next",
                                id = "front",
                                style = ButtonStyle.green
                            )]])

            except asyncio.TimeoutError:
                #Disable and get outta here
                await msg.edit(
                    components = [Button(
                                label = f"Page {int( pages.index( pages[pageno])) + 1}/{len( pages)}",
                                id = "cur",
                                style = ButtonStyle.grey,
                                disabled = True)])
                break


def setup(bot):
    bot.add_cog(MembersCog(bot))