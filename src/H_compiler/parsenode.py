class ParseNode():
    def __init__(self, type):
        self.__type = type
        self.__nodes = []

    def add_node(self, node):
        self.__nodes.append(node)

    @property
    def nodes(self):
        return self.__nodes

    @property
    def type(self):
        return self.__type