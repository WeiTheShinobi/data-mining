words = ["Five","Four","Three","Two","One","Sad mother","Five"]

# 第一句
def firstSong(index):
    if index < 4:
        print(words[index] + " little ducks went out one day")
    elif index == 4:
        print(words[index] + " little duck went out one day")
    elif index == 5:
        print(words[index] + " duck went out one day")
    else:
        print(words[index] + " little ducks went out to play")

# 第二三句
def secondSong():
    print("Over the hill and far away")
    print("Mother duck said, \"Quack, quack, quack, quack\"")

# 第四句
def thirdSong(index):
    if index < 3:
        print("But only " + words[index + 1].lower() + " little ducks came back")
    elif index == 3:
        print("But only " + words[index + 1].lower() + " little duck came back")
    elif index == 4:
        print("But none of the five little ducks came back")
    else:
        print("And all of the five little ducks came back")

# 第五句
def lastSong(index):
    if index <= 3:
        for i in range(4, index, -1):
            if i == 4:
                print(words[i],end="")
            else:
                print(words[i].lower(), end="")
            if i - index > 1:
                print("",end=", ")
        print()

def duckSong():
    for i in range(7):
        firstSong(i)
        secondSong()
        thirdSong(i)
        lastSong(i)
        print()

if __name__ == '__main__':
    duckSong()
