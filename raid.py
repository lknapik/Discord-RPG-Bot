import os
from tinydb import TinyDB, Query
from tinydb.operations import set
import profile as pf
import random
import math
class Raids():
    
    def __init__(self):
        if not os.path.isfile('raids.json'):
            with open('raids.json', 'w'): pass
    
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
            self.formLevel(userID, depth)
        else:
            return("Raid already created.")
    
    def formLevel(self, userID, depth):
        db = TinyDB('raids.json')
        #Set level type, 1-6 are battles, 7-8 are nothing, 9-10 are treasure rooms
        levelType = random.randint(1,10)
        #List of possible enemy types, no impact on stats as of now
        enemyTypes = ['Skeleton', 'Goblin', 'Zombie', 'Wisps', 'Lizard', 'Wolves']
        if(depth == 1 | levelType <= 6):
            db.update(set('enemyStrength', math.ceil(0.2*depth*(random.randint(1,10)))), Query().userID == userID)
            db.update(set('enemyDexterity', math.ceil(0.2*depth*(random.randint(1,10)))), Query().userID == userID)
            db.update(set('enemyIntelligence', math.ceil(0.2*depth*(random.randint(1,10)))), Query().userID == userID)
            db.update(set('enemyRace', enemyTypes[random.randint(0,5)]), Query().userID == userID)
            db.update(set('reward', (depth*random.randint(1,10))), Query().userID == userID)
        elif(levelType == 7 | levelType == 8):
            db.update(set('enemyRace', 'none'), Query().userID == userID)
            db.update(set('reward', 0), Query().userID == userID)
        else:
            db.update(set('enemyRace', 'treasure'), Query().userID == userID)
            db.update(set('reward', math.ceil(0.5*depth*(random.randint(1,10)))), Query().userID == userID)