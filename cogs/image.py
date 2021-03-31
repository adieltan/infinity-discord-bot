import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime, requests
from discord.ext import commands


class ImageCog(commands.Cog, name='Image'):
    """*Image Commands*"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="monkey")
    @commands.cooldown(1,5)
    async def monkey(self, ctx):
        """Random monkey image."""
        hex_int = random.randint(0,16777215)
        pic = requests.get(url="https://api.monkedev.com/attachments/monkey", params={'key':'mHigCVSfOLzuUI1yXwGFUSG0C'})
        picj = pic.json()
        imageurl = picj["url"]
        fac = requests.get(url="https://api.monkedev.com/facts/monkey", params={'key':'mHigCVSfOLzuUI1yXwGFUSG0C'})
        fact = fac.json()["fact"]
        embed=discord.Embed(title="Monkey", description=f"[Image]({imageurl})", color=hex_int)
        embed.add_field(name="Monkey Fact", value=fact)
        embed.set_image(url=imageurl)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_footer(text="MonkeDev Api")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="bird")
    @commands.cooldown(1,5)
    async def bird(self, ctx):
        """Random bird image."""
        hex_int = random.randint(0,16777215)
        pic = requests.get(url="https://api.monkedev.com/attachments/bird", params={'key':'mHigCVSfOLzuUI1yXwGFUSG0C'})
        picj = pic.json()
        imageurl = picj["url"]
        embed=discord.Embed(title="Bird", description=f"[Image]({imageurl})", color=hex_int)
        embed.set_image(url=imageurl)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_footer(text="MonkeDev Api")
        await ctx.reply(embed=embed, mention_author=False)

    
def setup(bot):
    bot.add_cog(ImageCog(bot))