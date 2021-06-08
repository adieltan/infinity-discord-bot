import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime
from discord.ext import commands


class customCog(commands.Cog, name='custom'):
    """*Custom commands for server.*"""
    def __init__(self, bot):
        self.bot = bot
        
    def udevent():
        def predicate(ctx):
            return ctx.guild.id==841654825456107530 or ctx.guild.id==830731085955989534 
        return commands.check(predicate)

    @commands.command(name='bb')
    @udevent()
    @commands.has_role(841805626300301374)
    async def bb(self, ctx, victim:discord.Member):
        """Ban battle."""
        admin = ctx.guild.get_role(841655266743418892)
        banned = ctx.guild.get_role(851027190308929586)
        spec = ctx.guild.get_role(842926861239582750)
        if ctx.channel.id in [843027975070810114, 841654825456107533]:
            pass
        else:
            await ctx.reply("Not allowed in this channel.")
            return
        if banned in ctx.author.roles:
            await ctx.reply("You are banned.")
            return
        elif spec in ctx.author.roles:
            await ctx.reply("You have no weapon.")
            return
        elif admin in victim.roles:
            await ctx.reply("Unbannable")
            return
        elif spec in victim.roles:
            await ctx.reply("He has no weapons just eyes. No harm to you.")
            return
        elif banned in victim.roles:
            await ctx.reply("Already banned.")
            return
        else:
            await victim.add_roles(banned)
            await ctx.reply(f"Banned {victim.mention}")

    @commands.command(name='group', aliases=['g'])
    @udevent()
    @commands.has_permissions(administrator=True)
    async def group(self, ctx, code:str, groupleader:discord.User, member1:discord.User=None, member2:discord.User=None, *, message:str="Good luck"):
        """Dmes the group members the code."""
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="Kahoot Event Info", description="Message to your group from the host. [Server Invite](https://discord.gg/gEetr37)", color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
        embed.add_field(name="Verification Code", value=f"Type `{code}` in <#841657242053771274> to be verified and handed the group role.")
        embed.set_footer(text=code)
        if message:
            embed.add_field(name="Message", value=message)
        try:
            await groupleader.send("https://discord.gg/gEetr37", embed=embed)
        except:
            await ctx.reply(f"Can't send to {groupleader.mention}")
        try:
            await member1.send("https://discord.gg/gEetr37", embed=embed)
        except:
            await ctx.reply(f"Can't send to {member1.mention}")
        try:
            await member2.send("https://discord.gg/gEetr37", embed=embed)
        except:
            await ctx.reply(f"Can't send to {member2.mention}")

    @commands.command(name="donolog", aliases=["dl"])
    @udevent()
    @commands.has_permissions(administrator=True)
    async def logging(self, ctx, user:discord.User, quantity:float, item:str, value_per:str, *, proof:str):
        """Logs the dono."""
        raw = float(value_per.replace(",", ""))
        channel = self.bot.get_channel(842738964385497108)
        valu = math.trunc(raw)*quantity
        human = format(int(valu), ',')
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="Ultimate Dankers Event Donation", description=f"**Donator** : {user.mention}\n**Donation** : {quantity} {item}(s) worth {human} [Proof]({proof})", color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(icon_url=ctx.author.avatar_url, name=f"Logged by: {ctx.author.name}")
        embed.add_field(name="Logging command", value=f"`,d a {user.id} {valu:.2e} {proof}`\nLog in <#814490036842004520>", inline=False)
        embed.add_field(name="Raw", value=f"||`{ctx.message.content}`||", inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f"React with a ✅ after logged.")
        await channel.send(f"{user.id}", embed=embed)
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
            'ish287hc':850514046910070836,
            'aif225zh':850514176182845460,
            'apf255cz':850514187801460796,
            'sjf285cz':850514197133656095,
            'kao342gd':850514329538527232,
            'foa295ca':850514341480366160,
            'dif631cj':850514350769700884,
            'spg742hd':850515659006672908,
            'amg995xa':850515660878249984,
            'sog411ap':850515662194343936,
            'spg721va':850515663554478120,
            'kdf173sb':850515664447078421,
            'ksj284dd':850515666075123713,
            'orh184xa':850515667442335804,
            'oks853ff':850515670839459840,
            'idi384hd':850515672140087337,
            'ied994hs':850515673796706304,
            'phh274aa':850515675071774720,
            'pra025sa':850515676535455744,
            'dha500fa':850515677793484810,
            'gir328sh':850515679068684318,
            'kek246gg':850515680179519509,
            'pat426dd':850515681816608819,
            'flg327vs':850515683279110144,
            'uso385da':850515684647501924,
            'dkf532bs':850515685967790090,
            'ifg384cs':850515687239974912,
            'rog284fs':850515688514650132,
            'kdk945ds':850515689852239923,
            'iso294ds':850515691332567101,
            'sid885gs':850515692644990986,
            'ldf939jv':850515693866844180,
            'aof265hf':850515694923939881,
            'glb876gf':850515696496017414,
            'rog876ga':850515697506451467,
            'pth864gf':850515699134365696,
            'kdf984ga':850515700150042635,
            'sog765gs':850515701588426772,
            'afc645ff':850515702867558440,
            'dif877fd':850515704154554399,
            'apf274hs':850515705585860629,
            'off964hf':850515706700103711,
            'skk394gp':850515708071641100,
            'ffs045hz':850515709792354315,
            'osf887ff':850515711453560862,
            'kfd845cx':850515712699269140,
            'kff763fd':850515713977876490,
            'eud924hb':850515715320053791,
            'doc485sb':850515716658692096,
            'kdf94ss':850515717577244723,
            'c$&mrbeme' :841805626300301374,
            'c$&tospetca' :842926861239582750,
            'c$&$of&fx29' :841980807215841301,
            'c$&&gh$yx64' :841980878153842708,
            'laoxogosga919445-(:dld':841655266743418892
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