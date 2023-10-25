# Importing the necessary libraries
import nextcord
import os
import sqlite3
from nextcord.ext import commands
from nextcord.utils import get

# Token must be kept secret and not exposed in the code, prefer using environment variables
TOKEN = os.getenv("DISCORD_TOKEN")

# Setting up the bot intents (they define what events the bot is allowed to see)
intents = nextcord.Intents.default()
intents.message_content = True # enabling the bot to see message content
client = commands.Bot(command_prefix='.', intents=intents)

client.remove_command('help') # removed default help command

# User IDs (It would be better if you stored them in a list or dictionary, depending on their use)
kosho_id = 436061310225088512
chatbox = 368680598853648405
rizla_id = 400318006611279872
chris_id = 404314269212213248
forb_id = [rizla_id, chris_id]

all_rolls = []
voices = {}

class Pet:
    '''
    This class contains user id and their pet's name.
    '''
    def __init__(self, userid, pet_name):
        self.userid = userid
        self.pet_name = pet_name

class User:
    '''
    The User class contains user id, their current amount, total score, and bank balance.
    '''
    def __init__(self, userid, amount, score, bank):
        self.userid = userid
        self.amount = amount
        self.score = score
        self.bank = bank

# Setting up the sqlite database connection
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Creating tables if they do not exist.
c.execute("CREATE TABLE IF NOT EXISTS users (userid TEXT, amount INTEGER, score INTEGER, bank INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS pets (userid TEXT, pet_name TEXT)")

# All your database operations (INSERT, SELECT, UPDATE, DELETE) go here.
# ...

@client.command()
async def load(ctx, extension):
    '''Command to load a new extension.'''
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Loaded.')

@client.command()
async def unload(ctx, extension):
    '''Command to unload an existing extension.'''
    client.unload_extension(f'cogs.{extension}')
    await ctx.send('Unloaded.')

@client.command()
async def reload(ctx, extension):
    '''Command to reload an existing extension.'''
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Reloaded.')

# Automatically loading all cogs on startup
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Running the bot 
client.run(TOKEN)
