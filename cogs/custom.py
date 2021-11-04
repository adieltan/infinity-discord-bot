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
        for vd in self.children:
            vd.disabled = True
        await self.msg.edit(view=self)

    options = [discord.SelectOption(emoji='<a:redformingstar:894910459147329577>', label=f'{i}', description=f'{iv_classes[i]}') for i in iv_classes]
    @discord.ui.select(placeholder="Choose the item's category", min_values=1, max_values=1, options=options)
    async def select(self, selectoption:discord.SelectOption, interaction:discord.Interaction):
        await interaction.response.defer()
        try:
            value = selectoption.values[0]
            for so in self.select.options:
                so.default = so.value == selectoption.values[0]
            items = '\n'.join(
                f"{i.title()}" for i in self.ivlist if self.ivlist[i]['t'] == value
            )

            embed = discord.Embed(title="Item List", description=items + ('\n\n📝 DM Admin if donating Bolt / Karen / Odd Eye.' if value == '7' else '') + ('\n\n📝 DM Admin if donating Blob.' if value == '8' else ''), color=discord.Color.random()).set_footer(text=f'{iv_classes[value]}')
            await self.msg.edit(embed=embed, view=self)
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

class MmConfirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        self.value = None
        self.party_ids = None
        self.msg = None

    async def on_timeout(self) -> None:
        for v in self.children:
            v.disabled = True
        return await self.msg.edit('Timeout.', view=self)
    
    async def interaction_check(self, interaction:discord.Interaction):
        if interaction.user.id in self.party_ids:
            return True
        await interaction.response.send_message("Eh don't be busybody.", ephemeral=True)
        return False

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.party_ids.remove(interaction.user.id)
        if bool(self.party_ids) is None:
            self.value = True
            for v in self.children:
                v.disabled = True
            await self.msg.edit(view=self)
            self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = False
        for v in self.children:
                v.disabled = True
        await self.msg.edit(f"Cancelled my {interaction.user.mention}", view=self)
        self.stop()

class MmClaim(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value = None
        self.msg = None

    async def on_timeout(self) -> None:
        for v in self.children:
            v.disabled = True
        return await self.msg.edit('Timeout.', view=v)
    
    async def interaction_check(self, interaction:discord.Interaction):
        mm = interaction.guild.get_role(895755547343724554)
        if mm in interaction.user.roles:
            return True
        await interaction.response.send_message("Eh don't be busybody.", ephemeral=True)
        return False

    @discord.ui.button(label='Claim', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = True
        for v in self.children:
            v.disabled = True
        await self.msg.edit(f"Claimed by {interaction.user.mention}", view=v)
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

    @commands.command(name="donolog", aliases=["dl"])
    @server([841654825456107530])
    @commands.has_role(841655266743418892)
    async def donolog(self, ctx, user:discord.User, quantity:int, item:str, value_per:str, *, proof:str):
        """Logs the dono."""
        raw = float(value_per.replace(",", ""))
        channel = self.bot.get_channel(842738964385497108)
        valu = math.trunc(raw)*quantity
        human = format(int(valu), ',')
        embed=discord.Embed(title="Ultimate Dankers Event Donation", description=f"**Donator:** {user.mention}\n**Donation:** __{quantity} {item}(s)__ worth __{human}__  [Proof]({proof})\n\n**Log in <#814490036842004520>**\n```\n,d a {user.id} {valu:.2e} {proof}```", color=discord.Color.random())
        embed.timestamp=discord.utils.utcnow()
        embed.set_thumbnail(url=user.avatar)
        embed.set_footer(text=f'\nLogged by {ctx.author.name} • React with a ✅ after logged.', icon_url=ctx.author.avatar)
        await channel.send(f"{user.id}", embed=embed)
        await ctx.reply("Logged in <#842738964385497108>")

    @commands.command(name='bb')
    @server([841654825456107530, 830731085955989534])
    #ban battle
    @commands.has_role(841805626300301374)
    async def bb(self, ctx, victim:discord.Member):
        """Ban battle."""
        admin = ctx.guild.get_role(841655266743418892)
        banned = ctx.guild.get_role(905455999958278184)
        # spec = ctx.guild.get_role(842926861239582750)
        if ctx.channel.id not in [905453845524676608]:
            return
        else:
            await ctx.reply("Not allowed in this channel.")
        if banned in ctx.author.roles:
            await ctx.reply("You are banned.")
        # elif spec in ctx.author.roles:
        #     await ctx.reply("You have no weapon.")
        elif admin in victim.roles:
            await ctx.reply("Unbannable")
        # elif spec in victim.roles:
        #     await ctx.reply("He has no weapons just eyes. No harm to you.")
        elif banned in victim.roles:
            await ctx.reply("Already banned.")
        else:
            await victim.add_roles(banned)
            await ctx.reply(f"Banned {victim.mention}")

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

    @commands.group(name='mm', invoke_without_command=True)
    # @commands.cooldown(1, 30)
    @commands.max_concurrency(1, commands.BucketType.user)
    @server([894628265963159622])
    async def mm(self, ctx, user:discord.Member, *, info:str=None):
        """Calls mm?"""
        c = [894637152577658951, 894637521433141328, 894638146141167656, 894651965278150696, 894651980901920819, 895239173940858880]
        if ctx.channel.id not in c:
            return await ctx.reply(f"Only usable in {' '.join([f'<#{cc}>' for cc in c])}")
        e = discord.Embed(title='Middleman Request', description=info, timestamp=discord.utils.utcnow(), color=discord.Color.random()).set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        v = MmConfirm()
        v.party_ids = [ctx.author.id, user.id]
        v.msg = await ctx.reply(f"{user.mention}", embed=e, view=v)
        await v.wait()
        if v.value is True:
            channel = ctx.guild.get_channel(905440448556957696)
            e.description = f"{ctx.author.mention}, {user.mention}"
            e.add_field(name='Info', value=info)
            mv = MmClaim()
            mv.msg = await channel.send(f"<@&895755547343724554>", embed=e, view=mv)
            await mv.wait()
            if mv.value is True:
                access = ctx.guild.get_role(905438843250032682)
                await ctx.author.add_roles(access)
                await user.add_roles(access)

    @mm.command(name='done', aliases=['d'])
    @commands.has_any_role(895755547343724554)
    async def mmdone(self, ctx, users:commands.Greedy[discord.Member]):
        """Removes the mm access role."""
        access = ctx.guild.get_role(905438843250032682)
        for u in users:
            await u.remove_roles(access)
        await ctx.reply(f"Removed MM Access role for {len(users)} members.")


def setup(bot):
    bot.add_cog(CustomCog(bot))