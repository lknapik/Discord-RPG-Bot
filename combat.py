import raid as rd 
from tinydb import TinyDB, Query
import profile as pf
import os
import math
import random
class Combat:

    profile = pf.Profile()
    raid = rd.Raids()

    def __init__(self):
        if not os.path.isfile('weapons.json'):
            with open('weapons.json', 'w'):
                weaponDB = TinyDB('weapons.json')
                weaponDB.insert({'name': "none",
                                'type': "melee",
                                'stats': 0})
                weaponDB.insert({'name': "none",
                                'type': "magic",
                                'stats': 0})       

    def raidRun(self, userID):
        raidUser, raidDB = raid.getRaid(userID)
        profileUser, profileDB = profile.getUser(userID)
        enemyDex = raidUser['enemyDexterity']
        userDex = profileUser['dexterity']
        chanceToRun = (userDex/enemyDex)
        if(chanceToRun > random.random()):
            depth += 1
            raid.formLevel(userID, depth)
            return("Successufully Ran")
        else:
            enemyDamage = self.enemyTurn(userID)
            return("Failed to run " + enemyDamage)
    
    def raidMelee(self, userID):
        raidUser, raidDB = raid.getRaid(userID)
        profileUser, profileDB = profile.getUser(userID)
        strength = profileUser['strength']
        weapon = profileUser['weaponMelee']
        damage = self.calcMelee(strength, weapon)
        enemyDamage = self.enemyTurn(userID)
        return(damage + ' ' + enemyDamage)

    def raidMagic(self, userID):
        raidUser, raidDB = raid.getRaid(userID)
        profileUser, profileDB = profile.getUser(userID)
        intellligence = profileUser['intelligence']
        weapon = profileUser['weaponMagic']
        mana = raidUser['mana']
        damage = self.calcMana(intellligence, weapon, mana)
        enemyDamage = self.enemyTurn(userID)
        return(damage + ' ' + enemyDamage)

    def enemyTurn(self, userID):
        raidUser, raidDB = raid.getRaid(userID)
        profileUser, profileDB = profile.getUser(userID)


    def calcMelee(self, strength, weapon):
        return("nice")
    def calcMagic(self, intelligence, weapon, mana):
        return("nice")