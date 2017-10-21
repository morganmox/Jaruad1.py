def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
scores = []
tmp = []
with open("Score.txt") as scoree:
    for line in scoree:
        if line!="\n":
            tmp = line.split(":")
            if len(tmp)==2:
                if isInt(tmp[0])== True:
                    score = int(tmp[0])
                    scores.append((score,tmp[1]))
scores.sort(key=lambda s:s[0])

text_file = open("Score.txt","w")
for score,name in reversed(scores):
    text_file.write(str(score))
    text_file.write(":")
    text_file.write(name)
text_file.close()

highscore = "\n***HIGH SCORE***\n"
text_file = open("Score.txt","r")
rank = 1
while rank<=10 :
    n = text_file.readline()
    if len(n)>0:
        highscore=highscore+"\n["+str(rank)+"] . "+n
        rank+=1
    else:
        break
text_file.close()
print(highscore)
