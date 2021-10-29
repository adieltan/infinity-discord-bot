from __future__ import annotations
import re, discord, itertools, asyncio
from thefuzz import process
from discord.ext import commands, menus
from collections import namedtuple
from jishaku.codeblocks import Codeblock
from typing import Any, Tuple, List, Union, Optional, Dict, TYPE_CHECKING
from discord import ui
from random import randint
from abc import ABCMeta

# Unimportant part

class Menu(ui.View):
    def __init__(self, ctx, pages:list[discord.Embed]) -> None:
        super().__init__(timeout=30)
        self.current_page = 0
        self.pages = pages
        self.ctx = ctx
        self.msg = None

    async def on_timeout(self):
        self.clear_items()
        await self.msg.edit(view=None)

    async def interaction_check(self, interaction:discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            return True
        await interaction.response.send_message("Eh don't be busybody.", ephemeral=True)
        return False

    @ui.button(emoji='<:rewind:899651431294967908>', style=discord.ButtonStyle.blurple)
    async def first_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[0])
        self.current_page = 0

    @ui.button(emoji='<:left:876079229769482300>', style=discord.ButtonStyle.blurple)
    async def before_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[(self.current_page - 1) % len(self.pages)])
        self.current_page = (self.current_page - 1) % len(self.pages)

    @ui.button(emoji='<a:infinity:874548940610097163>', style=discord.ButtonStyle.blurple)
    async def stop_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await self.msg.delete()
        self.stop()

    @ui.button(emoji='<:right:876079229710762005>', style=discord.ButtonStyle.blurple)
    async def next_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[(self.current_page + 1) % len(self.pages)])
        self.current_page = (self.current_page + 1) % len(self.pages)

    @ui.button(emoji='<:forward:899651567869906994>', style=discord.ButtonStyle.blurple)
    async def last_page(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[len(self.pages) -1 ])
        self.current_page = len(self.pages) - 1


