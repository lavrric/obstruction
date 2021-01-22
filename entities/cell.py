class Cell:
    def __init__(self, ident, state):
        self.__id = ident
        self.__state = state
        self.validate()

    def __eq__(self, other):
        if self.id == other.id and self.state == other.state:
            return 1
        return 0

    @property
    def id(self):
        return self.__id

    @property
    def state(self):
        return self.__state

    def validate(self):
        if not isinstance(self.__id, int) or self.__id < 0 or self.__id > 35:
            raise AttributeError("Not valid id (cell)!")
        if not isinstance(self.__state, int) or self.__state < 0 or self.__state > 3:
            raise AttributeError("Not valid state!")