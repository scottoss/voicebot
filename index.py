import discord
from discord.ext import commands
import datetime
import time
import asyncio

import httplib2
from urllib.parse import urlencode, quote # For URL creation
from urllib import parse, request
import re
mary_host = "84.27.169.137"
mary_port = "6754"
bot = commands.Bot(command_prefix='>', description="This is a Helper Bot")


@bot.command(pass_context=True)
async def join(ctx):
         voice = await ctx.author.voice.channel.connect()

@bot.command(pass_context=True)
async def tts(ctx, *, text: str):
         input_text = "{}".format(text)
        
         query_hash = {"INPUT_TEXT":input_text,
                       "INPUT_TYPE":"TEXT", # Input text
                       "LOCALE":"en_US",
                       "VOICE":"dfki-spike-hsmm", # Voice informations  (need to be compatible)
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
    print('My Ready is Body')

bot.run('NzAxODUzODE2MTQzNzQxMDI5.Xp3iTQ.zPu0vaCDaAXicbv-GjQTqrgn5BE')
