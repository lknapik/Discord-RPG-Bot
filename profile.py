import os
from tinydb import TinyDB, Query
class Profile():

    def __init__(self):
        if not os.path.isfile('profiles.json'):
            with open('profiles.json', 'w'): pass
    
    def createProfile(self, userID):
        db = TinyDB('profiles.json')
        print(db.search(Query().userID.exists()))
        if len(db.search(Query().userID == userID)) == 0:
            db.insert({'userID': userID, 'strength': 0, 'dexterity': 0, 'constitution': 0, 'intelligence': 0, 'wisdom': 0, 'charisma': 0, 'unspent': 0})
            return("Profile created successfully, don't forget to spend your 10 skill points!")
        else:
            return("User already exists!")