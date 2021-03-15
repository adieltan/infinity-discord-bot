import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, qrcode
from PyDictionary import PyDictionary
dictionary=PyDictionary()
from discord.ext import commands

class ConversionCog(commands.Cog, name='Conversion'):
    """*Conversion commands.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="define", aliases=["meaning"])
    @commands.cooldown(1,6)
    async def define(self, ctx, word):
        """Defines a word."""
        await ctx.trigger_typing()
        arg = word.lower()
        out = str(dictionary.meaning(arg))
        await ctx.reply(out, mention_author=False)

    @commands.command(name="translate", aliases=['tr'])
    @commands.cooldown(1,6)
    async def translate(self, ctx,language:str, arg):
        """Translates a term."""
        await ctx.trigger_typing()
        out = str(dictionary.translate(arg, language))
        await ctx.reply(out, mention_author=False)

    @commands.command(name="synonym", aliases=['sy'])
    @commands.cooldown(1,6)
    async def synonym(self, ctx, arg):
        """Gets the synonym of a term"""
        await ctx.trigger_typing()
        out = str(dictionary.synonym(arg))
        await ctx.reply(out, mention_author=False)

    @commands.command(name="antonym", aliases=['an'])
    @commands.cooldown(1,6)
    async def antonym(self, ctx, arg):
        """Gets the antonym of a term"""
        await ctx.trigger_typing()
        out = str(dictionary.antonym(arg))
        await ctx.reply(out, mention_author=False)

    @commands.command(name='qrcode', aliases=['qr'])
    @commands.cooldown(1,6)
    async def qr(self, ctx, *args):
        """Generates a qr code."""
        await ctx.typing()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=3)
        msg = " ".join(args)
        qr.add_data(msg)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('dqr.jpg')
        q = discord.File('D:\\TRH\\code\dqr.jpg')
        await ctx.reply(file=q, mention_author=False)

    @commands.command(name='silentqr', aliases=['sqr'])
    @commands.cooldown(1,6)
    async def silentqr(self, ctx, *args):
        """Generates a silent qr code."""
        await ctx.trigger_typing()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=3)
        msg = " ".join(args)
        qr.add_data(msg)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('dqr.jpg')
        q = discord.File('D:\\TRH\\code\dqr.jpg')
        await ctx.message.delete()
        await ctx.send(file=q)

    @commands.command(name='qrdecode')
    @commands.cooldown(1,4)
    async def decode(self,ctx):
        """Decodes a qr code"""
        await ctx.reply("No I don't do that. Go google it ||https://zxing.org/w/decode.jspx||", mention_author=False)


def setup(bot):
    bot.add_cog(ConversionCog(bot))