class Paginator:
    """A class that creates pages for Discord messages.

    Attributes
    -----------
    prefix: Optional[:class:`str`]
        The prefix inserted to every page. e.g. three backticks.
    suffix: Optional[:class:`str`]
        The suffix appended at the end of every page. e.g. three backticks.
    max_size: :class:`int`
        The maximum amount of codepoints allowed in a page.
    color: Optional[:class:`discord.Color`, :class: `int`]
        The color of the disord embed. Default is a random color for every invoke
    ending_note: Optional[:class:`str`]
        The footer in of the help embed
    """

    def __init__(
        self, show_index, color=0,
    ):
        self.ending_note = None
        self.color = color
        self.char_limit = 6000
        self.field_limit = 25
        self.prefix = ""
        self.suffix = ""
        self.show_index = show_index
        self.clear()

    def clear(self):
        """Clears the paginator to have no pages."""
        self._pages = []

    def _check_embed(self, embed: discord.Embed, *chars: str):
        """
        Check if the embed is too big to be sent on discord

        Args:
            embed (discord.Embed): The embed to check

        Returns:
            bool: Will return True if the emebed isn't too large
        """
        return (
            len(embed) + sum(len(char) for char in chars if char) < self.char_limit
            and len(embed.fields) < self.field_limit
        )

    def _new_page(self, title: str, description: str):
        """
        Create a new page

        Args:
            title (str): The title of the new page

        Returns:
            discord.Emebed: Returns an embed with the title and color set
        """
        return discord.Embed(title=title, description=description, color=self.color).set_author(name='Infinity', icon_url='https://cdn.discordapp.com/avatars/732917262297595925/2e48cb5004ee713a664a622eac81d594.png')

    def _add_page(self, page: discord.Embed):
        """
        Add a page to the paginator

        Args:
            page (discord.Embed): The page to add
        """
        page.set_footer(text=self.ending_note)
        self._pages.append(page)

    def add_cog(
        self, title: Union[str, commands.Cog], commands_list: List[commands.Command]
    ):
        """
        Add a cog page to the help menu

        Args:
            title (Union[str, commands.Cog]): The title of the embed
            commands_list (List[commands.Command]): List of commands
        """
        cog = isinstance(title, commands.Cog)
        if not commands_list:
            return

        page_title = title.qualified_name if cog else title
        embed = self._new_page(page_title, (title.description or "") if cog else "")

        self._add_command_fields(embed, page_title, commands_list)

    def _add_command_fields(
        self, embed: discord.Embed, page_title: str, commands: List[commands.Command]
    ):
        """
        Adds command fields to Category/Cog and Command Group pages

        Args:
            embed (discord.Embed): The page to add command descriptions
            page_title (str): The title of the page
            commands (List[commands.Command]): The list of commands for the fields
        """
        for command in commands:
            if not self._check_embed(
                embed,
                self.ending_note,
                command.name,
                command.short_doc,
                self.prefix,
                self.suffix,
            ):
                self._add_page(embed)
                embed = self._new_page(page_title, embed.description)

            embed.add_field(
                name=command.name,
                value=f'{self.prefix}{command.short_doc or "No Description"}{self.suffix}',
                inline=False,
            )
        self._add_page(embed)

    @staticmethod
    def __command_info(command: Union[commands.Command, commands.Group]):
        info = ""
        if command.description:
            info += command.description + "\n\n"
        if command.help:
            info += command.help
        if not info:
            info = "None"
        return info

    def add_command(self, command: commands.Command, signature: str):
        """
        Add a command help page

        Args:
            command (commands.Command): The command to get help for
            signature (str): The command signature/usage string
        """
        desc = f"{command.description}\n\n" if command.description else ""

        page = self._new_page(
            command.qualified_name,
            f"{self.prefix}{self.__command_info(command)}{self.suffix}" or "",
        )
        if command.hidden:
            page.add_field(name="Hidden", value="✅")
        if command.aliases:
            aliases = ", ".join(command.aliases)
            page.add_field(
                name="Aliases",
                value=f"{self.prefix}{aliases}{self.suffix}",
                inline=False,
            )
        if command._max_concurrency:
            page.add_field(name="Concurrent uses", value=f"{command._max_concurrency.number} uses per {command._max_concurrency.per}")
        page.add_field(
            name="Usage", value=f"```\n{self.prefix}{signature}{self.suffix}\n```", inline=False
        )
        self._add_page(page)

    def add_group(self, group: commands.Group, commands_list: List[commands.Command]):
        """
        Add a group help page

        Args:
            group (commands.Group): The command group to get help for
            commands_list (List[commands.Command]): The list of commands in the group
        """
        page = self._new_page(
            group.name, f"{self.prefix}{self.__command_info(group)}{self.suffix}" or ""
        )

        self._add_command_fields(page, group.name, commands_list)

    def add_index(self, title: str, bot: commands.Bot):
        """
        Add an index page to the response of the bot_help command

        Args:
            include (bool): Include the index page or not
            title (str): The title of the index page
            bot (commands.Bot): The bot instance
        """
        if self.show_index:
            index = self._new_page(title, bot.description or "")

            for page_no, page in enumerate(self._pages, 1):
                index.add_field(
                    name=f"• {page.title} ",
                    value=f'{self.prefix}{page.description or "No Description"}{self.suffix}',
                    inline=True,
                )
            index.set_footer(text=self.ending_note)
            self._pages.insert(0, index)
        else:
            self._pages[0].description = bot.description

    @property
    def pages(self):
        """Returns the rendered list of pages."""
        if len(self._pages) == 1:
            return self._pages
        lst = []
        start = 1 if not self.show_index else 0
        pages = len(self._pages) if not self.show_index else len(self._pages) - 1
        for page_no, page in enumerate(self._pages, start):
            page: discord.Embed
            if self.show_index and page_no == 0:
                pass
            else:
                page.description = f"`Page: {page_no}/{pages}`\n{page.description}"
            lst.append(page)
        return lst


