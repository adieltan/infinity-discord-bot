import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 

import qrcode
from udpy import AsyncUrbanClient

class ConversionCog(commands.Cog, name='Conversion'):
    """*Conversion commands.*"""
    def __init__(self, bot):
        self.bot = bot
        self.urban = AsyncUrbanClient

    @commands.command(name="define", aliases=["meaning"])
    @commands.cooldown(1,6)
    async def define(self, ctx, *, phrase:str):
        """Defines a word."""
        await ctx.trigger_typing()
        defs = self.urban.get_definition(term=phrase)
        embed=discord.Embed(title=phrase, description="**Definition:**", color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        for defi in defs:
            if defi.example:
                eg = f"Example {defi.example}"
            else:eg=None
            embed.add_field(name=defi.word, value=f"{defi.description}\n{eg}\nUpvotes: {defi.upvotes} Downvotes: {defi.downvotes}")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="translate", aliases=['tr'])
    @commands.cooldown(1,6)
    async def translate(self, ctx,language:str, arg):
        """Translates a term."""
        pass

    @commands.command(name='qrcode', aliases=['qr'])
    @commands.cooldown(1,6)
    async def qr(self, ctx, *,text:str=None):
        """Generates a qr code."""
        ctx.typing()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=3)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        f = discord.File(buffer, filename="qr.png")
        
        embed=discord.Embed(title="Qr Generator", description=f"{text}", color=discord.Color.random())
        embed.set_image(url="attachment://qr.png")
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(file=discord.File(buffer, filename="qr.png"), embed=embed, mention_author=True)

#    @commands.command(name='qrdecode', aliases=['qrde', 'deqr'])
    #@commands.cooldown(1,4)
    #async def decode(self,ctx):
        #"""Decodes a qr code"""
        #fim = await file.read()
        #image = Image.open(io.BytesIO(initial_bytes=im))
        #byte = pyzbar.decode(image=image)[0].data
        #text = byte.decode("utf-8")
        #await ctx.reply(f"Decoded: \n{text}", mention_author=False)

    @commands.command(name='morse')
    @commands.cooldown(1,2)
    async def morse(self, ctx, *, text:str):
        """Encodes the text to morse code."""
        global morse 
        morse = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'}
        txt = text.upper()
        cipher = '' 
        for letter in txt: 
            if letter != ' ': 
    
                # Looks up the dictionary and adds the 
                # correspponding morse code 
                # along with a space to separate 
                # morse codes for different characters 
                cipher += morse[letter] + ' '
            else: 
                # 1 space indicates different characters 
                # and 2 indicates different words 
                cipher += ' '
        
        embed=discord.Embed(name="Morse Encoder", description=cipher, color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=True)

    @commands.command(name='morsedecode', aliases=['morsede', 'demorse'])
    @commands.cooldown(1,2)
    async def morse_to_eng(self, ctx, *, morsecode:str): 
        """Decodes the morse code to text."""
        morsecode += ' '
        decipher = '' 
        citext = '' 
        for letter in morsecode: 
            # checks for space 
            if (letter != ' '): 
                # counter to keep track of space 
                i = 0
                # storing morse code of a single character 
                citext += letter 
            # in case of space 
            else: 
                # if i = 1 that indicates a new character 
                i += 1
                # if i = 2 that indicates a new word 
                if i == 2 : 
                    # adding space to separate words 
                    decipher += ' '
                else: 
                    # accessing the keys using their values (reverse of encryption) 
                    decipher += list(morse.keys())[list(morse.values()).index(citext)] 
                    citext = '' 
        
        embed=discord.Embed(name="Morse Decoder", description=decipher, color=discord.Color.random())
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=True)


    @commands.command(name= 'binary', aliases=['bin'])
    @commands.cooldown(1,3)
    async def bin (self, ctx, *, input:str):
        """Find the binary form of a text"""
        binlist = [bin(ord(n))[2:] for n in input]
        text = ''
        for b in binlist:
            text = text + ' ' + b
        
        embed=discord.Embed(title="Binary converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name= 'binarydecode', aliases=['binde', 'debin'])
    @commands.cooldown(1,3)
    async def binde (self, ctx, *, input:str):
        """Find the binary form of a text reversed"""
        binlist = input.split(' ')
        text = ''
        for b in binlist:
            b = int(b, 2)
            text = text + chr(b)
        
        embed=discord.Embed(title="Binary converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name= 'hexadecimal', aliases=['hex'])
    @commands.cooldown(1,3)
    async def hex (self, ctx, *, input:str):
        """Find the hexadecimal form of a text"""
        binlist = [hex(ord(n))[2:] for n in input]
        text = ''
        for b in binlist:
            text = text + ' ' + b
        
        embed=discord.Embed(title="Hexadecimal converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name= 'hexadecimaldecode', aliases=['hexde', 'dehex'])
    @commands.cooldown(1,3)
    async def hexde (self, ctx, *, input:str):
        """Find the hexadecimal form of a text reversed"""
        binlist = input.split(' ')
        text = ''
        for b in binlist:
            b = int(b, 16)
            text = text + chr(b)
        
        embed=discord.Embed(title="Hexadecimal converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name= 'octadecimal', aliases=['oct'])
    @commands.cooldown(1,3)
    async def oct (self, ctx, *, input:str):
        """Find the octadecimal form of a text"""
        binlist = [oct(ord(n))[2:] for n in input]
        text = ''
        for b in binlist:
            text = text + ' ' + b
        
        embed=discord.Embed(title="Octadecimal converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name= 'octadecimaldecode', aliases=['octde', 'deoct'])
    @commands.cooldown(1,3)
    async def octde (self, ctx, *, input:str):
        """Find the octadecimal form of a text reversed"""
        binlist = input.split(' ')
        text = ''
        for b in binlist:
            b = int(b, 8)
            text = text + chr(b)
        
        embed=discord.Embed(title="Octadecimal converter", description=f"{input}", color=discord.Color.random())
        embed.add_field(name="Converted", value=text)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(ConversionCog(bot))