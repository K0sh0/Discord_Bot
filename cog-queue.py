"""Revised Discord bot code with efficiency improvements and explanatory comments."""

# Necessary imports
import nextcord
from nextcord.ext import commands
import qbit

class Queue(commands.Cog):
  """Class Queue inheriting from commands.Cog for command handling."""
  
  def __init__(self, client):
    """Initializes the class with the client passively connected."""
    self.client = client

  queue = []
  role_id = [411543029086945282, 617046246535725179, 617046246535725179]

  async def _display_queue(self, ctx):
    """Displays the current queue in the chat."""
    tracker = len(self.queue)
    await ctx.send("\n".join([f"{i+1}) {name}" for i, name in enumerate(self.queue)]))

  @commands.command()            
  async def addq(self, ctx):
    """Adds the user who invoked the command to the queue."""
    if(ctx.author.id in qbit.forb_id):
      return 0
    
    un = ctx.author.name
    if un not in self.queue:
      self.queue.append(un)
  
    await self._display_queue(ctx)

  @commands.command()
  async def endq(self, ctx):
    """Removes the user who invoked the command from the queue."""

    if(ctx.author.id in qbit.forb_id):
      return 0

    un = ctx.author.name
    if un in self.queue:
      self.queue.remove(un)

    await self._display_queue(ctx)
    
  @commands.command()
  async def list(self, ctx):
    """Displays the current queue in the chat."""

    if(ctx.author.id in qbit.forb_id):
      return 0
    
    await self._display_queue(ctx)

  @commands.command()
  async def hisendq(self, ctx, other: nextcord.Member):
    """Remove another user from the queue, if the command issuer has appropriate roles."""

    mod = False
    if any(r.id in self.role_id for r in ctx.author.roles):
      mod = True

    if not mod:
      return 0

    un = other.name
    if un in self.queue:
      self.queue.remove(un)
      
    await self._display_queue(ctx)

def setup(client):
  """Adds the Queue instance to the client."""
  client.add_cog(Queue(client))
