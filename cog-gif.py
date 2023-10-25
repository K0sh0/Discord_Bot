# Import modules for Discord Bot, Qbit, Random, Asyncio, JSON, Time, Regex, fnmatch, SQLite3, and other essential functionalities
import nextcord
from nextcord.ext import commands
import qbit
import random
import asyncio
import json
import time
import os
import re
import fnmatch
import sqlite3
from datetime import datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from nextcord.utils import get

class Gifs(commands.Cog):

    # Constructor method for the class Gifs which initialises the bot client.
    def __init__(self, client):
        self.client = client

        # Consolidate all gifs into a dictionary to reduce redundancy and improve maintainability.
        self.gifs = {
            'robbie': ['https://imgur.com/o0SC0o6'],
            'fe': ['https://imgur.com/U65srcp'],
            # (other GIF links)...
        }

    # Get GIF bot command.
    @commands.command()
    async def gif(self, ctx, *, var=''):
        # Block the command for certain users.
        if(ctx.author.id in qbit.forb_id):
            return 0

        # Walk through the directory and append all relevant images.
        images = [
            os.path.join(root, filename)
            for root, dirs, files in os.walk('./images')
            for filename in files
            if var in filename
        ]

        # Try to send a random image and handle the case of no images or other errors.
        if images:
            try:
                await ctx.send(file=nextcord.File(random.choice(images)))
            except Exception:
                await ctx.send("There is error sending an image.")
        else:
            await ctx.send("There are no such image.")

    # Run gif sending command. 
    @commands.command()
    async def sendgif(self, ctx, *, var=''):
        # Sending gif based on keyword.
        try:
            await ctx.send(random.choice(self.gifs.get(var, ["No such gifs"])))
        except Exception:
            await ctx.send("There is error sending a gif.")

# Add this cog while bot setup.
def setup(client):
    client.add_cog(Gifs(client))
