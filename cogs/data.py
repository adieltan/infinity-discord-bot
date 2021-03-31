from brawlstats.errors import NotFoundError
import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime, requests, brawlstats
from discord.ext import commands

bstoken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjZjYzI5MmVkLWUyNzUtNDhhMi05MTgyLWNkNmUzYjg2MGI1ZCIsImlhdCI6MTYxNzA2MTEyOCwic3ViIjoiZGV2ZWxvcGVyLzIxNTMyYmY2LTk4MjgtYzI4My1iZmNjLWI1MDZiYjJkNGI2NiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTQuMTkyLjIwOS4xMTYiLCIwLjAuMC4wIl0sInR5cGUiOiJjbGllbnQifV19.t6Nfks_5xyfFdWfV9tRdOGs_lEInh_FbaXoZL0PkfM6xi3GY8AWStDWw_6_71UfvnwOhVAa2pn3iajq0hYhzQQ"

class DataCog(commands.Cog, name='Data'):
    """*Data from websites or api*"""
    def __init__(self, bot):
        self.bot = bot
        self.client = brawlstats.Client(token=bstoken, is_async=True)
        
    @commands.command(name="bsplayer", aliases=['brawlstarsplayer', 'bsp'])
    @commands.cooldown(1,5)
    async def bsplayer(self, ctx, playertag:str=None):
        """Shows info about the Brawl Stars player"""
        if playertag is None:
            await ctx.reply(f"PlayerTag valid charactors: `0289PYLQGRJCUV`")
            return
        try:
            player = self.client.get_player(playertag, use_cache=True)
        except Exception as e:
            await ctx.reply(e)
            return
        embed=discord.Embed(title="Brawl Stars Player Info", description=f"Name: **{player.name}** \nTag: *{player.tag}*\nTrophies: *{player.trophies}* \nExp: *{player.expPoints}* points / Level *{player.expLevel}*", color=int(player.name_color.replace("ff","",1)[2:], base=16))
        club = player.get_club()
        embed.add_field(name="Club", value=f"Name: {club.name}\nTag: {club.tag}\nDescription: {club.description}\nType: {club.type}\nTrophies: {club.trophies}\nRequired Trophies: {club.required_trohpies}\nMember Count: {len(club.members)}")
        embed.add_field(name="Stats", value=f"Highest Trophies: {player.highest_trophies}\nPower Play Points: {player.power_play_points} / {player.highest_power_play_points} (Highest)\nTeam victories: {player.team_victories}\nSolo victories: {player.solo_victories}\nDuo victories: {player.duo_victories}", inline=False)
        top_brawler = player.brawlers.sort(key=player.brawler.trophies, reverse=True)[0]
        embed.add_field(name="Brawler", value=f"Number of brawlers: {len(player.brawlers)}\nTop Brawler: {top_brawler.name} ({top_brawler.trophies} trophies)")
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_footer(text="Brawl Stars Api")
        await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(DataCog(bot))