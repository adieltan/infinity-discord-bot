import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #users
    async def get_user(self, user_id:int):
        return await self.bot.db.profile.find_one({'_id':user_id}) or {}

    async def users(self, filter:dict={}):
        return await self.bot.db.profile.count_documents(filter)

    async def edit_user(self, user_id:int, fields:dict):
        return await self.bot.db.profile.update_one({'_id':user_id}, {'$set':fields}, upsert=True)

    async def del_user(self, user_id:int):
        return await self.bot.db.profile.find_one_and_delete({'_id':user_id})

    #servers
    async def get_server(self, server_id:int):
        return await self.bot.db.server.find_one({'_id':server_id}) or {}

    async def servers(self):
        return await self.bot.db.server.count_documents({})

    async def edit_server(self, server_id:int, fields:dict):
        return await self.bot.db.server.update_one({'_id':server_id}, {'$set':fields}, upsert=True)

    async def del_server(self, server_id:int):
        return await self.bot.db.server.find_one_and_delete({'_id':server_id})

def setup(bot):
    bot.add_cog(Database(bot))


class Menu(discord.ui.View):
    def __init__(self, ctx, pages:list[discord.Embed]) -> None:
        super().__init__(timeout=60)
        self.current_page = 0
        self.pages = pages
        self.ctx = ctx
        self.value = None

    async def interaction_check(self, interaction:discord.Interaction):
        return interaction.user.id == self.ctx.author.id

    @discord.ui.button(emoji='<:rewind:899651431294967908>', style=discord.ButtonStyle.blurple)
    async def first_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[0])
        self.current_page = 0

    @discord.ui.button(emoji='<:left:876079229769482300>', style=discord.ButtonStyle.blurple)
    async def before_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[(self.current_page - 1) % len(self.pages)])
        self.current_page = (self.current_page - 1) % len(self.pages)

    @discord.ui.button(emoji='<:right:876079229710762005>', style=discord.ButtonStyle.blurple)
    async def next_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[(self.current_page + 1) % len(self.pages)])
        self.current_page = (self.current_page + 1) % len(self.pages)

    @discord.ui.button(emoji='<:forward:899651567869906994>', style=discord.ButtonStyle.blurple)
    async def last_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[len(self.pages) -1 ])
        self.current_page = len(self.pages) - 1

class Confirm(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.value = None
        self.ctx = ctx
    
    async def interaction_check(self, interaction:discord.Interaction):
        return interaction.user.id == self.ctx.author.id

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = False
        self.stop()