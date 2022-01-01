from operator import matmul
import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord import interactions
from discord.channel import DMChannel
from discord.ext import commands, tasks

from thefuzz import process
import collections

from ._utils import Database, Confirm, NitroButtons, server

class DropdownRoles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.Select(custom_id='DarkNightLunaDropdownRoles', placeholder="Get/remove your roles here...", min_values=1, max_values=1, 
    options=[
        discord.SelectOption(label="News Ping", value="731723678164713554", description="Receives notifications for server related announcements or updates.", emoji='📢'),
        discord.SelectOption(label="Bump Ping", value="782937437206609941", description="Receives notifications for bumping our server through DISBOARD every 2 hours.", emoji='⬆'),
        discord.SelectOption(label="Chat Revival", value="848826846669439026", description="You will become the army that perform medical operations on dead chats.", emoji='💊'),
        discord.SelectOption(label="Infinity Updates", value="926836460835991604", description="Receives notifications for Infinity bot's updates.", emoji='♾'),
        discord.SelectOption(label="Karuta Access", value="926815232079314994", description="Shows the Karuta category for more fun..", emoji='♾'),
        discord.SelectOption(label="Ultra Supporter", value="926834703506485309", description="Get this role to support Beggar's youtube.", emoji='<:tp_Youtube:848819450223788042>')
    ])
    async def select(self, select:discord.ui.Select, interaction:discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        selected = [interaction.guild.get_role(int(s.value)) for s in select.values]
        for s in selected:
            if s in interaction.user.roles:
                await interaction.user.remove_roles(s)
                await interaction.followup.send(f"Removed {s.mention} from you.", ephemeral=True)
            else:
                await interaction.user.add_roles(s)
                await interaction.followup.send(f"Added {s.mention} to you.", ephemeral=True)

class CustomCog(commands.Cog, name='Custom'):
    """Custom commands for server."""
    def __init__(self, bot):
        self.bot = bot
        self.COG_EMOJI = '🔧'
        self.youtubeupdate.start()


    @commands.group(name="nitro", hidden=True, invoke_without_command=True)
    @commands.guild_only()
    async def nitro(self, ctx):
        """Mockup fake nitro."""
        db = await Database.get_server(self, ctx.guild.id)
        if not db.get('nitro'):
            try:
                return await ctx.reply(f"Nitro generated will not be usable. Use at your own risk.\nCommand not intended for public use.")
            except:
                return await ctx.send(f"Nitro generated will not be usable. Use at your own risk.\nCommand not intended for public use.")
        letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        text = ''.join([random.choice(letters) for _ in range(16)])
        embed=discord.Embed(title="You've been gifted a subscription.", description="Infinity#5345 has gifted you Nitro for 1 year.", color=0x2F3136)
        embed.set_image(url="https://cdn.discordapp.com/app-assets/521842831262875670/store/633877574094684160.png?size=1024")
        embed.set_footer(text='\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800Expires in 46 hours.')
        v = NitroButtons(ctx)
        v.msg = await ctx.send(f"https://discord.gift\{text}",embed=embed, view=v)

    @nitro.command(name="toggle")
    @commands.has_guild_permissions(administrator=True)
    async def toggle(self, ctx):
        """Turns on / off the nitro command in the server."""
        db = await Database.get_server(self, ctx.guild.id)
        if db.get('nitro'):
            await Database.edit_server(self, ctx.guild.id, {'nitro':False})
            return await ctx.reply(f"Disabled `nitro` command for guild {ctx.guild.id}")
        else:
            await Database.edit_server(self, ctx.guild.id, {'nitro':True})
            return await ctx.reply(f"Enabled `nitro` command for guild {ctx.guild.id}")

    @commands.command(name='dropdownroles')
    @server([709711335436451901])
    async def dropdownroles(self, ctx):
        """Posts the Dropdown."""
        await ctx.delete()
        await ctx.send(embed=discord.Embed().set_image(url='https://us-east-1.tixte.net/uploads/u.very-stinky.com/de0tyff-9efba6d3-d8c0-44c9-b25f-9445d45b34ab.png'), view=DropdownRoles())
    

    @commands.Cog.listener()
    @server([709711335436451901])
    async def on_member_join(self, member:discord.Member):
        if member.guild.id != 709711335436451901 or member.bot is True:
            return
        bamboo_chat = self.bot.get_channel(717962272093372556)
        bots = sum(m.bot for m in member.guild.members)
        embed=discord.Embed(description=f"**Welcome to {member.guild.name}, {member.name} {member.mention}.**\nHave fun and enjoy your stay here.", color=discord.Color.random(), timestamp=member.created_at).set_footer(text=f"{member.guild.member_count - bots} Pandas").set_thumbnail(url=member.display_avatar)
        results = await Database.get_server(self, member.guild.id)
        dic = results.get('leaveleaderboard', {})
        leavetimes = dic.get(f"{member.id}")
        if leavetimes is not None:
            embed.description += f"\nLeft the server {leavetimes} times."
        await bamboo_chat.send(f"<a:qb_hi:912918224411164682> <@&848824685222952980> <:tp_panda:839699254951804948> Welcome {member.mention}. <a:qb_clap:912917970337005618>", embed=embed, allowed_mentions=discord.AllowedMentions(roles=True))

    @tasks.loop(hours=24, reconnect=True)
    async def youtubeupdate(self):
        await self.bot.wait_until_ready()
        sub = self.bot.get_channel(861445998630273056)
        views = self.bot.get_channel(861446020026466334)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url=f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC52Xt2wq5H16HglMwNAvLeg&key={os.getenv('googleapi')}") as data:
                json = await data.json()
                items = json['items']
                stats= items[0]['statistics']
                await sub.edit(name=f"{format(int(stats['subscriberCount']), ',')} ⬅ Beggar's Subscribers")
                await views.edit(name=f"{format(int(stats['viewCount']), ',')} ⬅ Beggar's Views")

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

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type != discord.InteractionType.application_command:
            return
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(f"{interaction.data}\n{type(interaction.user)}", ephemeral=True)
        if interaction.data.get('id') == '923799170702250054' and interaction.data.get('options', [])[0]['value'] == 4 and (interaction.guild.get_role(906556235040587836) in interaction.user.roles):
            nxt: discord.TextChannel = self.bot.get_channel(906544174055186466)
            role: discord.Role = interaction.guild.get_role(906402631818305568)
            invite = await nxt.create_invite(max_uses=1)
            await interaction.followup.send(str(invite), ephemeral=True)
            await interaction.user.add_roles(role)
        elif interaction.data.get('id') == '923799446079303710' and interaction.data.get('options', [])[0]['value'].lower() == 'waltdisneyworld' and (interaction.guild.get_role(906747055832186890) in interaction.user.roles):
            nxt: discord.TextChannel = self.bot.get_channel(906544179319042057)
            role: discord.Role = interaction.guild.get_role(906544173350535320)
            invite = await nxt.create_invite(max_uses=1)
            await interaction.followup.send(str(invite), ephemeral=True)
            await interaction.user.add_roles(role)
        elif interaction.data.get('id') == '923799659099607060' and interaction.data.get('options', [])[0]['value'].lower() == 'monday' and (interaction.guild.get_role(917653201178726410) in interaction.user.roles):
            nxt: discord.TextChannel = self.bot.get_channel(906544180166262808)
            role: discord.Role = interaction.guild.get_role(917653221353353226)
            invite = await nxt.create_invite(max_uses=1)
            await interaction.followup.send(str(invite), ephemeral=True)
            await interaction.user.add_roles(role)
        else:
            await interaction.followup.send("Wrong", ephemeral=True)

def setup(bot):
    bot.add_cog(CustomCog(bot))