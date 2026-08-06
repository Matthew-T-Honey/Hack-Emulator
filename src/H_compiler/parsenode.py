class ParseNode():
    def __init__(self, type, line):
        self.__type = type
        self.__line = line
        self.__nodes = []

    def add_node(self, node):
        self.__nodes.append(node)

    @property
    def nodes(self):
        return self.__nodes

    @property
    def type(self):
        return self.__type

    @property
    def line(self):
        return self.__line

    def __str__(self):
        return str(self.type)+"{\n"+"\n".join([str(node) for node in self.nodes])+"}"