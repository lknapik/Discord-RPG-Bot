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
    
    def getUser(self, userID):
        db = TinyDB('profiles.json')
        userInfo = {}
        userInfo = db.search(Query().userID == userID)
        userInfo = userInfo[0]
        return(userInfo, db)


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
                        'meleeEquipment': "none",
                        'magicEquipment': "none",
                        'defenseEquipment': "none",
                        'timeToTrain': 0,
                        'timeToRaid': 0})
            return("Profile created successfully, don't forget to spend your 10 skill points!")
        else:
            return("User already exists!")

    def getUserInfo(self, userID):
        db = TinyDB('profiles.json')
        if len(db.search(Query().userID == userID)) == 0:
            return("No profile created, use newProfile to make one!")
        else:
            userInfo, db = self.getUser(userID)
            level = userInfo['level']
            health = userInfo['health']
            mana = userInfo['mana']
            gold = userInfo['gold']
            xpToNext = (math.ceil((math.sqrt(userInfo['totalExp']+100)))**2)-userInfo['totalExp']
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

            content = "```Level: {} XP to Next: {}\n Unspent Skillpoints: {}\n Health: {}  Mana: {}  Gold: {}\n Melee: {}  Magic: {}  Armor: {}\n".format(level, xpToNext, unspent, health, mana, gold, melee, magic, defense)
            stats = "Strength: {} Dexterity: {}\n Constitution: {}  Intelligence: {}\n Wisdom: {}  Charisma: {}```".format(strength, dexterity, constitution, intelligence, wisdom, charisma)
            content = content+stats

            return(content)

    def updateSkill(self, userID, points, skill):
        userInfo, db = self.getUser(userID)
        points = int(points)
        if(userInfo['unspent'] < points):
            return("Not enough skill points!")
        else:
            skill = str(skill)
            if(skill == 'str'):
                skill = 'strength'
            elif(skill == 'dex'):
                skill = 'dexterity'
            elif(skill == 'con'):
                skill = 'constitution'
            elif(skill == 'int'):
                skill = 'intelligence'
            elif(skill == 'wis'):
                skill = 'wisdom'
            elif(skill == 'cha'):
                skill = 'charisma'
            db.update(add(skill, points), Query().userID == userID)
            db.update(subtract('unspent', points), Query().userID == userID)
            return("Success!")
    

    def train(self, userID):
        userInfo, db = self.getUser(userID)
        trainTime = userInfo['timeToTrain']
        timeSince = int(time.time()) - trainTime
        if timeSince < 600:
            return("Please wait {} seconds.".format(600-timeSince))
        else:
            wisdom = userInfo['wisdom']
            expGain = random.randint(1,5)+(wisdom*random.randint(1,5))
            db.update(add('totalExp', expGain), Query().userID == userID)
            db.update(set('timeToTrain', int(time.time())), Query().userID == userID)
            self.levelCheck(userID)
            return("Gained {} Exp Points!".format(expGain))

        
    def levelCheck(self,userID):
        userInfo, db = self.getUser(userID)
        totalExp = userInfo['totalExp']
        currentLevel = userInfo['level']
        newLevel = math.floor(math.sqrt(totalExp+100))+1
        if newLevel > currentLevel:
            db.update(set('level', math.floor(math.sqrt(totalExp+100))+1), Query().userID == userID)
            db.update(add('unspent', 2), Query().userID == userID)
    
