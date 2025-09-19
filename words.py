wordslist = []
for j in ["english", "british_variant_1", "british_variant_2", "american"]:
    for i in [10, 20, 35, 40, 50, 55, 60, 70, 80, 95]:
        with open(f"scowl-2020.12.07/final/{j}-words.{i}", "r") as words:
            wordslist.extend(words.read().splitlines())
wordslist = list(set(wordslist))
wordslist.sort()

guessed = []
if input("Would you like to start a new game or import game? s/i ") == "s":
    cont = input("What string would you like to search for? ")
    sw = input("Do you want the word to strictly start with the string? y/n: ") == "y"
    contlist = []
    if not sw:
        for word in wordslist:
            if cont in word: contlist.append(word)
        print(f"There are {len(contlist)} words containing '{cont}'.")
    else:
        contL = len(cont)
        for word in wordslist:
            if word[:contL] == cont: contlist.append(word)
        print(f"There are {len(contlist)} words starting with '{cont}'.")
else:
    gameId = input("Enter your game id: ")
    with open("savesId.txt") as file:
        ids = file.readlines()
    if (gameId + "\n") in ids:
        print("Found your game!")
        with open(f"saves/{gameId}.txt") as file:
            cont = file.readline()[:-1]
            sw = file.readline() == "True"
            gameString = file.readline()
        print("Your game: look for words that " + ("start with" if sw else "contain") + f" {cont}.")
        contlist = []
        if not sw:
            for word in wordslist:
                if cont in word: contlist.append(word)
            print(f"There are {len(contlist)} words containing '{cont}'.")
        else:
            contL = len(cont)
            for word in wordslist:
                if word[:contL] == cont: contlist.append(word)
            print(f"There are {len(contlist)} words starting with '{cont}'.")
        for i in gameString.split(",")[:-1]:
            contlist.remove(wordslist[int(i)])
            guessed.append(wordslist[int(i)])
        print(f"You've guessed {len(guessed)} words: {guessed}")
            
    else:
        print("Your game doesn't exist. Please create a new game or enter an existing id.")
        exit()

if input("Would you like to show all words? y/n: ") == "y":
    for word in contlist:
        print(word)
elif input("Would you like to guess? y/n: ") == "y":
    print("Type -1 to quit\nType -2 to save & quit")
    for i in range(len(contlist)):
        while True:
            word = input(f"Word #{i+1}: ")
            if word in contlist:
                contlist.remove(word)
                guessed.append(word)
                print("Your guess was correct!")
                break
            elif word == "-1":
                print(f"Well done! You got {i} point(s)!\nThe remaining words are:")
                for word in contlist:
                    print(word)
                exit()
            elif word == "-2":
                print(f"You got {i} point(s)!")
                import random
                with open("savesId.txt", "r") as file:
                    ids = file.readlines()
                while True:
                    writeId = ""
                    for i in range(9):
                        writeId += str(random.randint(0,9))
                    if (writeId+"\n") not in ids: break
                with open("savesId.txt", "a") as file:
                    file.write(writeId + "\n")
                with open(f"saves/{writeId}.txt", "w") as file:
                    file.write(f"{cont}\n{sw}\n")
                    for i in guessed:
                        file.write(str(wordslist.index(i)) + ",")
                print(f"Your game id is {writeId}.")
                exit()
            if cont not in word:
                print("Your word doesn't " + ("start with" if sw else "contain") + f" '{cont}'. Try again!")
            elif word in guessed:
                print("You have already guessed that word. Try again!")
            else:
                print("That word doesn't exist. Try again!")
    print("Congratulations! You guessed all words!")
elif input("Would you like to search if a word exists? y/n: ") == "y":
    print("It exists!" if input("Enter your word: ") in contlist else "It doesn't exist")