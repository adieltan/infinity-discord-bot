import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, requests, inspect, re, datetime
from discord.ext.commands.bot import BotBase
from discord.ext.commands.errors import ExtensionNotLoaded, TooManyArguments
from discord.ext import commands, tasks

class botcantalk(BotBase):
    def __init__(self, **options):
        self=self
        super().__init__(**options)
        super(BotBase)
            
    async def process_commands(self, message):
        """Listens to bot now too."""

        ctx = await self.get_context(message)
        await self.invoke(ctx)

class bot2(botcantalk, discord.Client):
    def __init__(self, **options):
        self=self
        super().__init__(**options)



class OwnerCog(commands.Cog, name='Owner'):
    """*Only owner can use this.*"""
    def __init__(self, bot):
        self.bot = bot
        self.bo2 = bot2
        
    @commands.command(name='reload', aliases=['load'])
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Command which Reloads/loads a Module."""
        cog="cogs." + cog.removeprefix("cogs.")
        try:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except ExtensionNotLoaded:
                self.bot.load_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}', mention_author=False)
        else:
            await ctx.reply(f'**`SUCCESSFULLY`** *reloaded* __{cog}__', mention_author=False)

    @commands.command(name='unload')
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        cog="cogs." + cog.removeprefix("cogs.")
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}', mention_author=False)
        else:
            await ctx.reply(f'**`SUCCESSFULLY`** *unloaded* __{cog}__', mention_author=False)

    @commands.command(name='eval', aliases=['e'])
    @commands.is_owner()
    async def eval(self, ctx, *, command):
        """Evaluate"""
        res = eval(command)
        if inspect.isawaitable(res):
            await ctx.reply(await res, mention_author=False)
        else:
            await ctx.reply(res, mention_author=False)



    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        """Tracks gift record on dank memer."""
        if ('pls gift' or 'pls shareitem') in message.content.lower():
            #getting id of recipant
            inp = str(message.content).split(sep=" ")
            recipant = message.mentions[0].id or re.findall("^(?:\d{18})$", message.content)[0]
            sender = message.author.id
            quantity = inp[2]
            item = inp[3]
            #leftovers
            remarks = inp[-1]
            def fromdankmemer(m):
                return m.author.id == 270904126974590976 and m.mentions[0].id == sender and ('You gave') in m.content

            try:
                vali = await self.bo2.wait_for(event="validation_from_dank", check=fromdankmemer, timeout=15 )
            except asyncio.TimeoutError:
                await message.channel.send("Guess we won't have a reply from dank today.\n**Checks:**\n- Check if dank is in the server\n- Check if the channel has dank enabled.\n- Check permissions for Dank Memer\n- Maybe you are dumb.")
                return    
            #input from dank
            #should be something like "@Rh You gave A Koala 1 bread, now ye have 17 and they've got 1" is sucessful
            #changing ','s which python dosen't understand and the input to a list 
            inpfd = str(vali.content).replace(",", "").split(sep=" ")
            #recipant final amount
            rfa = int(inpfd[-1])
            #sender final amount
            sfa = int(inpfd[-5])
            #validated item
            vi = inpfd[-9] 
            #validated item quantity
            viq = int(inpfd[-10])
            if quantity == viq:
                hex_int = random.randint(0,16777215)
                embed = discord.Embed(title="Dank Memer Item Transfer Validator", url=message.jump_url, description=f":green_circle: **Successful**\n[Trigger Message]({message.jump_url})\n[Validation Message]({vali.jump_url})", color=hex_int)
                embed.timestamp=datetime.datetime.utcnow()
                embed.set_author(icon_url=message.author.avatar_url, name=message.author)  
                embed.add_field(name="Original Message", value=f"{message.author.mention}\n{message.content}\nSent: {quantity} {item}\nNow has: {sfa} {vi}\nRemarks: {remarks}", inline=False)
                embed.add_field(name="Validation Message", value=f"{vali.content}", inline=False)
                embed.add_field(name="Recipant", value=f"<@{recipant}>\nReceived: {viq} {vi}\nNow has: {rfa} {vi}", inline=False)

                await message.channel.send(embed=embed)

            elif quantity != viq:
                hex_int = random.randint(0,16777215)
                embed = discord.Embed(title="Dank Memer Item Transfer Validator", url=message.jump_url, description=f":yellow_circle: **Await human verification**\n[Trigger Message]({message.jump_url})\n[Validation Message]({vali.jump_url})", color=hex_int)
                embed.timestamp=datetime.datetime.utcnow()
                embed.set_author(icon_url=message.author.avatar_url, name=message.author)  
                embed.add_field(name="Original Message", value=f"{message.author.mention}\n{message.content}\nSent: {quantity} {item}\nNow has: {sfa} {vi}\nRemarks: {remarks}", inline=False)
                embed.add_field(name="Validation Message", value=f"{vali.content}", inline=False)
                embed.add_field(name="Recipant", value=f"<@{recipant}>\nReceived: {viq} {vi}\nNow has: {rfa} {vi}", inline=False)



    @commands.command(name='logout', aliases=['shutdown', 'gosleep'])
    @commands.is_owner()
    async def logout(self, ctx):
        """Logs out."""
        await ctx.reply("👋")
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type= discord.ActivityType.playing, name="with the exit door."))
        await asyncio.sleep(8)
        await self.bot.close()


def setup(bot):
    bot.add_cog(OwnerCog(bot))