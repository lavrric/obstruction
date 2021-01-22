class OpAndReverse:
    def __init__(self, id, op, reverse_op):
        self.__id = id
        self.__op = op
        self.__reverse_op = reverse_op

    @property
    def id(self):
        return self.__id

    @property
    def op(self):
        return self.__op

    @property
    def reverse_op(self):
        return self.__reverse_op
