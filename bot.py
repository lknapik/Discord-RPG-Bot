import discord
from discord.ext import commands
import profile as pf

TOKEN = 'MzI2NTAzNDI5MDY3Mzc0NjAy.D1oFxQ.lzUDmu46mgs8Da6_qjg3vgiaOrg'

client = commands.Bot(command_prefix = ".")

profile = pf.Profile()

@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(game=discord.Game(name='that grind'))

@client.command()
async def ping():
    await client.say('Pong!')

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

@client.command()
async def newProfile():
    userID = client.user.id
    status = profile.createProfile(userID)
    await client.say(status)

client.run(TOKEN)