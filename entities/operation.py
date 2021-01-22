class Operation:
    def __init__(self, *params):
        self.__list_of_func = params

    @property
    def list_of_func(self):
        return self.__list_of_func
