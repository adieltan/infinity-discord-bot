import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt

class EconomyCog(commands.Cog, name='Economy'):
    """*Economy Commands*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="shop", invoke_without_command=True)
    async def shop(self, ctx, item=None):
        """Finds the information about the item in Infinity shop."""
        if item is None:
            cursor = self.bot.dba['items'].find().sort('_id')
            items = []
            async for document in cursor:
                items.append(document)
            pages = [items[i:i + 12] for i in range(0, len(items), 12)]
            embeds = []
            for page in pages:
                text = '\n'.join([f"{item.get('emoji')} [**{item.get('name')}**]({item.get('image')} \"{item.get('_id')}\") " for item in page])
                embed=discord.Embed(title=f"Infinity Shop", description=f"{text}", color=discord.Color.random())
                embeds.append(embed)
                await ctx.reply(embed=embed)
        else:
            item = await self.bot.dba['items'].find_one({"name":item})
            embed=discord.Embed(title=f"Infinity Shop", description=f"{item.get('emoji')} [**{item.get('name')}**]({item.get('image')} \"{item.get('_id')}\")\n```\n{item.get('description')}\n```", color=discord.Color.random())
            embed.set_thumbnail(url=f"{item.get('image')}")
            await ctx.reply(embed=embed) 


    @shop.command(name="additem", aliases=['ai', 'add'])
    @commands.is_owner()
    async def additem(self, ctx, item_id:str, item_emoji:discord.PartialEmoji, item_name:str, item_price:float=None, item_description:str=None):
        """Adds an item to the bot's economy system."""
        await self.bot.dba['items'].update_one({"_id":item_id}, {"$set": {'name':item_name, 'emoji':f"{item_emoji}", 'price':item_price, 'image':f"{item_emoji.url}", 'description':f"{item_description}"}}, True)
        item = await self.bot.dba['items'].find_one({"_id":item_id})
        embed=discord.Embed(title=f"Infinity Shop", description=f"{item.get('emoji')} [**{item.get('name')}**]({item.get('image')} \"{item.get('_id')}\")\n```\n{item.get('description')}\n```", color=discord.Color.random())
        embed.set_thumbnail(url=f"{item.get('image')}")
        await ctx.reply(embed=embed) 

    @shop.command(name="edititem", aliases=['ei', 'edit'])
    @commands.is_owner()
    async def edititem(self, ctx, item_id:str=None, key=None, *, content=None):
        """Edits an item from the bot's economy system."""
        if key is None or content is None or item_id is None:
            await ctx.reply(f"Available keys: `name` `description` `price`")
        await self.bot.dba['items'].update_one({"_id":item_id}, {"$set": {key:content}}, True)
        item = await self.bot.dba['items'].find_one({"_id":item_id})
        embed=discord.Embed(title=f"Infinity Shop", description=f"{item.get('emoji')} [**{item.get('name')}**]({item.get('image')} \"{item.get('_id')}\")\n```\n{item.get('description')}\n```", color=discord.Color.random())
        embed.set_thumbnail(url=f"{item.get('image')}")
        await ctx.reply(embed=embed) 

def setup(bot):
    bot.add_cog(EconomyCog(bot))