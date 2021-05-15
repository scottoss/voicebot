import discord
from discord.ext import commands
import datetime
import time
import asyncio
import os

import httplib2
from urllib.parse import urlencode, quote # For URL creation
from urllib import parse, request
import re
mary_host = "84.27.169.137"
mary_port = "6754"
bot = commands.Bot(command_prefix=os.environ['PREFIX'], description="This is a Helper Bot")


@bot.command()
async def volume(self, ctx, volume: int):
         """Changes the player's volume"""

         if ctx.voice_client is None:
             return await ctx.send("Not connected to a voice channel.")

         ctx.voice_client.source.volume = volume / 100
         await ctx.send(f"Changed volume to {volume}%")

                  
@bot.command()
async def radio(ctx):
         """Plays a file from the local filesystem"""

         source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(os.environ['RADIO_LINK']))
         ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

         await ctx.send(f'Now playing: Derpystown-radio')
         await ctx.send('to stop it u need to dissconnect the bot from the vc yourself')


         


@bot.command(pass_context=True)
async def darkpony(ctx):
         """fuck with dark"""
         voice = await ctx.author.voice.channel.connect()

         voice.play(discord.FFmpegPCMAudio('dark.wav'))
         while voice.is_playing():
             await asyncio.sleep(.1)
         await voice.disconnect()
         
@bot.command(pass_context=True)
async def sfx1(ctx):
         """play sfx1"""
         voice = await ctx.author.voice.channel.connect()

         voice.play(discord.FFmpegPCMAudio(os.environ['SFX1']))
         while voice.is_playing():
             await asyncio.sleep(.1)
         await voice.disconnect()
         
         
@bot.command(pass_context=True)
async def sfx2(ctx):
         """play sfx2"""
         voice = await ctx.author.voice.channel.connect()

         voice.play(discord.FFmpegPCMAudio(os.environ['SFX2']))
         while voice.is_playing():
             await asyncio.sleep(.1)
         await voice.disconnect()
         
         
        
@bot.command(pass_context=True)
async def sfx3(ctx):
         """play sfx3"""
         voice = await ctx.author.voice.channel.connect()

         voice.play(discord.FFmpegPCMAudio(os.environ['SFX3']))
         while voice.is_playing():
             await asyncio.sleep(.1)
         await voice.disconnect()
         
         
@bot.command(pass_context=True)
async def sfx4(ctx):
         """play sfx4"""
         voice = await ctx.author.voice.channel.connect()

         voice.play(discord.FFmpegPCMAudio(os.environ['SFX4']))
         while voice.is_playing():
             await asyncio.sleep(.1)
         await voice.disconnect()

         
         
         
@bot.command(pass_context=True)
async def ping(ctx):
         """check if i am still alive"""
         await ctx.send('i am still alive')
         
         
@bot.command(pass_context=True)
async def rick(ctx):
         """get rickrolled"""
         voice = await ctx.author.voice.channel.connect()

         voice.play(discord.FFmpegPCMAudio('rick.mp3'))
         while voice.is_playing():
             await asyncio.sleep(.1)
         await voice.disconnect()
         
         

@bot.command(pass_context=True)
async def tts(ctx, *, text: str):
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
        
         voice = await ctx.author.voice.channel.connect()

 
         voice.play(discord.FFmpegPCMAudio('output_wav.wav'))
         while voice.is_playing():
             await asyncio.sleep(.1)
         await voice.disconnect()





 

# Events
@bot.event
async def on_ready():
    print('My Body is Ready')

bot.run(os.environ['TOKEN'])
