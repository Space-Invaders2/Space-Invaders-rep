import sys

import pytest

sys.path.append("code")  # noqa

from behavior_tree.node import *

# sys.path.append("../")


@pytest.fixture(scope="class")
def custom_config():
    def func():
        pass

    entity = GameObject()
    black_board = BlackBoard(entity)
    root_node = RootNode(entity, black_board)
    composite_node = CompositeNode(root_node)
    decorate_node = DecoratorNode(root_node, func)
    task_node = TaskNode(root_node, func)
    node = Node(root_node)
    return {
        "entity": entity,
        "black_board": black_board,
        "root_node": root_node,
        "composite_node": composite_node,
        "decorate_node": decorate_node,
        "task_node": task_node,
        "node": node,
    }


def node_types():
    entity = GameObject()
    black_board = BlackBoard(entity)
    root_node = RootNode(entity, black_board)
    composite_node = CompositeNode(root_node)
    decorate_node = DecoratorNode(root_node, decorator_functions.decorator_function)
    task_node = TaskNode(root_node, task_functions.check_blackboardvar)
    node = Node(root_node)
    return [root_node, composite_node, decorate_node, task_node, node]


@pytest.mark.parametrize("key", ["key", 5, None, 9.0])
def test_black_board(custom_config, key):
    black_board = custom_config["black_board"]
    value = "value"
    black_board.set_atribute(key, value)
    assert black_board.get_atribute(key) == value


@pytest.mark.parametrize("key", ["key", 5, None, 9.0])
def test_black_board_none(custom_config, key):
    black_board = custom_config["black_board"]
    assert black_board.get_atribute(key) == None


@pytest.mark.parametrize("node", node_types())
def test_node_tag(node):
    node: Node
    var = "var"
    node.set_node_tag(var)
    assert node.node_tag == var


@pytest.mark.parametrize("node", node_types())
def test_node_to_str(node):
    node: Node
    var = "var"
    node.set_node_tag(var)
    assert str(node) == var


def test_root(custom_config):
    root_node = custom_config["root_node"]
    node = custom_config["node"]
    assert node.root == root_node


def test_other_root(custom_config):
    node = custom_config["node"]
    other_root = RootNode(custom_config["entity"], custom_config["black_board"])
    assert node.root != other_root


def test_add_child(custom_config):
    composite_node: CompositeNode
    composite_node = custom_config["composite_node"]
    node = custom_config["node"]
    composite_node.add_child(node)
    assert composite_node.childs[0] == node


def test_add_n_child(custom_config):
    composite_node: CompositeNode
    composite_node = custom_config["composite_node"]
    root_node = custom_config["root_node"]
    nodes = []
    node3 = None
    for i in range(1, 10):
        node = Node(root_node, f"node {i}")
        composite_node.add_child(node)
        nodes.append(node)
        if i == 3:
            node3 = node
    assert len(composite_node.childs) == 10
    assert composite_node.get_child(3) == node3


def test_decorate_node(custom_config):
    def func(child: Node, black_board: BlackBoard):
        if black_board.get_atribute("var") == "value":
            child.execute()

    decorate_node: DecoratorNode
    decorate_node = custom_config["decorate_node"]
    node = Node("")
    decorate_node.add_child(node)
    assert len(decorate_node.childs) == 1
    decorate_node.set_decorate(func)

    result = decorate_node.execute()

    assert result == None


def func(black_board: BlackBoard):
    if black_board.get_atribute("var") == "value":
        black_board.set_atribute("updated", True)
    else:
        black_board.set_atribute("updated", False)


def test_task_node(custom_config):
    task_node: TaskNode
    task_node = custom_config["task_node"]
    task_node.set_task(func)

    black_board: BlackBoard = custom_config["black_board"]
    black_board.set_atribute("var", "value")
    result = task_node.execute()
    assert black_board.get_atribute("updated")
    assert result == None


def test_task_node_false(custom_config):
    task_node: TaskNode
    task_node = custom_config["task_node"]
    task_node.set_task(func)

    black_board: BlackBoard = custom_config["black_board"]
    black_board.set_atribute("var", "not value")
    task_node.execute()
    assert not black_board.get_atribute("updated")
