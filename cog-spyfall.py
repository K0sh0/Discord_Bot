import asyncio
import random
import time
from datetime import datetime
from nextcord.ext import commands
from nextcord.utils import get
import nextcord

class Spyfall(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.dict_values()
        
    def dict_values(self):
        """ Reset cases for each game instance """
        self.sf_host_on = False
        self.sf_host = False
        self.sf_start_on = False
        self.sf_players = []
        self.sf_spy = None
        self.sf_poke = []
        self.sf_poke_on = False
        self.sf_caught = False
        self.sf_location = False
        self.sf_loc_1 = ['spyfall/wedding.png', 'spyfall/airplane.png','spyfall/art_museum.png']
        #The rest of your files go here
    
    async def send_instructions(self, instruct, name):
        """ Send the instructions to a player """
        for instruction in instruct:
            await name.send(instruction)
            
    async def every_player_send(self, str_, len_players):
        """ Send a string to each player """
        for i in range(len_players):
            await self.sf_players[i].send(str_)
            
    @commands.command()
    async def spyfall(self, ctx):
        """
        !spyfall - Command to setup the game of Spyfall
        """
         #If Spyfall is not active and author is not in spyfall players then initiate the game
        if not self.sf_host_on and ctx.author not in self.sf_players:
            self.dict_values() #Resetting all values
            self.sf_host_on = True
            self.sf_host = ctx.author

            instruct = [
                'Find out which one of you is the mole',
                'One of you is secretly the spy',
                'During each round, each player will either be DMd a spy card or the secret location',
                'The spy can reveal himself any time and guess the location.',
                'The players voted the wrong guy',
                'Everyone else will receive a smaller reward',
                'The spy can reveal himself and guess the location',
                'If time runs out before players vote out the spy, they receive a smaller reward'
                 ]
            
            await ctx.send(f'{ctx.author.name} is the host.')
            self.sf_players.append(ctx.author)

            await self.send_instructions(instruct, ctx.author)
            await ctx.send(" ".join(instruct))
        #Else if host deactivates the command, terminate the game
        elif self.sf_host_on == True and self.sf_host == ctx.author:
            self.sf_host_on = False
            await ctx.send(f'{ctx.author.name} is no longer the host. Game over.')
