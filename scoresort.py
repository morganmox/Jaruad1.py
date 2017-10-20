scores = []
with open("Score.txt") as scoree:
    for line in scoree:
        if line!="\n":
            score,name = line.split(":")
            score  = int(score)
            scores.append((score,name))
scores.sort(key=lambda s:s[0])
text_file = open("Score.txt","w")
for score,name in reversed(scores):
    text_file.write(str(score))
    text_file.write(":")
    text_file.write(name)
text_file.close()
