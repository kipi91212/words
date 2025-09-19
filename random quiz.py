from random import choice, shuffle
import requests
from bs4 import BeautifulSoup

# User input
print("Welcome to the word quizzing program!\n Rules:\n  - The program will give you a defintion and 5 words. Your objective is to decide which of the 5 words matches the definition.")
print("Generating random words may take a while, especially for harder levels.\n")
level = input("Choose level {int (1 to 10) or range (e.g. '2-5')}: ")
try:
    level = int(level)
    start, end = level, level
except ValueError:
    parts = level.split("-")
    if len(parts) != 2:
        exit("Please enter a valid input.")
    try:
        start, end = int(parts[0]), int(parts[1])
    except ValueError:
        exit("Please enter a valid input.")
if not (1 <= start <= end <= 10):
    exit("Please enter a valid input.")
print()

# Import word list (got from "words/words.py")
wordslist = []
for j in ["english", "british_variant_1", "british_variant_2", "american"]:
    for i in [10, 20, 35, 40, 50, 55, 60, 70, 80, 95][(start-1):end]:
        with open(f"scowl-2020.12.07/final/{j}-words.{i}", "r") as words:
            wordslist.extend(words.read().splitlines())
wordslist = list(set(wordslist))
wordslist.sort()

# Import games list
try:
    with open('quizGames.txt', 'r') as file:
        previous_games = file.read()
        current_game_id = int(previous_games.split("#")[-1].split(":")[0])+1
except FileNotFoundError:
    newdata = "Game #0: (Level: 0, Score: 0/0)\n"
    with open('quizGames.txt', 'w') as file:
        file.write(newdata)
        previous_games = newdata
        current_game_id = 1

# Fetch data function (got from "(another file)/get_data.py")
def fetch_word_data(word):
    # Setup
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
        
    # Get data
    definitions = soup.select("span.def")
    definitions = [defn.text.strip() for defn in definitions if not defn.find_parent("span", class_="idm-g")]
    
    return definitions

# Main loop
alphabet = ['A','B','C','D','E']
score = [0,0]
while True:
    definitions = []
    while len(definitions) == 0:
        correctword = choice(wordslist).removesuffix("'s")
        definitions = fetch_word_data(correctword)
    words = [correctword]
    for i in range(4):
        while True:
            selectedword = choice(wordslist).removesuffix("'s")
            if (not (selectedword in words)): break
        words.append(selectedword)
    shuffle(words)
    
    if len(definitions) == 1:
        print("Definition:", definitions[0])
    else:
        print("Definitions: ")
        for d in definitions:
            print("-", d)
    printstr = ""
    for i, w in enumerate(words):
        printstr += f"{alphabet[i]}. {w}          "
    print("Options:\n" + printstr)
    answer = input("Your answer: ")
    correctanswer = alphabet[words.index(correctword)]
    score[1] += 1
    if answer.upper() == correctanswer:
        score[0] += 1
        print("Your answer was correct!")
    else:
        print(f"Your answer was incorrect! The correct answer is {correctanswer}.")
    print(f"Score: {score[0]}/{score[1]}\n")
    with open('quizGames.txt', 'w') as file:
        file.write(previous_games + f"Game #{current_game_id}: (Level: {level}, Score: {score[0]}/{score[1]})\n")