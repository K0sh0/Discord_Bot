import nextcord
from nextcord.ext import commands, tasks
import random
import asyncio
from datetime import datetime
from PIL import Image

class Horse_Race(commands.Cog):
  
    # Initiate the class
    def __init__(self, client):
        self.client = client

    # Conversion of global variables into class attributes
    horses_on = False
    text_channel = None
    bets = []
    next_race = None
    horses_png = ['images/1.png', 'images/1.png', 'images/2.png', 'images/3.png',
                  'images/4.png', 'images/5.png', 'images/6.png', 'images/7.png']
    
    # Function to manage the horse race
    def horse_race_management(self, ctx, start_race: bool = False):
        
        # Do nothing if user's id is in the forbidden list
        if ctx.author.id in qbit.forb_id:
            return
        
        # Start or stop horse racing based on their id
        if ctx.message.author.id == qbit.kosho_id:
            self.text_channel = ctx.message.channel
            if start_race:
                self.horse_race.start()
            else:
                self.horse_race.stop()
        
    # Function wrapper to start the horse race
    @commands.command()
    async def horse_start(self, ctx):
        self.horse_race_management(ctx, start_race=True)
        
    # Function wrapper to stop the horse race
    @commands.command()
    async def horse_stop(self, ctx):
        self.horse_race_management(ctx, start_race=False)
        # Send some additional information to the text channel
        await self.text_channel.send(file=nextcord.File("images/712.png"))
        await self.text_channel.send("Tracks are closed.  See ya next time!")
      
    # Rest of the code...
    # It has been omitted for brevity, but the same principles of commenting, simplification and 
    # encapsulation into functions can be applied.

def setup(client):
    client.add_cog(Horse_Race(client))
