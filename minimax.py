from objects import Board, Node

class AlphaBeta:
    def __init__(self, root, depth: int, mdp) -> None: 
        self.root_state = root
        self.mdp = mdp
        self.depth = depth

    def get_depth(self) -> int: return self.depth
    def create_root(self, state, action) -> None: return Node(state, None, action)

    def expand(self, node: Node) -> None:
        node.set_children([self.mdp.execute(node,action) for action in self.mdp.get_actions(node)])
        if not node.get_children(): return

    def min_max(self, node: Node, iteration: int) -> None:
        children_rewards = [self.evaluate(child, iteration + 1) for child in node.get_children()]
        alpha, beta = -float("inf"), float("inf")
        for reward in children_rewards:
            if iteration % 2:
                if reward > alpha: alpha = reward
            elif reward < beta: beta = reward
        node.increase_reward(alpha if iteration % 2 else beta)

    def evaluate(self, node: Node = None, iteration: int = 0):
        if not self.mdp.non_terminal(node):
            node.reward = float("inf") if node.get_action()[0] == self.mdp.action_type else -float("inf")
            return node.get_reward()
        if iteration == self.get_depth():
            node.increase_reward(self.mdp.qfunction(node))
            return node.get_reward()
        self.expand(node)
        self.min_max(node, iteration)
        if not node.is_root(): return node.get_reward()

    def minimax(self, root: Node = None) -> Node:
        if root == None: root = self.create_root(self.root_state, (self.mdp.action_type, None))
        self.expand(root)
        self.evaluate(root)
        return root
