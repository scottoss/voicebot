import asyncio
import os
import discord
import youtube_dl
import httplib2
from urllib.parse import urlencode, quote # For URL creation
from urllib import parse, request
import re
mary_host = os.environ['MARY_HOST']
mary_port = os.environ['MARY_PORT']

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

   
        
    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')
        
        

    @commands.command()
    async def radio(self, ctx):
        """Plays the radio station"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('https://casting.sparklebot.nl/radio/8000/radio.mp3'))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: derpystown radio')


    @commands.command()
    async def darkpony(self, ctx):
        """fuck with darkpony"""
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('dark.wav'))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: fuck you dark')
 



    @commands.command()
    async def sfx1(self, ctx):
        """play sfx1"""
        url = os.environ['SFX1']
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        
        
        
    @commands.command()
    async def sfx2(self, ctx):
        """play sfx2"""
        url = os.environ['SFX2']
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        
        
        
        
    @commands.command()
    async def sfx3(self, ctx):
        """play sfx3"""
        url = os.environ['SFX3']
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        
        
    @commands.command()
    async def sfx4(self, ctx):
        """play sfx4"""
        url = os.environ['SFX4']
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)




    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
       

        await ctx.voice_client.disconnect()

        
    @commands.command(pass_context=True)
    async def tts(self, ctx, *, text: str):
         """text to speech api"""
         input_text = "{}".format(text)
        
         query_hash = {"INPUT_TEXT":input_text,
                       "INPUT_TYPE":"TEXT", # Input text
                       "LOCALE":"en_US",
                       "VOICE":os.environ['MAIN_VOICE'], # Voice informations  (need to be compatible)
                       "OUTPUT_TYPE":"AUDIO",
                       "AUDIO":"WAVE", # Audio informations (need both)
                       }
         query = urlencode(query_hash)
         print("query = \"http://%s:%s/process?%s\"" % (mary_host, mary_port, query))

         h_mary = httplib2.Http()
         resp, content = h_mary.request("http://%s:%s/process?" % (mary_host, mary_port), "POST", query)

         if (resp["content-type"] == "audio/x-wav"):

             # Write the wav file
             f = open("output_wav.wav", "wb")
             f.write(content)
             f.close()
            
         source = discord.FFmpegPCMAudio('output_wav.wav')
         ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
        
        
        
    @radio.before_invoke
    @tts.before_invoke
    @darkpony.before_invoke
    @sfx1.before_invoke
    @sfx2.before_invoke
    @sfx3.before_invoke
    @sfx4.before_invoke
    @yt.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

            
  
activity1 = discord.Activity(type=discord.ActivityType.listening, name="rd help")
activity2 = discord.Activity(type=discord.ActivityType.listening, name="!help")

bot1 = commands.Bot(command_prefix='rd ', description='this bot is made by DerpysTown#1416', activity=activity1, status=discord.Status.idle)
bot2 = commands.Bot(command_prefix='!', description = 'this bot is made by DerpysTown#1416', activity=activity2, status=discord.Status.idle)


bot1.add_cog(Music(bot1))
bot2.add_cog(Music(bot2))


loop = asyncio.get_event_loop()
loop.create_task(bot1.start(os.environ['TOKEN']))
loop.create_task(bot2.start(os.environ['TOKEN2']))
loop.run_forever()
