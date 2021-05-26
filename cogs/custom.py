import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime
from discord.ext import commands


class customCog(commands.Cog, name='custom'):
    """*Custom commands for server.*"""
    def __init__(self, bot):
        self.bot = bot

    def rhserver():
        def predicate(ctx):
            return ctx.guild.id==709711335436451901
        return commands.check(predicate)

    @commands.command(name="heist")
    @commands.has_role(783134076772941876)
    @rhserver()
    @commands.cooldown(1,18)
    async def heist(self, ctx, amount: float, sponsor: discord.Member=None, *, msg:str=None):
        """Gets people ready for a heist."""
        if sponsor == None:
            sponsor = ctx.author
        heistping = ctx.guild.get_role(807925829009932330)
        hex_int = random.randint(0,16777215)
        embed = discord.Embed(title='Heist', description=f'{amount}', color=hex_int)
        embed.set_author(name=sponsor.display_name, icon_url=sponsor.avatar.url)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_image(url="https://media3.giphy.com/media/5QMOICVmXremPSa0k7/giphy.gif")
        embed.add_field(name='Additional info', value=f"{msg} ", inline=False)
        embed.set_footer(text='Remember to thank them !')
        await ctx.reply(content=f"{heistping.mention()}", embed=embed, allowed_mentions=True,  mention_author=False)

    def udevent():
        def predicate(ctx):
            return ctx.guild.id==841654825456107530 or ctx.guild.id==830731085955989534 
        return commands.check(predicate)

    @commands.command(name="donolog", aliases=["dl"])
    @udevent()
    @commands.cooldown(1,7)
    @commands.has_permissions(administrator=True)
    async def logging(self, ctx, user:discord.User, item:str, value:str, proof:str):
        """Logs the dono."""
        raw = float(value.replace(",", ""))
        channel = self.bot.get_channel(842738964385497108)
        valu = math.trunc(raw)
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="Ultimate Dankers Event Donation", color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
        embed.add_field(name="Donator", value=f'{user.mention}', inline=True)
        embed.add_field(name="Donation", value=f"[{item} worth {valu}]({proof})", inline=True)
        embed.add_field(name="Logging command", value=f"`~dono add {user.id} {valu} {proof}`\n\nYou may log it in <#824211968021495871>", inline=False)
        embed.set_footer(text=f"React with a ✅ after logged.")
        await channel.send(embed=embed)
        await ctx.reply("Logged in <#842738964385497108>")

    @commands.Cog.listener()
    async def on_message (self, message: discord.Message):
        if message.channel.id != 841657242053771274:
            return
        elif message.author.bot == True:
            await message.delete()
            return
        await message.delete()
        codes = {
            'jej662jh':841657703037927485,
            'hbd762jh':841657711334391838,
            'idi264jg':841657819731066882,
            'ggo531hk':841657855480037396,
            'ksp173hc':841657864715108353,
            'jep173hd':841924109507231764,
            'pan284hf':841924120387649557,
            'iap822jg':841924128965394433,
            'c$&apf129ka':841924483064528898,
            'jpa194og':841924891066499132,
            'pag183kc':841924910444314624,
            'wog734hd':842348151234101269,
            'jge953ka':842348167172849684,
            'kfr737oa':842348180116471838,
            'ofj827nv':842348765923115009,
            'kgr733al':842349560172904448,
            'shs635jb':842349792629358612,
            'jbc839ns' :842349859935879199,
            'jdh930hc' :842349903405121577,
            'ihh929ca' :842350062314586143,
            'hdi294ha' :842350821009915925,
            'dgs936kd' :842350914354544700,
            'hej294hc' :842350999045406792,
            'ahg837bv' :842351454831640597,
            'ajd284gc' :842351481096634399,
            'sbd478nv' :842351516686090240,
            'ahh387vc' :842351641268453386,
            'aud294bc' :842351748894556171,
            'jsj838pa' :842351786383900714,
            'jdj828al' :842351911323041792,
            'dnd284ak' :842352214864429076,
            'alf284sk' :842352242241830943,
            'c$&fuf838ka' :842352267247878154,
            'c$&djd746kh' :842352382485463050,
            'c$&hdj828sk' :842352473715769345,
            'c$&sno837bh' :842352497888591902,
            'c$&sjd839jv' :842352520860663838,
            'c$&sif837ka' :842352542075846676,
            'c$&isk194wj' :842352781671006208,
            'c$&zck384nv' :842352782094630913,
            'c$&jsj283bv' :842352850179719170,
            'c$&shh239bs' :842374700483215390,
            'c$&lka927sj' :842374840059953172,
            'c$&sdd929js' :842374904698503268,
            'c$&sld929dx' :842374988563480586,
            'c$&skd930fz' :842375032310464522,
            'c$&dog829mv' :842375088878911519,
            'c$&dkp305jc' :842375212342837268,
            'c$&sjc204kb' :842375271248035840,
            'c$&ieh194jv' :842375721531342900,
            'c$&mrbeme' :841805626300301374,
            'c$&tospetca' :842926861239582750,
            'c$&$of&fx29' :841980807215841301,
            'c$&&gh$yx64' :841980878153842708
        }
        admin = self.bot.get_channel(841654825456107533)
        member = message.guild.get_role(841805626300301374)
        await message.author.add_roles(member, reason="Verification")
        try:
            id = codes[message.content]
            role = message.guild.get_role(id)
            await message.author.add_roles(role, reason="Code input")
        except:
            await admin.send(f"The code `{message.content}` is invalid.")
        else:
            await admin.send(f"Added {role.mention} to {message.author.mention}")



def setup(bot):
    bot.add_cog(customCog(bot))