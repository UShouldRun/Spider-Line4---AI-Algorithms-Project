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
    def __init__(self, root, root_sign: int, depth: int, mdp) -> None:
        self.root_state = root
        self.depth = depth
        self.mdp = mdp
        self.root_sign = root_sign

    def create_root(self, state, action) -> Node: return Node(state, None, action)

    def expand(self, node) -> None:
        node.set_children([self.mdp.execute(node,action) for action in self.mdp.get_actions(node)])
        if not node.get_children(): return

    def grow_tree(self, node: Node, iteration: int = 0) -> None:
        if not self.mdp.non_terminal(node):
            node.reward = float("inf")
            return
        if iteration == self.depth:
            node.increase_reward(self.mdp.qfunction(node))
            return
        self.expand(node)
        for child in node.get_children(): self.grow_tree(child, iteration + 1)

    def neg_or_max(self, sign: int, children_eval: list[float]) -> float:
        eval = -float("inf")
        for child_eval in children_eval: eval = max(eval, sign * child_eval)
        return eval

    def evaluate_tree(self, node: Node, sign: int):
        if not node.get_children(): return node.get_reward()
        children_eval = [self.evaluate_tree(child, -sign) for child in node.get_children()]
        node.increase_reward(self.neg_or_max(sign, children_eval))
        if not node.is_root(): return node.get_reward()
        return

    def negamax(self, root_action: str, root: Node = None) -> Node:
        if root == None: root = self.create_root(self.root_state, (root_action, None))
        self.grow_tree(root)
        self.evaluate_tree(root, self.root_sign)
        return root