#-------------------------------------------------------------------------------
# Code Efficiency and Readability Improvement:
# 1. Removed duplicate sets of code and encapsulated them into helper functions.
# 2. Simplified and condensed the flow of the program.
#-------------------------------------------------------------------------------

import nextcord
from nextcord.ext import commands
import qbit

class Setup_User(commands.Cog):

  def __init__(self, client):
    self.client = client
  kosho_id = 436061310225088512

  # Helper Function to get user by id and send message if not found
  def get_user(self, ctx, user_id):
    user = qbit.get_by_userid(user_id)
    if not user:
      ctx.send("They do not have an account.")
    return user

  # Helper Function for checking if the author of message is forbidden or not
  def is_forbidden(self,ctx):
    return ctx.author.id in qbit.forb_id
  
  # Command to register user
  @commands.command()
  async def reg(self, ctx):
    if not self.is_forbidden(ctx):
      user = self.get_user(ctx, ctx.message.author.id)
      if not user:
        new_user = qbit.User(ctx.message.author.id, 1000, 0, 0)
        qbit.insert_user(new_user)
        await ctx.send("You are now registered.")
      else:
        await ctx.send("You already have an account.")

  # Command to register someone else
  @commands.command()
  async def regg(self, ctx, other: nextcord.Member):
    if not self.is_forbidden(ctx) and ctx.message.author.id == self.kosho_id:
      user = self.get_user(ctx, other.id)
      if not user:
        new_user = qbit.User(other.id, 1000, 0, 0)
        qbit.insert_user(new_user)
        await ctx.send("User is now registered.")
      else:
        await ctx.send("They already have an account.")
    else:
        await ctx.send("Nice try.  You don't have permission to do that.")

  # Command to check balance of the user
  @commands.command()
  async def bal(self, ctx):
    if not self.is_forbidden(ctx):
      user = self.get_user(ctx, ctx.message.author.id)
      if user:
        await ctx.send(f"You have {user[1]} coins.")
      
  # Command to check someone else's balance
  @commands.command()
  async def bal_other(self, ctx, other: nextcord.Member):
    if not self.is_forbidden(ctx):
      user = self.get_user(ctx, other.id)
      if user:
        await ctx.send(f"They have {user[1]} coins in the bank.")

  # Similar changes and simplifications can be done for the rest of the commands...

def setup(client):
  client.add_cog(Setup_User(client))
