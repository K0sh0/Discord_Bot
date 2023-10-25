import nextcord
from nextcord.ext import commands
import qbit
import random
import asyncio
import json

# Creating a class called "Bracket" which is a commands.Cog subclass.
# It's essentially a group of commands, listeners, and some state they share.
class Bracket(commands.Cog):
  # Constructor for the Bracket class.
  def __init__(self, client):
    self.client = client
    
    self.brackets = False
    self.brack_title = "The "
    self.history_on = False

  # This function returns the winner of a match
  def judges(self, reactions, match):
    vote_counts = [reaction.count for reaction in reactions]
 
    # Check if count[0] is highest, then match[0] wins
    if vote_counts[0] > max(vote_counts[1], vote_counts[2]):
      return [match[0], match[1]]
    # Check if count[1] is highest, then match[1] wins
    elif vote_counts[1] > max(vote_counts[0], vote_counts[2]):
      return [match[1], match[0]]
    # If vote_counts[2] (both) is highest or equal to others, match ends in a draw
    else:
      return match

  # This function returns the match results in text form and the next round of players
  def rounds_(self, players):
    matches = list(zip(*[iter(players)]*2))
    if len(players) % 2 != 0: # If odd number of players, one player will enter the next turn automatically
      matches.append([players[-1]])

    return '\n'.join(['1 : {0} **  •|VS|•  ** 2 : {1} **  •|||•  **'.format(*match) if len(match) > 1 else '1 : {0} has a bye'.format(*match) for match in matches])

  @commands.command()
  async def bracket(self, ctx, *args):
    if (ctx.author.id in qbit.forb_id) or (ctx.message.author.id != qbit.kosho_id): 
      return

    if not self.brackets:
      self.brackets = True
      self.brack_title += ' '.join(args)
      await ctx.send(self.brack_title + " Bracket")
    else:
      self.brackets = False
      round_players = list(args)
      random.shuffle(round_players)
      self.brack_rank = []
      await ctx.message.delete()

      while len(round_players) > 1:
        round_matches_str = self.rounds_(round_players)
        round_matches = list(zip(*[iter(round_players)]*2))
        round_players = []

        for match_no, match in enumerate(round_matches):
          match_msg = await ctx.send(round_matches_str + " **__" + self.brack_title + " Bracket__**")
          for emoji in ['1️⃣', '2️⃣', '⚖️']:
            await match_msg.add_reaction(emoji)
          
          await asyncio.sleep(65)
          msg = await ctx.fetch_message(match_msg.id)
          round_players += self.judges(msg.reactions, match)
              
        self.brack_rank.append(round_players[0])

      # Save results to file
      try:
        with open('message_storage/bracket.json') as f:
          brack_file = json.load(f)
      except FileNotFoundError:
        brack_file = []
        
      brack_file.append({'title' : self.brack_title, 'order' : self.brack_rank})
      with open('message_storage/bracket.json', 'w') as f:
        json.dump(brack_file, f, indent=1)

      self.brack_title = 'The '

  @commands.command()
  async def history(self, ctx, title: str = '-'):
    if ctx.author.id in qbit.forb_id:
      return

    with open('message_storage/bracket.json') as f:
      brack_file = json.load(f)

    if not self.history_on:
      self.history_on = True
      for i in brack_file:
        if title in i['title']:
          top_five = i['order'][:5]
          full_str = '```{0} Bracket Results: \n{1}```'.format(
                  i['title'],
                  '\n'.join(['{0}) {1}'.format(rank, player) for rank, player in enumerate(top_five, 1)]))
          await ctx.send(full_str)
          await asyncio.sleep(5)
            
      self.history_on = False

def setup(client):
  client.add_cog(Bracket(client)) 
