import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime, re
from discord.ext import commands
from discord.ext.commands import BucketType
from numpy import append


class rhCog(commands.Cog, name='rh'):
    """*Custom commands for rh's server.*"""
    def __init__(self, bot):
        self.bot = bot
        self.rh = bot.get_guild(709711335436451901)
        self.ba = bot.get_guild(703135571710705815)

    def rhserver():
        def predicate(ctx):
            return ctx.guild.id==709711335436451901
        return commands.check(predicate)

    def typicals():
        def predicate(ctx):
            return ctx.guild.id==703135571710705815 or 709711335436451901
        return commands.check(predicate)

    @commands.command(name="banappealable", aliases=['ba'])
    @commands.has_permissions(ban_members=True)
    @typicals()
    @commands.cooldown(1,5)
    async def ba(self, ctx, member:discord.Member, *, reason:str=None):
        """Bans a member and send them a link to our appeal server."""
        if ctx.author.top_role < member.top_role and ctx.author != ctx.guild.owner:
            await ctx.reply("Failed due to role hierarchy.")
            return
        message = f"You have been banned from {ctx.guild.name} by {ctx.author.mention} for {reason}.\nAppeal at https://discord.gg/3TnPvzdtdU ."
        try:
            await member.send(message)
        except:
            await ctx.reply(f"{member.mention}'s dms are not open.")
        reason = f"Banned by {ctx.author.name} for {reason}. Appealable."
        await ctx.guild.ban(member, reason=reason)
        await ctx.reply(f'**{member}** was ***BANNED***\nReason: __{reason}__', mention_author=False)


    @commands.command(name="heist")
    @commands.has_any_role(783134076772941876)
    @rhserver()
    @commands.cooldown(1,5, type=BucketType.guild)
    async def heist(self, ctx, msg:str=None):
        """Gets people ready for a heist."""
        heistping = ctx.guild.get_role(807925829009932330)
        heistchannel = ctx.guild.get_channel(783135856017145886)
        
        embed = discord.Embed(title='Dank Memer Heist', color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.add_field(name='Info', value=f"{msg} ", inline=False)
        embed.set_footer(text='Remember to thank them !')
        await heistchannel.send(content=f"{heistping.mention} ", embed=embed, allowed_mentions=discord.AllowedMentions.all(),  mention_author=False)

    @commands.command(name="partneredheist")
    @commands.has_any_role(847626436622024704)
    @rhserver()
    @commands.cooldown(1,5, type=BucketType.guild)
    async def pheist(self, ctx, amount: float, *, msg:str=None):
        """Sends your partnered heist ad."""
        heistping = ctx.guild.get_role(807925829009932330)
        pheistchannel = ctx.guild.get_channel(848429520263839784)
        
        into = format(amount, ',')
        embed = discord.Embed(title='Heist', description=f'Amount: {into}', color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.add_field(name='Info', value=f"{msg} ", inline=False)
        embed.set_footer(text='Remember to thank them !')
        await pheistchannel.send(content=f"{heistping.mention} ", embed=embed, allowed_mentions=discord.AllowedMentions.all(),  mention_author=False)

    @commands.command(name="verify")
    @commands.has_permissions(manage_roles=True)
    @rhserver()
    async def verify(self, ctx, member:discord.Member):
        """Gives someone the verified role."""
        panda= ctx.guild.get_role(717957198675968024)
        await member.add_roles(panda, reason="Verification")
        await ctx.reply(f"Verified {member.mention}")

    @commands.command(name="statuscheck", aliases=["sc"])
    @commands.has_permissions(manage_roles=True)
    @rhserver()
    @commands.cooldown(1,40, type=BucketType.guild)
    async def statuscheck(self, ctx):
        """Checks online member's status."""
        members = ctx.guild.members
        advertiser = ctx.guild.get_role(848463384185536552)
        onlines = []
        removed = []
        added = []
        for m in members:
            if m.status is not (discord.Status.offline or discord.Status.invisible):
                onlines.append(m)
                print(onlines)
                content = str(m.activity)
                print(content)
                invite = re.findall("?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?", content)
                if len(invite) < 0:
                    pass
                else:
                    for inv in invite:
                        invinfo = await self.bot.fetch_invite(inv)
                        if invinfo.name == ctx.guild.name:
                            m.add_roles(advertiser, reason="Advertising is present in status.")
                            added.append(m)
                            pass
                        else:
                            continue
                
                pass
            else:
                if advertiser in m.roles:
                    m.remove_roles(advertiser, reason="Advertising not present in status.")
                    removed.append(m)                    
                else:
                    pass
                pass

        
        embed=discord.Embed(title="Status Check", description=f"Checking for guys that advertised our server in their status.", color=discord.Color.random())
        embed.set_author(name=f"{ctx.author.name}", icon_url=f'{ctx.author.avatar_url}')
        embed.add_field(name="Added", value=f"`{len(added)}`\n{[m.mention for m in added]}")
        embed.add_field(name="Removed", value=f"`{len(removed)}`\n{[m.mention for m in removed]}")
        embed.timestamp = datetime.datetime.now()
        await ctx.reply(embed=embed, mention_author=False)
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id != 848892659828916274:
            return
        elif message.author.bot == True:
            return
        roles = {
            'mal' :854353177804931083,
            'fem' :854353177377898509,
            "ari" :736915483651080202,
            'tau' :807926824952266782,
            "gem" :807925920404471808,
            'can' :736915593235529808,
            'leo' :736915617755561995,
            'vir' :736915640039768064,
            'lib' :736915677079928915,
            'sco' :736915700014120960,
            'sag' :736915732121649252,
            'cap' :736915778036695139,
            'aqu' :807973226533224478,
            'pis' :807926062855618600,
            'new' :731723678164713554,
            'giv' :807926618223018015,
            'gam' :759685837088227328,
            'eve' :759685837088227328,
            'inf' :848814884330537020,
            'bum' :782937437206609941,
            'cha' :848826846669439026,
            'pol' :848807930085900320,
            'you' :848814523552366652,
            'sel' :848814467412131850,
            'wel' :848824685222952980,
            'par' :848784334747598908,
            'nop' :848784758661185596,
            'dsh' :783133558172286977,
            'dgi' :783133954047213609,
            'dfl' :848807540476870666,
            'dlo' :794183280508796939,
            'dhe' :807925829009932330,
            'dev' :807926892723437588,
            'dpa' :848808489278898217,
            'cod' :791132663011606540
        }
        try:
            raw = message.content.lower()
            key = raw.replace(' ','')[0:3]
            id = roles[key]
            role = message.guild.get_role(id)
        except:
            await message.reply(f"The code `{message.content}` is invalid.\nBe sure to check out <#723892038587646002> to see what roles you can get.")
        else:
            if role not in message.author.roles:
                try:
                    await message.author.add_roles(role, reason="Self role.")
                    await message.reply(f"Added {role.mention} to {message.author.mention}")
                except:
                    await message.reply("Failed")
            else:
                try:
                    await message.author.remove_roles(role, reason="Self roles.")
                except:
                    await message.replay(f"The code `{message.content}` is invalid.")
                else:
                    await message.reply(f"Removed {role.mention} from {message.author.mention}")

def setup(bot):
    bot.add_cog(rhCog(bot))