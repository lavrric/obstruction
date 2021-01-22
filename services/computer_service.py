from random import randint


class ComputerPlayer:
    def __init__(self, board, history_service=None):
        self.__board = board
        self.__history_service = history_service

    def find_move(self):
        """
        finds a random move to do
        TODO Optimal, not random
        :return: pair <int, int> - the move
        """
        done = 0
        while not done:
            i = randint(0, 5)
            j = randint(0, 5)
            if not self.__board.get_board()[i][j].state:
                done = 1
                return i, j

    def maximize(self):
        """
        finds the optimal move to do according to minimax
        :param maximize: int, is the move of the computer or of the player
        (computer - maximize, player - not maximize a.k.a. minimize)
        :return: pair <int, int> - the move
        """
        if self.__board.ctrl_win():
            return -1, -1, -1
        max_score = -1, -1, -1
        for i in range(6):
            for j in range(6):
                if self.__board.check_free(i, j):
                    self.__board.make_move(i, j, 1, assignUndo=True)
                    score = self.__minimize()
                    self.__history_service.undo()
                    if score[0] == 1:
                        return score[0], i, j
                    if max_score[0] <= score[0]:
                        max_score = score[0], i, j
        return max_score

    def __minimize(self):
        """
        finds the optimal move to do according to minimax
        :param maximize: int, is the move of the computer or of the player
        (computer - maximize, player - not maximize a.k.a. minimize)
        :return: pair <int, int> - the move
        """
        if self.__board.ctrl_win():
            return 1, 1, 1
        min_score = 1, -1, -1
        for i in range(6):
            for j in range(6):
                if self.__board.check_free(i, j):
                    self.__board.make_move(i, j, 1, assignUndo=True)
                    score = self.maximize()
                    self.__history_service.undo()
                    if score[0] == -1:
                        return score[0], i, j
                    if min_score[0] >= score[0]:
                        min_score = score[0], i, j
        return min_score
