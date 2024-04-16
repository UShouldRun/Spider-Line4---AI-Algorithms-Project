from objects import Node

class AlphaBeta:
    """ Attributes:
        root_state: The initial state of the MDP.
        depth: The depth of the search tree.
        mdp: The Markov Decision Process (MDP) environment.

    Methods:
        __init__(root, depth, mdp): Initializes the AlphaBeta object.
        reset(): Resets the AlphaBeta object.
        get_depth() -> int: Returns the depth of the search tree.
        create_root(state, action) -> Node: Creates the root node.
        expand(node, iteration) -> None: Expands the children of a node at a certain depth.
        min_value(node, alpha, beta, iteration) -> int: Calculates the minimum value for Alpha-Beta pruning.
        max_value(node, alpha, beta, iteration) -> int | None: Calculates the maximum value for Alpha-Beta pruning.
        minimax(root_action, root) -> Node: Executes the Alpha-Beta search from the root node.
        watch_stats(root) -> None: Prints statistics of the Alpha-Beta search. """
    
    def __init__(self, root, depth: int, mdp) -> None: 
        self.root_state = root
        self.mdp = mdp
        self.depth = depth
        self.nodes_depth = 0

        self.stop = False

    def reset(self) -> None:
        self.nodes_depth = 0
        Node.reset()
    def get_depth(self) -> int: return self.depth
    def get_stop(self) -> bool: return self.stop
    def set_stop(self, stop: bool) -> None: self.stop = stop

    def create_root(self, state, action) -> Node:
        return Node(state, None, action)

    def expand(self, node: Node, iteration: int) -> None:
        node.set_children([self.mdp.execute(node,action) for action in self.mdp.get_actions(node)])
        if iteration < self.get_depth() - 1:
            for child in node.get_children():
                value = float("inf") if iteration % 2 else -float("inf")
                child.set_reward(value)

    def min_value(self, node: Node, alpha: float, beta: float, iteration: int) -> int:
        if self.get_stop(): return

        if not self.mdp.non_terminal(node):
            node.reward = float("inf")
            return node.get_reward()
        if iteration == self.get_depth():
            node.increase_reward(self.mdp.qfunction(node))
            self.nodes_depth += 1
            return node.get_reward()

        value = float("inf")
        self.expand(node, iteration)
        for child in node.get_children():
            value = min(value, self.max_value(child, alpha, beta, iteration + 1))
            beta = min(beta, value)
            if beta <= alpha: break

        node.set_reward(value)
        return node.get_reward()

    def max_value(self, node: Node, alpha: float, beta: float, iteration: int = 0) -> int | None:
        if self.get_stop(): return
        if not self.mdp.non_terminal(node):
            node.reward = -float("inf")
            self.nodes_depth += 1
            return node.get_reward()
        if iteration == self.get_depth():
            node.increase_reward(self.mdp.qfunction(node))
            self.nodes_depth += 1
            return node.get_reward()

        value = -float("inf")
        self.expand(node, iteration)
        for child in node.get_children():
            value = max(value, self.min_value(child, alpha, beta, iteration + 1))
            alpha = max(alpha, value)
            if beta <= alpha: break

        node.set_reward(value)
        if node.is_root(): return
        return node.get_reward()

    def minimax(self, root_action: str, root: Node = None, eval: bool = True) -> Node:
        self.reset()
        if root == None: root = self.create_root(self.root_state, (root_action, None))
        self.max_value(root, -float("inf"), float("inf"))
        if eval: self.watch_stats(root)
        return root

    def watch_stats(self, root) -> None:
        print(f"Total explored nodes: {self.nodes_depth}")
        print(f"Total created nodes: {Node.next_node_id - 1}")