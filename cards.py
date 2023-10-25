# Import necessary modules
import nextcord
from nextcord.ext import commands
import random
import asyncio, qbit

# Define a class for card related commands
class Cards(commands.Cog):
  # Class initializer function
  def __init__(self, client):
    self.client = client

  # Set of all card images
  play_cards = ['300/2_of_clubs_300.png', '300/3_of_clubs_300.png',
                         '300/4_of_clubs_300.png', ...]

  # Define a function that returns the value of a card based on its index position in the deck
  @staticmethod
  def get_card_value(card_index):
      return card_index % 13

  # This is a high card game with bot
  @commands.command()
  async def cards(self, ctx, bet = 100):
    
    # Ignore the users in the forbidden id list
    if ctx.author.id in qbit.forb_id:
      return

    user_id = ctx.message.author.id
    user = qbit.get_by_userid(user_id)

    # Only process the card game if the user has enough balance, the bet is positive and it's not a chatbox channel
    if user[1] >= bet and bet >= 0 and ctx.message.channel.id != qbit.chatbox:
      
      user_card_index, house_card_index = random.sample(range(len(self.play_cards)), 2)

      for card_index in [user_card_index, house_card_index]:
        await ctx.send(file = nextcord.File(self.play_cards[card_index]))
        await asyncio.sleep(3.5)

      user_card_value = self.get_card_value(user_card_index)
      house_card_value = self.get_card_value(house_card_index)

       if house_card_value > user_card_value:
        my_val = user[1] - bet
        qbit.update_pay((my_val, search_id[0]))
        await ctx.send('Loser.')
       
      elif user_card_value > house_card_value:
        my_val = user[1] + bet
        qbit.update_pay((my_val, user[0]))
        await ctx.send('Winner!')
       
      else:
        await ctx.send('Draw.')

def setup(client):
  client.add_cog(Cards(client))
