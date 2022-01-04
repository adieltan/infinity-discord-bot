import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks


class ImageCog(commands.Cog, name="Image"):
    """Image Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.COG_EMOJI = "📸"

    @commands.command(name="monkey")
    @commands.cooldown(1, 5)
    async def monkey(self, ctx):
        """Random monkey image + fact."""

        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                url="https://api.monkedev.com/attachments/monkey",
                params={"key": str(os.getenv("monkedevapi"))},
            ) as pic:
                picj = await pic.json()
                imageurl = picj["url"]
            async with cs.get(
                url="https://api.monkedev.com/facts/monkey",
                params={"key": str(os.getenv("monkedevapi"))},
            ) as fac:
                fa = await fac.json()
                fact = fa["fact"]
        embed = discord.Embed(
            title="Monkey",
            description=f"[Image]({imageurl})",
            color=discord.Color.random(),
        )
        embed.add_field(name="Monkey Fact", value=fact)
        embed.set_image(url=imageurl)
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text="MonkeDev Api")
        await ctx.reply(embed=embed, mention_author=False)
        await cs.close()

    @commands.command(name="bird")
    @commands.cooldown(1, 5)
    async def bird(self, ctx):
        """Random bird image + fact."""

        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                url="https://api.monkedev.com/attachments/bird",
                params={"key": str(os.getenv("monkedevapi"))},
            ) as pic:
                picj = await pic.json()
        imageurl = picj["url"]
        embed = discord.Embed(
            title="Bird",
            description=f"[Image]({imageurl})",
            color=discord.Color.random(),
        )
        embed.set_image(url=imageurl)
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text="MonkeDev Api")
        await ctx.reply(embed=embed, mention_author=False)
        await cs.close()

    @commands.command(name="cat")
    @commands.cooldown(1, 5)
    async def cat(self, ctx):
        """Random cat image + fact."""

        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                url="https://api.monkedev.com/facts/cat",
                params={"key": str(os.getenv("monkedevapi"))},
            ) as fa:
                fac = await fa.json()
                fact = fac["fact"]
            async with cs.get(
                "https://api.thecatapi.com/v1/images/search?apikey=4df9ec4d-2037-4c28-bb99-95307fcdae9a"
            ) as ca:
                cat = await ca.json()
                image = cat[0]["url"]
        embed = discord.Embed(
            title="Cat", description=f"[Image]({image})", color=discord.Color.random()
        )
        embed.add_field(name="Cat Fact", value=fact)
        embed.timestamp = discord.utils.utcnow()
        embed.set_image(url=image)
        embed.set_footer(text="MonkeDev Api")
        await ctx.reply(embed=embed, mention_author=False)
        await cs.close()

    @commands.command(name="dog")
    @commands.cooldown(1, 5)
    async def dog(self, ctx):
        """Random dog image + fact."""

        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                url="https://api.monkedev.com/facts/dog",
                params={"key": str(os.getenv("monkedevapi"))},
            ) as fa:
                fac = await fa.json()
                fact = fac["fact"]
            async with cs.get("https://dog.ceo/api/breeds/image/random") as do:
                dog = await do.json()
                image = dog["message"]
        embed = discord.Embed(
            title="Dog", description=f"[Image]({image})", color=discord.Color.random()
        )
        embed.add_field(name="Dog Fact", value=fact)
        embed.timestamp = discord.utils.utcnow()
        embed.set_image(url=image)
        embed.set_footer(text="MonkeDev Api + Dog Api")
        await ctx.reply(embed=embed, mention_author=False)
        await cs.close()

    @commands.command(name="fox")
    @commands.cooldown(1, 5)
    async def fox(self, ctx):
        """Random fox image + fact."""

        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/fox") as fa:
                fac = await fa.json()
                fact = fac["fact"]
            async with cs.get("https://randomfox.ca/floof/") as im:
                img = await im.json()
                image = img["image"]
        embed = discord.Embed(
            title="Fox", description=f"[Image]({image})", color=discord.Color.random()
        )
        embed.add_field(name="Fox Fact", value=fact)
        embed.timestamp = discord.utils.utcnow()
        embed.set_image(url=image)
        embed.set_footer(text="RandomFoxAPI + SomeRandomAPI")
        await ctx.reply(embed=embed, mention_author=False)
        await cs.close()

    @commands.command(name="meme")
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/meme") as mem:
                meme = await mem.json()
                url = meme["image"]
                caption = meme["caption"]
                category = meme["category"]

        embed = discord.Embed(
            title="Meme",
            description=f"[Image]({url})\n{caption}",
            color=discord.Color.random(),
        )
        embed.timestamp = discord.utils.utcnow()
        embed.set_image(url=url)
        embed.set_footer(text=category)
        await ctx.reply(embed=embed, mention_author=False)

        await cs.close()


def setup(bot):
    bot.add_cog(ImageCog(bot))
