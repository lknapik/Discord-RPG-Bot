import discord
from discord.ext import commands
import profile as pf
import raid as rd
import combat as cb

#Gain bot's token, stored in seperate file for security
f = open('token.txt', 'r')
TOKEN = f.read()
f.close()

#Set bot's prefix
client = commands.Bot(command_prefix = ".")

profile = pf.Profile()
raid = rd.Raids()
combat = cb.Combat()

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

#Allows for the distribution of skill points after leveling up format of "spendPoints 3 int"
@client.command()
async def spendPoints(*args):
    userID = client.user.id
    statsTerms = ['str', 'strength', 'dex', 'dexterity', 
                    'con', 'constitution', 'int', 'intelligence', 
                    'wis', 'wisdom', 'cha', 'charisma']
    if profile.checkForProfile(userID) == False:
        await client.say("Profile does not exist, use newProfile to make one!")
    if isinstance(args[0], int):
        await client.say("{} is not a number").format(args[0])
    if (args[1] not in statsTerms):
        await client.say("{} is not a skill").format(args[1])
    else:
        outcome = profile.updateSkill(userID, args[0], args[1])
        await client.say(outcome)

#Lets the user access a shop to buy new weapons or magics (price is lower based off charisma)


#Lets the user train to level up without fighting (training is more efficient based off wisdom)
@client.command()
async def train():
    userID = client.user.id 
    response = profile.train(userID)
    await client.say(response)

#Display user's profile
@client.command()
async def stats():
    userID = client.user.id
    user = client.user.name
    
    content = profile.getUserInfo(userID)
    em = discord.Embed(title="{}'s Profile".format(user), description = content, colour=0xDEADBF)
    await client.say(embed=em)

#Show current raid status
@client.command()
async def showRaid():
    userID = client.user.id
    user = client.user.name

    content = raid.getRaidInfo(userID)
    em = discord.Embed(title="{}'s Profile".format(user), description = content, content = 0xDEADBF)
    await client.say(embed=em)

#Create a new raid
@client.command()
async def createRaid():
    userID = client.user.id
    result = raid.createRaid(userID)
    await client.say(result)

#Run Away
@client.command()
async def raidRun():
    userID = client.user.id
    result = combat.runAway(userID)
    await client.say(result)

#Attack melee
@client.command()
async def raidMelee():
    userID = client.user.id
    result = combat.raidMelee(userID)
    await client.say(result)

#Attack magic
@client.command()
async def raidMagic():
    userID = client.user.id
    result = combat.raidMagic(userID)
    await client.say(result)

client.run(TOKEN)