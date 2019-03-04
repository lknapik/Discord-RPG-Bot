# Discord-RPG-Bot
An extended version of the once popular DueUtil bot

Attempts to replicate a D&D quest in terms of combat
Each player has 6 basic stats and access to melee and magic

Strength: Refers directly to melee attack damage\
Dexterity: Increases chance to hit, and chance to dodge\
Constitution: Increases total health and mana regen per turn\
Intelligence: Increases magic damage and total mana\
Wisdom: Increases chance to gain more from training\
Charisma: Lowers the shop's prices\
Weapons will act as stat boosters for their respective class, Melee -> Strength, Magic -> Intelligence\
Armor can boost Dexterity and then provides some protection on damage recived, not a Constitution boost!

Exp to next level is modeled by the function Level = sqrt(TotalExp)\
Needs to be adjusted as the first 10 levels happen quite quickly

Raids work as the primary source of gold and combat\
A player starts at the top of a dungeon and works down with a chance to encounter either and enemy or treasure\
The raid is over once the player loses all their health (there is no way to heal)