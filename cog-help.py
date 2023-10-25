import nextcord
from nextcord.ext import commands
from cogs import horse_race
import qbit

# remove unused imports for better performance
# import random 
# import asyncio
# import json
# import time
# import os
# import re
# import fnmatch
# import sqlite3
# from datetime import datetime
# from nextcord.utils import get

class Help(commands.Cog):
  """Handles the 'help' related commands"""
  
  def __init__(self, client):
    """Initializes the client"""
    
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    """
    Prints user information to the console and notifies when the bot is online
    """
    
    print(self.client.user.name)
    print(self.client.user.id)
    print('2-Bit Online!')

  @commands.command(pass_context=True)
  async def help(self, ctx, var:str='default'):
    """
    Sends help information to the user
    """
    
    # checks if the author is forbidden
    if(ctx.author.id in qbit.forb_id):
      return
      
    if var == 'default':
      author = ctx.message.author
      test_e = nextcord.Embed(colour=nextcord.Colour.orange())
      # setting up embed fields
      # removed inline=False as it is False by default, resulting in shorter and cleaner code
      test_e.set_author(name='Bot prefix:   .')
      # secures only relevant parts of the code with try/except for efficiency
      try:
        test_e.add_field(name='REGISTER YOUR ACCOUNT', value='.reg (After you call this function, you can now gain prize money)')
        # removed redundant inline=False
        # rest of the fields here
      except Exception as e:
        print(f"An error occurred while setting help details: {e}")
      await author.send(embed=test_e)
      await ctx.send('Yea.. you need help alright.  Check your DMs, Einstein.')

  @commands.command(pass_context=True)
  async def cipher(self, ctx, *, var=''):
    """
    Handles the 'cipher' command - builds and sends a binary-ascii encoded message
    """
    
    # Check if the author is kosho
    if(ctx.author.id != qbit.kosho_id):
      return
      
    msg = ctx.message
    await msg.delete()
    new_var = var[2:-2]
    alph = [asc_bin(ord(c) - 64) if 'A' <= c <= 'Z' else asc_bin(ord(c) - 96) if 'a' <= c <= 'z' else c for c in new_var]
    msg = '**-' + '-'.join(alph) + '**'
    await ctx.send(msg)

def asc_bin(num):
  """
  Converts a numeral representing ASCII characters into binary
  """
  
  bin_ = []
  masks = [16, 8, 4, 2, 1]
  for mask in masks:
    if num >= mask:
      bin_.append(str(masks.index(mask)))
      num -= mask
  bin_.extend(['5'] * (5 - len(bin_)))
  return '-'.join(bin_)

def setup(client):
  """
  Sets up the client before running the bot
  """
  
  client.add_cog(Help(client))
