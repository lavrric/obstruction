from entities.op_and_reverse import OpAndReverse


class HistoryService:
    def __init__(self, history_repository):
        self.__history_repository = history_repository
        self.__position = 0

    def add_op(self, op, reverse_op):
        op_and_reverse = OpAndReverse(self.__position, op, reverse_op)
        if self.__position == len(self.__history_repository):
            self.__history_repository.create_item(op_and_reverse)
        else:
            self.__history_repository.update_item(op_and_reverse)
        self.__position = self.__position + 1

    def undo(self):
        if self.__position == 0:
            raise AttributeError("NO MORE UNDOES")
        reverse_op = self.__history_repository.item_by_id(self.__position-1).reverse_op
        for function in reverse_op.list_of_func:
            function.func(*function.parameters)
        self.__position = self.__position-1

    def redo(self):
        if self.__position == len(self.__history_repository):
            raise AttributeError("NO MORE REDOES")
        op = self.__history_repository.item_by_id(self.__position).op
        for function in op.list_of_func:
            function.func(*function.parameters)
        self.__position = self.__position+1
