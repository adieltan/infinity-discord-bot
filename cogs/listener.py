import discord, random, string, os, logging, asyncio, discord.voice_client, sys, traceback, json, pymongo
from pymongo import MongoClient
from discord.ext import commands, tasks

class ListenerCog(commands.Cog, name='Listener'):
    """*Listening Commands.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message (self, message: discord.Message):
        if message.author.bot == True:
            return
        elif message.author == self.bot.user:
            return
        #excluded trigger guilds
        elif message.guild.id in [1]:
            return
        elif ('hi ') in message.content.lower():
            greeting = ('Hi', 'Hello', '안녕하세요 (Annyeonghaseyo)', '你好', 'こんにちは(Konnichiwa)', 'Bonjour')
            response = random.choice(greeting)
            await message.reply(response, mention_author=False, delete_after=5)
            pass
        elif ('hello ') in message.content.lower():
            greeting = ('Hi', 'Hello', '안녕하세요 (Annyeonghaseyo)', '你好', 'こんにちは(Konnichiwa)', 'Bonjour')
            response = random.choice(greeting)
            await message.reply(response, mention_author=False, delete_after=5)
            pass
        elif ('**f**') in message.content.lower():
            await message.add_reaction("a:f_:819009528204099624")
            pass
        elif ("701009836938231849") in message.content.lower():
            emoji =[":r1:715894707850313758", ":r2:747584481124286544"]
            for emj in emoji:
                await message.add_reaction(emj)
        elif ("732917262297595925") in message.content.lower():
            await message.add_reaction("♾️")


    @commands.Cog.listener()
    async def on_command_error (self, ctx, error):
        er = str(error)
        #skips wrong command
        if ("is not found") in er:
            return
        else:
            await ctx.reply(er, mention_author=False)

        if ("cooldown") in er:
            return
        elif ("not found") in er:
            return
        else:
            owner = await self.bot.application_info()
            hex_int = random.randint(0,16777215)
            embed=discord.Embed(title="Error", description="An error was recorded", color=hex_int)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Trigger", value=ctx.message.content)
            embed.add_field(name="Error", value=er)
            embed.add_field(name="User", value=f"User: {ctx.author.name} <@{ctx.author.id}>\nChannel: <#{ctx.channel.id}>\n[Message]({ctx.message.jump_url})")
            await owner.owner.send(embed=embed)

def setup(bot):
    bot.add_cog(ListenerCog(bot))