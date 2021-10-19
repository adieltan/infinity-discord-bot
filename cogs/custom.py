from operator import matmul
import discord, random, string, os, asyncio, sys, math, requests, json, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.channel import DMChannel
from discord.ext import commands, tasks

from thefuzz import process
import collections

def server(id:list):
    def predicate(ctx):
        return ctx.guild.id in id
    return commands.check(predicate)

class NitroButtons(discord.ui.View):
    def __init__(self, msg, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.msg = msg

    async def on_timeout(self):
        self.clear_items()
        self.add_item(discord.ui.Button(label='\u2800\u2800\u2800\u2800\u2800Accept\u2800\u2800\u2800\u2800\u2800', style=discord.ButtonStyle.gray, disabled=True))
        self.msg.embeds[0].description= "Looks like someone already redeemed this gift."
        await self.msg.edit(embed=self.msg.embeds[0], view=self)

    @discord.ui.button(label="\u2800\u2800\u2800\u2800\u2800Accept\u2800\u2800\u2800\u2800\u2800", style=discord.ButtonStyle.green)
    async def accept(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.send_message('https://imgur.com/NQinKJB', ephemeral=True)

class CustomCog(commands.Cog, name='Custom'):
    """🔧 Custom commands for server."""
    def __init__(self, bot):
        self.bot = bot
        self.youtubeupdate.start()
        self.ongoing_bm_game = dict()

    @commands.command(name="nitro")
    @server([709711335436451901, 336642139381301249, 895176280813752330])
    async def nitro(self, ctx):
        """Generates nitro codes."""
        letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        text = ''.join([random.choice(letters) for _ in range(16)])
        embed=discord.Embed(title="You've been gifted a subscription.", description="Infinity#5345 has gifted you Nitro for 1 year.", color=0x2F3136)
        embed.set_image(url="https://cdn.discordapp.com/app-assets/521842831262875670/store/633877574094684160.png?size=1024")
        mes = await ctx.send(f"https://discord.gift\{text}",embed=embed)
        await mes.edit(view=NitroButtons(mes, ctx))

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
        embed.set_thumbnail(url=f"{donator.avatar}")
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
        try:
            if member is None:
                message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                member = message.mentions[0]
            if panda in member.roles:
                await ctx.reply(f"User already verified.")
                return

            await member.add_roles(panda, reason="Verification")
            await ctx.reply(f"Verified {member.mention}")
        except:
            await ctx.reply(f"Verification uncessful.")

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

    async def self_role(self, message:discord.Message):
        """Adds a specific pickable role to the member (Typical Pandas)."""
        if message.channel.id != 848892659828916274:
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
            'Wishlist Ping': 890775726524104714,
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
        if message.content=='list':
            text = ''
            for role in roles:
                text += f"{role} : <@&{roles[role]}>\n"
            await message.reply(text, mention_author=False, allowed_mentions=discord.AllowedMentions.none(), delete_after=100)
            return
        try:
            fuzzy = process.extractOne(message.content, roles.keys())
            id = roles.get(fuzzy[0])
            role = message.guild.get_role(id)
            if fuzzy[1] < 70:
                raise
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
    async def on_message(self, message:discord.Message):
        if message.author.bot is True:
            return
        if message.channel.id == 848892659828916274:
            await self.self_role(message=message)
            return
        else:
            await self.treasure_mystery(message=message)
            return


    @commands.Cog.listener()
    @server([709711335436451901])
    async def on_member_join(self, member:discord.Member):
        if member.guild.id != 709711335436451901 or member.bot is True:
            return
        else:
            bamboo_chat = self.bot.get_channel(717962272093372556)
            bots = sum(m.bot for m in member.guild.members)
            embed=discord.Embed(description=f"**Welcome to {member.guild.name}, {member.name} {member.mention}.**\nHave fun and enjoy your stay here.", color=discord.Color.random(), timestamp=member.created_at).set_footer(text=f"{member.guild.member_count - bots} Pandas").set_thumbnail(url=member.avatar)
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
        embed.set_author(icon_url=ctx.author.avatar, name=f"Logged by: {ctx.author.name}")
        embed.add_field(name="Logging command", value=f"`,d a {user.id} {valu:.2e} {proof}`\nLog in <#814490036842004520>", inline=False)
        embed.add_field(name="Raw", value=f"||`{ctx.message.content}`||", inline=False)
        embed.set_thumbnail(url=user.avatar)
        embed.set_footer(text=f"React with a ✅ after logged.")
        await channel.send(f"{user.id}", embed=embed)
        await ctx.reply("Logged in <#842738964385497108>")

    async def treasure_mystery(self, message:discord.Message):
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

    @commands.command(name='bm')
    @server([888587803812839424])
    async def banmystery(self, ctx, target:typing.Union[discord.Member, str]=None):
        """Intialises a banmystery game."""
        role = ctx.guild.get_role(888588301852893254)
        surviver = 888589185475313685
        rooms = [888589270045040650, 888589293814173727, 888589315087675423, 888589338751946752, 888589353901768715, 888589372432207922, 888589388978733088, 888589409174290462, 888589443836022805, 888589480624291870]
        chars = list(string.ascii_uppercase)
        if bool(self.ongoing_bm_game) is False and dict(iter(ctx.channel.permissions_for(ctx.author)))['administrator'] is True:
            if len(role.members) < 2:
                await ctx.reply(f"Too less people.")
            self.ongoing_bm_game = {'banner':random.choice(role.members), 'code':[''.join([random.choice(chars) for _ in range(5)]) for _ in range(10)], 'cd':0}
            await ctx.author.send(f"{self.ongoing_bm_game['banner'].mention} is the banner.")
            await self.ongoing_bm_game['banner'].send(f"You are the banner. Run `=bm` in all the ban rooms to search for ban codes. 1 out of the 3 codes will work. \nRun `=bm <code>` to use them and I will ban a random person. All codes are 1 time used. \nOnce you have searched all the 10 channels, I will refresh the codes and there will be 10 new set of codes. \nYou need to try and ban everyone in the server and the survivors need to find out who you are and run `=bb {self.ongoing_bm_game['banner'].mention}` in <#{surviver}> to eject you. \nThey have a cd of 60 seconds and you can sabotage them by suspecting in <#{surviver}>. I will tell you how long their cd each time you search.")
            await ctx.reply(f"{role.mention}. Game started.\n\n__**Normal People:**__\nUse `=bm` in <#{surviver}>to see list of survivors. `=bm <mention_suspect>` to eject them. 60 seconds cd btw. \n\n__**Banner:**__\n`=bm` in ban rooms to search for code. 1 out of the 3 codes will work.\n`=bm <code>` in same channel to ban a random person.\nCodes refresh after all 10 channels have been searched.")
            return
        if bool(self.ongoing_bm_game) is False:
            return
        elif ctx.channel.id in rooms:
            await ctx.message.delete()
            if ctx.author is self.ongoing_bm_game['banner']:
                if any(self.ongoing_bm_game['code']) is False:
                    self.ongoing_bm_game['code'] = [''.join([random.choice(chars) for _ in range(5)]) for _ in range(10)]
                code = self.ongoing_bm_game['code'][rooms.index(ctx.channel.id)]
                if target is None:
                    #search
                    codes = [''.join(random.sample(code, len(code))), ''.join(random.sample(code, len(code))), code]
                    random.shuffle(codes)
                    await ctx.author.send(f"""{' '.join(codes)}\n{f"Suspect will be available in {self.ongoing_bm_game['cd'] + 60 - round(datetime.datetime.utcnow().timestamp())} seconds." if self.ongoing_bm_game['cd'] + 60 > round(datetime.datetime.utcnow().timestamp()) else 'Suspect is ready.'}""")
                elif target.upper() == code:
                    members = ctx.guild.get_role(888588301852893254).members
                    members.remove(ctx.author)
                    await random.choice(members).remove_roles(role)
                    await ctx.author.send(f"Got 1 player out.")
                    self.ongoing_bm_game['code'][rooms.index(ctx.channel.id)] = False
                    if len(ctx.guild.get_role(888588301852893254).members) == 1:
                        await ctx.reply(f"{role.mention}. Great job Banner{ctx.author.mention}.")
                        self.ongoing_bm_game = dict()
                else: await ctx.author.send('Wrong code.')
        elif ctx.channel.id == surviver:
            if round(datetime.datetime.utcnow().timestamp()) < self.ongoing_bm_game['cd'] + 60:
                await ctx.message.add_reaction('⏳')
            elif target is None:
                suspects = '\n'.join(m.mention for m in role.members)
                await ctx.reply(embed=discord.Embed(description=f"**__SUSPECTS**__\n{suspects}"))
            elif target == self.ongoing_bm_game['banner']:
                await self.ongoing_bm_game['banner'].remove_roles(role)
                await ctx.reply(f"{role.mention} Great job. {self.ongoing_bm_game['banner'].mention} was the Banner.")
                self.ongoing_bm_game = dict()
            else:
                await ctx.reply(f"Wrong Guess.")
                self.ongoing_bm_game['cd'] = round(datetime.datetime.utcnow().timestamp())

    def iv_view(self, name, price, emoji):
        emoji = discord.Embed(title="Item Value", description=f"Value: ⏣ {price.format(',')}", colour=discord.Colour.random()).set_footer(text=name.lower(), _url=f"https://cdn.discordapp.com/emojis/{emoji}").set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{emoji}")
        return emoji


    @commands.group(name='iv', invoke_without_command=True)
    @server([894628265963159622])
    async def iv(self, ctx, items):
        """Item Value calculation tool."""
        server = await self.bot.dba['server'].find_one({'_id':894628265963159622}) or {}
        ivlist = server.get('iv') or {}
        if len(ivlist) == 0:
            return await ctx.reply("No items.")
        item = items.lower()
        fuzzy = process.extractOne(item, ivlist.keys())
        if fuzzy[1] < 50:
            await ctx.reply(f"{item} Not Found")
        else:
            await ctx.reply(embed=self.iv_view(fuzzy[0], ivlist[fuzzy[0]]['v'], ivlist[fuzzy[0]]['e']))

    @iv.command(name='add')
    #@commands.has_guild_permissions(administrator=True)
    @commands.is_owner()
    async def iv_add(self, ctx, item_name, value, emoji:typing.Union[discord.PartialEmoji, str]):
        server = await self.bot.dba['server'].find_one({'_id':894628265963159622}) or {}
        ivlist = server.get('iv') or {}
        if item_name in ivlist.keys():
            return await ctx.reply(f"{item_name} already exists.", embed=self.iv_view(item_name, value, ivlist[item_name]['e']))
        ivlist[item_name.lower()] = {'v':value, 'e':emoji.url.replace('https://cdn.discordapp.com/emojis/', '') if type(emoji) is discord.PartialEmoji else emoji.replace('https://cdn.discordapp.com/emojis/', '')}
        await self.bot.dba['server'].update_one({'_id':894628265963159622}, {'$set':{'iv':ivlist}})
        await ctx.reply(f"{item_name} added with value ⏣ {value.format(',')}.", embed=self.iv_view(item_name, value, emoji))

    @iv.command(name='remove')
    #@commands.has_guild_permissions(administrator=True)
    @commands.is_owner()
    async def iv_remove(self, ctx, item_name):
        server = await self.bot.dba['server'].find_one({'_id':894628265963159622}) or {}
        ivlist = server.get('iv') or {}
        if len(ivlist) == 0:
            return await ctx.reply(f"No items.")
        fuzzy = process.extractOne(item_name.lower(), ivlist.keys())
        if fuzzy[1] < 50:
            await ctx.reply(f"{item_name} Not Found")
        else:
            ivlist.pop(fuzzy[0])
            await self.bot.dba['server'].update_one({'_id':894628265963159622}, {'$set':{'iv':ivlist}})
            await ctx.reply(f"{fuzzy[0]} removed.")

    @iv.command(name='edit')
    #@commands.has_guild_permissions(administrator=True)
    @commands.is_owner()
    async def iv_edit(self, ctx, item_name, new:typing.Union[str, int]):
        """Edits name/value for an item."""
        server = await self.bot.dba['server'].find_one({'_id':894628265963159622}) or {}
        ivlist = server.get('iv') or {}
        if len(ivlist) == 0:
            return await ctx.reply(f"No items.")
        fuzzy = process.extractOne(item_name.lower(), ivlist.keys())
        if fuzzy[1] < 50:
            await ctx.reply(f"{item_name} Not Found")
        else:
            if type(new) is str:
                ivlist[new] = fuzzy[0]
                ivlist.pop(fuzzy[0])
                await self.bot.dba['server'].update_one({'_id':894628265963159622}, {'$set':{'iv':ivlist}})
                await ctx.reply(f"{item_name} renamed to {new}.")
            elif type(new) is int:
                ivlist[fuzzy[0]]['v'] = new
                await self.bot.dba['server'].update_one({'_id':894628265963159622}, {'$set':{'iv':ivlist}})
                await ctx.reply(f"{item_name}'s value is now {new.format(',')}.")

    @iv.command(name='list')
    async def iv_list(self, ctx):
        server = await self.bot.dba['server'].find_one({'_id':894628265963159622}) or {}
        ivlist = server.get('iv') or {}
        text = 'Item - Value\n'
        for i in ivlist:
            text += f"{i} - ⏣ {ivlist[i]['v']}\n"
        buffer = io.BytesIO(text.encode('utf-8'))
        await ctx.reply(file=discord.File(buffer, filename='iv.txt'))



def setup(bot):
    bot.add_cog(CustomCog(bot))