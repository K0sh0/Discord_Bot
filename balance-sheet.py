import nextcord
from nextcord.ext import commands
import qbit

class BalanceSheet(commands.Cog):
  """
  This class represents a nextcord commands Cog. It includes commands for balance sheet functionalities.
  """

  def __init__(self, client):
    """
    This function initializes the client.
    """
    self.client = client

  @commands.command()
  async def rich(self, ctx, len_list: int = 5):
    """
    This function fetches and displays user balance details.
    """
    # Check if the author is in the forbidden list, if yes return 0
    if(ctx.author.id in qbit.forb_id):
      return 0

    # Get balance list
    this_id = ctx.message.author.id
    bal_list = qbit.display_list(this_id)

    # Sort the list in descending order
    bal_list.sort(reverse=True, key=lambda e: e[1])

    # Determine the number of display blocks
    blocks = len_list // 15
    remaining = len_list % 15

    # Iterate through blocks and aggregate balance details
    num_00 = 0
    for block in range(blocks+1):
      t_ = '         ALL-TIME BALANCE '

      for i in range(15 if block != blocks else remaining):
        id_ = int(bal_list[num_00][0])
        name_ = self.client.get_user(id_) or await self.client.fetch_user(id_)
        name_st = name_.name.ljust(20)[:20]

        bal_ = str(bal_list[num_00][1]).ljust(11)

        num_ = str((block * 15) + i + 1).rjust(3)

        score_ = str(bal_list[num_00][2]).ljust(5)

        bank_str = str(bal_list[num_00][3])

        # Aggregate balance details
        this_ = (num_ + ') ' + name_st + '    $' + bal_ + '    Score: ' + score_ + '    Bank: $' + bank_str)
        t_ = t_ + '\n' + this_

      t_ = '```' + t_ + '```'
      if(ctx.message.channel.id != qbit.chatbox):  
        await ctx.send(t_)

def setup(client):
  """
  This function sets up the class by adding it as a cog to the client.
  """
  client.add_cog(BalanceSheet(client))
