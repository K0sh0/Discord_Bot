import nextcord
from nextcord.ext import commands
import qbit
import json

class CopyDataBase(commands.Cog):
    """
    This class represents a nextcord command Cog that contains commands to copy a database to JSON file 
    and recover it back to the database.
    """
    def __init__(self, client):
        """
        Initialize the class with a nextcord client.
        """
        self.client = client

    @commands.command()
    async def to_json(self, ctx):
        """
        Convert the entire database to a JSON file.
        """
        # Checks if the author's ID is forbidden
        if ctx.author.id in qbit.forb_id:
            return

        # Retrieving and converting the data to JSON
        big_data = json.dumps(qbit.get_full_list(ctx.message.author.id), indent=1)

        # Writing the JSON data into a file
        with open('hold_users.json', 'w') as outfile:
            outfile.write(big_data)

    @commands.command()
    async def from_json(self, ctx):
        """
        Recover the database from the JSON file.
        """
        # Checks if the author's ID is forbidden
        if ctx.author.id in qbit.forb_id:
            return

        # Opening the file and loading the data
        with open('hold_users.json') as f:
            hold_users = json.load(f)

        # Populating the database with the data from the file
        for user in hold_users:
            this_id, this_amount, this_score = map(int, user)
            qbit.insert_user(qbit.User(this_id, this_amount, this_score, 0))

def setup(client):
    """
    Function to add the CopyDataBase cog to the client.
    """
    client.add_cog(CopyDataBase(client))