class GoodHelp(commands.HelpCommand):
    def __init__(self, **options):

        self.color = options.pop(
            "color",
            discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)),
        )
        self.dm_help = options.pop("dm_help", False)
        self.index_title = options.pop("index_title", "Categories")
        self.no_category = options.pop("no_category", "No Category")
        self.sort_commands = options.pop("sort_commands", True)
        #self.menu = options.pop("menu", DefaultMenu())
        self.paginator = Paginator(
            color=self.color, show_index=options.pop("show_index", True)
        )
        self.ending_note = options.pop("ending_note", "")

        super().__init__(**options)

    async def prepare_help_command(
        self, ctx: commands.Context, command: commands.Command
    ):
        if ctx.guild is not None:
            perms = ctx.channel.permissions_for(ctx.guild.me)
            if not perms.embed_links:
                raise commands.BotMissingPermissions(("embed links",))
            if not perms.read_message_history:
                raise commands.BotMissingPermissions(("read message history",))
            if not perms.add_reactions:
                raise commands.BotMissingPermissions(("add reactions permission",))

        self.paginator.clear()
        self.paginator.ending_note = self.get_ending_note()
        await super().prepare_help_command(ctx, command)

    def get_ending_note(self):
        """Returns help command's ending note. This is mainly useful to override for i18n purposes."""
        note = self.ending_note or (
            "Use {ctx.clean_prefix}help [command] or help [category] for more information \n <> is required | [] is optional"
        )
        return note.format(ctx=self.context, help=self)

    async def send_pages(self):
        pages = self.paginator.pages
        destination = self.get_destination()
        if not pages:
            await destination.send(f"```{self.get_ending_note()}```")
        if len(pages) < 2:
            await self.context.channel.send(embed=pages[0])
        else:
            v = Menu(self.context, pages)
            v.msg = await self.context.channel.send(embed=pages[0], view=v)

    def get_destination(self):
        ctx = self.context
        if self.dm_help is True:
            return ctx.author
        else:
            return ctx.channel

    async def send_bot_help(self, mapping: dict):
        bot = self.context.bot
        channel = self.get_destination()
        async with channel.typing():
            mapping = dict((name, []) for name in mapping)
            help_filtered = (
                filter(lambda c: c.name != "help", bot.commands)
                if len(bot.commands) > 1
                else bot.commands
            )
            for cmd in await self.filter_commands(
                help_filtered, sort=self.sort_commands,
            ):
                mapping[cmd.cog].append(cmd)
            self.paginator.add_cog(self.no_category, mapping.pop(None))
            sorted_map = sorted(
                mapping.items(),
                key=lambda cg: cg[0].qualified_name
                if isinstance(cg[0], commands.Cog)
                else str(cg[0]),
            )
            for cog, command_list in sorted_map:
                self.paginator.add_cog(cog, command_list)
            self.paginator.add_index(self.index_title, bot)
        await self.send_pages()

    async def send_command_help(self, command: commands.Command):
        filtered = await self.filter_commands([command])
        if filtered:
            self.paginator.add_command(command, self.get_command_signature(command))
            await self.send_pages()

    async def send_group_help(self, group: commands.Group):
        async with self.get_destination().typing():
            filtered = await self.filter_commands(
                group.commands, sort=self.sort_commands
            )
            # if filtered:
            self.paginator.add_group(group, filtered)
        await self.send_pages()

    async def send_cog_help(self, cog: commands.Cog):
        async with self.get_destination().typing():
            filtered = await self.filter_commands(
                cog.get_commands(), sort=self.sort_commands
            )
            self.paginator.add_cog(cog, filtered)
        await self.send_pages()

class Help(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
        
       # Focus here
       # Setting the cog for the help
       help_command = GoodHelp()
       help_command.cog = self # Instance of YourCog class
       bot.help_command = help_command
       self.bot.help_command = help_command

    def cog_unload(self) -> None:
        self.bot.help_command = commands.HelpCommand


def setup(bot):
    bot.add_cog(Help(bot))