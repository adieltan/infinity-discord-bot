import discord, random, string, os, asyncio, sys, math, requests, json, pymongo, datetime, psutil, dns, io, PIL, re, aiohttp, typing
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle
import matplotlib.pyplot as plt
 


class FunCog(commands.Cog, name='Fun'):
    """*Fun commands.*"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name= 'roll', aliases=['dice', 'throw'])
    @commands.cooldown(1,5)
    async def roll(self, ctx, number_of_dice:int, number_of_sides:int):
        """Randomly rolls dices. [number_of_dice] cannot be higher than 25."""
        if number_of_dice > 25: 
            await ctx.send(f"*number_of_dice* cannot be over 25.\nYour input: **{number_of_dice}**")
            return
        
        embed = discord.Embed(title=f"{ctx.author}'s Rolling Game", color=discord.Color.random())
        embed.set_author(icon_url=ctx.author.avatar_url, name=str(ctx.author))
        embed.timestamp=datetime.datetime.utcnow()
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
                embed.timestamp=datetime.datetime.utcnow()
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author)
                text= "\n".join([f'{winner.mention} `{winner.id}`' for winner in winners])
                embed.add_field(name="Winners", value=text)
                embed.set_footer(text=f"{numbers} winners")
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="8ball", aliases=['eightball', '8b'])
    @commands.cooldown(1,5)
    async def ball(self, ctx, *, mess):
        """Ask 8ball about your life."""
        if "suicide" in mess.lower():
            await ctx.reply("NO SUICIDE.")
            return
        
        fac = requests.get(url="https://api.monkedev.com/fun/8ball", params={'key':str(os.getenv("monkedevapi"))})
        fact = fac.json()["answer"]
        embed=discord.Embed(title="8ball", description=mess, color=discord.Color.random())
        embed.add_field(name="Conclusion", value=fact)
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_footer(text="MonkeDev Api")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="哥哥", aliases=['geigei'])
    async def gege(self, ctx):
        await ctx.reply("我只会心疼哥哥\nhttps://cdn.discordapp.com/attachments/717962272093372556/861518164160151582/video-1625470606.mp4")

    @commands.command(name="english")
    async def canuspeakenglish(self,ctx):
        await ctx.reply("Can you speak english?\nhttps://cdn.discordapp.com/attachments/779326170612367390/863212817360748594/video0-13.mp4")

def setup(bot):
    bot.add_cog(FunCog(bot))