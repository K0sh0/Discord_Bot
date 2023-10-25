import nextcord
from nextcord.ext import commands
import qbit
import random

class Dice(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def roll(self, ctx, wager: int = 100, bet: str = 'field', quant: int = 2, di: int = 6):
    """
    This function rolls a pair of dice n number of times specified by quant.
    User can wage on particular outcomes with different betting options.
    """
    
    # Check if user is prohibited from executing the command
    if ctx.author.id in qbit.forb_id:
      return

    this_guy = qbit.get_by_userid(ctx.message.author.id)
            
    # Check conditions before performing dice roll
    if ctx.message.channel.id != qbit.chatbox and this_guy[1] >= wager and 0 < wager:
      
      # Define the sets for all the different possible bets
      field = set([3, 4, 9, 10, 11])
      high_low = set([2, 12])
      craps = set([2, 3, 12])
      
      # Rolling the dice
      dice = [random.randint(1, 6) for _ in range(quant)]
      
      # Calculating the sum of numbers rolled
      summ = sum(dice)
      
      # Storing roll's result
      qbit.all_rolls.append(summ)
      
      total_result = f"Total: {summ} --- {dice}"
      await ctx.send(total_result)    
      
      # Check the bet type and decide if the user won the bet
      if bet == 'field':
        if summ in field or summ in high_low:
          wager *= 2 if summ in high_low else 1
          winning_message = f'Winner! ${wager}'
          await ctx.send(winning_message)
          this_pay = this_guy[1] + wager
        else:
          this_pay = this_guy[1] - wager
      elif bet in ['snake-eyes', 'midnight']:
        winning_number = 2 if bet == 'snake-eyes' else 12
        this_pay = this_guy[1] + wager * 30 if summ == winning_number else this_guy[1] - wager
      elif bet in ['high-low', 'seven', 'three', 'eleven', 'craps'] or bet.isdigit():
        multiplier = {'high-low': 15, 'seven': 4, 'three': 15, 'eleven': 15, 'craps': 7}
        check_numbers = {'high-low': high_low, 'seven': {7}, 'three': {3}, 'eleven': {11}, 'craps': craps, 'any-craps': craps}
        check_number = check_numbers.get(bet, {int(bet)})
        this_pay = this_guy[1] + wager * multiplier.get(bet, 1) if summ in check_number else this_guy[1] - wager
      else:
        this_pay = this_guy[1] + wager * 10 if summ == int(bet[0]) * 2 and dice[0] == int(bet[0]) else this_guy[1] - wager
      
      qbit.update_pay((this_pay, ctx.message.author.id))

  @commands.command()
  async def rolls(self, ctx):
    """
    Function for showing statistics of all the rolls.
    """
    
    # Check if user is prohibited from executing the command
    if ctx.author.id in qbit.forb_id:
      return

    if ctx.message.channel.id != qbit.chatbox:
      
      # sort and count dice results
      qbit.all_rolls.sort()
      
      # calculating and sending result pattern percentage
      for i in range(2,13):
        count  = qbit.all_rolls.count(i)
        percentage = count/len(qbit.all_rolls)*100
        await ctx.send(f'{i} --- {count} --- {percentage:.2f}%')

      # sending total of rolls
      await ctx.send(len(qbit.all_rolls))

def setup(client):
  client.add_cog(Dice(client))
