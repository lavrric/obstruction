from entities.cell import Cell
from entities.function import Function
from entities.operation import Operation


class BoardService:
    def __init__(self, board_repository, history_service=None):
        self.__board_repository = board_repository
        self.__history_service = history_service
        for i in range(6):
            for j in range(6):
                self.__board_repository.create_item(Cell(self.cell_id(i, j), 0))

    @staticmethod
    def cell_id(i, j):
        return 6*i+j

    def get_cell(self, i, j):
        return self.__board_repository.item_by_id(self.cell_id(i, j))

    def check_free(self, i, j):
        return not self.get_cell(i, j).state

    def make_move(self, i, j, num, **kwargs):
        """
        states: 0 - nothing, 1 - shaded, 2 - an O (first player), 3 - an X (second player)
        :param i: the row - 0 to 5
        :param j: the column - 0 to 5
        :param num: the number of the player, 1 or 2
        :return: -
        """
        if i < 0 or i > 5 or j < 0 or j > 5:
            raise AttributeError("Invalid coordinates.")
        if num not in [1, 2]:
            raise AttributeError("Not valid num of player!")
        if not self.check_free(i, j):
            raise AttributeError("Can't make a move there!")

        op_list = [Function(self.__board_repository.update_item, Cell(self.cell_id(i, j), num + 1))]
        rev_op_list = [Function(self.__board_repository.update_item, Cell(self.cell_id(i, j), self.get_cell(i, j).state))]

        self.__board_repository.update_item(Cell(self.cell_id(i, j), num + 1))

        for ii in range(max(0, i-1), min(6, i+2)):
            for jj in range(max(0, j-1), min(6, j+2)):
                if i != ii or j != jj:

                    if "assignUndo" in kwargs and kwargs["assignUndo"]:
                        op_list.append(Function(self.__board_repository.update_item, Cell(self.cell_id(ii, jj), 1)))
                        rev_op_list.append(Function(self.__board_repository.update_item, Cell(self.cell_id(ii, jj), self.get_cell(ii, jj).state)))

                    self.__board_repository.update_item(Cell(self.cell_id(ii, jj), 1))

        if "assignUndo" in kwargs and kwargs["assignUndo"]:
            ops = Operation(*op_list)
            reverse_ops = Operation(*rev_op_list)
            self.__history_service.add_op(ops, reverse_ops)

    def ctrl_win(self):
        """
        checks if the game is won
        :return: 1 if won, 0 if not yet won/lost
        """
        for i in range(6):
            for j in range(6):
                if self.check_free(i, j):
                    return 0
        return 1
        
    def get_board(self):
        board = []
        for i in range(6):
            row = []
            for j in range(6):
                row.append(self.get_cell(i, j))
            board.append(row)
        return board
