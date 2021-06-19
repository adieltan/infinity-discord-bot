import discord, random, string, os, logging, asyncio, discord.voice_client, sys, math, datetime, aiohttp
from discord.ext import commands


class MusicCog(commands.Cog, name='Music'):
    """*Music Commands*"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['lyrc']) # adding a aliase to the command so we can use !lyrc or !lyrics
    async def lyrics(ctx, *, search=None):
        """A command to find lyrics easily!"""
        
        if not search: # if user hasnt typed anything, throw a error
            embed = discord.Embed(title="No search argument!", description="You havent entered anything, so i couldnt find lyrics!")
            await ctx.reply(embed=embed)
            
            # ctx.reply is available only on discord.py 1.6.0!
            
        song = search.replace(' ', '%20') # replace spaces with "%20"
        
        async with aiohttp.ClientSession() as lyricsSession: # define session
            async with lyricsSession.get(f'https://some-random-api.ml/lyrics?title={song}') as jsondata: # define json data
                if not (300 > jsondata.status >= 200):
                    await ctx.send(f'Recieved Poor Status code of {jsondata.status}.')
                else:
                    lyricsData = await jsondata.json() # load json data
            songLyrics = lyricsData['lyrics'] # the lyrics
            songArtist = lyricsData['author'] # the authors name
            songTitle = lyricsData['title'] # the songs title
            
            try:
                for chunk in [songLyrics[i:i+2000] for i in range(0, len(songLyrics), 2000)]: # if the lyrics extend the discord character limit (2000): split the embed
                    embed = discord.Embed(title=f'{songTitle} by {songArtist}', description=chunk, color=discord.Color.blurple())
                    embed.timestamp = datetime.utcnow()
                    
                    await lyricsSession.close() # closing the session
                    
                    await ctx.reply(embed=embed)
                    
            except discord.HTTPException:
                embed = discord.Embed(title=f'{songTitle} by {songArtist}', description=chunk, color=discord.Color.blurple())
                embed.timestamp = datetime.utcnow()
                
                await lyricsSession.close() # closing the session
                
                await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(MusicCog(bot))