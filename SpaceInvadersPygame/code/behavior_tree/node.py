import sys

sys.path.append("../")  # noqa

from game_objects.game_object import GameObject


class BlackBoard:
    def __init__(self, entity):
        self._entity = entity
        self._atribute = {}

    def set_atribute(self, key, value):
        self._atribute[key] = value

    def get_atribute(self, key):
        if key in self._atribute.keys():
            value = self._atribute[key]
            return value
        else:
            return None

    def __str__(self):
        string = ""
        string += f"Black Board entity: {self._entity} \n"
        for key in self._atribute:
            string += f" key: {key:15}, value: {self._atribute[key]:15} \n"
        return string


class Node:
    def __init__(self, root_node, node_tag="Node"):
        self.node_tag = node_tag
        self.root = root_node

    def set_node_tag(self, node_tag):
        self.node_tag = node_tag

    def __str__(self, space):
        return space + self.__repr__()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.node_tag

    def execute(self):
        print("node exe")
        return None


class CompositeNode(Node):
    def __init__(self, root_node, childs: Node = [], node_tag="CompostiteNode"):
        super().__init__(root_node, node_tag)
        self.childs: Node = childs

    def __str__(self, space=""):
        string = space + self.node_tag
        space += " "
        if not hasattr(self.childs, "__iter__"):
            string += "\n" + self.childs.__str__(space)
        elif len(self.childs) == 1:
            string += "\n" + self.childs[0].__str__(space)
        else:
            for child in self.childs:
                string += "\n" + child.__str__(space)
        return string

    def add_child(self, position, child):
        self.childs.insert(position, child)

    def add_child(self, child):
        self.childs.append(child)

    def remove_child(self, position):
        self.childs.pop(position)

    def remove_child(self):
        self.childs.pop()

    def get_child(self, position):
        return self.childs[position]

    def execute(self):
        return self.execute_childs()

    def execute_childs(self):
        for child in self.childs:
            if not child.execute():
                return False
        return True


class RootNode(CompositeNode):
    def __init__(self, entity, blackboard, childs: Node = [], node_tag="RootNode"):
        super().__init__(None, childs, node_tag)
        self.entity = entity
        self.black_board: BlackBoard = blackboard

    def execute(self):
        return None


class TaskNode(Node):
    def __init__(self, root_node, func, node_tag="TaskNode"):
        super().__init__(root_node, node_tag)
        self.func = func

    def set_task(self, func):
        self.func = func

    def execute(self):
        result = self.func(self.root.black_board)
        return result


class DecoratorNode(CompositeNode):
    def __init__(
        self, root_node, decorate, childs: Node = [], node_tag="DecoratorNode"
    ):
        super().__init__(root_node, childs, node_tag)
        self._decorate = decorate

    def set_decorate(self, func):
        self._decorate = func

    def execute(self):
        return self._decorate(self.childs[0].execute, self.root.black_board)


class decorator_functions:
    staticmethod

    def decorator_function(function, black_board: BlackBoard):
        if black_board.get_atribute("decorate"):
            pass
            function()
        else:
            print("not decorated")


class task_functions:
    staticmethod

    def check_blackboardvar(black_board: BlackBoard):
        def check_var(var, value):
            if black_board.get_atribute(var) == value:
                print("var")
                return True
            else:
                print("not var")
                return False

        check_var("var", "var")

    def count_down(self, max_loop, increment, black_board):
        count_down = black_board.get_atribute("count_down")
        if count_down == None or count_down > max_loop:
            black_board.set_atribute("count_down", 0)
        else:
            black_board.set_atribute("count_down", count_down + increment)
        return self

    def loop_1000(self, black_board: BlackBoard):
        return self.count_down(1000, 1, black_board)


def create_bench_behavior():
    entity = GameObject()
    black_board = BlackBoard(entity)

    black_board.set_atribute("momentum", [0, 0])
    black_board.set_atribute("pos", [0, 0])
    black_board.set_atribute("direction", [0, 0])

    root_node = RootNode(entity, black_board, [])
    composite = CompositeNode(root_node, [])
    task = TaskNode(root_node, task_functions.check_blackboardvar)
    decorated_task = DecoratorNode(
        root_node, decorator_functions.decorator_function, task
    )

    root_node.add_child(composite)
    composite.add_child(decorated_task)
    black_board.set_atribute("var", "var")
    black_board.set_atribute("decorate", False)

    root_node.execute()

    print(black_board)
    print(root_node)
