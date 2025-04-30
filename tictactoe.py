from abc import ABC, abstractmethod
from enum import Enum
from unittest.mock import patch
import unittest

class Player(ABC):
    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol

    @property
    def name(self):
        return self._name

    @property
    def symbol(self):
        return self._symbol

    def make_move(self, board):
        pass

class HumanPlayer(Player):
    def make_move(self, board):
        while True:
            try:
                move = input(f"{self._name}, enter your move (1-9): ")
                position = int(move) - 1
                if 0 <= position < 9 and board.is_position_empty(position):
                    return position
                print("Invalid move, try again!")
            except ValueError:
                print("Please enter a number between 1 and 9.")

class ComputerPlayer(Player):
    def make_move(self, board):
        import random
        empty_positions = [i for i in range(9) if board.is_position_empty(i)]
        return random.choice(empty_positions)

class GameSymbol(Enum):
    X = "X"
    O = "O"
    EMPTY = " "

class Board:
    _instance = None  # singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reset()
        return cls._instance

    def reset(self):
        self._cells = [GameSymbol.EMPTY.value] * 9

    def display(self):
        for i in range(0, 9, 3):
            print(f" {self._cells[i]} | {self._cells[i+1]} | {self._cells[i+2]} ")
            if i < 6:
                print("-----------")

    def is_position_empty(self, position):
        return self._cells[position] == GameSymbol.EMPTY.value
    
    def update_cell(self, position, symbol):
        if 0 <= position < 9:
            self._cells[position] = symbol

    def is_full(self):
        return GameSymbol.EMPTY.value not in self._cells

    def check_winner(self):
        # horizontal
        for i in range(0, 9, 3):
            if self._cells[i] == self._cells[i+1] == self._cells[i+2] != GameSymbol.EMPTY.value:
                return self._cells[i]
        # vertical
        for i in range(3):
            if self._cells[i] == self._cells[i+3] == self._cells[i+6] != GameSymbol.EMPTY.value:
                return self._cells[i]
        # diagonal
        if self._cells[0] == self._cells[4] == self._cells[8] != GameSymbol.EMPTY.value:
            return self._cells[0]
        if self._cells[2] == self._cells[4] == self._cells[6] != GameSymbol.EMPTY.value:
            return self._cells[2]
        return None

class TicTacToeGame:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]
        self.current_player_index = 0

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def get_current_player(self):
        return self.players[self.current_player_index]

    def play(self):
        self.board.reset()

        # Parodyti seną rezultatą (tik vieną paskutinį laimėtoją) iš praeito žaidimo
        try:
            with open("praeitas.txt", "r") as f:
                paskutinis = f.read().strip()
                if paskutinis:
                    print("\n Praeito žaidimo rezultatas:")
                    print(paskutinis)
        except FileNotFoundError:
            print("\n(Nerasta senų rezultatų.)")

        winner = None
        while not winner and not self.board.is_full():
            self.board.display()
            current_player = self.get_current_player()
            position = current_player.make_move(self.board)
            self.board.update_cell(position, current_player.symbol)
            winner = self.board.check_winner()
            self.switch_player()

        self.board.display()
        if winner:
            winning_player = next(p for p in self.players if p.symbol == winner)
            print(f"Congratulations {winning_player.name}! You won!")
            result_text = f"{winning_player.name} ({winning_player.symbol}) laimėjo!"
        else:
            print("It's a tie!")
            result_text = "Lygiosios!"

        # Įrašyti tik paskutinį nugalėtoją į failą "praeitas.txt" (perrašysim)
        with open("praeitas.txt", "w") as f:
            f.write(result_text + "\n")

        # Įrašyti dabartinio žaidimo nugalėtoją į failą "dabar.txt"
        with open("dabar.txt", "w") as f:
            f.write(result_text + "\n")

        if input("Play again? (y/n): ").lower() == 'y':
            self.play()

def main():
    print("Welcome to Tic-Tac-To!")
    choice = input("Play against computer? (y/n): ").lower()
    player1 = HumanPlayer(input("Enter Player 1 name: "), GameSymbol.X.value)

    if choice == "y":
        player2 = ComputerPlayer("Computer", GameSymbol.O.value)
    else:
        player2 = HumanPlayer(input("Enter Player 2 name: "), GameSymbol.O.value)

    game = TicTacToeGame(player1, player2)
    game.play()

if __name__ == "__main__":
    main()


