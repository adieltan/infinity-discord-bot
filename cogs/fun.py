import discord, random, string, os, asyncio, sys, math, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

from thefuzz import process
import collections
from PIL import Image
import time

from ._utils import Database, ThreeChoices

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return
        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                assert isinstance(child, discord.ui.Button) # just to shut up the linter
                child.disabled = True
            view.stop()
        await interaction.response.edit_message(content=content, view=view)

class TicTacToe(discord.ui.View):
    X = -1
    O = 1
    Tie = 2
    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X
        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X
        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X
        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie
        return None

class CoinFlip(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=20)
        self.value = None
        self.msg = None

    async def on_timeout(self):
        for v in self.children:
            v.disabled = True
        return await self.msg.edit('Timeout.', view=self)

    @discord.ui.button(label='Heads', style=discord.ButtonStyle.green)
    async def heads(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.value = True
        self.stop()

    @discord.ui.button(label='Tails', style=discord.ButtonStyle.red)
    async def tails(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.value = False
        self.stop()

class EightCornersJoin(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.msg = None
        self.players = []
        self.endtime = round(discord.utils.utcnow().timestamp()) + (5*60)

    async def interaction_check(self, interaction: discord.Interaction):
        if round(discord.utils.utcnow().timestamp()) <= self.endtime:
            return True
        self.stop()
        return False

    async def on_timeout(self):
        for v in self.children:
            v.disabled = True
        e = self.msg.embeds[0]
        e.description=f'Timer: Ended.\nPlayer count: {len(self.players)} players.\n`=8cg` to learn more about the game.'
        self.msg.edit(embed=e, view=None)
    
    @discord.ui.button(emoji='<a:Join:855683444310147113>', label='Join', style=discord.ButtonStyle.green)
    async def join(self, button:discord.ui.Button, interaction:discord.Interaction):
        if interaction.user in self.players:
            return await interaction.response.send_message('You already joined the game.', ephmeral=True)
        await interaction.response.send_message(embed=discord.Embed(title="Game join confirmation",description=f"You have joined the game. [Message]({self.msg.jump_url})",color=discord.Color.random()), ephemeral=True)
        self.players.append(interaction.user)

    @discord.ui.button(emoji='<a:Bomb:855685941484847125>', label='Skip', style=discord.ButtonStyle.red)
    async def skip(self, button:discord.ui.Button, interaction:discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await interaction.response.send_message('Skipping', ephemeral=True)
            for v in self.children:
                v.disabled = True
            e = self.msg.embeds[0]
            e.description=f'Timer: Ended.\nPlayer count: {len(self.players)}    players.\n`=8cg` to learn more about the game.'
            await self.msg.edit(embed=e, view=None)
            return self.stop()
        else:
            await interaction.response.send_message("You aren't the host.", ephemeral=True)
class FunCog(commands.Cog, name='Fun'):
    """🥳 Fun / minigame commands."""
    def __init__(self, bot):
        self.bot = bot
        self.ongoing_mm_games = dict()
    
    @commands.group(name='pet', invoke_without_command=True)
    async def pet(self, ctx):
        """Pet..."""
        pets = {
        '🐶': 'dog', 
        '🐱': 'cat',
        '🐭': 'mouse',
        '🐹': 'hamster',
        '🐰': 'rabbit',
        '🦊': 'fox',
        '🐻': 'bear',
        '🐼': 'panda',
        '🐨': 'koala',
        '🐯': 'tiger',
        '🦁': 'lion',
        '🐮': 'cow',
        '🐷': 'pig',
        '🐧': 'penguin',
        '🐦': 'bird',
        '🐤': 'chick',
        '🦆': 'duck',
        '🦉': 'owl',
        '🐺': 'wolf'}
        v = ThreeChoices(ctx)
        random.shuffle(v.children)
        e = discord.Embed(title='Pets', description='\n'.join(f"{pet} {pets[pet].title()}" for pet in pets))
        v.msg = await ctx.reply(embed=e, view=v)
        await v.wait()
        if v.value:
            await v.msg.edit('Congrats')
        else:
            await v.msg.edit('Failed')


    @commands.command(name= 'roll', aliases=['dice', 'throw'])
    @commands.cooldown(1,5)
    async def roll(self, ctx, number_of_dice:int, number_of_sides:int):
        """Randomly rolls dices. [number_of_dice] cannot be higher than 25."""
        if number_of_dice > 25: 
            await ctx.send(f"*number_of_dice* cannot be over 25.\nYour input: **{number_of_dice}**")
            return
        
        embed = discord.Embed(title=f"{ctx.author}'s Rolling Game", color=discord.Color.random())
        embed.set_author(icon_url=ctx.author.avatar, name=str(ctx.author))
        embed.timestamp=discord.utils.utcnow()
        for _ in range(number_of_dice):
            embed.add_field(name='\uFEFF', value=f'{random.choice(range(1,number_of_sides + 1))}', inline=True)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5)
    async def choose(self, ctx, choice1, choice2):
        """Randomly helps you choose one between two choices."""
        cho=choice1, choice2
        ran=random.choice(cho)
        msg = await ctx.reply(f'(*&^{choice1}%$^$#%%^&{choice2}**&(#&$&#^&))', mention_author=False)
        await asyncio.sleep(1.0)
        await msg.edit(content=f'I choose **{ran}**')

    @commands.command(name="draw", aliases=["rollreaction", "roll reactions"])
    @commands.cooldown(1,3)
    async def draw(self, ctx, numbers:int):
        """Draws random people that reacted to a message."""
        me = ctx.message.reference
        users = []
        winners = []
        if me == None:
            await ctx.reply("You have to reply to the message you wanna draw from!", mention_author=True)
        elif numbers > 80:
            await ctx.reply("Thats a little too much.")
        else:
            meh = me.message_id           
            message = await ctx.channel.fetch_message(meh)
            reactions = message.reactions
            if len(reactions) < 1:
                await ctx.reply("No one reacted to that message.")
            else:
                users = [await reaction.users().flatten() for reaction in reactions][0]
                if numbers > len(users):
                    numbers = len(users)
                while len(winners) < numbers:
                    win = random.choice(users)
                    winners.append(win)
                    users.remove(win)
                embed=discord.Embed(title="Draw results", description=f"[Jump]({message.jump_url})\n{message.content}", color=discord.Color.random())
                embed.timestamp=discord.utils.utcnow()
                embed.set_author(icon_url=ctx.author.avatar, name=ctx.author)
                text= "\n".join([f'{winner.mention} `{winner.id}`' for winner in winners])
                embed.add_field(name="Winners", value=text)
                embed.set_footer(text=f"{numbers} winners")
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="8corners", aliases=['8c', 'corner', 'corners'])
    @commands.cooldown(1, 100, commands.BucketType.category)
    async def corners(self, ctx):
        """8 corners Game."""
        self.teams = []

        class team:
            def __init__(tself, name, emoji, status: bool = True):
                tself.name = name
                tself.emoji = self.bot.get_emoji(emoji)
                tself.status = status
                tself.members = []
                self.teams.append(tself)
            def add(tself, person: discord.User):
                tself.members.append(person)
                return tself.members
            def getmembers(tself):
                return tself.members
            def count(tself):
                return int(len(tself.members))
            def resetmembers(tself):
                tself.members = []
                return tself.members
            def resetteam(defaultteams:list=[]):
                self.teams = defaultteams
        players = []
        joinv = EightCornersJoin(ctx)
        embed = discord.Embed(title="8 Corners Game",
                              description=f"React to the message to join.\nStarting <t:{joinv.endtime}:R>\n`=8cg` to learn more about the game.",
                              color=discord.Color.random(), timestamp = discord.utils.utcnow())
        dead = []
        joinv.msg = await ctx.reply(embed=embed, view=joinv)
        await joinv.wait()
        players = joinv.players
        if len(players) <= 1:
            return await ctx.reply('Sadly, not many players joined.')
        while len(players) > math.floor(len(players)/3):
            chosen = []
            afk = []
            for team in self.teams:
                team.resetmembers()
            embed = discord.Embed(title="8 corners game",
                                  description=f"__**Statistics**__\n**Players count:** {len(players)}",
                                  colour=discord.Color.green())
            stats = await ctx.send(embed=embed)
            team.resetteam()
            rainbow = team("Rainbow Team", 855682390905978922)
            cyan = team("Cyan Team", 855682336107528192)
            colours = ["a:RainbowTeam:855682390905978922", "<a:CyanTeam:855682336107528192>"]
            cyan = team("Cyan Team", 855682336107528192)
            if len(players) > 3 :
                purple = team("Purple Team", 855682262460923956)
                colours.append("<a:PurpleTeam:855682262460923956>")
            if len(players) > 6 : 
                green = team("Green Team", 855682185641852979)
                colours.append("<a:GreenTeam:855682185641852979>")
            if len(players) > 9 : 
                yellow = team("Yellow Team", 855682130414796811)
                colours.append("<a:YellowTeam:855682130414796811>")
            if len(players) > 12: 
                red = team("Red Team", 855682071786553375)
                colours.append("<a:RedTeam:855682071786553375>")
            if len(players) > 15: 
                pink = team("Pink Team", 855682043157151784)
                colours.append("<a:PinkTeam:855682043157151784>")
            if len(players) > 18: 
                blue = team("Blue Team", 855681996490932224)
                colours.append("<a:BlueTeam:855681996490932224>")

            # colour choosing stage
            embed = discord.Embed(title=f"8 corners game", description="Loading reactions.",
                                  colour=discord.Color.random())
            cmes = await joinv.msg.reply(embed=embed)
            for t in self.teams: await cmes.add_reaction(t.emoji)
            await cmes.add_reaction('<a:Bomb:855685941484847125>')
            embed.description = f"React to the specific colour to choose teams.\nTimer: 2m"
            await cmes.edit(embed=embed)
            chosen = []
            timeout = 2 * 60
            timeout_start = time.time()
            rcount = math.ceil(len(players) / len(colours))

            def check(reaction, user):
                if reaction.message.id != cmes.id:
                    return False
                elif user not in players:
                    return False
                return True

            async def choose(t: team, user):
                t.add(user)
                chosen.append(user)
                try:
                    await user.send(f"You joined the {t.name} ({t.count()})")
                except:
                    await ctx.send(f"{user.mention},  You joined the {t.name}.")

            while time.time() < timeout_start + timeout:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=5)
                    peop = len(await reaction.users().flatten()) - 1
                    if '<a:Bomb:855685941484847125>' == str(reaction.emoji):
                        if ctx.author == user:
                            break
                    elif peop > rcount:
                        await cmes.remove_reaction(reaction.emoji, user)
                        await user.send("The team is full please chose another team/color.")
                    elif user in chosen:
                        await cmes.remove_reaction(reaction.emoji, user)
                        await user.send("You have already selected a team/color.")
                    elif reaction.emoji == rainbow.emoji:
                        await choose(rainbow, user)
                    elif reaction.emoji == cyan.emoji:
                        await choose(cyan, user)
                    elif reaction.emoji == purple.emoji:
                        if len(players) > 3:
                            await choose(purple, user)
                    elif reaction.emoji == green.emoji:
                        if len(players) > 6:
                            await choose(green, user)
                    elif reaction.emoji == yellow.emoji:
                        if len(players) > 9:
                            await choose(yellow, user)
                    elif reaction.emoji == red.emoji:
                        if len(players) > 12:
                            await choose(red, user)
                    elif reaction.emoji == pink.emoji:
                        if len(players) > 15:
                            await choose(pink, user)
                    elif reaction.emoji == blue.emoji:
                        if len(players) > 18:
                            await choose(blue, user)
                except:
                    embed.description = f"React to the specific colour to choose teams.\nTimer: {round((timeout_start + timeout) - time.time())} seconds\n"
                    embed.color = discord.Color.random()
                    await cmes.edit(embed=embed)
            embed.description = f"Timer ended"
            await cmes.edit(embed=embed)
            await cmes.clear_reactions()
            text = '\n'.join([f"{t.emoji} {t.name}: {t.count()}" for t in self.teams])
            embed = discord.Embed(title="8 corners game", description=f"""**Team Members Count**\n{text}""")
            teamstat = await cmes.reply(embed=embed)

            rancol = random.choice(self.teams)
            for a in rancol.getmembers():
                dead.append(a)
                players.remove(a)

            die = ["**{}** has lava in their field and everyone there died.",
                    "The plane carrying **{}**'s members crashed into a canyon.",
                    "Beggar felt hungry suddently and ate up all members of **{}**",
                    "**{}**'s members were no where to be found.",
                    "**{}**'s members were found in the stomach of a shark.",
                    "The plague doctor killed all members of **{}**",
                    "**{}** is the impostor.",
                    "**{}** got stomped by a giant toad.",
                    "God wants **{}** dead.", 
                    "Rick Astey rick rolled **{}**.", 
                    "Randomizer decided to trow **{}** to the trash bin.", 
                    "**{}** was hacked and destroyed.",
                    "**{}** got stuck in the Quantum Field.", 
                    "**{}** pressed Alt+F4.", 
                    "**{}**'s supercomputer got [hacked](https://bit.ly/3h5kbvl).", 
                    "**{}** got hit by a F-35's Laser-Guided Bombs.", 
                    "**{}** got infected with Covid-19."]

            for p in players:
                if p not in chosen:
                    afk.append(p)
                    players.remove(p)

            mes = f"{random.choice(die)} \n{len(afk)} died because they didn't choose anything."
            chance = random.randint(0, 100)
            if len(dead)>0:
                if chance < 10:
                    lucky = random.choice(dead)
                    players.append(lucky)
                    dead.remove(lucky)
                    mes = mes + f"\n{len(players)} player left in the game. \n{lucky.name} got revived"
                else:mes = mes + f"\n{len(players)} player left in the game."
            else:mes = mes + f"\n{len(players)} player left in the game."
            embed.description = mes.format(rancol.name)
            await teamstat.reply(embed=embed)
        scores = {}
        defaultscore = float(0)
        for player in players:
             scores.update({f"{player.id}":defaultscore})
        sort = sorted( scores.items(), key=lambda key_value:key_value[1], reverse=True)
        scores = collections.OrderedDict(sort)
        text = '\n'.join([f"<@{k}> `🎈` **{v}** points"for k,v in  scores.items()])
        embed=discord.Embed(title="8 Corners Hunger Game", description=f"""You have to complete certain tasks to earn a point in the leaderboards. \nIf <a:Bomb:855685941484847125> is in the message means you will get hurt (lose points) if you follow the task.\nYou have 1 minute to answer each normal task.\nFirst person to get 25 points wins.\n{text}""", color=discord.Color.magenta())
        hunger = await ctx.send(embed=embed)
        def scoreedit(scores, id, difference:float):
            scores.update({f"{id}":float( scores[f"{id}"])+difference})
            sort = sorted(scores.items(), key=lambda key_value:key_value[1], reverse=True)
            scores = collections.OrderedDict(sort)
        tasks = [
                "What is sodium's chemical name?",
                "What is `Lqilqlwb` decrypted into plain text.\n||Ceaser cipher - 3||",
                "In a certain code language, ‘123’ means ‘bright little boy’, ‘145’ means ‘tall big boy’ and ‘637’ means ‘beautiful little flower’. Which digit in that language means ‘bright’?",
                "In a certain language ‘go for morning walk’ is written as ‘$*?#’,  ‘good for health’ is written as ‘£?@’ and ‘good to walk fast’ is written as ‘+@↑#’, then what is the code for ‘health’ in that code language?",
                ]
        answers = [
                "Na",
                "Infinity",
                "2",
                "£",
                ]
        inactive = 0
        while float(list( scores.values())[0]) < float(25) or inactive > 20:
            sort = sorted( scores.items(), key=lambda key_value:key_value[1], reverse=True)
            scores = collections.OrderedDict(sort)
            text = '\n'.join([f"<@{k}> `🎈` **{v}** points"for k,v in  scores.items()])
            rand = random.randint(0,len(tasks)-1)
            embed=discord.Embed(title="Hunger Games", description=f"{tasks[rand]} {'||<a:Bomb:855685941484847125>||' if random.randint(1,10) < 3 else ''}", color=discord.Color.purple())
            embed.add_field(name="Scoreboard", value=text, inline=False)
            g_round = await hunger.reply(embed=embed)
            def check(m):
                return f"{m.author.id}" in  scores.keys() and answers[rand].lower() in m.content.lower().split(' ')[0] and m.channel.id == ctx.channel.id
            try:
                if 'bomb' in embed.description.lower():t = 20
                else:t = 60
                res = await self.bot.wait_for("message", check=check, timeout=t)
            except asyncio.TimeoutError:
                if 'bomb' in embed.description:
                   await g_round.reply("No one got bombed.")
                   inactive += 1
            else:
                point = random.randint(1,3)
                if 'bomb' in embed.description.lower():
                    await res.reply(f"{res.author.mention} got bombed and lost **{point}** point(s).")
                    scoreedit(scores, res.author.id, point*-1)
                else:
                    await res.reply(f"{res.author.mention} got the correct answer and earned **{point}** point(s).")
                    scoreedit(scores, res.author.id, point)
        sort = sorted( scores.items(), key=lambda key_value:key_value[1], reverse=True)
        scores = collections.OrderedDict(sort)
        try:    winner1 = ctx.guild.get_member(int(list(scores.keys())[0]))
        except: winner1 = None
        try:    winner2 = ctx.guild.get_member(int(list(scores.keys())[1]))
        except: winner2 = None
        try:    winner3 = await ctx.guild.get_member(int(list( scores.keys())[2]))
        except: winner3 = None
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://i.imgur.com/iJ4XpZb.png") as img:
                bg = Image.open(io.BytesIO(await img.read()))
            if winner1 is not None:
                async with cs.get(f"{winner1.avatar_as(static_format='png', size= 512)}") as img:
                    offset = (1825, 1625)
                    ava1 = Image.open(io.BytesIO(await img.read()))
                    img = ava1.resize((512, 512), Image.ANTIALIAS)
                    bg.paste(img, offset)
            if winner2 is not None:
                async with cs.get(f"{winner2.avatar_as(static_format='png', size=1024)}") as img:
                    offset = (1150, 1790)
                    ava2 = Image.open(io.BytesIO(await img.read()))
                    img = ava2.resize((512, 512), Image.ANTIALIAS)
                    bg.paste(img, offset)
            if winner3 is not None:
                async with cs.get(f"{winner3.avatar_as(static_format='png', size=1024)}") as img:
                    offset = (2400, 1790)
                    ava3 = Image.open(io.BytesIO(await img.read()))
                    img = ava3.resize((512, 512), Image.ANTIALIAS)
                    bg.paste(img, offset)
        byte_io = io.BytesIO()
        bg.save(byte_io, 'PNG')
        byte_io.seek(0)
        f = discord.File(fp=byte_io, filename="image.png")
        embed = discord.Embed(title="8 Corners Game", description=f"Game Ended", colour=discord.Colour.red())
        winningtxt = '\n'.join([f"<@{k}> ~ **{v}** points"for k,v in  scores.items()])
        embed.add_field(name="Winners", value=winningtxt, inline=False)
        embed.set_footer(text="Credits: Mixel, Rh, A Typical Beggar")
        embed.set_image(url="attachment://image.png")
        embed.timestamp=discord.utils.utcnow()
        await ctx.reply(file=f, embed=embed)
        await cs.close()

    @commands.command(name='8cornersguide', aliases=['8cg'], hidden=True)
    @commands.cooldown(1,3,commands.BucketType.channel)
    async def eightcg(self, ctx):
        """Guide for the 8 corners game."""
        embed=discord.Embed(title="8 Corners Game Guide", description=f"Info about the 8 corners game.", color=discord.Color.random())
        embed.add_field(name="Introduction", value=f"The idea originally came from [Link](https://youtu.be/SEmKz665hnY) because <@703135131459911740> is unoriginal as you guys can tell. But the challenges that you will face to either revive yourself, or get spared when your corner is chosen, will be harder than those in the video.")
        embed.add_field(name="Before Game", value=f"React to the emoji to enter the game.", inline=False)
        embed.add_field(name="Colour selection", value="At the start of each round, all players who are alive are able to choose a corner. While users that are eliminated or dead will not be allowed to select.\nIf a player is afk and does not select a corner, they will be out.", inline=False)
        embed.add_field(name="Gameplay", value="When the round starts, there will be a wheel of fate that spins all the colours. Whatever colour it lands on, all users that picked that colour is eliminated. After that, the colour cannot be chosen anymore.\nIf your colour is chosen, there will be a redemption round among the people in the corner unless there is less than 3 people.", inline=False)
        embed.add_field(name="Redemption round", value="When the redemption round starts, the bot will randomly select a mini game. It ranges from a ban battle, to the fastest reaction time, deciphering codes and even doing nothing and just seeing your luck as a wheel of redemption gets spun and the player it lands on, gets revived.", inline=False)
        embed.timestamp=discord.utils.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='ttt', aliases=['tictactoe'])
    @commands.cooldown(1,10)
    async def ttt(self, ctx):
        """Starts a game of tic-tac-toe."""
        await ctx.reply(f'TicTacToe', view=TicTacToe())

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

    @commands.command(name="coinflip", aliases=["flip", 'cf'])
    @commands.cooldown(1,10)
    async def coinflip(self, ctx):
        """Flips a coin ... Maybe giving you bonus if you guess the right face. Guess will be randomised if you didn't provide one so..."""
        embed=discord.Embed(title="Coinflip", description="Flips a coin.", color=discord.Color.orange())
        v = CoinFlip()
        v.msg =  await ctx.reply("Choose a side.", embed=embed, view=v)
        await v.wait()
        for vd in v.children:
            vd.disabled = True
        heads = "https://media.discordapp.net/attachments/838703506743099422/862199206314770432/Untitled6_20210707131105.png"
        tails = "https://media.discordapp.net/attachments/838703506743099422/862215258218954832/Infinity_coin_head2_20210707140756.png"
        correct = random.choice([True, False])
        embed.description=f"Flips a coin. {ctx.author.mention}'s guess ➡"
        if v.value is True:
            embed.set_thumbnail(url=f"{heads}")
        elif v.value is False:
            embed.set_thumbnail(url=f"{tails}")
        elif v.value is None:
            return

        if correct is True:
            embed.set_image(url=heads)
        else:
            embed.set_image(url=tails)
        if v.value == correct:
            embed.color = discord.Color.green()
            embed.set_footer(text="Correct Guess")
        else:
            embed.color = discord.Color.red()
            embed.set_footer(text="Wrong Guess")

        await v.msg.edit(embed=embed, view=v)
    
    @commands.command(name='messagemania', aliases=['mms'])
    @commands.has_permissions(manage_messages=True)
    async def messagemania(self, ctx, seconds:int=None):
        """Message Mania Minigame."""
        timer = '<a:timer:890234490100793404>'
        if ctx.channel.id in self.ongoing_mm_games.keys():
            await ctx.reply(f"There is an ongoing game in this channel.")
            return
        if not seconds:
            seconds = 390
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages=True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        message = await ctx.send(embed=discord.Embed(description=f"<a:verified:876075132114829342> {ctx.channel.mention} Unlocked\nChannel will be locked soon.\n\n__Commands:__\n`mmp`: Purges 10 messages from the channel.\n`mmu`: Purges messages from a random user.\n`mmm`: Mutes a user from talking for 30 seconds.", colour=discord.Color.green()))
        self.ongoing_mm_games[ctx.channel.id] = message.created_at
        timestamp = round(message.created_at.replace(tzinfo=datetime.timezone.utc).timestamp())
        await message.edit(embed=discord.Embed(description=f"<a:verified:876075132114829342> {ctx.channel.mention} Unlocked\nChannel will be locked at <t:{timestamp+seconds}:T> <t:{timestamp+seconds}:R>.\n\n__Commands:__\n`mmp`: Purges 10 messages from the channel.\n`mmu`: Purges messages from a random user.\n`mmm`: Mutes a user from talking for 30 seconds.", colour=discord.Color.green()))
        await asyncio.sleep(seconds)
        overwrite.send_messages=False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=discord.Embed(description=f"<a:verified:876075132114829342> {ctx.channel.mention} Locked", colour=discord.Color.red()))
        messages = await ctx.channel.history(limit=None, after=message.created_at).flatten()
        messages = [x.author.id for x in messages if x.author.bot is False]
        counter=collections.Counter(messages)
        winners = '\n'.join(f"<medal here>  <@{x[0]}>: {x[1]} messages" for x in counter.most_common(5))
        winners = winners.replace('<medal here>', '🥇', 1).replace('<medal here>', '🥈', 1).replace('<medal here>', '🥉', 1).replace('<medal here>', '🏅', 1).replace('<medal here>', '🏅', 1)
        embed = discord.Embed(title="Message Mania", description=f"**__Winners__**\n{winners}", color=discord.Color.gold()).set_thumbnail(url="https://media.discordapp.net/attachments/841654825456107533/890903767845834762/MM.png")
        try:
            await ctx.reply(embed=embed)
        except:
            await ctx.send(embed=embed)
        del self.ongoing_mm_games[ctx.channel.id]

    @commands.command(name='mmp', hidden=True)
    @commands.cooldown(1,60, commands.BucketType.user)
    async def messagemaniammp(self, ctx):
        if ctx.channel.id not in self.ongoing_mm_games.keys():
            return
        def pinc(msg):
            if msg.pinned or msg.id == ctx.message.id or msg.author.bot is True:
                return False
            else:
                return True
        try:    
            await ctx.channel.purge(limit=10, check=pinc, after=self.ongoing_mm_games[ctx.channel.id])
            await ctx.message.add_reaction('<a:verified:876075132114829342>')
        except:
            pass

    @commands.command(name='mmu', hidden=True)
    @commands.cooldown(1,180, commands.BucketType.channel)
    async def messagemaniammu(self, ctx):
        if ctx.channel.id not in self.ongoing_mm_games.keys():
            return

        messages = await ctx.channel.history(after=self.ongoing_mm_games[ctx.channel.id]).flatten()
        user = random.choice([set([x.author.id for x in messages if x.author.bot is not True])])

        def pinc(msg):
            if msg.pinned or msg.id == ctx.message.id or msg.author.id != next(iter(user)):
                return False
            else:
                return True
        try:
            await ctx.channel.purge(limit=100, check=pinc, after=self.ongoing_mm_games[ctx.channel.id])
            await ctx.message.add_reaction('<a:verified:876075132114829342>')
        except:
            pass

    @commands.command(name='mmm', hidden=True)
    @commands.cooldown(1,120, commands.BucketType.channel)
    async def messagemaniammm(self, ctx):
        if ctx.channel.id not in self.ongoing_mm_games.keys():
            return
        try:
            messages = await ctx.channel.history(after=self.ongoing_mm_games[ctx.channel.id]).flatten()
            user = random.choice([set([x.author for x in messages if x.author.bot is not True])])
            await ctx.channel.set_permissions(next(iter(user)), send_messages=False)
            await ctx.send(f"{next(iter(user)).mention} muted for 30s.")
            await asyncio.sleep(30)
            await ctx.channel.set_permissions(user.pop(), overwrite=None)
            await ctx.message.add_reaction('<a:verified:876075132114829342>')
        except:
            pass

def setup(bot):
    bot.add_cog(FunCog(bot))