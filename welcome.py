yourname = input("Welcome to jaruad1.py! Please enter your name.\n")
for letter in yourname:
    if letter==':':
        yourname = "##INVALID_NAME##"
        
difficult = input("Select a difficulty.\n(Easy/Normal/Hard/Heroic)\n").lower()
if difficult == 'normal' or difficult == 'human':
    lives = 350
    proof = 5
    stat = 'human.'
    multiply = 1
elif difficult == 'hard' or difficult == 'veteran':
    lives = 300
    proof = 3
    stat = 'veteran.'
    multiply = 1.25
elif difficult == 'heroic' or difficult == 'hero' or difficult == 'god':
    lives = 200
    proof = 1
    stat = 'god.'
    multiply = 1.5
else:
    lives = 9999
    proof = 999
    stat = 'monkey.'
    multiply = 0.5
