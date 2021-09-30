from operator import matmul
import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.channel import DMChannel
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle
import matplotlib.pyplot as plt


from numpy import append
from thefuzz import process
import collections

def server(id:list):
    def predicate(ctx):
        return ctx.guild.id in id
    return commands.check(predicate)
class CustomCog(commands.Cog, name='Custom'):
    """🔧 Custom commands for server."""
    def __init__(self, bot):
        self.bot = bot
        self.youtubeupdate.start()
        self.ongoing_mm_games = dict()

    @commands.command(name="nitro")
    @server([709711335436451901])
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
                    await interaction.respond(ephemeral=True, content="Claim your gift after completing this survey. ||(rickroll)||", components=[[Button(label="\u2800\u2800\u2800\u2800\u2800Claim\u2800\u2800\u2800\u2800\u2800", style=ButtonStyle.URL, url="https://youtu.be/dQw4w9WgXcQ")]])
                except:pass

    @commands.command(name="heist")
    @commands.has_any_role(783134076772941876)
    @server([709711335436451901])
    @commands.cooldown(1,5, type=commands.BucketType.guild)
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

    @commands.command(name="postheist", aliases=['ph'], hidden=True)
    @server([709711335436451901])
    @commands.cooldown(1,5, type=commands.BucketType.user)
    async def pheist(self, ctx, amount: float, invite:str,*, msg:str=None):
        """Sends your partnered heist ad."""
        partnered = self.bot.get_guild(709711335436451901).get_role(880822281394356244).members
        if ctx.author not in partnered:
            await ctx.reply(embed=discord.Embed(title="You are not partnered.", description="DM <@701009836938231849> to partner.", color=discord.Color.red()))
            return
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
    @server([709711335436451901])
    async def verify(self, ctx, member:discord.Member=None):
        """Gives someone the verified role."""
        panda= ctx.guild.get_role(717957198675968024)
        if member is None:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            member = message.mentions[0]
             
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
    @server([709711335436451901])
    async def on_member_update(self, before, after):
        """Checks online member's status."""
        await self.supporter_autorole(after)

    @commands.Cog.listener()
    @server([709711335436451901])
    async def on_message(self, message: discord.Message):
        if message.channel.id != 848892659828916274:
            return
        elif len(message.content) < 1:
            return
        elif message.author.bot is True:
            return
        roles = {
            'He/Him': 854353177804931083,
            'She/Her': 854353177377898509,
            'They/Them': 854353177184698418,
            'Any Pronouns': 854353176169283644,
            'Pronouns: Ask Me': 854353176697503785,
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
                    await message.reply(embed=discord.Embed(title="Roles add", description=f"Added {role.mention} to {message.author.mention}", color=discord.Color.green()).set_footer(text=f"{fuzzy[1]}%"))
                except:
                    await message.reply("Failed")
            else:
                try:
                    await message.author.remove_roles(role, reason="Self roles.")
                except:
                    await message.reply(f"The code `{message.content}` is invalid.")
                else:
                    await message.reply(embed=discord.Embed(title="Roles add", description=f"Removed {role.mention} from {message.author.mention}", color=discord.Color.red()).set_footer(text=f"{fuzzy[1]}%"))

    @commands.Cog.listener()
    @server([709711335436451901])
    async def on_member_join(self, member:discord.Member):
        if member.guild.id != 709711335436451901 or member.bot is True:
            return
        else:
            bamboo_chat = self.bot.get_channel(717962272093372556)
            bots = sum(m.bot for m in member.guild.members)
            embed=discord.Embed(description=f"**Welcome to {member.guild.name}, {member.name} {member.mention}.**\nHave fun and enjoy your stay here.", color=discord.Color.random(), timestamp=member.created_at).set_footer(text=f"{member.guild.member_count - bots} Pandas").set_thumbnail(url=member.avatar_url)
            results = await self.bot.dba['server'].find_one({'_id':member.guild.id}) or {}
            dic = results.get('leaveleaderboard')
            leavetimes = dic.get(f"{member.id}")
            if leavetimes is not None:
                embed.description += f"\nLeft the server {leavetimes} times."
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
        

    @commands.command(name="donolog", aliases=["dl"], hidden=True)
    @server([841654825456107530])
    async def logging(self, ctx, user:discord.User, quantity:float, item:str, value_per:str, *, proof:str):
        """Logs the dono."""
        guild = self.bot.get_guild(841654825456107530)
        admin = guild.get_role(841655266743418892).members
        if ctx.author not in admin:
            return
        raw = float(value_per.replace(",", ""))
        channel = self.bot.get_channel(842738964385497108)
        valu = math.trunc(raw)*quantity
        human = format(int(valu), ',')
        
        embed=discord.Embed(title="Ultimate Dankers Event Donation", description=f"**Donator** : {user.mention}\n**Donation** : {quantity} {item}(s) worth {human} [Proof]({proof})", color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=ctx.author.avatar_url, name=f"Logged by: {ctx.author.name}")
        embed.add_field(name="Logging command", value=f"`,d a {user.id} {valu:.2e} {proof}`\nLog in <#814490036842004520>", inline=False)
        embed.add_field(name="Raw", value=f"||`{ctx.message.content}`||", inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f"React with a ✅ after logged.")
        await channel.send(f"{user.id}", embed=embed)
        await ctx.reply("Logged in <#842738964385497108>")

    @commands.Cog.listener()
    @server([888337006042689536, 888337125433569290])
    async def on_message(self, message:discord.Message):
        """Treasure Mystery"""
        try:
            if "732917262297595925" in message.content and message.guild.id == 888337006042689536:
                channel = self.bot.get_channel(888337930379223060)
                invite = await channel.create_invite(max_age=300, max_uses=1)
                await message.author.send(f"You advanced to the next level! {str(invite)}")
            elif "help" in message.content.lower() and message.guild.id == 888337125433569290:
                channel = self.bot.get_channel(888344586680934430)
                invite = await channel.create_invite(max_age=300, max_uses=1)
                await message.author.send(f"You advanced to the next level! {str(invite)}")
        except:
            pass

    @commands.command(name='messagemania', aliases=['mm'])
    @commands.has_any_role(841655266743418892)
    @server([841654825456107530])
    async def messagemania(self, ctx, seconds:int=None):
        """Message Mania Minigame."""
        timer = '<a:timer:890234490100793404>'
        if ctx.channel.id in self.ongoing_mm_games.keys():
            await ctx.reply(f"There is an ongoing game in this channel.")
            return
        if seconds is None:
            seconds = 390
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages=True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        message = await ctx.send(embed=discord.Embed(description=f"<a:verified:876075132114829342> {ctx.channel.mention} Unlocked\nChannel will be locked soon.\n\n__Commands:__\n`mmp`: Purges 10 messages from the channel.\n`mmu`: Purges messages from a random user.\n`mmm`: Mutes a user from talking for 30 seconds.", colour=discord.Color.green()))
        self.ongoing_mm_games[ctx.channel.id] = message.created_at
        timestamp = round(message.created_at.replace(tzinfo=datetime.timezone.utc).timestamp())
        await message.edit(embed=discord.Embed(description=f"<a:verified:876075132114829342> {ctx.channel.mention} Unlocked\nChannel will be locked at <t:{timestamp+seconds}:T> <t:{timestamp+seconds}:R>.\n\n__Commands:__\n`mmp`: Purges 10 messages from the channel.\n`mmu`: Purges messages from a random user.\n`mmm`: Mutes a user from talking for 30 seconds.", colour=discord.Color.green()))
        await asyncio.sleep(seconds)
        overwrite.send_messages=False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=discord.Embed(description=f"<a:verified:876075132114829342> {ctx.channel.mention} Locked", colour=discord.Color.red()))
        messages = await ctx.channel.history(limit=None, after=message.created_at).flatten()
        messages = [x.author.id for x in messages if x.author.bot is False]
        counter=collections.Counter(messages)
        winners = '\n'.join(f"<medal here>  <@{x[0]}>: {x[1]} messages" for x in counter.most_common(5))
        winners = winners.replace('<medal here>', '🥇', 1).replace('<medal here>', '🥈', 1).replace('<medal here>', '🥉', 1).replace('<medal here>', '🏅', 1).replace('<medal here>', '🏅', 1)
        embed = discord.Embed(title="Message Mania", description=f"**__Winners__**\n{winners}", color=discord.Color.gold()).set_thumbnail(url="https://images-ext-1.discordapp.net/external/LMTQPkVKqF0jESGgD5djPe1ROAUCybuofm-ismCdBUs/https/media.discordapp.net/attachments/841654825456107533/890903767845834762/MM.png")
        try:
            await ctx.reply(embed=embed)
        except:
            await ctx.send(embed=embed)
        del self.ongoing_mm_games[ctx.channel.id]

    @commands.command(name='mmp', hidden=True)
    @commands.cooldown(1,60, commands.BucketType.user)
    @server([841654825456107530])
    async def messagemaniammp(self, ctx):
        if ctx.channel.id not in self.ongoing_mm_games.keys():
            return
        def pinc(msg):
            if msg.pinned or msg.id == ctx.message.id or msg.author.bot is True:
                return False
            else:
                return True
        try:    
            await ctx.channel.purge(limit=10, check=pinc, after=self.ongoing_mm_games[ctx.channel.id])
            await ctx.message.add_reaction('<a:verified:876075132114829342>')
        except:
            pass

    @commands.command(name='mmu', hidden=True)
    @commands.cooldown(1,180, commands.BucketType.channel)
    @server([841654825456107530])
    async def messagemaniammu(self, ctx):
        if ctx.channel.id not in self.ongoing_mm_games.keys():
            return

        messages = await ctx.channel.history(after=self.ongoing_mm_games[ctx.channel.id]).flatten()
        user = random.choice([set([x.author.id for x in messages if x.author.bot is not True])])

        def pinc(msg):
            if msg.pinned or msg.id == ctx.message.id or msg.author.id != next(iter(user)):
                return False
            else:
                return True
        try:
            await ctx.channel.purge(limit=100, check=pinc, after=self.ongoing_mm_games[ctx.channel.id])
            await ctx.message.add_reaction('<a:verified:876075132114829342>')
        except:
            pass

    @commands.command(name='mmm', hidden=True)
    @commands.cooldown(1,120, commands.BucketType.channel)
    @server([841654825456107530])
    async def messagemaniammm(self, ctx):
        if ctx.channel.id not in self.ongoing_mm_games.keys():
            return
        try:
            messages = await ctx.channel.history(after=self.ongoing_mm_games[ctx.channel.id]).flatten()
            user = random.choice([set([x.author for x in messages if x.author.bot is not True])])
            await ctx.channel.set_permissions(next(iter(user)), send_messages=False)
            await ctx.send(f"{next(iter(user)).mention} muted for 30s.")
            await asyncio.sleep(30)
            await ctx.channel.set_permissions(user.pop(), overwrite=None)
            await ctx.message.add_reaction('<a:verified:876075132114829342>')
        except:
            pass

def setup(bot):
    bot.add_cog(CustomCog(bot))