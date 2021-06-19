import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime, aiohttp
from discord.ext import commands


class ImageCog(commands.Cog, name='Image'):
    """*Image Commands*"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="monkey")
    @commands.cooldown(1,5)
    async def monkey(self, ctx):
        """Random monkey image + fact."""
        hex_int = random.randint(0,16777215)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url="https://api.monkedev.com/attachments/monkey", params={'key':'mHigCVSfOLzuUI1yXwGFUSG0C'}) as pic:
                picj = await pic.json()
                imageurl = picj["url"]
            async with cs.get(url="https://api.monkedev.com/facts/monkey", params={'key':'mHigCVSfOLzuUI1yXwGFUSG0C'}) as fac:        
                fa = await fac.json()
                fact = fa['fact']
        embed=discord.Embed(title="Monkey", description=f"[Image]({imageurl})", color=hex_int)
        embed.add_field(name="Monkey Fact", value=fact)
        embed.set_image(url=imageurl)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_footer(text="MonkeDev Api")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="bird")
    @commands.cooldown(1,5)
    async def bird(self, ctx):
        """Random bird image + fact."""
        hex_int = random.randint(0,16777215)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url="https://api.monkedev.com/attachments/bird", params={'key':'mHigCVSfOLzuUI1yXwGFUSG0C'}) as pic:
                picj = await pic.json()
        imageurl = picj["url"]
        embed=discord.Embed(title="Bird", description=f"[Image]({imageurl})", color=hex_int)
        embed.set_image(url=imageurl)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_footer(text="MonkeDev Api")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="cat")
    @commands.cooldown(1,5)
    async def cat(self, ctx):
        """Random cat image + fact."""
        hex_int = random.randint(0,16777215)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url="https://api.monkedev.com/facts/cat", params={'key':'mHigCVSfOLzuUI1yXwGFUSG0C'}) as fa:
                fac = await fa.json()
                fact = fac["fact"]
            async with cs.get('https://api.thecatapi.com/v1/images/search?apikey=4df9ec4d-2037-4c28-bb99-95307fcdae9a') as ca:
                cat = await ca.json()
                image = cat[0]['url']
        embed=discord.Embed(title="Cat", description=f"[Image]({image})", color=hex_int)
        embed.add_field(name="Cat Fact", value=fact)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_image(url=image)
        embed.set_footer(text="MonkeDev Api")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="dog")
    @commands.cooldown(1,5)
    async def dog(self, ctx):
        """Random dog image + fact."""
        hex_int = random.randint(0,16777215)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url="https://api.monkedev.com/facts/dog", params={'key':'mHigCVSfOLzuUI1yXwGFUSG0C'}) as fa:
                fac = await fa.json()
                fact = fac["fact"]
            async with cs.get('https://dog.ceo/api/breeds/image/random') as do:
                dog = await do.json()
                image = dog['message']
        embed=discord.Embed(title="Dog", description=f"[Image]({image})", color=hex_int)
        embed.add_field(name="Dog Fact", value=fact)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_image(url=image)
        embed.set_footer(text="MonkeDev Api + Dog Api")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="fox")
    @commands.cooldown(1,5)
    async def fox(self, ctx):
        """Random fox image + fact."""
        hex_int = random.randint(0,16777215)
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/facts/fox') as fa:
                fac = await fa.json()
                fact = fac["fact"]
            async with cs.get('https://randomfox.ca/floof/') as im:
                img = await im.json()
                image = img['image']
        embed=discord.Embed(title="Fox", description=f"[Image]({image})", color=hex_int)
        embed.add_field(name="Fox Fact", value=fact)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_image(url=image)
        embed.set_footer(text="RandomFoxAPI + SomeRandomAPI")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='meme')
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/meme') as mem:
                meme = await mem.json()
                url = meme['image']
                caption = meme['caption']
                category = meme['category']
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="Meme", description=f"[Image]({url})\n{caption}", color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_image(url=url)
        embed.set_footer(text=category)
        await ctx.reply(embed=embed, mention_author=False)
                
        await cs.close()

def setup(bot):
    bot.add_cog(ImageCog(bot))