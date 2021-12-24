from __future__ import annotations
import re, discord, itertools, asyncio, typing
from discord.ext import commands
from typing import Any, Tuple, List, Union, Optional, Dict, TYPE_CHECKING

class HelpDropdown(discord.ui.Select):
    def __init__(self, help_command: "MyHelpCommand", options: list[discord.SelectOption]):
        super().__init__(placeholder="Choose a category...", options=options)
        self._help_command = help_command

    async def callback(self, interaction: discord.Interaction):
        embed = (
            await self._help_command.cog_help_embed(self._help_command.context.bot.get_cog(self.values[0]))
            if self.values[0] != self.options[0].value
            else await self._help_command.bot_help_embed(self._help_command.get_bot_mapping())
        )
        await interaction.response.edit_message(embed=embed)


class HelpView(discord.ui.View):
    def __init__(self, help_command: "MyHelpCommand", options: list[discord.SelectOption]):
        super().__init__(timeout=90)
        self.add_item(HelpDropdown(help_command, options))
        self._help_command = help_command

    async def on_timeout(self):
        # remove dropdown from message on timeout
        self.clear_items()
        await self._help_command.response.edit(view=self)

    async def interaction_check(self, interaction:discord.Interaction):
        if self._help_command.context.author == interaction.user:
            return True
        await interaction.response.send_message("Eh don't be busybody.", ephemeral=True)
        return False

class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"

    async def _cog_select_options(self) -> list[discord.SelectOption]:
        options: list[discord.SelectOption] = []
        options.append(discord.SelectOption(
            label="Home",
            emoji="🏠",
            description="Go back to the main menu.",
        ))

        for cog, command_set in self.get_bot_mapping().items():
            if cog:
                help_filtered = (
                    filter(lambda c: c.name != "help", command_set)
                    if len(command_set) > 1
                    else command_set
                )
                filtered = await self.filter_commands(help_filtered, sort=True)
                if not filtered:
                    continue
                emoji = getattr(cog, "COG_EMOJI", None)
                options.append(discord.SelectOption(
                    label=cog.qualified_name,
                    emoji=emoji,
                    description=cog.description[:100] if cog and cog.description else None
                ))

        return options

    async def _help_embed(
        self, title: str, description: Optional[str] = None, mapping: Optional[dict] = None,
        command_set: Optional[typing.Set[commands.Command]] = None, set_author: bool = False
    ) -> discord.Embed:
        embed = discord.Embed(title=title)
        if description:
            embed.description = description
        if set_author:
            avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
            embed.set_author(name=self.context.bot.user.name, icon_url=avatar)
        if command_set:
            help_filtered = (
            filter(lambda c: c.name != "help", command_set)
            if len(command_set) > 1
            else command_set
            )
            filtered = await self.filter_commands(help_filtered, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.short_doc or "No description 😜",
                    inline=False
                )
        elif mapping:
            # add a short description of commands in each cog
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort=True)
                if not filtered:
                    continue
                name = cog.qualified_name if cog else "No category"
                emoji = getattr(cog, "COG_EMOJI", None)
                cog_label = f"{emoji} {name}" if emoji else name
                # \u2002 is an en-space
                cmd_list = "\u2002".join(
                    f"`{self.context.clean_prefix}{cmd.name}`" for cmd in filtered
                )
                value = (
                    f"{cog.description}\n{cmd_list}"
                    if cog and cog.description
                    else cmd_list
                )
                embed.add_field(name=cog_label, value=value)
        embed.color = discord.Color.random()
        if self.context.guild:
            embed.set_thumbnail(url=self.context.guild.icon)
        else:
            embed.set_thumbnail(url=self.context.author.display_avatar)
        return embed

    async def bot_help_embed(self, mapping: dict) -> discord.Embed:
        return await self._help_embed(
            title="Bot Commands",
            description=self.context.bot.description,
            mapping=mapping,
            set_author=True,
        )
    
    async def send_bot_help(self, mapping: dict):
        mapping = dict((name, []) for name in mapping)
        help_filtered = (
            filter(lambda c: c.name != "help", self.context.bot.commands)
            if len(self.context.bot.commands) > 1
            else self.context.bot.commands
            )
        for cmd in await self.filter_commands(
            help_filtered, sort=self.sort_commands,
        ):
            mapping[cmd.cog].append(cmd)
        embed = await self.bot_help_embed(mapping)
        options = await self._cog_select_options()
        self.response = await self.get_destination().send(embed=discord.Embed(color=0xBB2528).set_image(url='https://cdn.discordapp.com/attachments/813251835371454515/919210575643435008/christmas-background.jpg'), view=HelpView(self, options))

    async def send_command_help(self, command: commands.Command):
        emoji = getattr(command.cog, "COG_EMOJI", None)
        embed = await self._help_embed(
            title=f"{emoji} {command.qualified_name} {command.signature}" if emoji else command.qualified_name,
            description=command.help if command.help else 'No description 😜',
            command_set=command.commands if isinstance(command, commands.Group) else None
        )
        await self.get_destination().send(embed=embed)

    async def cog_help_embed(self, cog: typing.Optional[commands.Cog]) -> discord.Embed:
        if cog is None:
            return await self._help_embed(
                title=f"No category",
                command_set=self.get_bot_mapping()[None]
            )
        emoji = getattr(cog, "COG_EMOJI", None)
        return await self._help_embed(
            title=f"{emoji} {cog.qualified_name}" if emoji else cog.qualified_name,
            description=cog.description,
            command_set=cog.get_commands()
        )

    async def send_cog_help(self, cog: commands.Cog):
        embed = await self.cog_help_embed(cog)
        await self.get_destination().send(embed=embed)

    # Use the same function as command help for group help
    send_group_help = send_command_help


class Help(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
       self.bot = bot
        
       # Focus here
       # Setting the cog for the help
       help_command = MyHelpCommand()
       bot.help_command = help_command
       self.bot.help_command = help_command

    def cog_unload(self) -> None:
        self.bot.help_command = commands.HelpCommand


def setup(bot):
    bot.add_cog(Help(bot))
