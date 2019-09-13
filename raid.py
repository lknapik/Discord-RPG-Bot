import os
from tinydb import TinyDB, Query, where
from tinydb.operations import set, increment, add
import profile as pf
import random
import math
class Raids():
    
    def __init__(self):
        if not os.path.isfile('raids.json'):
            with open('raids.json', 'w'): pass

    def getRaid(self,userID):
        db = TinyDB('raids.json')
        raid = {}
        raid = db.search(Query().userID == userID)
        raid = raid[0]
        return raid, db
        
    
    def createRaid(self, userID):
        db = TinyDB('raids.json')
        profile = pf.Profile()
        if len(db.search(Query().userID == userID)) == 0:
            userInfo, profileDB = profile.getUser(userID)
            db.insert({'userID': userID,
                        'health': userInfo['health'],
                        'mana': userInfo['mana'],
                        'depth': 1,
                        'reward': 0,
                        'enemyRace': "none",
                        'enemyHealth': 5,
                        'enemyStrength': 0,
                        'enemyDexterity': 0,
                        'enemyIntelligence': 0,
                        'enemyMelee': "none",
                        'enemyMagic': "none"})
            depth = 1
            enemyRaces = ['Skeleton', 'Goblin', 'Zombie', 'Wisps', 'Lizard', 'Wolves']
            db.update(set('enemyStrength', math.ceil(0.2*depth*(random.randint(1,10)))), Query().userID == userID)
            db.update(set('enemyDexterity', math.ceil(0.2*depth*(random.randint(1,10)))), Query().userID == userID)
            db.update(set('enemyIntelligence', math.ceil(0.2*depth*(random.randint(1,10)))), Query().userID == userID)
            db.update(set('enemyRace', enemyRaces[random.randint(0,5)]), Query().userID == userID)
            db.update(set('reward', (depth*random.randint(1,10))), Query().userID == userID)
            return("Raid Created, use showRaid to view")
        else:
            return("Raid already created.")
    
    #This automatically increases depth, dont do it anywhere else
    def formLevel(self, userID):
        raidUser, raidDB = self.getRaid(userID)
        depth = raidUser['depth']
        depth += 1
        raidDB.update(set('depth', depth), Query().userID == userID)
        #Set level type, 1-6 are battles, 7-8 are nothing, 9-10 are treasure rooms
        levelType = random.randint(1,10)
        #List of possible enemy types, no impact on stats as of now
        enemyRaces = ['Skeleton', 'Goblin', 'Zombie', 'Wisps', 'Lizard', 'Wolves']
        if(levelType <= 6):
            raidDB.update(set('enemyStrength', math.ceil(0.2*depth*(random.randint(1,10)))), Query().userID == userID)
            raidDB.update(set('enemyDexterity', math.ceil(0.2*depth*(random.randint(1,10)))), Query().userID == userID)
            raidDB.update(set('enemyIntelligence', math.ceil(0.2*depth*(random.randint(1,10)))), Query().userID == userID)
            raidDB.update(set('enemyHealth', math.ceil(0.2*depth*(random.randint(10,30)))), Query().userID == userID)
            raidDB.update(set('enemyRace', enemyRaces[random.randint(0,5)]), Query().userID == userID)
            raidDB.update(set('reward', (depth*random.randint(1,10))), Query().userID == userID)
        elif(levelType == 7 | levelType == 8):
            raidDB.update(set('enemyRace', 'none'), Query().userID == userID)
            raidDB.update(set('reward', 0), Query().userID == userID)
        elif(levelType == 9 | levelType == 10):
            raidDB.update(set('enemyRace', 'treasure'), Query().userID == userID)
            raidDB.update(set('reward', math.ceil(0.5*depth*(random.randint(1,10)))), Query().userID == userID)

    def getRaidInfo(self, userID):
        content = ""
        db = TinyDB('raids.json')
        if len(db.search(Query().userID == userID)) == 0:
            return("No raid created, use createRaid to make one!")
        else:
            raidInfo, db = self.getRaid(userID)
            userHealth = raidInfo['health']
            userMana = raidInfo['mana']
            depth = raidInfo['depth']
            enemyRace = raidInfo['enemyRace']
            enemyHealth = raidInfo['enemyHealth']
            content = "```Current Health: {} Current Mana: {} Raid Depth: {}\nEnemy Type: {} Enemy Health: {}```".format(userHealth, userMana, depth, enemyRace, enemyHealth)
            return content
    
    def nextLevel(self, userID):
        raid, raidDB = self.getRaid(userID)
        profile = pf.Profile()
        profileUser, profileDB = profile.getUser(userID)
        self.formLevel(userID)
        if (raid['enemyHealth'] > 0):
            raidDB.update(set('health', profileUser['health']), Query().userID == userID)
            raidDB.update(set('mana', profileUser['mana']), Query().userID == userID)
            return("An enemy stands in your way")
        elif(raid['enemyRace'] == 'none'):
            raidDB.update(set('health', profileUser['health']), Query().userID == userID)
            raidDB.update(set('mana', profileUser['mana']), Query().userID == userID)
            self.formLevel(userID)
            return("You move to the next room")
        elif(raid['enemyRace'] == 'treasure'):
            reward = raid['reward']
            profileDB.update(add('gold', reward), Query().userID == userID) 
            raidDB.update(set('health', profileUser['health']), Query().userID == userID)
            raidDB.update(set('mana', profileUser['mana']), Query().userID == userID)
            self.formLevel(userID)
            return("Collected {} gold, and moved to the next room".format(reward))
        else:
            raidDB.update(set('health', profileUser['health']), Query().userID == userID)
            raidDB.update(set('mana', profileUser['mana']), Query().userID == userID)
            self.formLevel(userID)
            return("You move to the next room")
    
    def resetRaid(self, userID):
        raid, raidDB = self.getRaid(userID)
        raidDB.remove(where('userID') == userID)