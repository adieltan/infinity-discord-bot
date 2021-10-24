import discord, random, string, os, asyncio, sys, math, requests, json, datetime, psutil, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks

from thefuzz import process
import collections
from PIL import Image
import time

class FunCog(commands.Cog, name='Fun'):
    """🥳 Fun / minigame commands."""
    def __init__(self, bot):
        self.bot = bot
        self.ongoing_mm_games = dict()
    
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

        emoji = discord.PartialEmoji(name='Join', animated=True, id=855683444310147113)
        bomb = discord.PartialEmoji(name='Bomb', animated=True, id=855685941484847125)

        embed = discord.Embed(title="8 Corners Game",
                              description=f"React to the message to join.\nTimer: 5 minutes\n`=8cg` to learn more about the game.",
                              color=discord.Color.random())
        embed.timestamp = discord.utils.utcnow()
        players = []
        alive = []
        dead = []
        info = await ctx.reply(embed=embed, mention_author=False, components=[[Button(emoji=emoji, style=ButtonStyle.green, id="join"), Button(emoji=bomb, style=ButtonStyle.red, id="skip")]])

        timeout = 5 * 60
        timeout_start = time.time()

        def check(reaction, user):
            if reaction.message.id != info.id:
                return False
            if user.bot is True:
                return False
            return True

        # joining reaction check
        while time.time() < timeout_start + timeout:
            try:
                interaction = await self.bot.wait_for("button_click", check=lambda i:i.component.id in ['join', 'skip'], timeout=5)
                if interaction.component.id == 'join' and interaction.user not in players:
                    players.append(interaction.user)
                    await interaction.respond(ephemeral=True, embed=discord.Embed(title="Game join confirmation",description=f"You have joined the game. [Message]({info.jump_url})",color=discord.Color.random()))
                elif interaction.component.id == 'skip' and interaction.user == ctx.author:break
            except:
                timeleft = (timeout_start + timeout) - time.time()
                embed.description = f"React to the button on the message to join.\nTimer: {round(timeleft)} seconds.\nPlayer count: {len(players)} players.\n`=8cg` to learn more about the game."
                await info.edit(embed=embed, mention_author=False)
        embed.description = f"Timer: Ended.\nPlayer count: {len(players)} players.\n`=8cg` to learn more about the game."
        await info.edit(embed=embed, components=[])

        if len(players) <= 1:
            await ctx.reply("Sadly, no enough players joined.")
            return
        while len(players) > math.floor(len(players)/3):
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
    async def coinflip(self, ctx):
        """Flips a coin ... Maybe giving you bonus if you guess the right face. Guess will be randomised if you didn't provide one so..."""
        embed=discord.Embed(title="Coinflip", description="Flips a coin.", color=discord.Color.orange())
        choose = await ctx.reply("Choose a side.", embed=embed, components=[Select(placeholder="Select coin side.", options=[SelectOption(label="heads", value="Heads"), SelectOption(label="tails", value="Tails")])])

        try:
            interaction = await self.bot.wait_for("select_option", check = lambda i: i.component[0].label in ["heads","tails"], timeout=30)
            guess = interaction.component[0].label
        except:
            await ctx.reply("You didn't respond in time.")
            await choose.edit(components=[])
            return
        face = ['heads', 'tails']
        heads = "https://media.discordapp.net/attachments/838703506743099422/862199206314770432/Untitled6_20210707131105.png?width=652&height=652"
        tails = "https://media.discordapp.net/attachments/838703506743099422/862215258218954832/Infinity_coin_head2_20210707140756.png?width=652&height=652"
        embed.description=f"Flips a coin. {ctx.author.mention}'s guess ➡"
        if guess == "heads":
            embed.set_thumbnail(url=f"{heads}")
        elif guess == "tails":
            embed.set_thumbnail(url=f"{tails}")
        await choose.edit(embed=embed, components=[])
        
        correct = random.choice(face)
        if correct == "heads":embed.set_image(url=f"{heads}")
        else:embed.set_image(url=f"{tails}")
        if guess == correct:
            embed.color = discord.Color.green()
            embed.set_footer(text="Correct Guess")
        else:
            embed.color = discord.Color.red()
            embed.set_footer(text="Wrong Guess")

        await choose.reply(f"{ctx.author.mention}",embed=embed)
    
    @commands.command(name='messagemania', aliases=['mm'])
    @commands.has_permissions(manage_messages=True)
    async def messagemania(self, ctx, seconds:int=None):
        """Message Mania Minigame."""
        timer = '<a:timer:890234490100793404>'
        if ctx.channel.id in self.ongoing_mm_games.keys():
            await ctx.reply(f"There is an ongoing game in this channel.")
            return
        if seconds is None:
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
        embed = discord.Embed(title="Message Mania", description=f"**__Winners__**\n{winners}", color=discord.Color.gold()).set_thumbnail(url="https://images-ext-1.discordapp.net/external/LMTQPkVKqF0jESGgD5djPe1ROAUCybuofm-ismCdBUs/https/media.discordapp.net/attachments/841654825456107533/890903767845834762/MM.png")
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