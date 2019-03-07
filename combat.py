import raid as rd 
from tinydb import TinyDB, Query
from tinydb.operations import set, add, subtract
import profile as pf
import os
import math
import random
class Combat:

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
        profile = pf.Profile()
        raid = rd.Raids()
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
        profile = pf.Profile()
        raid = rd.Raids()
        raidUser, raidDB = raid.getRaid(userID)
        profileUser, profileDB = profile.getUser(userID)
        strength = profileUser['strength']
        weapon = profileUser['meleeEquipment']
        damage = self.calcMelee(strength, weapon)
        enemyDamage = self.enemyTurn(userID)
        health = raidUser['health'] - enemyDamage
        enemyHealth = raidUser['enemyHealth'] - damage
        enemyType = raidUser['enemyRace']
        reward = raidUser['reward']
        if(enemyHealth <= 0):
            raidDB.update(set('health', profileUser['health']), Query().userID == userID)
            raidDB.update(set('mana', profileUser['mana']), Query().userID == userID)
            profileDB.update(add('totalExp', reward), Query().userID == userID)
            profile.levelCheck(userID)
            depth += 1
            raid.formLevel(userID, depth)
            return("You killed the {} and gained {} exp".format(enemyType, reward))
        elif(health <= 0):
            raidDB.update(set('health', profileUser['health']), Query().userID == userID)
            raidDB.update(set('mana', profileUser['mana']), Query().userID == userID)
            depth += 1
            raid.createRaid(userID)
            return("You died and retured to the top of the dungeon")
        else:
            return("You did {} points of damage, the enemy returned with {} points of damage.".format(damage, enemyDamage))

    def raidMagic(self, userID):
        profile = pf.Profile()
        raid = rd.Raids()
        raidUser, raidDB = raid.getRaid(userID)
        profileUser, profileDB = profile.getUser(userID)
        intellligence = profileUser['intelligence']
        weapon = profileUser['magicEquipment']
        mana = raidUser['mana']
        damage = self.calcMana(intellligence, weapon, mana)
        enemyDamage = self.enemyTurn(userID)
        health = raidUser['health'] - enemyDamage
        enemyHealth = raidUser['enemyHealth'] - damage
        enemyType = raidUser['enemyRace']
        reward = raidUser['reward']
        if(enemyHealth <= 0):
            raidDB.update(set('health', profileUser['health']), Query().userID == userID)
            raidDB.update(set('mana', profileUser['mana']), Query().userID == userID)
            profileDB.update(add('totalExp', reward), Query().userID == userID)
            profile.levelCheck(userID)
            depth += 1
            raid.formLevel(userID, depth)
            return("You killed the {} and gained {} exp".format(enemyType, reward))
        elif(health <= 0):
            raidDB.update(set('health', profileUser['health']), Query().userID == userID)
            raidDB.update(set('mana', profileUser['mana']), Query().userID == userID)
            depth += 1
            raid.createRaid(userID)
            return("You died and retured to the top of the dungeon")
        else:
            return("You did {} points of damage, the enemy returned with {} points of damage.".format(damage, enemyDamage))

    def enemyTurn(self, userID):
        profile = pf.Profile()
        raid = rd.Raids()
        raidUser, raidDB = raid.getRaid(userID)
        profileUser, profileDB = profile.getUser(userID)
        attackType = random.randint(1,2)
        if(attackType == 1):
            strength = raidUser['enemyStrength']
            weapon = raidUser['enemyMelee']
            damage = self.calcMelee(strength, weapon)
        elif(attackType == 2):
            intelligence = raidUser['enemyIntelligence']
            weapon = raidUser['enemyMagic']
            mana = 2
            damage = self.calcMagic(intelligence, weapon, mana)
        return(damage)

    def calcMelee(self, strength, weapon):
        weaponDB = TinyDB('weapons.json')
        weaponStats = {}
        weaponStats = weaponDB.search((Query()['name'] == str(weapon)) & (Query()['type'] == 'melee'))
        weaponStats = weaponStats[0]
        boost = weaponStats['stats']
        total = strength + boost
        damage = math.ceil(0.2*total*random.randint(1,5))
        return(damage)

    def calcMagic(self, intelligence, weapon, mana):
        weaponDB = TinyDB('weapons.json')
        weaponStats = {}
        weaponStats = weaponDB.search((Query()['name'] == str(weapon)) & (Query()['type'] == 'magic'))
        weaponStats = weaponStats[0]
        boost = weaponStats['stats']
        total = intelligence + boost
        damage = math.ceil(0.2*total*random.randint(1,5))
        return(damage)