from operator import matmul
import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.channel import DMChannel
from discord.ext import commands, tasks

from thefuzz import process
import collections

from ._utils import Database, Confirm, NitroButtons, server



class CustomCog(commands.Cog, name='Custom'):
    """Custom commands for server."""
    def __init__(self, bot):
        self.bot = bot
        self.COG_EMOJI = '🔧'
        self.youtubeupdate.start()


    @commands.command(name="nitro", hidden=True)
    async def nitro(self, ctx):
        """Generates nitro codes."""
        letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        text = ''.join([random.choice(letters) for _ in range(16)])
        embed=discord.Embed(title="You've been gifted a subscription.", description="Infinity#5345 has gifted you Nitro for 1 year.", color=0x2F3136)
        embed.set_image(url="https://cdn.discordapp.com/app-assets/521842831262875670/store/633877574094684160.png?size=1024")
        embed.set_footer(text='\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800Expires in 46 hours.')
        v = NitroButtons(ctx)
        v.msg = await ctx.send(f"https://discord.gift\{text}",embed=embed, view=v)

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


def setup(bot):
    bot.add_cog(CustomCog(bot))