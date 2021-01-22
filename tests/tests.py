import unittest
from random import randint

from entities.cell import Cell
from repo.repo import Repository
from services.board_service import BoardService
from services.computer_service import ComputerPlayer
from services.history_service import HistoryService


class Tests(unittest.TestCase):
    def test_cell(self):
        cell = Cell(1, 1)
        self.assertEqual(cell.id, 1)
        self.assertEqual(cell.state, 1)
        self.assertNotEqual(Cell(1, 1), Cell(1, 2))

        self.assertRaises(AttributeError, lambda: Cell(37, 0))
        self.assertRaises(AttributeError, lambda: Cell(6, 4))

    def test_repositories(self):
        repo = Repository()

        repo.create_item(Cell(1, 1))
        repo.create_item(Cell(2, 3))
        self.assertEqual(repo.all_items()[0], Cell(1, 1))
        self.assertEqual(repo.all_items()[1], Cell(2, 3))

        self.assertRaises(AttributeError, lambda: repo.create_item(Cell(1, 3)))
        self.assertRaises(AttributeError, lambda: repo.item_by_id(23))

        repo.update_item(Cell(1, 3))
        self.assertEqual(repo.item_by_id(1), Cell(1, 3))

        self.assertRaises(AttributeError, lambda: repo.update_item(Cell(32, 0)))

        repo.delete_item_by_id(1)
        repo.delete_item_by_id(2)
        self.assertFalse(len(repo))

    def test_board(self):
        repo = Repository()
        board = BoardService(repo)

        self.assertEqual(len(board.get_board()), 6)
        self.assertEqual(len(board.get_board()[randint(0, 5)]), 6)

        board.make_move(0, 0, 1)
        self.assertEqual(board.get_cell(0, 0), Cell(board.cell_id(0, 0), 2))
        for i in [0, 1]:
            for j in [0, 1]:
                if i+j:
                    self.assertEqual(board.get_cell(i, j), Cell(board.cell_id(i, j), 1))

        board.make_move(2, 2, 2)
        self.assertEqual(board.get_cell(2, 2), Cell(board.cell_id(2, 2), 3))
        for i in [1, 3]:
            for j in [1, 3]:
                if i != 2 or j != 2:
                    self.assertEqual(board.get_cell(i, j), Cell(board.cell_id(i, j), 1))

        self.assertRaises(AttributeError, lambda: board.make_move(1, 1, 1))
        self.assertRaises(AttributeError, lambda: board.make_move(6, 1, 1))
        self.assertRaises(AttributeError, lambda: board.make_move(4, 4, 3))

        self.assertFalse(board.ctrl_win())
        board.make_move(3, 0, 2)
        board.make_move(5, 1, 2)
        board.make_move(4, 4, 2)
        board.make_move(1, 4, 2)
        self.assertFalse(board.ctrl_win())
        board.make_move(0, 2, 2)
        self.assertTrue(board.ctrl_win())

    def test_board_undo(self):
        repo = Repository()
        history_repo = Repository()
        history_service = HistoryService(history_repo)
        board = BoardService(repo, history_service)

        self.assertRaises(AttributeError, lambda: history_service.undo())
        self.assertRaises(AttributeError, lambda: history_service.redo())
        board.make_move(2, 2, 2, assignUndo=True)

        self.assertEqual(board.get_cell(2, 2), Cell(board.cell_id(2, 2), 3))
        for i in [1, 3]:
            for j in [1, 3]:
                if i != 2 or j != 2:
                    self.assertEqual(board.get_cell(i, j), Cell(board.cell_id(i, j), 1))

        history_service.undo()

        self.assertEqual(board.get_cell(2, 2), Cell(board.cell_id(2, 2), 0))
        for i in [1, 3]:
            for j in [1, 3]:
                self.assertEqual(board.get_cell(i, j), Cell(board.cell_id(i, j), 0))

        history_service.redo()
        self.assertEqual(board.get_cell(2, 2), Cell(board.cell_id(2, 2), 3))
        for i in [1, 3]:
            for j in [1, 3]:
                if i != 2 or j != 2:
                    self.assertEqual(board.get_cell(i, j), Cell(board.cell_id(i, j), 1))

        board.make_move(0, 0, 2, assignUndo=True)
        history_service.undo()
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                if not i or not j:
                    self.assertEqual(board.get_cell(i, j), Cell(board.cell_id(i, j), 0))
                elif i == 2 and j == 2:
                    self.assertEqual(board.get_cell(i, j), Cell(board.cell_id(i, j), 3))
                else:
                    self.assertEqual(board.get_cell(i, j), Cell(board.cell_id(i, j), 1))

    def test_minimax(self):
        count_won = 100
        count = 100
        for _ in range(count):
            print(_)
            history_repository = Repository()
            history_service = HistoryService(history_repository)

            board_repository = Repository()
            board = BoardService(board_repository, history_service)

            computer = ComputerPlayer(board, history_service)
            won = 0
            first = True
            while not won:
                i, j = computer.find_move()

                board.make_move(i, j, 1)
                won = board.ctrl_win()
                if won:
                    count_won = count_won-1
                    print("lost")
                    break
                if first:
                    i, j = computer.find_move()
                    first = not first
                else:
                    score, i, j = computer.maximize()
                board.make_move(i, j, 2)
                won = board.ctrl_win()
                if won:
                    print("won")
        print(count_won)
        self.assertGreaterEqual(count_won, 66)
