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


@bot.command(pass_context=True)
async def radio(ctx):
         voice = await ctx.author.voice.channel.connect()

         voice.play(discord.FFmpegPCMAudio(os.environ['RADIO_LINK']))
         await ctx.send('playing the radio now, to stop it u need to dissconnect the bot from the vc yourself')





@bot.command(pass_context=True)
async def heartbeat(ctx):
         await ctx.send('i am still alive')
         
@bot.command(pass_context=True)
async def ping(ctx):
         await ctx.send('i am still alive')
         
         
@bot.command(pass_context=True)
async def rick(ctx):
         voice = await ctx.author.voice.channel.connect()

         voice.play(discord.FFmpegPCMAudio('rick.mp3'))
         while voice.is_playing():
             await asyncio.sleep(.1)
         await voice.disconnect()
         
         

@bot.command(pass_context=True)
async def tts(ctx, *, text: str):
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




@bot.listen()
async def on_message(message):
    if "tts help" in message.content.lower():
        # in this case don't respond with the word "Tutorial" or you will call the on_message event recursively
        await message.channel.send('its easy just use: >tts <your text here>')
        await bot.process_commands(message)
 

# Events
@bot.event
async def on_ready():
    print('My Body is Ready')

bot.run(os.environ['TOKEN'])
