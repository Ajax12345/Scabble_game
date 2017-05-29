import random
from itertools import chain
import string
from time import gmtime, strftime
import operator
class Scrabble:
    def __init__(self, user_difficult):
        self.the_values = {i.strip('\n').split()[0]: list(map(int, i.strip('\n').split()[1:])) for i in open('letters.txt').readlines()}
        self.worths = {a:b[1] for a, b in self.the_values.items()}
        self.letters = [[a for i in range(b[0])] for a, b in self.the_values.items()]
        self.new_letters = list(chain(*self.letters))
        self.new_letters = [i for i in self.new_letters if i != '']
        self.dictionary = [i for i in open('first.txt').read().splitlines()]
        self.board = [["-" for i in range(15)] for i in range(15)]
        self.hand_letters = []
        self.computer_letters = []
        self.human_score = 0
        self.computer_score = 0
        self.user_difficult = user_difficult




    def human_play(self):
        #need a new hand for a turn


        self.can_play = True
        if len(self.new_letters) >= abs(len(self.hand_letters)-7):
            for i in range(abs(len(self.hand_letters)-7)):
                self.letter = random.choice(self.new_letters)

                self.hand_letters.append(self.letter)

                self.new_letters.remove(self.letter)

        else:
            self.can_play = False

        if self.can_play:
            print "Here are your letters: "
            for i in self.hand_letters:
                print i,

            print

        #print "Do you need help:"

        #if raw_input() == "y":
            #print [i for i in self.dictionary if all(self.hand_letters.count(c.upper()) >= i.count(c) for c in i)]


            self.user = raw_input("Enter your word: ")
            self.cord1 = tuple(map(int, raw_input("Enter the corrdinates of the beginning location on the board: ").split()))
            self.cord2 = tuple(map(int, raw_input("Enter the corrdinates of the ending location on the board: ").split()))
            self.user_enter(self.cord1, self.cord2, self.user)

            for i in self.user:

                self.hand_letters.remove(i)

            for i in self.user:
                self.human_score += self.worths[i]

    def user_enter(self, loc1, loc2, word):
        if loc1[0] == loc2[0]:
            for i, a in enumerate(word):
                self.board[loc1[0]][loc1[1]+i] = a

        else:
            for i, a in enumerate(word):
                self.board[loc1[0]+i][loc1[1]] = a


    def computer_move(self):

        for i in range(abs(len(self.computer_letters)-7)):
            self.letter = random.choice(self.new_letters)

            self.computer_letters.append(self.letter)
            try:
                self.new_letters.remove(self.letter)

            except ValueError:
                pass


        self.possibilites = [i for i in self.dictionary if all(self.computer_letters.count(c.upper()) >= i.count(c) for c in i) and len(i) > 1]

        print self.possibilites



        self.best_combos = {i:sum([self.worths[b.upper()] for b in i]) for i in self.possibilites}
        #find word to use, given difficulty level
        self.the_word = ''
        if self.user_difficult == 5:
            self.the_word = [i for i, b in self.best_combos.items() if b == max(self.best_combos.values())][0]

        elif self.user_difficult == 4:
            if len(self.best_combos) >= 2:
                self.sorted_dict = sorted(self.best_combos.items(), key = operator.itemgetter(1))

                self.the_word = self.sorted_dict[1][0]

            else:
                self.the_word = [i for i, b in self.best_combos.items() if b == max(self.best_combos.values())][0]

        elif self.user_difficult == 3:
            if len(self.best_combos) >=3:
                self.sorted_dict = sorted(self.best_combos.items(), key = operator.itemgetter(1))
                self.the_word = self.sorted_dict[2][0]

            else:
                self.the_word = [i for i, b in self.best_combos.items() if b == max(self.best_combos.values())][0]

        elif self.user_difficult == 2:
            if len(self.best_combos) >= 4:
                self.sorted_dict = sorted(self.best_combos.items(), key = operator.itemgetter(1)) #returns a list of tuples containing the key and value
                self.the_word = self.sorted_dict[3][0]

        else:
            self.the_word = [i for i, b in self.best_combos.items() if b == min(self.best_combos.values())][0]
        print "the Word is", self.the_word
        for i in self.the_word:

            try:
                self.computer_letters.remove(i.upper())

            except ValueError:
                pass
        self.find_square(self.the_word)

        self.computer_score += self.best_combos[self.the_word]


    def find_square(self, word):
        self.vertical = [True if i.count("-") >= len(word) else False for i in self.board]
        print "Computer letters: ", self.computer_letters
        print "Computer Word: ", word
        self.horizontal = [True if i.count("-") >= len(word) else False for i in map(list, zip(*self.board))]
        self.done = True
        for i, row in enumerate(self.board):
            if any(b in row for b in string.ascii_letters):
                self.indices = [c for c in range(15) if self.board[i][c] != "-"]
                #print self.indices

                self.first = row[:self.indices[0]]
                self.second = row[self.indices[-1]+1:]
                #print self.first
                #print self.second


                if all(j == "-" for j in self.first) and len(self.first) >= len(word):
                    #self.user_enter([0 ,i], [len(word)-1, i], word)
                    self.user_enter([i, 0], [i, self.indices[-1]], word)
                    self.done = False
                    break

                elif all(j == "-" for j in self.second) and len(self.second) >= len(word):
                    #self.user_enter([0, i], [len(word)-1, i], word)
                    self.user_enter([i, self.indices[-1]+1], [i, self.indices[-1]+len(word)-1], word)
                    self.done = False
                    break

            else:
                self.user_enter([i, 0], [i, len(word)-1], word)
                break


        if self.done:
            self.new_board = map(list, zip(*self.board))
            for i, row in enumerate(self.new_board):
                if any(b in row for b in string.ascii_letters):
                    self.indices = [c for c in range(15) if self.new_board[i][c] != "-"]
                    #print self.indices

                    self.first = row[:self.indices[0]]
                    self.second = row[self.indices[-1]+1:]
                    #print self.first
                    #print self.second


                    if all(j == "-" for j in self.first) and len(self.first) >= len(word):
                        #self.user_enter([0 ,i], [len(word)-1, i], word)
                        #self.user_enter([i, 0], [i, self.indices[-1]], word)
                        self.user_enter([0, i], [self.indices[-1], i], word)
                        #self.done = False
                        break

                    elif all(j == "-" for j in self.second) and len(self.second) >= len(word):
                        #self.user_enter([0, i], [len(word)-1, i], word)
                        #self.user_enter([i, self.indices[-1]+1], [i, self.indices[-1]+len(word)-1], word)
                        self.user_enter([self.indices[-1]+1, i], [self.indices[-1]+len(word)-1, i], word)
                        #self.done = False
                        break

                else:
                    self.user_enter([0, i], [len(word)-1, i], word)
                    break


    def display_board(self):
        return self.board

    def show_player_score(self):
        return self.human_score

    def show_computer_score(self):
        return self.computer_score

    def still_letters(self):
        return len(self.new_letters) > 0

difficulty_level = input("Enter the desired difficulty level on a scale of 1 to 5, with five being the hardest and one being the easiest: ")

the_game = Scrabble(difficulty_level)
rounds = 0
player1 = 0
player2 = 0
#while the_game.still_letters(): #need condition to play as long as there are words in the alphabet left

while rounds < 3:
    for i in the_game.display_board():
        for b in i:
            print b,

        print


    the_game.human_play()
    the_game.computer_move()
    print "Human score: ", the_game.show_player_score()
    print "Computer score: ", the_game.show_computer_score()
    player1 = the_game.show_player_score()
    player2 = the_game.show_computer_score()


    for i in the_game.display_board():
        for b in i:
            print b,

        print

    print
    print

    the_game.show_player_score()
    rounds += 1

if player1 > player2:
    print "You won!"

elif player2 > player1:
    print "You lost. The computer won!"

else:
    print "Tie game"

f = open('scrabble_game_stats.txt', 'a')

the_date = strftime("%Y-%m-%d", gmtime())
f.write(the_date+"    "+str(player1)+"         "+str(player2)+"        "+str(difficulty_level)+"\n")
f.close()
