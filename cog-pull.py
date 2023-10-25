import nextcord
from nextcord.ext import commands
import qbit
from datetime import datetime
import json
import os

class Pull(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gather_messages(self, ctx):
        # verifies that the command was initiated by the right user (kosho)
        if ctx.message.author.id != qbit.kosho_id:             
            return None
        await self.pull_messages(ctx)

    @commands.command()
    async def pull_messages(self, ctx, times_pull=50):
        room = qbit.client.get_channel(ctx.message.channel.id)  # get current channel
        if ctx.message.author.id != qbit.kosho_id:             
            return None
        await ctx.send("Started")
        test_before = None
        for j in range(times_pull):
            messages = await room.history(limit=66666, before=test_before).flatten()  # pull last 66666 messages before the most recent message
            just_quotes = [message.content for message in messages]  # get message content
            self.save_quotes_to_file(just_quotes, 'DFEAM_' + str(j))  # save the quotes to json file
            test_before = messages[-1]  # used as condition to pull older messages in next iteration
        await ctx.send('Success')
            
    def save_quotes_to_file(self, quotes, filename):
        # saves quotes in json format in a new file
        this_quotes = json.dumps(quotes, sort_keys=True, indent=1)
        with open( filename + '.json', 'w') as outfile:
            outfile.write(this_quotes)

def setup(client):
    client.add_cog(Pull(client))
