import discord
from discord.ext import commands
import profile as pf

TOKEN = 'MzI2NTAzNDI5MDY3Mzc0NjAy.D1oFxQ.lzUDmu46mgs8Da6_qjg3vgiaOrg'

client = commands.Bot(command_prefix = ".")

profile = pf.Profile()


#Let serverhost know when the bot has first initalized
@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(game=discord.Game(name='that grind'))

#Both ping and echo and basic commands, should work as they only use basic discord.py functionality
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

#Allows for a user to create their profile, if one already exists the user is notified
@client.command()
async def newProfile():
    userID = client.user.id
    status = profile.createProfile(userID)
    await client.say(status)

#Allows for the distribution of skill points after leveling up

#Lets the user access a shop to buy new weapons or magics (price is lower based off charisma)


#Lets the user train to level up without fighting (training is more efficient based off wisdom)


#Display user's profile
@client.command()
async def stats():
    userID = client.user.id
    user = client.user.name
    content = profile.getUserInfo(userID)
    em = discord.Embed(title="{}'s Profile".format(user), description = content, colour=0xDEADBF)
    await client.say(em)

client.run(TOKEN)