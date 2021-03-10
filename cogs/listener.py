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
        elif ('hi ') in message.content.lower():
            greeting = ('Hi', 'Hello', '안녕하세요 (Annyeonghaseyo)', '你好', 'こんにちは(Konnichiwa)', 'Bonjour')
            response = random.choice(greeting)
            await message.reply(response, mention_author=True, delete_after=5)
            pass
        elif ('hello ') in message.content.lower():
            greeting = ('Hi', 'Hello', '안녕하세요 (Annyeonghaseyo)', '你好', 'こんにちは(Konnichiwa)', 'Bonjour')
            response = random.choice(greeting)
            await message.reply(response, mention_author=True, delete_after=5)
            pass

    @commands.Cog.listener()
    async def on_command_error (self, ctx, error):
        await ctx.reply(f'<@{ctx.author.id}>\n{error}')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == 270904126974590976:
            pass
        elif before.author.bot == True:
            return
        elif before.author == self.bot.user:
            return
        fmt = '**{0.author}** edited their message:\n```{0.content} ```'
        await before.channel.send(fmt.format(before, after), delete_after=8)

def setup(bot):
    bot.add_cog(ListenerCog(bot))