import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp
from discord.ext.commands.core import group
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import matplotlib.pyplot as plt
 
from PIL import Image, ImageDraw, ImageFont
import time, collections

class MiniGamesCog(commands.Cog, name='MiniGames'):
    """*Minigames.*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8corners", aliases=['8c', 'corner', 'corners'])
    @commands.cooldown(1, 10, commands.BucketType.category)
    async def corners(self, ctx):
        """8 corners Game."""
        await ctx.trigger_typing()
        self.teams = []

        class team:
            def __init__(tself, name, emoji, status: bool = True):
                tself.name = name
                tself.emoji = self.bot.get_emoji(emoji)
                tself.status = status
                tself.members = []
                self.teamsteams.append(tself)
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

        emoji = discord.PartialEmoji(name='Join', animated=True, id=855683444310147113)
        bomb = discord.PartialEmoji(name='Bomb', animated=True, id=855685941484847125)

        embed = discord.Embed(title="8 Corners Game",
                              description=f"React to the message to join.\nTimer: 5 minutes\n`=8cg` to learn more about the game.",
                              color=discord.Color.random())
        embed.timestamp = datetime.datetime.utcnow()
        players = []
        alive = []
        dead = []
        info = await ctx.reply(embed=embed, mention_author=False)

        timeout = 5 * 60
        timeout_start = time.time()

        def check(reaction, user):
            if reaction.message.id != info.id:
                return False
            if user.bot is True:
                return False
            return True

        await info.add_reaction(emoji)
        await info.add_reaction(bomb)
        # joining reaction check
        while time.time() < timeout_start + timeout:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=5)
                if reaction.emoji.name == emoji.name and user not in players:
                    players.append(user)
                    try:
                        await user.send(embed=discord.Embed(title="Game join confirmation",
                                                            description=f"You have joined the game. [Message]({info.jump_url})",
                                                            color=discord.Color.random()))
                    except:
                        await info.reply(f"{user.mention}, You have joined the game.")
                elif bomb == reaction.emoji and user == ctx.author:break
            except:
                timeleft = (timeout_start + timeout) - time.time()
                embed.description = f"React to the button on the message to join.\nTimer: {round(timeleft)} seconds.\nPlayer count: {len(players)} players.\n`=8cg` to learn more about the game."
                await info.edit(embed=embed, mention_author=False)
        await info.clear_reactions()
        embed.description = f"Timer: Ended.\nPlayer count: {len(players)} players.\n`=8cg` to learn more about the game."
        await info.edit(embed=embed)

        while len(players) > 10:
            chosen = []
            afk = []
            for team in self.teams:team.resetmembers()
            embed = discord.Embed(title="8 corners game",
                                  description=f"__**Statistics**__\n**Players count:** {len(players)}",
                                  colour=discord.Color.green())
            stats = await ctx.send(embed=embed)
            paged = [players[i:i + 80] for i in range(0, len(players), 80)]
            pageno = 0
            while pageno < len(paged):
                lis = [f'{m.mention}' for m in paged[pageno]]
                await ctx.send(f"**Players Page {pageno + 1}**\n" + ''.join(lis))
                pageno += 1
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
            cmes = await info.reply(embed=embed)
            for t in self.teams: await cmes.add_reaction(t.emoji)
            await cmes.add_reaction(bomb)
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
                    if bomb == reaction.emoji:
                        if ctx.author == user:
                            break
                    elif peop > rcount:
                        await cmes.remove_reaction(reaction.emoji, user)
                        await user.send("The team is full please chose another team/color.")
                        continue
                    elif user in chosen:
                        await cmes.remove_reaction(reaction.emoji, user)
                        await user.send("You have already selected a team/color.")
                        continue
                    elif reaction.emoji == rainbow.emoji:
                        await choose(rainbow, user)
                        continue
                    elif reaction.emoji == cyan.emoji:
                        await choose(cyan, user)
                        continue

                    elif reaction.emoji == purple.emoji:
                        if len(players) > 3:
                            await choose(purple, user)
                            continue
                    elif reaction.emoji == green.emoji:
                        if len(players) > 6:
                            await choose(green, user)
                            continue
                    elif reaction.emoji == yellow.emoji:
                        if len(players) > 9:
                            await choose(yellow, user)
                            continue
                    elif reaction.emoji == red.emoji:
                        if len(players) > 12:
                            await choose(red, user)
                            continue
                    elif reaction.emoji == pink.emoji:
                        if len(players) > 15:
                            await choose(pink, user)
                            continue
                    elif reaction.emoji == blue.emoji:
                        if len(players) > 18:
                            await choose(blue, user)
                            continue
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
        self.scores = {}
        defaultscore = float(0)
        for player in players:
            self.scores.update({f"{player.id}":defaultscore})
        sort = sorted(self.scores.items(), key=lambda key_value:key_value[1], reverse=True)
        self.scores = collections.OrderedDict(sort)
        text = '\n'.join([f"<@{k}> `🎈` **{v}** points"for k,v in self.scores.items()])
        embed=discord.Embed(title="8 Corners Hunger Game", description=f"""You have to complete certain tasks to earn a point in the leaderboards. \nIf <a:Bomb:855685941484847125> is in the message means you will get hurt (lose points) if you follow the task.\nYou have 1 minute to answer each task.\nFirst person to get 25 points wins.\n{text}""", color=discord.Color.magenta())
        hunger = await ctx.send(embed=embed)
        def scoreedit(id, difference:float):
            self.scores.update({f"{id}":float(self.scores[f"{id}"])+difference})
            sort = sorted(self.scores.items(), key=lambda key_value:key_value[1], reverse=True)
            self.scores = collections.OrderedDict(sort)
        tasks = [
                "What is sodium's chemical name?",
                "What is `Lqilqlwb` decrypted into plain text.\n||Ceaser cipher - 3||",
                ]
        answers = [
                "Na",
                "Infinity",
                ]
        while float(list(self.scores.values())[0]) < float(25):
            sort = sorted(self.scores.items(), key=lambda key_value:key_value[1], reverse=True)
            self.scores = collections.OrderedDict(sort)
            text = '\n'.join([f"<@{k}> `🎈` **{v}** points"for k,v in self.scores.items()])
            rand = random.randint(0,len(tasks)-1)
            embed=discord.Embed(title="Hunger Games", description=f"{tasks[rand]} {'||<a:Bomb:855685941484847125>||' if random.randint(1,10) < 3 else ''}", color=discord.Color.purple())
            embed.add_field(name="Scoreboard", value=text, inline=False)
            g_round = await hunger.reply(embed=embed)
            def check(m):
                return f"{m.author.id}" in self.scores.keys() and answers[rand].lower() in m.content.lower() and m.channel.id == ctx.channel.id
            try:
                res = await self.bot.wait_for("message", check=check, timeout=60)
            except asyncio.TimeoutError:
                if 'bomb' in embed.description:
                   await g_round.reply("No one got bombed.")
            else:
                point = random.randint(1,3)
                if 'bomb' in embed.description.lower():
                    await res.reply(f"{res.author.mention} got bombed and lost **{point}** point(s).")
                    scoreedit(res.author.id, point*-1)
                else:
                    await res.reply(f"{res.author.mention} got the correct answer and earned **{point}** point(s).")
                    scoreedit(res.author.id, point)
        sort = sorted(self.scores.items(), key=lambda key_value:key_value[1], reverse=True)
        self.scores = collections.OrderedDict(sort)
        try:    winner1 = ctx.guild.get_member(int(list(self.scores.keys())[0]))
        except: winner1 = None
        try:    winner2 = ctx.guild.get_member(int(list(self.scores.keys())[1]))
        except: winner2 = None
        try:    winner3 = await ctx.guild.get_member(int(list(self.scores.keys())[2]))
        except: winner3 = None
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://i.imgur.com/iJ4XpZb.png") as img:
                bg = Image.open(io.BytesIO(await img.read()))
            if winner1 is not None:
                async with cs.get(f"{winner1.avatar_url_as(static_format='png', size=1024)}") as img:
                    offset = (1300,1100)
                    ava1 = Image.open(io.BytesIO(await img.read()))
                    img = ava1.resize((1024, 1024), Image.ANTIALIAS)
                    bg.paste(img, offset)
            if winner2 is not None:
                async with cs.get(f"{winner2.avatar_url_as(static_format='png', size=1024)}") as img:
                    offset = (30,2160)
                    ava2 = Image.open(io.BytesIO(await img.read()))
                    img = ava2.resize((1024, 1024), Image.ANTIALIAS)
                    bg.paste(img, offset)
            if winner3 is not None:
                async with cs.get(f"{winner3.avatar_url_as(static_format='png', size=1024)}") as img:
                    offset = (3100,2360)
                    ava3 = Image.open(io.BytesIO(await img.read()))
                    img = ava3.resize((1024, 1024), Image.ANTIALIAS)
                    bg.paste(img, offset)
        #fnt = ImageFont.truetype(font="verdana.ttf", size=150)
        fnt = ImageFont.truetype( size=150)
        draw = ImageDraw.Draw(bg)
        try:
            draw.text((2400, 1100), '\n'.join([winner1.name[i:i+20] for i in range(0, len(winner1.name), 20)]), font=fnt, fill=(0,0,0))
            draw.text((30, 3300), '\n'.join([winner2.name[i:i+14] for i in range(0, len(winner2.name), 14)]), font=fnt, fill=(0,0,0))
            draw.text((3100, 3500), '\n'.join([winner3.name[i:i+12] for i in range(0, len(winner3.name), 12)]), font=fnt, fill=(0,0,0))
        except:
            pass
        byte_io = io.BytesIO()
        bg.save(byte_io, 'PNG')
        byte_io.seek(0)
        f = discord.File(fp=byte_io, filename="image.png")
        embed = discord.Embed(title="8 Corners Game", description=f"Game Ended", colour=discord.Colour.red())
        winningtxt = '\n'.join([f"<@{k}> ~ **{v}** points"for k,v in self.scores.items()])
        embed.add_field(name="Winners", value=winningtxt, inline=False)
        embed.set_footer(text="Credits: Mixel, Rh, A Typical Beggar")
        embed.set_image(url="attachment://image.png")
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(file=f, embed=embed)
        await cs.close()

        embed = discord.Embed(title="8 Corners Game", description=f"Game Ended", colour=discord.Colour.red())
        winningtxt = '\n'.join([f"<@{k}> ~ **{v}** points"for k,v in self.scores.items()])
        embed.add_field(name="Winners", value=winningtxt, inline=False)
        embed.set_footer(text="Credits: Mixel, Rh, A Typical Beggar")
        await ctx.reply(embed=embed)

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
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='ttt', aliases=['tictactoe'])
    @commands.cooldown(1,10)
    async def ttt(self, ctx, opponent:discord.Member):
        """Starts a game of tic-tac-toe."""
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

        def placed(value):
            if value in ['X', 'O']:
                return True
            else:
                return False

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

                components = [[Button(style=getButtonStyle(board[i+ia-1]),label=board[i+ia-1],disabled=placed(board[i+ia-1])) for ia in range(3)] for i in range(1,9,3)]

                if gameWon:
                    components = [[Button(style=getButtonStyle(board[i+ia-1]),label=board[i+ia-1],disabled=bool(gameWon)) for ia in range(3)] for i in range(1,9,3)]
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
    async def coinflip(self, ctx, amount:int, guess:str=None):
        """Flips a coin ... Maybe giving you bonus if you guess the right face. Guess will be randomised if you didn't provide one so..."""
        face = ["heads", "tails"]
        if guess == None:
            guess = random.choice(face)
        else: 
            guess = guess.lower()
            if guess[0] == "h":
                guess = "heads"
            elif guess[0] == "t":
                guess = "tails"
            else:
                guess = random.choice(face)
        correct = random.choice(face)
        embed = discord.Embed(title="CoinFlip Machine", description=f"{ctx.author.mention}'s guess = {guess}", color=16776960)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.set_image("https://cdn.dribbble.com/users/58530/screenshots/2323771/coin-flip.gif")
        message = await ctx.reply(embed=embed, mention_author=True)

        if guess == correct:
            embed = discord.Embed(title="CoinFlip Machine", description=f"{ctx.author.mention}", color=1900331)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            embed.timestamp=datetime.datetime.utcnow()
            message.edit(embed=embed)

        elif guess != correct:
            embed = discord.Embed(title="CoinFlip Machine", description=f"{ctx.author.mention}", color=16711680)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            embed.timestamp=datetime.datetime.utcnow()
            message.edit(embed=embed)

    
def setup(bot):
    bot.add_cog(MiniGamesCog(bot))