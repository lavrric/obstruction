from repo.repo import Repository
from services.board_service import BoardService
from services.computer_service import ComputerPlayer
from services.history_service import HistoryService


class UI:
    def __init__(self, board, computer_player):
        self.__board = board
        self.__computer = computer_player

    def print_board(self):
        board = self.__board.get_board()
        for i in range(6):
            s = ""
            for j in range(6):
                if board[i][j].state == 3:
                    s = s+"X"
                elif board[i][j].state == 2:
                    s = s+"O"
                elif board[i][j].state == 1:
                    s = s+"s"
                else:
                    s = s+"-"
            print(s)

    def run(self):
        won = 0
        first = True
        while not won:
            moved = 0
            while not moved:
                try:
                    print("Player 1 move: ")
                    i = int(input("Row (0-indexed): "))
                    j = int(input("Column (0-indexed): "))

                    self.__board.make_move(i, j, 1)
                    moved = 1
                    self.print_board()

                    won = self.__board.ctrl_win()
                    if won:
                        print("\nPLAYER 1 WON!")
                        break
                except Exception as err:
                    print("error:", err)
            if first:
                i, j = self.__computer.find_move()
                first = not first
            else:
                score, i, j = self.__computer.maximize()
            print("Computer moved:", i, j)
            self.__board.make_move(i, j, 2)
            self.print_board()
            won = self.__board.ctrl_win()
            if won:
                print("\nComputer WON!")
                break


history_repository = Repository()
history_service = HistoryService(history_repository)

board_repository = Repository()
board = BoardService(board_repository, history_service)

computer = ComputerPlayer(board, history_service)
ui = UI(board, computer)
ui.run()
