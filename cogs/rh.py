import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 

from discord.ext.commands import BucketType
from numpy import append
from fuzzywuzzy import process


class rhCog(commands.Cog, name='rh'):
    """*Custom commands for rh's server.*"""
    def __init__(self, bot):
        self.bot = bot
        self.rh = bot.get_guild(709711335436451901)
        self.ba = bot.get_guild(703135571710705815)
        self.youtubeupdate.start()
        self.supporter.start()

    def rhserver():
        def predicate(ctx):
            return ctx.guild.id in [709711335436451901,703135571710705815]
        return commands.check(predicate)

    @commands.command(name="nitro")
    @rhserver()
    async def nitro(self, ctx):
        """Generates nitro codes."""
        letters = string.ascii_lowercase + string.ascii_lowercase + string.digits
        text = ''.join([random.choice(letters) for _ in range(16)])
        embed=discord.Embed(title="You've been gifted a subscription.", description="Infinity#5345 has gifted you Nitro for 1 year.", color=0x2F3136)
        embed.set_image(url="https://cdn.discordapp.com/app-assets/521842831262875670/store/633877574094684160.png?size=1024")
        mes = await ctx.send(f"<https://dizcord.gift/{text}>",embed=embed, components=[Button(label="\u2800\u2800\u2800\u2800\u2800Accept\u2800\u2800\u2800\u2800\u2800", id="Accept", style=ButtonStyle.green)])
        while True:
            try:
                interaction = await self.bot.wait_for("button_click",check = lambda i: i.component.id == "Accept",timeout = 20)
            except asyncio.TimeoutError:
                embed.description="Looks like someone already redeemed this gift."
                await mes.edit(embed=embed, components=[Button(label="\u2800\u2800\u2800\u2800\u2800Accept\u2800\u2800\u2800\u2800\u2800", id="Accept", style=ButtonStyle.gray, disabled=True)])
                break
            else:
                try:
                    await interaction.respond(type=InteractionType.ChannelMessageWithSource, ephemeral=True, content="Claim your gift after completing this survey. ||(rickroll)||", components=[[Button(label="\u2800\u2800\u2800\u2800\u2800Claim\u2800\u2800\u2800\u2800\u2800", style=ButtonStyle.URL, url="https://youtu.be/dQw4w9WgXcQ")]])
                except:pass

    @commands.command(name="heist")
    @commands.has_any_role(783134076772941876)
    @rhserver()
    @commands.cooldown(1,5, type=BucketType.guild)
    async def heist(self, ctx, amount:float, donator:discord.User, *, msg:str=None):
        """Gets people ready for a heist."""
        heistping = self.bot.get_guild(709711335436451901).get_role(807925829009932330)
        heistchannel = self.bot.get_guild(709711335436451901).guild.get_channel(783135856017145886)

        into = format(amount, ',')
        embed = discord.Embed(title='Dank Memer Heist', description=f"Amount: {into}", color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.add_field(name='Info', value=f"Donator: {donator.mention}\n{msg} ", inline=False)
        embed.set_thumbnail(url=f"{donator.avatar_url}")
        embed.set_footer(text=f'Remember to thank {donator.name} !')
        await heistchannel.send(content=f"{heistping.mention} ", embed=embed, allowed_mentions=discord.AllowedMentions.all(),  mention_author=False)

    @commands.command(name="postheist", aliases=['ph'])
    @commands.has_any_role(880822281394356244)
    @rhserver()
    @commands.cooldown(1,5, type=BucketType.user)
    async def pheist(self, ctx, amount: float, invite:str,*, msg:str=None):
        """Sends your partnered heist ad."""
        eventping = self.bot.get_guild(709711335436451901).get_role(807926892723437588)
        eventchannel = self.bot.get_guild(709711335436451901).get_channel(783135856017145886)
        inviteinfo = await self.bot.fetch_invite(invite)

        into = format(amount, ',')
        embed = discord.Embed(title='Heist', description=f'Amount: {into}', color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.add_field(name='Info', value=f"{msg} ", inline=False)
        embed.add_field(name='Server', value=f"[**{inviteinfo.guild.name}**]({inviteinfo.url})\nMembers: {inviteinfo.approximate_member_count}")
        await eventchannel.send(f"{eventping.mention} {invite}", embed=embed, allowed_mentions=discord.AllowedMentions(roles=[eventping]),  mention_author=False)

    @commands.command(name="verify")
    @commands.has_permissions(manage_roles=True)
    @rhserver()
    async def verify(self, ctx, member:discord.Member):
        """Gives someone the verified role."""
        panda= ctx.guild.get_role(717957198675968024)
        await member.add_roles(panda, reason="Verification")
        await ctx.reply(f"Verified {member.mention}")

    async def supporter_autorole(self, member:discord.Member):
        await self.bot.wait_until_ready()
        if member.guild.id != 709711335436451901 or member.bot is True:
            return
        advertiser = member.guild.get_role(848463384185536552)
        channel = member.guild.get_channel(751683666710626324)
        if member.raw_status == 'offline' and advertiser in member.roles:
            await member.remove_roles(advertiser, reason="Not advertising for us.")
            await channel.send(embed=discord.Embed(description=f"Removed {advertiser.mention} from {member.mention}", color=discord.Color.red()))
            return
        activity = [activity for activity in member.activities if type(activity) is discord.activity.CustomActivity]
        try:
            if len(activity) < 1 and advertiser in member.roles:
                await member.remove_roles(advertiser, reason="Not advertising for us.")
                await channel.send(embed=discord.Embed(description=f"Removed {advertiser.mention} from {member.mention}", color=discord.Color.red()))
                return
            elif activity[0].name is None:
                activity[0].name = ""
            else:
                invites = re.findall("(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?", str(activity[0].name))
                invited = False
                for link in invites:
                    try:
                        invite = await self.bot.fetch_invite(url=f"{link}")
                        if invite.guild.id == 709711335436451901:
                            invited = True
                            if advertiser not in member.roles:
                                await member.add_roles(advertiser, reason="Supporter")
                                await channel.send(embed=discord.Embed(description=f"Added {advertiser.mention} to {member.mention}", color=discord.Color.green()))
                            break
                    except:
                        continue
                if invited is False and advertiser in member.roles:
                    await member.remove_roles(advertiser, reason="Not advertising for us.")
                    await channel.send(embed=discord.Embed(description=f"Removed {advertiser.mention} from {member.mention}", color=discord.Color.red()))
        except:
            pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Checks online member's status."""
        await self.supporter_autorole(after)

    @tasks.loop(hours=1, reconnect=True)
    async def supporter(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(709711335436451901)
        for member in guild.members:
            await self.supporter_autorole(member)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id != 848892659828916274:
            return
        elif len(message.content) < 1:
            return
        elif message.author.bot == True:
            return
        roles = {
            'Any Pronouns': 854353176169283644,
            'Pronouns: Ask Me': 854353176697503785,
            'They/Them': 854353177184698418,
            'She/Her': 854353177377898509,
            'He/Him': 854353177804931083,
            'Aries': 736915483651080202,
            'Taurus': 807926824952266782,
            'Gemini': 807925920404471808,
            'Cancer': 736915593235529808,
            'Leo': 736915617755561995,
            'Virgo': 736915640039768064,
            'Libra': 736915677079928915,
            'Scorpio': 736915700014120960,
            'Sagittarius': 736915732121649252,
            'Capricorn': 736915778036695139,
            'Aquarius': 807973226533224478,
            'Pisces': 807926062855618600,
            'News': 731723678164713554,
            'Giveaway': 807926618223018015,
            'Game/Event Time': 759685837088227328,
            'Infinity Updates': 848814884330537020,
            'Bump Ping': 782937437206609941,
            'Chat Revival': 848826846669439026,
            'Poll Ping': 848807930085900320,
            'Youtube Upload Pings': 848814523552366652,
            'New Self Roles': 848814467412131850,
            'Welcomer': 848824685222952980,
            'Partnership Ping': 848784334747598908,
            'No Partnership Ping': 848784758661185596,
            'D Shop': 783133558172286977,
            'D Giveaway': 783133954047213609,
            'D Event': 807926892723437588,
        }
        try:
            fuzzy = process.extractOne(message.content, roles.keys())
            id = roles.get(fuzzy[0])
            role = message.guild.get_role(id)
        except:
            await message.reply(f"The code `{message.content}` is invalid.\nBe sure to check out <#723892038587646002> to see what roles you can get.")
        else:
            if role not in message.author.roles:
                try:
                    await message.author.add_roles(role, reason="Self role.")
                    await message.reply(embed=discord.Embed(title="Roles add", description=f"Added {role.mention} to {message.author.mention}", color=discord.Color.green()))
                except:
                    await message.reply("Failed")
            else:
                try:
                    await message.author.remove_roles(role, reason="Self roles.")
                except:
                    await message.reply(f"The code `{message.content}` is invalid.")
                else:
                    await message.reply(embed=discord.Embed(title="Roles add", description=f"Removed {role.mention} from {message.author.mention}", color=discord.Color.red()))

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        if member.guild.id != 709711335436451901 or member.bot is True:
            return
        else:
            bamboo_chat = self.bot.get_channel(717962272093372556)
            bots = sum(m.bot for m in member.guild.members)
            embed=discord.Embed(title=f"Welcome to {member.guild.name}, {member.name}.", description=f"Have fun and enjoy your stay here. \nMember Name: **{member.name}** {member.mention}\nMember Count: **{member.guild.member_count - bots} Pandas**", color=discord.Color.random(), timestamp=member.created_at)
            embed.set_thumbnail(url=member.avatar_url)
            await bamboo_chat.send(f"<a:Welcome:848827232944259092> <@&848824685222952980> <:tp_panda:839699254951804948> Welcome {member.mention}. <a:Welcome:848827232944259092>", embed=embed, allowed_mentions=discord.AllowedMentions(roles=True))

    @commands.Cog.listener()
    async def on_ready(self):
        vc = self.bot.get_channel(736791916397723780)
        try:await vc.connect()
        except:pass

        channel = self.bot.get_channel(813251835371454515)
        await channel.send("∞")

    @tasks.loop(hours=24, reconnect=True)
    async def youtubeupdate(self):
        await self.bot.wait_until_ready()
        rhsub = self.bot.get_channel(859359926526935061)
        rhviews = self.bot.get_channel(859361059302277120)
        tbsub = self.bot.get_channel(861445998630273056)
        tbviews = self.bot.get_channel(861446020026466334)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url=f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCW4gBQyPWrTeyKN6EPV6sGA&key={os.getenv('googleapi')}") as data:
                json = await data.json()
                items = json['items']
                stats= items[0]['statistics']
                await rhsub.edit(name=f"{format(int(stats['subscriberCount']), ',')} ⬅ rh's Subscribers")
                await rhviews.edit(name=f"{format(int(stats['viewCount']), ',')} ⬅ rh's Views")
            async with cs.get(url=f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC52Xt2wq5H16HglMwNAvLeg&key={os.getenv('googleapi')}") as data:
                json = await data.json()
                items = json['items']
                stats= items[0]['statistics']
                await tbsub.edit(name=f"{format(int(stats['subscriberCount']), ',')} ⬅ Beggar's Subscribers")
                await tbviews.edit(name=f"{format(int(stats['viewCount']), ',')} ⬅ Beggar's Views")
        await cs.close()

def setup(bot):
    bot.add_cog(rhCog(bot))
