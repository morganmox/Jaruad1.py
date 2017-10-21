name = input("Welcome to jaruad1.py! Please enter your name.\n")
for letter in name:
    if letter==':':
        name = "##INVALID_NAME##"
        
difficult = input("Select a difficulty.\n(Easy/Normal/Hard/Heroic)\n").lower()
if difficult == 'normal' or difficult == 'human':
    HEART = 350
    FENCE = 5
    STATUS = 'human.'
    MUL = 1
elif difficult == 'hard' or difficult == 'veteran':
    HEART = 300
    FENCE = 3
    STATUS = 'veteran.'
    MUL = 1.25
elif difficult == 'heroic' or difficult == 'hero' or difficult == 'god':
    HEART = 200
    FENCE = 1
    STATUS = 'god.'
    MUL = 1.5
else:
    HEART = 9999
    FENCE = 999
    STATUS = 'monkey.'
    MUL = 0.5
