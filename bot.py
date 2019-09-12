import discord
from discord.ext import commands
import profile as pf
import raid as rd
import combat as cb
import sys

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
    await client.change_presence(activity=discord.Game(name='that grind'))

#Both ping and echo and basic commands, should work as they only use basic discord.py functionality
@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command()
async def halt(ctx):
    await sys.exit()

@client.command()
async def echo(ctx, *args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await ctx.send(output)

#Allows for a user to create their profile, if one already exists the user is notified
@client.command()
async def newProfile(ctx):
    userID = client.user.id
    status = profile.createProfile(userID)
    await ctx.send(status)

#Allows for the distribution of skill points after leveling up format of "spendPoints 3 int"
@client.command()
async def spendPoints(ctx, *args):
    userID = client.user.id
    statsTerms = ['str', 'strength', 'dex', 'dexterity', 
                    'con', 'constitution', 'int', 'intelligence', 
                    'wis', 'wisdom', 'cha', 'charisma']
    if profile.checkForProfile(userID) == False:
        await ctx.send("Profile does not exist, use newProfile to make one!")
    if isinstance(args[0], int):
        await ctx.send("{} is not a number").format(args[0])
    if (args[1] not in statsTerms):
        await ctx.send("{} is not a skill").format(args[1])
    else:
        outcome = profile.updateSkill(userID, args[0], args[1])
        await ctx.send(outcome)

#Lets the user access a shop to buy new weapons or magics (price is lower based off charisma)


#Lets the user train to level up without fighting (training is more efficient based off wisdom)
@client.command()
async def train(ctx):
    userID = client.user.id 
    response = profile.train(userID)
    await ctx.send(response)

#Display user's profile
@client.command()
async def stats(ctx):
    userID = client.user.id
    user = client.user.name
    
    content = profile.getUserInfo(userID)
    em = discord.Embed(title="{}'s Profile".format(user), description = content, colour=0xDEADBF)
    await ctx.send(embed=em)

#Show current raid status
@client.command()
async def showRaid(ctx):
    userID = client.user.id
    user = client.user.name

    content = raid.getRaidInfo(userID)
    em = discord.Embed(title="{}'s Profile".format(user), description = content, content = 0xDEADBF)
    await ctx.send(embed=em)

#Create a new raid
@client.command()
async def createRaid(ctx):
    userID = client.user.id
    print(userID)
    result = raid.createRaid(userID)
    await ctx.send(result)

#Run Away
@client.command()
async def raidRun(ctx):
    userID = client.user.id
    result = combat.runAway(userID)
    await ctx.send(result)

#Attack melee
@client.command()
async def raidMelee(ctx):
    userID = client.user.id
    result = combat.raidMelee(userID)
    await ctx.send(result)

#Attack magic
@client.command()
async def raidMagic(ctx):
    userID = client.user.id
    result = combat.raidMagic(userID)
    await ctx.send(result)

@client.command()
async def raidNext(ctx):
    userID = client.user.id 
    result = raid.nextLevel(userID)
    await ctx.send(result)

client.run(TOKEN)