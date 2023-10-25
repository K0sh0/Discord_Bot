# Import required libraries
import nextcord
from nextcord.ext import commands
import qbit    # No information provided in the context about the library - qbit?
import random
import asyncio
import json
import time
from datetime import datetime
from fuzzywuzzy import fuzz
from nextcord.utils import get

class Trivia(commands.Cog):

  def __init__(self, client):
    self.client = client

    # Initializes default variables for a game of trivia
    self.host_on = False
    self.host_auth = None
    self.cluu = []
    self.fin_set = []
    self.amount = []
    self.payday = []
    self.num_x = []

    # Player instruction strings. To improve efficiency, could be extracted to a text file outside of the code.

  # Trivia game command code, utilizing fuzzy comparison for answers
  @commands.command()
  async def trivia(self, ctx, rounds: int = 1, clues: int = 1):
    if ctx.author.id in qbit.forb_id:      # Block users in forb_id list (no context provided about what this is)
      return
    
    # Check if the game configuration is valid
    if rounds*clues > 25 or rounds > 10 or clues > 10:
      await ctx.send('Whoa! Too many questions. Try again.')
      return

    # Get a clue from a category
    def get_cat(clue, list_clues):
      return [c for c in list_clues if c['category'] == clue['category']]

    # Check incoming messages
    def check(m):
      return True

    with open('categories/jeo_0147.json') as f:
      copy = json.load(f)

    # Main game loop
    for _ in range(rounds):
      list_cat = get_cat(copy[random.randrange(len(copy))], copy)
      if len(list_cat) < clues or ctx.message.channel.id == self.chatbox:
        continue
      clues_set = random.sample(list_cat, clues)
      ...

  # Hosting command for managing the trivia game
  @commands.command()
  async def host(self, ctx):
    ...
    
  # Command to signify readiness with certain conditions and settings
  @commands.command()
  async def ready(self, ctx, rounds: int = 1, clues: int = 1, cat_10 = 0):
    ...
  
  # Command to remove a category from the game
  @commands.command()
  async def rem(self, ctx, ind: int = 0):
    ...
  
  # Command to transition to the next question
  @commands.command()
  async def next(self, ctx):
    ...

  # Command to fix the amount - used in case of a mistake
  @commands.command()
  async def corr(self, ctx, other: nextcord.Member, amount_0:int = 0):
    ...
  
  # Command to show the rounds
  @commands.command()
  async def rounds(self, ctx):
    ...
  
  # Command to show the score board
  @commands.command()
  async def show(self, ctx):
    ...
  
  # Command to update the scores after each round
  @commands.command()
  async def trans(self, ctx):
    ...

# Add the Trivia bot to the Discord client
def setup(client):
  client.add_cog(Trivia(client))
