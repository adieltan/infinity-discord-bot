import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

from thefuzz import process


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # users
    async def get_user(self, user_id: int):
        return await self.bot.db.profile.find_one({"_id": user_id}) or {}

    async def users(self, filter: dict = {}):
        return await self.bot.db.profile.count_documents(filter)

    async def edit_user(self, user_id: int, fields: dict):
        return await self.bot.db.profile.update_one(
            {"_id": user_id}, {"$set": fields}, upsert=True
        )

    async def del_user(self, user_id: int):
        return await self.bot.db.profile.find_one_and_delete({"_id": user_id})

    # servers
    async def get_server(self, server_id: int):
        return await self.bot.db.server.find_one({"_id": server_id}) or {}

    async def servers(self):
        return await self.bot.db.server.count_documents({})

    async def edit_server(self, server_id: int, fields: dict):
        return await self.bot.db.server.update_one(
            {"_id": server_id}, {"$set": fields}, upsert=True
        )

    async def del_server(self, server_id: int):
        return await self.bot.db.server.find_one_and_delete({"_id": server_id})


def setup(bot):
    bot.add_cog(Database(bot))


class Menu(discord.ui.View):
    def __init__(self, ctx, pages: list[discord.Embed]) -> None:
        super().__init__(timeout=60)
        self.current_page = 0
        self.pages = pages
        self.ctx = ctx
        self.value = None
        self.msg = None

    async def on_timeout(self) -> None:
        for vd in self.children:
            vd.disabled = True
        return await self.msg.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            return True
        await interaction.response.send_message("Eh don't be busybody.", ephemeral=True)
        return False

    @discord.ui.button(
        emoji="<:rewind:899651431294967908>", style=discord.ButtonStyle.blurple
    )
    async def first_page(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.edit_message(embed=self.pages[0])
        self.current_page = 0

    @discord.ui.button(
        emoji="<:left:876079229769482300>", style=discord.ButtonStyle.blurple
    )
    async def before_page(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.edit_message(
            embed=self.pages[(self.current_page - 1) % len(self.pages)]
        )
        self.current_page = (self.current_page - 1) % len(self.pages)

    @discord.ui.button(
        emoji="<:right:876079229710762005>", style=discord.ButtonStyle.blurple
    )
    async def next_page(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.edit_message(
            embed=self.pages[(self.current_page + 1) % len(self.pages)]
        )
        self.current_page = (self.current_page + 1) % len(self.pages)

    @discord.ui.button(
        emoji="<:forward:899651567869906994>", style=discord.ButtonStyle.blurple
    )
    async def last_page(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.edit_message(embed=self.pages[len(self.pages) - 1])
        self.current_page = len(self.pages) - 1


class Confirm(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.value = None
        self.ctx = ctx
        self.msg = None

    async def on_timeout(self) -> None:
        for v in self.children:
            v.disabled = True
        return await self.msg.edit("Timeout.", view=v)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            return True
        await interaction.response.send_message("Eh don't be busybody.", ephemeral=True)
        return False

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()
        self.value = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = False
        self.stop()


class ThreeChoices(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.value = None
        self.ctx = ctx
        self.msg = None

    async def on_timeout(self):
        for v in self.children:
            v.disabled = True
        return await self.msg.edit("Timeout.", view=self)

    code = "".join([random.choice(list(string.ascii_uppercase)) for _ in range(3)])

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            return True
        await interaction.response.send_message("Eh don't be busybody.", ephemeral=True)
        return False

    @discord.ui.button(label="".join(random.sample(code, len(code))))
    async def first(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = False
        self.children[self.children.index(button)].style = discord.ButtonStyle.red
        self.children[self.children.index(button)].disabled = True
        await self.msg.edit("Wrong", view=self)

    @discord.ui.button(label="".join(random.sample(code, len(code))))
    async def second(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = False
        self.children[self.children.index(button)].style = discord.ButtonStyle.red
        self.children[self.children.index(button)].disabled = True
        await self.msg.edit("Wrong", view=self)

    @discord.ui.button(label=code)
    async def third(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = True
        self.children[self.children.index(button)].style = discord.ButtonStyle.green
        for v in self.children:
            v.disabled = True
        await self.msg.edit("Correct", view=self)
        self.stop()



def is_owner():
    def predicate(ctx):
        return ctx.author.id in ctx.bot.owner_ids

    return commands.check(predicate)


def is_manager():
    def predicate(ctx):
        return ctx.message.author.id in ctx.bot.managers

    return commands.check(predicate)


def server(id: list):
    def predicate(ctx):
        return ctx.guild.id in id or ctx.author.id in ctx.bot.owners

    return commands.check(predicate)


def file(content: str, file_name: str):
    buffer = io.BytesIO(content.encode("utf-8"))
    return discord.File(buffer, filename=file_name)

class Member(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        converter = commands.MemberConverter()
        try:
            member = await converter.convert(ctx, argument)
        except:
            fuz = process.extractOne(argument, [r.name for r in ctx.guild.members if argument.lower() in r.name.lower()]) or (None, 0)
            if fuz[1] >= 75:
                return discord.utils.get(ctx.guild.members, name=fuz[0])
        else:
            return member
        raise commands.errors.BadArgument(
            f'Member  "{argument}" not found.'
        )

class TextChannel(commands.Converter):
    async def convert(self, ctx: commands.Context, argument:str):
        converter = commands.TextChannelConverter()
        try:
            channel = await converter.convert(ctx, argument)
        except:
            fuz = process.extractOne(argument, [r.name for r in ctx.guild.channels if argument.lower() in r.name.lower()]) or (None, 0)
            if fuz[1] >= 75:
                return discord.utils.get(ctx.guild.channels, name=fuz[0])
        else:
            return channel
        raise commands.errors.BadArgument(
            f'Channel "{argument}" not found.'
        )

class Role(commands.Converter):
    async def convert(self, ctx: commands.Context, argument:str):
        converter = commands.RoleConverter()
        try:
            role = await converter.convert(ctx, argument)
        except:
            roles = sorted(ctx.guild.roles, key = lambda i: i.name)
            fuz = process.extractOne(argument, [r.name for r in roles if argument.lower() in r.name.lower()]) or (None, 0)
            if fuz[1] >= 75:
                return discord.utils.get(ctx.guild.roles, name=fuz[0])
        else:
            return role
        raise commands.errors.BadArgument(
            f'Role "{argument}" not found.'
        )
