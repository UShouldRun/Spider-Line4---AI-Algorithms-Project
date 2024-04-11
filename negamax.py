from objects import Node

class Negamax:

    """
    Class for implementing the Negamax algorithm.

    Methods:
        __init__(root, max_depth, mdp): Initializes the Negamax object.
        create_root(state, action) -> Node: Creates the root node.
        expand(node) -> None: Expands the children of a node.
        grow_tree(node, iteration) -> None: Grows the tree from a node.
        neg_or_max(node, children_eval) -> float: Calculates the negamax or max value for a node.
        evaluate_tree(node) -> None: Evaluates the tree and updates the reward values.
        negamax(root) -> Node: Runs the Negamax algorithm.
    """

    def __init__(self, root, max_depth: int, mdp) -> None:
        self.root_state = root
        self.max_depth = max_depth
        self.mdp = mdp
        self.expanded_children = dict()

    def create_root(self, state, action) -> Node: return Node(state, None, action)

    def expand(self, node) -> None:
        node.set_children([self.mdp.execute(node,action) for action in self.mdp.get_actions(node)])
        if not node.get_children(): return
        self.expanded_children[node] = node.get_children()

    def grow_tree(self, node: Node, iteration: int = 0) -> None:
        if iteration == self.max_depth or not self.mdp.non_terminal(node):
            node.increase_reward(self.mdp.qfunction(node))
            return
        self.expand(node)
        for child in node.get_children(): self.grow_tree(child, iteration + 1)

    def neg_or_max(self, node: Node, children_eval: list[float]) -> float:
        if node.get_action()[0] != self.mdp.action_type: return -min(children_eval)
        return max(children_eval)

    def evaluate_tree(self, node: Node) -> None:
        if not node.get_children(): return node.get_reward()
        children_eval = [self.evaluate_tree(child) for child in node.get_children() if child != None]
        node.increase_reward(self.neg_or_max(node, children_eval))
        if not node.is_root(): return node.get_reward()

    def negamax(self, root: Node = None) -> Node:
        if root == None: root = self.create_root(self.root_state, (self.mdp.action_type, None))
        self.grow_tree(root)
        self.evaluate_tree(root)
        return root
