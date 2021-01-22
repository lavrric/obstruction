from repo.repo import Repository
from services.board_service import BoardService
from services.computer_service import ComputerPlayer
from tkinter import *

from services.history_service import HistoryService


class Application(Frame):
    def __init__(self, master, board, computer):
        super().__init__(master)
        self.__board = board
        self.__computer = computer
        self.__master = master
        self.__first = True
        self.__won = False
        self.__create_widgets()

    def __move_player(self, row, column):
        if not self.__board.check_free(row, column):
            return
        self.__board.make_move(row, column, 1)

        self.__won = self.__board.ctrl_win()
        if self.__won:
            Label(self.__master, text="PLAYER WON!", font=('Verdana', 12, 'bold')).grid(row=12, pady=(2, 10))
            self.__create_widgets()
            return
        if self.__first:
            print("F")
            i, j = self.__computer.find_move()
            self.__first = False
        else:
            i, j = self.__computer.maximize()[1:]

        Label(self.__master, text=f"Computer moved: row - {i + 1}, column - {j + 1}",
              font=('Verdana', 10, 'bold')).grid(row=11, pady=(0, 10))
        self.__board.make_move(i, j, 2)
        self.__won = self.__board.ctrl_win()
        if self.__won:
            Label(self.__master, text="COMPUTER WON!", font=('Verdana', 12, 'bold')).grid(row=12, pady=(2, 10))
            self.__create_widgets()
            return
        self.__create_widgets()
        return

    def __create_widgets(self):
        Label(self.__master, text="WELCOME, BOSS, THIS IS GONNA BE EPIC!",
              font=('Verdana', 15, 'bold')).grid(row=0, padx=20)
        Label(self.__master, text="O - Player moved there\n"
                                  "X - Computer moved there\n"
                                  "* - Obstructed",
              font=('Verdana', 12, 'bold')).grid(row=1, pady=10)
        for i in range(6):
            frame = Frame(self.__master)
            for j in range(6):
                state = self.__board.get_cell(i, j).state
                if state == 3:
                    s = "X"
                elif state == 2:
                    s = "O"
                elif state == 1:
                    s = "*"
                else:
                    s = " "
                button = Button(frame, text=s, borderwidth=2, height=3, width=5,
                                command=lambda row=i, column=j: self.__move_player(row, column))
                button.grid(row=i, column=j)
            frame.grid(row=i+3, column=0, pady=(0, 10 if i == 5 else 0))
        Label(self.__master, text="OBSTRUCT OR GET OBSTRUCTED!",
              font=('Verdana', 12, 'bold')).grid(row=2, pady=(5, 10))


history_repository = Repository()
history_service = HistoryService(history_repository)

board_repository = Repository()
board = BoardService(board_repository, history_service)

computer = ComputerPlayer(board, history_service)

root = Tk()
app = Application(master=root, board=board, computer=computer)
root.mainloop()
