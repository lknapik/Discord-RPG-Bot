import os
from tinydb import TinyDB, Query
from tinydb.operations import add, subtract, set
import math
import time
import random
class Profile():

    def __init__(self):
        if not os.path.isfile('profiles.json'):
            with open('profiles.json', 'w'): pass
    
    def checkForProfile(self, userID):
        db = TinyDB('profiles.json')
        if len(db.search(Query().userID == userID)) == 0:
            return(False)
        else:
            return(True)

    def createProfile(self, userID):
        db = TinyDB('profiles.json')
        if len(db.search(Query().userID == userID)) == 0:
            db.insert({'userID': userID, 
                        'health': 10,
                        'mana': 10,
                        'strength': 0, 
                        'dexterity': 0, 
                        'constitution': 0, 
                        'intelligence': 0, 
                        'wisdom': 0, 
                        'charisma': 0, 
                        'unspent': 10,
                        'level': 1,
                        'totalExp': 0,
                        'gold': 100,
                        'meleeEquipment': "None",
                        'magicEquipment': "None",
                        'defenseEquipment': "None",
                        'timeToTrain': 0})
            return("Profile created successfully, don't forget to spend your 10 skill points!")
        else:
            return("User already exists!")

    def getUserInfo(self, userID):
        db = TinyDB('profiles.json')
        if len(db.search(Query().userID == userID)) == 0:
            return("No profile created, use newProfile to make one!")
        else:
            userInfo = {}
            userInfo = db.search(Query().userID == userID)
            userInfo = userInfo[0]
            print(userInfo)
            level = userInfo['level']
            health = userInfo['health']
            mana = userInfo['mana']
            gold = userInfo['gold']
            xpToNext = (math.ceil((math.sqrt(userInfo['totalExp'])))**2)-userInfo['totalExp']
            unspent = userInfo['unspent']
            melee = userInfo['meleeEquipment']
            magic = userInfo['magicEquipment']
            defense = userInfo['defenseEquipment']
            strength = userInfo['strength']
            dexterity = userInfo['dexterity']
            constitution = userInfo['constitution']
            intelligence = userInfo['intelligence']
            wisdom = userInfo['wisdom']
            charisma = userInfo['charisma']

            content = "```Level: {} Health: {}  Mana: {}  Gold: {} \n XP to Next: {} Unspent Skillpoints: {} \n Melee: {}  Magic: {}  Armor: {} \n".format(level, health, mana, gold, xpToNext, unspent, melee, magic, defense)
            stats = "Strength: {} Dexterity: {} \n Constitution: {}  Intelligence: {} \n Wisdom: {}  Charisma: {}```".format(strength, dexterity, constitution, intelligence, wisdom, charisma)
            content = content+stats

            return(content)

    def updateSkill(self, userID, points, skill):
        db = TinyDB('profiles.json')
        userInfo = {}
        userInfo = db.search(Query().userID == userID)
        userInfo = userInfo[0]
        points = int(points)
        if(userInfo['unspent'] < points):
            return("Not enough skill points!")
        else:
            db.update(add('strength', points), Query().userID == userID)
            db.update(subtract('unspent', points), Query().userID == userID)
            return("Success!")
    

    def train(self, userID):
        db = TinyDB('profiles.json')
        userInfo = {}
        userInfo = db.search(Query().userID == userID)
        userInfo = userInfo[0]
        trainTime = userInfo['timeToTrain']
        timeSince = int(time.time()) - trainTime
        if timeSince < 600:
            return("Please wait {} seconds.".format(600-timeSince))
        else:
            charisma = userInfo['charisma']
            expGain = random.randint(1,5)+(charisma*random.randint(1,5))
            db.update(add('totalExp', expGain), Query().userID == userID)
            db.update(set('timeToTrain', int(time.time())), Query().userID == userID)
            self.levelCheck(userID)
            return("Gained {} Exp Points!".format(expGain))

        
    def levelCheck(self,userID):
        db = TinyDB('profiles.json')
        userInfo = {}
        userInfo = db.search(Query().userID == userID)
        userInfo = userInfo[0]
        totalExp = userInfo['totalExp']
        currentLevel = userInfo['level']
        newLevel = math.floor(math.sqrt(totalExp))+1
        if newLevel > currentLevel:
            db.update(set('level', math.floor(math.sqrt(totalExp))+1), Query().userID == userID)
            db.update(add('unspent', 2), Query().userID == userID)
    
