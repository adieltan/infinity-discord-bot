from asyncio.tasks import Task
import discord, random, string, asyncio, discord.voice_client, datetime, requests, math, aiohttp, time
from discord_components.interaction import InteractionEventType
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

class MiniGamesCog(commands.Cog, name='MiniGames'):
    """*Minigames.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='guess')
    @commands.cooldown(1,5)
    async def guess(self, ctx):
        """Guessing game"""
        await ctx.reply('Guess a number between 1 and 10.', mention_author=False)
        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()
        answer = random.randint(1, 10)

        try:
            guess = await self.bot.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.reply(f'Sorry, you took too long it was **__{answer}__**.', mention_author=False)

        if int(guess.content) == answer:
            await guess.reply('Congrats!', mention_author=False)
        else:
            await guess.reply(f'No It is actually **__{answer}__**.', mention_author=False)

    @commands.command(name="8corners", aliases=['8c', 'corner', 'corners'])
    @commands.cooldown(1,10, BucketType.category)
    async def corners(self, ctx, aliverole:discord.Role=None, deadrole:discord.Role=None):
        """8 corners Game."""
        await ctx.trigger_typing()
        hex_int = random.randint(0,16777215)
        emoji = discord.PartialEmoji(name='a:Join', animated=True, id=855683444310147113)
        colours = ['\U0001f534', '\U0001f7e0', '\U0001f7e1', '\U0001f7e2', '\U0001f535', '\U0001f7e4', '\U0001f7e3', '\U000026aa']
        embed=discord.Embed(title="8 Corners Game", description=f"React to the button on the message to join.\nTimer: 5 minutes\n`=8cg` to learn more about the game.", color=hex_int)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_footer(text="If you are already in the list of players, the interaction will fail. Else, please press the button again.")
        players = []
        alive = []
        dead = []
        info = await ctx.reply(embed=embed, mention_author=False, components=[Button(id="join", emoji= emoji, style=ButtonStyle.grey)])
        timeout = 5
        timeout_start = time.time()
        await info.add_reaction(emoji)
        while time.time() < timeout_start + timeout:
            try:
                interaction = await self.bot.wait_for("button_click", check=lambda i:i.component.id in ['join'], timeout =5)
                if interaction.user in players:
                    raise IndexError
                players.append(interaction.user)
                await interaction.respond(type=InteractionType.UpdateMessage, content=f"{len(players)} players.\n"+'\n'.join([f'{p.mention}'for p in players]), mention_author=False)
            except:
                timeleft = (timeout_start + timeout) - time.time()
                embed.description=f"React to the button on the message to join.\nTimer: {round(timeleft)} seconds.\n`=8cg` to learn more about the game."
                await info.edit(content=f"{len(players)} players.\n"+'\n'.join([f'{p.mention}'for p in players]), embed=embed, mention_author=False)
        embed.description=f"Timer: Ended.\n`=8cg` to learn more about the game."
        await info.edit(embed=embed, components=[Button(id="join", emoji= emoji, style=ButtonStyle.grey, disabled=True)])
        playercountfrombuttons = len(players)
        users = []
        message = await ctx.channel.fetch_message(info.id)
        reactions = message.reactions
        for reaction in reactions:
            if reaction.emoji == emoji:
                people = await reaction.users().flatten()
                for user in people:
                    users.append(user)
        await ctx.send(f'{reactions}')
        embed=discord.Embed(title="8 Corners Game", description=f"Processing reactions...\n__**Statistics**__\nRegistered players count using buttons: {playercountfrombuttons}\nNumber of reactions: {len(users)}")
        stats = await ctx.send(embed=embed)
        validfromreaction = 0
        for user in users:
            if user in players:
                pass
            elif user.bot:
                pass
            else:
                players.append(user)
                validfromreaction += 1
        embed.description=f"Reactions processed.\nAdding roles to players...\n__**Statistics**__\nRegistered players count using buttons: {playercountfrombuttons}\nNumber of reactions: {len(users)}\nRegistered players count using reactions: {validfromreaction}\n\n**Total players registered:** {len(players)}"
        await stats.edit(embed=embed)
        if aliverole:
            for m in aliverole.members:
                try:
                    await m.remove_roles(aliverole, reason="Minigame")
                except:pass
        if deadrole:
            for m in deadrole.members:
                try:
                    await m.remove_roles(aliverole, reason="Minigame")
                except:pass
        for p in players:
            p = ctx.guild.get_member(p.id)
            await p.add_roles(aliverole, reason='Minigame')

        
    @commands.command(name='8cornersguide', aliases=['8cg'])
    @commands.cooldown(1,3,BucketType.channel)
    async def eightcg(self, ctx):
        hex_int = random.randint(0,16777215)
        embed=discord.Embed(title="8 Corners Game Guide", description=f"Info about the 8 corners game.", color=hex_int)
        embed.add_field(name="Introduction", value=f"The idea originally came from [Link](https://youtu.be/SEmKz665hnY) because <@703135131459911740> is unoriginal as you guys can tell. But the challenges that you will face to either revive yourself, or get spared when your corner is chosen, will be harder than those in the video.")
        embed.add_field(name="Before Game", value=f"160 Players max.\nAn eliminated role can be selected at the start of the game.\nIf a player is AFK and does not select a corner, they will be out.", inline=False)
        embed.add_field(name="Colour selection", value="At the start of each round, all players with the role `@Alive` are able to choose a corner. While users with `@Eliminated` or without `@Alive` will not be allowed to select.\nWhen chosen a colour, look at the embed and make sure that your name is in the respective team and not under the Have Not Chosen Section.", inline=False)
        embed.add_field(name="Gameplay", value="When the round starts, there will be a wheel of fate that spins all the colours. Whatever colour it lands on, all users that picked that colour is eliminated. After that, the colour cannot be chosen anymore.\nIf your colour is chosen, there will be a redemption round among the people in the corner unless there is less than 3 people.", inline=False)
        embed.add_field(name="Redemption round", value="When the redemption round starts, the bot will randomly select a mini game. It ranges from a ban battle, to the fastest reaction time, deciphering codes and even doing nothing and just seeing your luck as a wheel of redemption gets spun and the player it lands on, gets revived.", inline=False)
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["ctp", "capturethephoenix"], hidden=True)
    async def catchthephoenix(self, ctx, member: discord.Member=None):
        points = {ctx.author: 0, member: 0}
        random_time = random.randrange(30)

        game = False
        if member is None:
            await ctx.send("...")
        elif member == self.bot.user:
            await ctx.send("...")
        elif member.bot:
            await ctx.send("...")
        else:
            game = True

        await ctx.send(...)
        while game:
            try:
                await asyncio.sleep(random_time)
                await ctx.send(...)
                message = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.author.id == ctx.author.id,
                    timout=45.0
                )
            except asyncio.TimeoutError:
                game = False
                ...
            if not message.content.lower() == "catch":
                continue
            if message.author.id == member.id:
                ...
            elif message.author.id == ctx.author.id:
                ...


    

    @commands.command(name='ttt', aliases=['tictactoe'], hidden=True)
    @commands.cooldown(1,10)
    async def ttt(self, ctx, opponent:discord.Member):

        def checkForWin(board):
            win = (
                board[0] == board[1] and board[1] == board[2]
                or board[3] == board[4] and board[4] == board[5]
                or board[6] == board[7] and board[7] == board[8]
                or board[0] == board[4] and board[4] == board[8]
                or board[2] == board[4] and board[4] == board[6]
                or board[0] == board[3] and board[3] == board[6]
                or board[1] == board[4] and board[4] == board[7]
                or board[2] == board[5] and board[5] == board[8]
            )
            if not any(i.isdigit() for i in board) and not win:
                return 2
            else:
                return win

        if ctx.author == opponent:
            await ctx.reply(f"{ctx.author.mention} You can't challenge yourself!")
            return
        if opponent.bot:
            await ctx.reply(f"{ctx.author.mention} You can't play with a bot. You will never hear a reply...")
            return

        components = [
            [Button(style=ButtonStyle.gray,label=str(ia+i)) for ia in range(3)] for i in range(1,9,3)
        ]
        gamemsg = await ctx.send(f'{opponent.mention}, {ctx.author.name} has challenged thee to tic-tac-toe! You go first.', components=components)
        turn = 'X'
        players = {
            'X': opponent,
            'O': ctx.author
        }

        def checkEvent(event):
            component = event.component
            if type(component) is not dict:
                component = event.component.to_dict()
            return (
                (component['label'] != 'X' and component['label'] != 'O')
                and event.message.id == gamemsg.id
                and (event.user == players[turn])
            )

        def getButtonStyle(value):
            if value == 'X':
                return ButtonStyle.blue
            elif value == 'O':
                return ButtonStyle.red
            else:
                return ButtonStyle.gray

        while True:
            try:
                boardClick = await self.bot.wait_for('button_click', check=checkEvent, timeout=20)
                moveComponent = boardClick.component
                if type(moveComponent) is not dict:
                    moveComponent = boardClick.component.to_dict()
                board = [button.label for button in boardClick.message.components]
                squareClicked = board.index(moveComponent["label"])
                board[squareClicked] = turn

                gameWon = checkForWin(board)

                components = [[Button(style=getButtonStyle(board[i+ia-1]),label=board[i+ia-1],disabled=bool(gameWon)) for ia in range(3)] for i in range(1,9,3)]

                if gameWon:
                    if gameWon == 2:
                        await boardClick.respond(type=7,content=f'Game Over! It is a tie!', components = components)
                    else:
                        await boardClick.respond(type=7,content=f'Game Over! {players[turn].mention} has won!', components = components)
                    break

                if (turn == 'X'):
                    turn = 'O'
                else:
                    turn = "X"
                
                await boardClick.respond(type=7,content=f"It is {players[turn].mention}'s turn.", components = components) 
            except asyncio.TimeoutError:
                try:
                    boardClick
                except:
                    components = [[Button(style=ButtonStyle.grey,label=str(ia+i)) for ia in range(3)] for i in range(1,9,3)]
                else:
                    board = [button.label for button in boardClick.message.components]
                    components = [[Button(style=getButtonStyle(board[i+ia-1]),label=board[i+ia-1],disabled=True) for ia in range(3)] for i in range(1,9,3)]
                await gamemsg.edit(content="Timeout", components=components)

    
def setup(bot):
    bot.add_cog(MiniGamesCog(bot))