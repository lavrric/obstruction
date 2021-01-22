class Function:
    def __init__(self, func, *parameters):
        self.__func = func
        self.__parameters = parameters

    @property
    def func(self):
        return self.__func

    @property
    def parameters(self):
        return self.__parameters
