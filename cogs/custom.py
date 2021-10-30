from operator import matmul
import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.channel import DMChannel
from discord.ext import commands, tasks

from thefuzz import process
import collections

from ._utils import Database, Confirm, NitroButtons, server


iv_classes = {
    '1': 'Shop Items',
    '2': 'Phallic Objects',
    '3': 'Work Items',
    '4': 'Pepe Items',
    '5': 'Animals',
    '6': 'Loot Boxes',
    '7': 'Rare Items',
    '8': 'Antique Items',
    '9': 'Random Items'}

class IvDropdownView(discord.ui.View):
    def __init__(self, ctx, ivlist):
        super().__init__(timeout=20)
        self.ctx = ctx
        self.msg = None
        self.ivlist = ivlist

    async def interaction_check(self, interaction:discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            return True
        await interaction.response.send_message("Eh don't be busybody.", ephemeral=True)
        return False
    
    async def on_timeout(self):
        v = self
        for vd in self.children:
            vd.disabled = True
        await self.msg.edit(view=self)

    options = [discord.SelectOption(label=f'{i}', description=f'{iv_classes[i]}') for i in iv_classes]
    @discord.ui.select(placeholder="Choose the item's category", min_values=1, max_values=1, options=options)
    async def select(self, selectoption:discord.SelectOption, interaction:discord.Interaction):
        await interaction.response.defer()
        try:
            value = selectoption.values[0]
            items = '\n'.join([f"{i.title()}" for i in self.ivlist if self.ivlist[i]['t'] == value])
            embed = discord.Embed(title="Item List", description=items + ('\n\n📝 DM Admin if donating Bolt / Karen / Odd Eye.' if value == '7' else '') + ('\n\n📝 DM Admin if donating Blob.' if value == '8' else ''), color=discord.Color.random()).set_footer(text=f'{iv_classes[value]}')
            await self.msg.edit(embed=embed)
        except:
            pass

class IvEdit(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.view = None
        self.value = None
        self.interaction = None
        self.ctx = ctx
    
    async def on_timeout(self):
        self.value = False

    async def interaction_check(self, interaction:discord.Interaction):
        return interaction.user.id == self.ctx.author.id

    @discord.ui.button(emoji='🏷️', label='Name', style=discord.ButtonStyle.green)
    async def name(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.interaction = interaction
        await interaction.response.defer(ephemeral=True)
        for v in self.children:
            if v != button:
                v.disabled = True
        self.view = self
        self.value = 'name'
        self.stop()

    @discord.ui.button(emoji='💰', label='Value', style=discord.ButtonStyle.green)
    async def value(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.interaction = interaction
        await interaction.response.defer(ephemeral=True)
        for v in self.children:
            if v != button:
                v.disabled = True
        self.view = self
        self.value = 'value'
        self.stop()

    @discord.ui.button(emoji='✅', label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.interaction = interaction
        await interaction.response.defer(ephemeral=True)
        for v in self.children:
            if v != button:
                v.disabled = True
        self.view = self
        self.value = True
        self.stop()

    @discord.ui.button(emoji='❌', label='Cancel', style=discord.ButtonStyle.gray)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.interaction = interaction
        await interaction.response.defer(ephemeral=True)
        for v in self.children:
            if v != button:
                v.disabled = True
        self.view = self
        self.value = False
        self.stop()
class CustomCog(commands.Cog, name='Custom'):
    """🔧 Custom commands for server."""
    def __init__(self, bot):
        self.bot = bot
        self.youtubeupdate.start()

    @commands.command(name="nitro")
    @server([709711335436451901, 336642139381301249, 895176280813752330, 894628265963159622, 841654825456107530, 746020135743127593])
    async def nitro(self, ctx):
        """Generates nitro codes."""
        letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        text = ''.join([random.choice(letters) for _ in range(16)])
        embed=discord.Embed(title="You've been gifted a subscription.", description="Infinity#5345 has gifted you Nitro for 1 year.", color=0x2F3136)
        embed.set_image(url="https://cdn.discordapp.com/app-assets/521842831262875670/store/633877574094684160.png?size=1024")
        embed.set_footer(text='\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800Expires in 46 hours.')
        v = NitroButtons(ctx)
        v.msg = await ctx.send(f"https://discord.gift\{text}",embed=embed, view=v)

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
        embed.timestamp=discord.utils.utcnow()
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
        embed.timestamp=discord.utils.utcnow()
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
            if not member:
                message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                member = message.mentions[0]
            if panda in member.roles:
                await ctx.reply('User already verified.')
                return

            await member.add_roles(panda, reason="Verification")
            await ctx.reply(f"Verified {member.mention}")
        except:
            await ctx.reply('Verification uncessful.')

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
            if not activity and advertiser in member.roles:
                await member.remove_roles(advertiser, reason="Not advertising for us.")
                await channel.send(embed=discord.Embed(description=f"Removed {advertiser.mention} from {member.mention}", color=discord.Color.red()))
                return
            elif not activity[0].name:
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
                if not invited and advertiser in member.roles:
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
            text = ''.join(f'{role} : <@&{value}>\n' for role, value in roles.items())
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


    @commands.Cog.listener()
    @server([709711335436451901])
    async def on_member_join(self, member:discord.Member):
        if member.guild.id != 709711335436451901 or member.bot is True:
            return
        bamboo_chat = self.bot.get_channel(717962272093372556)
        bots = sum(m.bot for m in member.guild.members)
        embed=discord.Embed(description=f"**Welcome to {member.guild.name}, {member.name} {member.mention}.**\nHave fun and enjoy your stay here.", color=discord.Color.random(), timestamp=member.created_at).set_footer(text=f"{member.guild.member_count - bots} Pandas").set_thumbnail(url=member.avatar or 'https://tenor.com/bjHxN.gif')
        results = await Database.get_server(self, member.guild.id)
        dic = results.get('leaveleaderboard', {})
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
    @commands.has_role(841655266743418892)
    async def donolog(self, ctx, user:discord.User, quantity:float, item:str, value_per:str, *, proof:str):
        """Logs the dono."""
        raw = float(value_per.replace(",", ""))
        channel = self.bot.get_channel(842738964385497108)
        valu = math.trunc(raw)*quantity
        human = format(int(valu), ',')
        embed=discord.Embed(title="Ultimate Dankers Event Donation", description=f"**Donator** : {user.mention}\n**Donation** : {quantity} {item}(s) worth {human} [Proof]({proof})", color=discord.Color.random())
        embed.timestamp=discord.utils.utcnow()
        embed.set_author(icon_url=ctx.author.avatar, name=f"Logged by: {ctx.author.name}")
        embed.add_field(name="Logging command", value=f"`,d a {user.id} {valu:.2e} {proof}`\nLog in <#814490036842004520>", inline=False)
        embed.add_field(name="Raw", value=f"||`{ctx.message.content}`||", inline=False)
        embed.set_thumbnail(url=user.avatar)
        embed.set_footer(text='React with a ✅ after logged.')
        await channel.send(f"{user.id}", embed=embed)
        await ctx.reply("Logged in <#842738964385497108>")


    def iv_view(self, name, price, emoji, item_type:typing.Literal[1,2,3,4,5,6,7,8,9]):
        emoji = (
            discord.Embed(
                title='Item Value',
                description=f"**{name.title()}**\nValue: ⏣ {'{:,}'.format(price)}\n",
                colour=discord.Colour.green()
                if price >= 200000
                else discord.Color.red(),
            )
            .set_footer(
                text=iv_classes[str(item_type)],
                icon_url=f"https://cdn.discordapp.com/emojis/{emoji}",
            )
            .set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{emoji}")
        )

        if price < 200000:
            emoji.description += f"```diff\n- Minimum donation is 200k.\n- 💸 You need another ⏣ {'{:,}'.format(round(2e5 - price))}\n```"
        return emoji

    @commands.group(name='iv', invoke_without_command=True)
    @server([894628265963159622])
    async def iv(self, ctx, *, items:str=None):
        """Item Value calculation tool. This command returns the list of items, lookup of single item or calculation of multiple items if invoked without subcommand."""
        server = await Database.get_server(self, 894628265963159622)
        ivlist = server.get('iv') or {}
        if len(ivlist) == 0:
            return await ctx.reply("No items.")
        if not items:
            classes = '\n'.join(f"{i}. {iv_classes[i]}" for i in iv_classes)
            embed = discord.Embed(title="Item Value", description=classes, color=discord.Color.random())   
            v = IvDropdownView(ctx, ivlist)
            v.msg = await ctx.reply(embed=embed, view=v)
        else:
            #search mode
            itemlist = items.split('+')
            if len(itemlist) < 2:
                #one item
                number = re.findall('\d+', itemlist[0])
                itemname = re.sub(r'[0-9]', '', itemlist[0])
                if itemname == '':
                    await ctx.reply(f"**{items}** is invalid.")
                    return
                try: quantity = number[0]
                except: quantity = 1
                fuz = process.extractOne(itemname, ivlist.keys())
                if fuz[1] < 75:
                    await ctx.reply(f"**{itemname}** Not Found")
                else:
                    await ctx.reply(embed=self.iv_view(f"{quantity} {fuz[0]}", ivlist[fuz[0]]['v'] * int(quantity), ivlist[fuz[0]]['e'], ivlist[fuz[0]]['t']))
            else:
                invalids = []
                value_list = []
                for item in itemlist:
                    number = re.findall('\d+', item)
                    itemname = re.sub(r'[0-9]', '', item).replace(' ', '')
                    if itemname == '':
                        value_list.append(int(number[0]))
                    else:
                        try: quantity = number[0]
                        except: quantity = 1
                        fuz = process.extractOne(itemname, ivlist.keys())
                        if fuz[1] < 75:
                            invalids.append(itemname)
                        else:
                            value = ivlist[fuz[0]]['v'] * int(quantity)
                            value_list.append(value)
                e=discord.Embed(title='Item Value Calculator', description=f'```fix\n{items}\n```', color=discord.Color.green() if sum(value_list) > 200000 else discord.Color.red())
                if invalids:
                    e.add_field(name='Invalid Items', value=', '.join(invalids), inline=False)
                e.add_field(
                    name="Calculation",
                    value='```fix\n'
                    + ' + '.join(str(value) for value in value_list)
                    + f"\n= ⏣ {sum(value_list)}\n```\n⏣ {'{:,}'.format(sum(value_list))}\n"
                    + (
                        f"```diff\n- Minimum donation is 200k.\n- 💸 You need another ⏣ {'{:,}'.format(round(2e5 - sum(value_list)))}\n```"
                        if sum(value_list) < 200000
                        else ''
                    ),
                    inline=False,
                )
                await ctx.reply(embed=e)

    @iv.command(name='add')
    @server([894628265963159622])
    @commands.is_owner()
    async def iv_add(self, ctx, item_type:typing.Literal[1,2,3,4,5,6,7,8,9], value:float, emoji:typing.Union[discord.PartialEmoji, str], *, item_name:str):
        value = round(value)
        server = await Database.get_server(self, 894628265963159622)
        ivlist = server.get('iv') or {}
        item_name = re.sub(r'[0-9]', '', item_name)
        if item_name.lower() in ivlist.keys():
            return await ctx.reply(f"{item_name.title()} already exists.", embed=self.iv_view(item_name, round(value), ivlist[item_name]['e'], ivlist[item_name]['t']))
        emoji = emoji.url.replace('https://cdn.discordapp.com/emojis/', '') if type(emoji) is discord.PartialEmoji else emoji.replace('https://cdn.discordapp.com/emojis/', '')
        ivlist[item_name.lower()] = {'v':value, 'e':emoji, 't':str(item_type)}
        await Database.edit_server(self, 894628265963159622, {'iv':ivlist})
        await ctx.reply(f"**{item_name.title()}** added with value ⏣ {'{:,}'.format(value)}.", embed=self.iv_view(item_name.lower(), value, emoji,   item_type))

    @iv.command(name='remove', aliases=['delete', 'del'])
    @server([894628265963159622])
    @commands.is_owner()
    async def iv_remove(self, ctx, *, item_name):
        server = await Database.get_server(self, 894628265963159622)
        ivlist = server.get('iv') or {}
        if len(ivlist) == 0:
            return await ctx.reply('No items.')
        fuz = process.extractOne(item_name.lower(), ivlist.keys())
        if fuz[1] < 75:
            await ctx.reply(f"{item_name.title()} Not Found")
        else:
            e=self.iv_view(f"{fuz[0]}", ivlist[fuz[0]]['v'], ivlist[fuz[0]]['e'], ivlist[fuz[0]]['t'])
            v = Confirm(ctx)
            v.msg = await ctx.reply('Are you sure to delete this item?', embed=e, view=v)
            msgv = discord.ui.View.from_message(v.msg)
            for vd in msgv.children:
                vd.disabled = True
            await v.wait()
            if v.value is False:
                await v.msg.edit('Cancelled', view=msgv)
            elif v.value is True:
                ivlist.pop(fuz[0])
                await Database.edit_server(self, 894628265963159622, {'iv':ivlist})
                await v.msg.edit("Confirmed.", view=msgv)
                await v.msg.reply(f"**{fuz[0].title()}** removed.")

    @iv.command(name='edit')
    @server([894628265963159622])
    @commands.is_owner()
    async def iv_edit(self, ctx, item_name:str):
        """Edits name/value for an item."""
        server = await Database.get_server(self, 894628265963159622)
        ivlist = server.get('iv') or {}
        if len(ivlist) == 0:
            return await ctx.reply(f"No items.")
        fuz = process.extractOne(item_name.lower(), ivlist.keys())
        if fuz[1] < 75:
            await ctx.reply(f"{item_name} Not Found")
        else:
            v = IvEdit(ctx)
            msg = await ctx.reply(f"Click the button to edit.", embed=self.iv_view(f"{fuz[0]}", ivlist[fuz[0]]['v'], ivlist[fuz[0]]['e'], ivlist[fuz[0]]['t']), view=v)
            dv = discord.ui.View.from_message(msg)
            for db in dv.children:
                db.disabled = True
            name = fuz[0]
            value = ivlist[fuz[0]]['v']
            while v.value not in (True, False):
                await v.wait()
                def author(m):
                    return m.author == ctx.author and m.channel.id == ctx.channel.id
                if v.value == 'name':
                    m = await v.interaction.followup.send(f'Send the new name for **{fuz[0]}** in 20 seconds.')
                    await msg.edit(view=v.view)
                    try:
                        message = await self.bot.wait_for('message', check=author, timeout=20)
                        name = message.content.lower()
                        v = IvEdit(ctx)
                        await msg.edit("Click Confirm to update.", embed=self.iv_view(name, value, ivlist[fuz[0]]['e'], ivlist[fuz[0]]['t']), view=v)
                    except asyncio.TimeoutError:
                        await v.interaction.followup.edit_message(m.id, 'Timeout.')
                        await msg.edit('Timeout.', view=dv)
                        v.value = False
                    except:
                        v = IvEdit(ctx)
                        await msg.edit("Name Invalid.", view=v)
                elif v.value == 'value':
                    m = await v.interaction.followup.send(f'Send the new value for **{fuz[0]}** in 20 seconds.')
                    await msg.edit(view=v.view)
                    try:
                        message = await self.bot.wait_for('message', check=author, timeout=20)
                        value = round(float(message.content.lower()))
                        v = IvEdit(ctx)
                        await msg.edit("Click Confirm to update.", embed=self.iv_view(name, value, ivlist[fuz[0]]['e'], ivlist[fuz[0]]['t']), view=v)
                    except asyncio.TimeoutError:
                        await v.interaction.followup.edit_message(m.id, 'Timeout.')
                        await msg.edit('Timeout.', view=dv)
                    except:
                        v = IvEdit(ctx)
                        await msg.edit("Number Invalid.", view=v)
                elif v.value is True:
                    await v.interaction.followup.send('Confirmed')
                    ivlist[name] = ivlist.pop(fuz[0])
                    ivlist[name]['v'] = value
                    await Database.edit_server(self, 894628265963159622, {'iv':ivlist})
                    await msg.edit(view=dv, embed=self.iv_view(name, value, ivlist[name]['e'], ivlist[name]['t']))
                else:
                    try:
                        await v.interaction.followup.send(content='Cancelled')
                        await msg.edit('Cancelled', view=dv)
                    except: 
                        pass
                    return

def setup(bot):
    bot.add_cog(CustomCog(bot))