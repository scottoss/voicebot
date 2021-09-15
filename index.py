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
    'noplaylist': False,
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
    #async def play(self, ctx, *, url):
    async def play(self, ctx):
        """Plays from a url (almost anything youtube_dl supports)"""

        #async with ctx.typing():
        #    player = await YTDLSource.from_url(url, loop=self.bot.loop)
        #    ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        #await ctx.send(f'Now playing: {player.title}')
        await ctx.send(f'Sorry this music feature is temporary disabled')
        

    @commands.command()
    async def compufm(self, ctx):
        """Plays CompuFm"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("http://yayponies.no:8000/listen.ogg"))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send("now playing: **CompuFm**")
        await ctx.send("**The Greatest Music on the Internet!**")
        
        
    @commands.command()
    async def radionl(self, ctx):
        """Plays RadioNL"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("https://stream.radionl.fm/radionl"))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send("now playing: **RadioNL**")
        await ctx.send("**beste nederlandse hits!**")
        



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
        
        
        

    @compufm.before_invoke
    @radionl.before_invoke
    @tts.before_invoke
    @play.before_invoke
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
activity2 = discord.Activity(type=discord.ActivityType.listening, name="r! help")
activity3 = discord.Activity(type=discord.ActivityType.listening, name="pp help")
activity4 = discord.Activity(type=discord.ActivityType.listening, name="aj help")
activity5 = discord.Activity(type=discord.ActivityType.listening, name="fs help")
activity6 = discord.Activity(type=discord.ActivityType.listening, name="t! help")
activity7 = discord.Activity(type=discord.ActivityType.listening, name="dh help")




bot1 = commands.Bot(command_prefix='rd ', description='i am 20% cooler', activity=activity1, status=discord.Status.online)
bot2 = commands.Bot(command_prefix='r! ', description = 'i am making dresses darling', activity=activity2, status=discord.Status.online)
bot3 = commands.Bot(command_prefix='pp ', description = 'i am planning a party just for you', activity=activity3, status=discord.Status.online)
bot4 = commands.Bot(command_prefix='aj ', description = 'yeehah', activity=activity4, status=discord.Status.online)
bot5 = commands.Bot(command_prefix='fs ', description = 'hi there', activity=activity5, status=discord.Status.online)
bot6 = commands.Bot(command_prefix='t! ', description = 'i am reading a book', activity=activity6, status=discord.Status.online)
bot7 = commands.Bot(command_prefix='dh ', description = 'derp', activity=activity7, status=discord.Status.online)


bot1.add_cog(Music(bot1))
bot2.add_cog(Music(bot2))
bot3.add_cog(Music(bot3))
bot4.add_cog(Music(bot4))
bot5.add_cog(Music(bot5))
bot6.add_cog(Music(bot6))
bot7.add_cog(Music(bot7))


loop = asyncio.get_event_loop()
loop.create_task(bot1.start(os.environ['TOKEN']))
loop.create_task(bot2.start(os.environ['TOKEN2']))
loop.create_task(bot3.start(os.environ['TOKEN3']))
loop.create_task(bot4.start(os.environ['TOKEN4']))
loop.create_task(bot5.start(os.environ['TOKEN5']))
loop.create_task(bot6.start(os.environ['TOKEN6']))
loop.create_task(bot7.start(os.environ['TOKEN7']))
loop.run_forever()

